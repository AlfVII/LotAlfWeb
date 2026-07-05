"""Read the administración seal off a scanned décimo with Claude vision.

Uses tool use with a strict schema so the model returns validated structured
data (no brittle text parsing). The town is then looked up in the SQLite
reference data to fill Comunidad + Provincia automatically.
"""
from anthropic import Anthropic

from . import db
from .config import get_settings

_PROMPT = (
    "Estas son las dos caras de un décimo de la Lotería Nacional española. "
    "En alguna de ellas suele haber un sello o cuño de la ADMINISTRACIÓN de loterías que lo vendió, "
    "con su número, localidad y a veces dirección, nombre y teléfono. "
    "Lee ESE sello y registra los datos de la administración con la herramienta. "
    "Conserva las tildes y signos tal cual (p. ej. 'A Coruña', \"L'Alfàs del Pi\"). "
    "Si un dato no aparece, déjalo como cadena vacía. No inventes nada."
)

_TOOL = {
    "name": "registrar_administracion",
    "description": "Registra los datos de la administración de lotería leídos del sello impreso en el décimo.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "numero": {"type": "string", "description": "Número de la administración, p. ej. '67' ('' si no aparece)"},
            "municipio": {"type": "string", "description": "Municipio/localidad con tildes ('' si no aparece)"},
            "nombre": {"type": "string", "description": "Nombre de la administración, p. ej. 'Doña Manolita' ('' si no)"},
            "calle": {"type": "string"},
            "numero_calle": {"type": "string"},
            "codigo_postal": {"type": "string"},
            "telefono": {"type": "string"},
        },
        "required": ["numero", "municipio", "nombre", "calle", "numero_calle", "codigo_postal", "telefono"],
        "additionalProperties": False,
    },
}


def _clean(v) -> str | None:
    v = (v or "").strip()
    return v or None


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


def extract_admin(images_b64: list[str]) -> dict:
    """Run Claude vision over the scanned faces; return retailer-form fields."""
    settings = get_settings()
    if not settings.ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY no configurada")
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    content: list[dict] = []
    for b in images_b64:
        if b:
            content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": "image/jpeg", "data": b},
            })
    content.append({"type": "text", "text": _PROMPT})

    msg = client.messages.create(
        model=settings.ANTHROPIC_MODEL,
        max_tokens=1024,
        tools=[_TOOL],
        tool_choice={"type": "tool", "name": "registrar_administracion"},
        messages=[{"role": "user", "content": content}],
    )
    for block in msg.content:
        if block.type == "tool_use" and block.name == "registrar_administracion":
            return _to_form(dict(block.input))
    return _to_form({})
