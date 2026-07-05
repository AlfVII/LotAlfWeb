"""Read the administración seal off a scanned décimo with Claude vision.

Two-pass strategy for the faint, overlapping stamp:
  1. Read both faces → admin data + per-face orientation + the seal's bounding box.
  2. Crop that box, upscale + contrast-boost it, and re-read the seal on its own —
     more effective pixels on the exact text, so the faint number/phone read better.
The town is looked up in the SQLite reference data to fill Comunidad + Provincia.
"""
from anthropic import Anthropic

from . import db
from .config import get_settings

_ADMIN_FIELDS = {
    "numero": {"type": "string", "description": "Número de la administración, p. ej. '67' ('' si no aparece)"},
    "municipio": {"type": "string", "description": "Municipio/localidad con tildes ('' si no aparece)"},
    "nombre": {"type": "string", "description": "Nombre de la administración, p. ej. 'Doña Manolita' ('' si no)"},
    "calle": {"type": "string"},
    "numero_calle": {"type": "string"},
    "codigo_postal": {"type": "string"},
    "telefono": {"type": "string"},
}
_ADMIN_REQUIRED = list(_ADMIN_FIELDS.keys())

# ---- Pass 1: both faces → data + orientation + seal location --------------
_PROMPT = (
    "Estas son las dos caras de un décimo de la Lotería Nacional española: la primera "
    "imagen es el ANVERSO y la segunda el REVERSO. "
    "En alguna de ellas suele haber un sello o cuño de la ADMINISTRACIÓN de loterías que lo vendió, "
    "con su número, localidad y a veces dirección, nombre y teléfono. "
    "Lee ESE sello y registra los datos de la administración con la herramienta. "
    "Conserva las tildes y signos tal cual (p. ej. 'A Coruña', \"L'Alfàs del Pi\"). "
    "Si un dato no aparece, déjalo como cadena vacía. No inventes nada. "
    "Indica para cada cara cuántos grados hay que girarla EN SENTIDO HORARIO (0, 90, 180 o 270) "
    "para que su texto quede derecho. "
    "Indica también en qué cara está el sello ('anverso', 'reverso' o 'ninguno') y su recuadro "
    "envolvente como fracciones (0..1) de esa imagen TAL COMO LA VES: sello_x, sello_y (esquina "
    "superior izquierda), sello_w, sello_h (ancho y alto)."
)

_TOOL = {
    "name": "registrar_administracion",
    "description": "Registra los datos de la administración de lotería leídos del sello impreso en el décimo.",
    "input_schema": {
        "type": "object",
        "properties": {
            **_ADMIN_FIELDS,
            "rotacion_anverso": {"type": "integer", "enum": [0, 90, 180, 270],
                                 "description": "Grados horarios para poner derecho el ANVERSO (1ª imagen)"},
            "rotacion_reverso": {"type": "integer", "enum": [0, 90, 180, 270],
                                 "description": "Grados horarios para poner derecho el REVERSO (2ª imagen)"},
            "sello_cara": {"type": "string", "enum": ["anverso", "reverso", "ninguno"],
                           "description": "Cara donde está el sello de la administración"},
            "sello_x": {"type": "number", "description": "Borde izq. del sello (0..1) en la imagen tal como se ve"},
            "sello_y": {"type": "number", "description": "Borde sup. del sello (0..1)"},
            "sello_w": {"type": "number", "description": "Ancho del sello (0..1)"},
            "sello_h": {"type": "number", "description": "Alto del sello (0..1)"},
        },
        "required": _ADMIN_REQUIRED + ["rotacion_anverso", "rotacion_reverso",
                                       "sello_cara", "sello_x", "sello_y", "sello_w", "sello_h"],
        "additionalProperties": False,
    },
}

