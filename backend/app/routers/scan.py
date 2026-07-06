"""Scanner bridge — the Plustek MobileOffice D620 duplex helper.

- POST /api/scan/duplex → both faces as base64 JPEGs (the slow scanner step).
- POST /api/scan/read   → given both faces, OCR the seal (two-pass, orientation-
                          corrected) and return the upright faces + form fields.
- POST /api/scan/decimo → convenience: duplex + read in one call.
Edit-mode only.
"""
import base64
import io
import os
import subprocess
import tempfile

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from PIL import Image, ImageEnhance, ImageOps

from ..config import get_settings
from ..security import require_editor

router = APIRouter(prefix="/api/scan", tags=["scan"])


def _b64(path: str) -> str | None:
    if os.path.isfile(path):
        with open(path, "rb") as fh:
            return base64.b64encode(fh.read()).decode("ascii")
    return None


def _rotate_b64(data_b64: str | None, deg_clockwise: int) -> str | None:
    """Rotate a base64 JPEG by N clockwise degrees (0/90/180/270). Returns base64."""
    if not data_b64 or not deg_clockwise:
        return data_b64
    img = Image.open(io.BytesIO(base64.b64decode(data_b64)))
    # PIL rotates counter-clockwise, so negate to get clockwise; expand keeps full frame.
    img = img.rotate(-deg_clockwise, expand=True)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=92)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _span(vals, thresh):
    """Longest contiguous run of indices whose value >= thresh (robust to a thin
    bright edge artifact that a naive edge-trim would stop on)."""
    best = (0, -1); cur = None
    for i, v in enumerate(vals):
        if v >= thresh:
            if cur is None:
                cur = i
            if i - cur > best[1] - best[0]:
                best = (cur, i)
        else:
            cur = None
    return best if best[1] >= best[0] else (0, len(vals) - 1)


def _trim_black_b64(data_b64: str | None, thresh: int = 70) -> str | None:
    """Trim near-black feeder margins (left after deskew) via a content bounding box."""
    if not data_b64:
        return data_b64
    img = Image.open(io.BytesIO(base64.b64decode(data_b64))).convert("RGB")
    g = ImageOps.grayscale(img)
    w, h = g.size
    rows = list(g.resize((1, h), Image.Resampling.BOX).getdata())  # mean per row
    cols = list(g.resize((w, 1), Image.Resampling.BOX).getdata())  # mean per column
    top, bottom = _span(rows, thresh)
    left, right = _span(cols, thresh)
    if right <= left or bottom <= top:
        return data_b64
    crop = img.crop((left, top, right + 1, bottom + 1))
    buf = io.BytesIO()
    crop.save(buf, format="JPEG", quality=92)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _crop_enhance_b64(data_b64: str, bbox, pad: float = 0.06, upscale: float = 2.5,
                      max_edge: int = 2200) -> str | None:
    """Crop the seal box (fractions x,y,w,h), pad it, upscale, and boost contrast so
    the faint stamp has more legible pixels for the focused second OCR pass."""
    x, y, w, h = bbox
    if w <= 0 or h <= 0:
        return None
    img = Image.open(io.BytesIO(base64.b64decode(data_b64))).convert("RGB")
    W, H = img.size
    x0 = max(0, int((x - pad) * W)); y0 = max(0, int((y - pad) * H))
    x1 = min(W, int((x + w + pad) * W)); y1 = min(H, int((y + h + pad) * H))
    if x1 - x0 < 20 or y1 - y0 < 20:
        return None
    crop = img.crop((x0, y0, x1, y1))
    nw, nh = int(crop.width * upscale), int(crop.height * upscale)
    if max(nw, nh) > max_edge:  # keep within a sane size for the vision API
        s = max_edge / max(nw, nh)
        nw, nh = int(nw * s), int(nh * s)
    crop = crop.resize((max(1, nw), max(1, nh)), Image.LANCZOS)
    crop = ImageOps.autocontrast(crop, cutoff=1)
    crop = ImageEnhance.Contrast(crop).enhance(1.6)
    buf = io.BytesIO()
    crop.save(buf, format="JPEG", quality=92)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _read_faces(front: str | None, back: str | None) -> tuple[str | None, str | None, dict]:
    """Two-pass OCR: read both faces, then re-read a cropped/enhanced seal.
    Returns (front_upright, back_upright, form_fields)."""
    from ..ocr import extract_admin, extract_admin_crop, merge_and_form
    raw, orient, seal = extract_admin([front, back])
    # Opus is conservative and returns no seal on very faint stamps; retry once with
    # the fallback model (sonnet-5 reads faint ones opus won't commit to). Only fires
    # on a miss, so it adds nothing to normal-scan cost.
    used_model = None
    if seal.get("cara") == "ninguno" or not (raw.get("municipio") or "").strip():
        fb = get_settings().ANTHROPIC_FALLBACK_MODEL
        if fb:
            raw2, orient2, seal2 = extract_admin([front, back], model=fb)
            if seal2.get("cara") != "ninguno" and (raw2.get("municipio") or "").strip():
                raw, orient, seal, used_model = raw2, orient2, seal2, fb
    # Pass 2 — focused re-read of the seal crop (from the face as Claude saw it).
    pass2 = None
    cara = seal.get("cara")
    src = front if cara == "anverso" else back if cara == "reverso" else None
    if src:
        try:
            crop = _crop_enhance_b64(src, seal["bbox"])
            if crop:
                pass2 = extract_admin_crop(crop, model=used_model)
        except Exception:
            pass2 = None
    form = merge_and_form(raw, pass2)
    # Upright + trim any residual black feeder margin (deskew can leave one).
    front_up = _trim_black_b64(_rotate_b64(front, orient.get("front", 0)))
    back_up = _trim_black_b64(_rotate_b64(back, orient.get("back", 0)))
    return front_up, back_up, form


