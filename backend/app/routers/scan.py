"""Scanner bridge — the Plustek MobileOffice D620 duplex helper.

- POST /api/scan/duplex  → both faces as base64 JPEGs.
- POST /api/scan/decimo  → both faces + OCR-extracted administración data
                           (Claude vision reads the seal; town → región/provincia).
Edit-mode only.
"""
import base64
import os
import subprocess
import tempfile

from fastapi import APIRouter, Depends, HTTPException

from ..config import get_settings
from ..security import require_editor

router = APIRouter(prefix="/api/scan", tags=["scan"])


def _b64(path: str) -> str | None:
    if os.path.isfile(path):
        with open(path, "rb") as fh:
            return base64.b64encode(fh.read()).decode("ascii")
    return None


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


@router.post("/duplex")
def scan_duplex(_: bool = Depends(require_editor)):
    front, back = _run_duplex()
    return {"front": front, "back": back}


@router.post("/decimo")
def scan_decimo(ocr: bool = True, _: bool = Depends(require_editor)):
    front, back = _run_duplex()
    extracted = None
    error = None
    if ocr:
        try:
            from ..ocr import extract_admin
            extracted = extract_admin([front, back])
        except Exception as exc:  # OCR is best-effort — never block the scan
            error = str(exc)
    return {"front": front, "back": back, "extracted": extracted, "ocr_error": error}