# ---- Pass 2: focused re-read of the cropped, enhanced seal -----------------
_CROP_PROMPT = (
    "Este es el recorte AMPLIADO y realzado del sello/cuño de una administración de la Lotería "
    "Nacional española. Lee con cuidado sus datos (número de administración, municipio, nombre, "
    "calle, número de calle, código postal, teléfono). Conserva tildes y signos. "
    "Si un dato no aparece, déjalo como cadena vacía. No inventes nada."
)
_TOOL_CROP = {
    "name": "registrar_administracion",
    "description": "Registra los datos leídos del recuadro ampliado del sello.",
    "input_schema": {
        "type": "object",
        "properties": dict(_ADMIN_FIELDS),
        "required": _ADMIN_REQUIRED,
        "additionalProperties": False,
    },
}


def _clean(v) -> str | None:
    v = (v or "").strip()
    return v or None


def _client() -> Anthropic:
    settings = get_settings()
    if not settings.ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY no configurada")
    return Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def _call(content: list[dict], tool: dict) -> dict:
    settings = get_settings()
    msg = _client().messages.create(
        model=settings.ANTHROPIC_MODEL,
        max_tokens=1024,
        thinking={"type": "disabled"},  # perception, not reasoning — faster/cheaper/deterministic
        tools=[tool],
        tool_choice={"type": "tool", "name": tool["name"]},
        messages=[{"role": "user", "content": content}],
    )
    for block in msg.content:
        if block.type == "tool_use" and block.name == tool["name"]:
            return dict(block.input)
    return {}


def _image_block(b64: str) -> dict:
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}}


def _to_form(d: dict) -> dict:
    town = _clean(d.get("municipio"))
    region = province = None
    if town:
        region, province = db.lookup_town(town)
    return {
        "retailer_region": region,
        "retailer_province": province,
        "retailer_town": town,
        "retailer_number": _clean(d.get("numero")),
        "retailer_name": _clean(d.get("nombre")),
        "retailer_street": _clean(d.get("calle")),
        "retailer_street_number": _clean(d.get("numero_calle")),
        "retailer_postal_code": _clean(d.get("codigo_postal")),
        "retailer_telephone": _clean(d.get("telefono")),
    }


def extract_admin(images_b64: list[str]) -> tuple[dict, dict, dict]:
    """Pass 1. Returns ``(raw_fields, orientation, seal)``.

    ``raw_fields`` is the raw Claude dict (before town lookup — the caller may
    refine it in pass 2 before converting to form fields).
    ``orientation`` = ``{"front": deg, "back": deg}`` (clockwise, to upright).
    ``seal`` = ``{"cara": "anverso"|"reverso"|"ninguno", "bbox": (x, y, w, h)}``
    with the box as fractions of the face as-scanned.
    """
    content = [_image_block(b) for b in images_b64 if b]
    content.append({"type": "text", "text": _PROMPT})
    data = _call(content, _TOOL)
    orient = {
        "front": int(data.get("rotacion_anverso") or 0) % 360,
        "back": int(data.get("rotacion_reverso") or 0) % 360,
    }
    seal = {
        "cara": data.get("sello_cara", "ninguno"),
        "bbox": (float(data.get("sello_x") or 0), float(data.get("sello_y") or 0),
                 float(data.get("sello_w") or 0), float(data.get("sello_h") or 0)),
    }
    return data, orient, seal


def extract_admin_crop(crop_b64: str) -> dict:
    """Pass 2. Re-read the enhanced seal crop; returns the raw Claude dict."""
    content = [_image_block(crop_b64), {"type": "text", "text": _CROP_PROMPT}]
    return _call(content, _TOOL_CROP)


def merge_and_form(pass1: dict, pass2: dict | None) -> dict:
    """Merge the focused pass-2 read over pass-1 (pass-2 wins where non-empty),
    then convert to retailer-form fields with región/provincia resolved."""
    merged = dict(pass1)
    for k in _ADMIN_FIELDS:
        v = _clean((pass2 or {}).get(k))
        if v:
            merged[k] = v
    return _to_form(merged)