def _run_duplex() -> tuple[str | None, str | None]:
    """Run scan_duplex.ps1 and return (front_b64, back_b64). Raises on failure."""
    script = get_settings().SCAN_SCRIPT
    if not script or not os.path.isfile(script):
        raise HTTPException(status_code=503, detail="Escáner no configurado.")
    outdir = tempfile.mkdtemp(prefix="lotalf_scan_")
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script,
             "-OutDir", outdir, "-BaseName", "web"],
            check=True, timeout=180, capture_output=True,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="El escáner no respondió a tiempo.")
    except subprocess.CalledProcessError as exc:
        raise HTTPException(status_code=500, detail=f"Fallo al escanear: {exc.stderr or exc}")
    front = _b64(os.path.join(outdir, "web_1.jpg"))
    back = _b64(os.path.join(outdir, "web_2.jpg"))
    if not front:
        raise HTTPException(status_code=500,
                            detail="No se obtuvo imagen (¿hay un décimo en el alimentador?).")
    return front, back


class FacesIn(BaseModel):
    front: str | None = None
    back: str | None = None


@router.post("/duplex")
def scan_duplex(_: bool = Depends(require_editor)):
    front, back = _run_duplex()
    return {"front": front, "back": back}


@router.post("/read")
def scan_read(body: FacesIn, _: bool = Depends(require_editor)):
    """OCR already-scanned faces (the 'Leyendo' step). Returns upright faces + fields."""
    if not body.front and not body.back:
        raise HTTPException(status_code=400, detail="No hay imágenes que leer.")
    front, back, extracted, error = body.front, body.back, None, None
    try:
        front, back, extracted = _read_faces(body.front, body.back)
    except Exception as exc:  # OCR is best-effort — never lose the scan
        error = str(exc)
    return {"front": front, "back": back, "extracted": extracted, "ocr_error": error}


@router.post("/decimo")
def scan_decimo(ocr: bool = True, _: bool = Depends(require_editor)):
    front, back = _run_duplex()
    extracted, error = None, None
    if ocr:
        try:
            front, back, extracted = _read_faces(front, back)
        except Exception as exc:
            error = str(exc)
    return {"front": front, "back": back, "extracted": extracted, "ocr_error": error}
