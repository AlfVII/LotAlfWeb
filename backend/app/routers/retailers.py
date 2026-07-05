"""Administraciones (lottery retailers).

Map markers are returned as a JSON array of objects (not the old <br>-joined
HTML string), which removes the stored-XSS / positional-parsing footgun.
Images are stored straight into Postgres — no /tmp scratch file (which never
existed on Windows anyway).
"""
from fastapi import APIRouter, Depends, Query, Body

from .. import db
from ..security import require_editor

router = APIRouter(prefix="/api/retailers", tags=["retailers"])

_RETAILER_COLS = {
    "retailer_number", "retailer_street", "retailer_street_number",
    "retailer_postal_code", "retailer_town", "retailer_telephone",
    "retailer_longitude", "retailer_latitude", "retailer_province",
    "retailer_region", "retailer_name", "retailer_email", "number", "image", "image_back",
}


def _to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _marker(d: dict, owned: bool) -> dict:
    return {
        "lat": _to_float(d.get("retailer_latitude")),
        "lng": _to_float(d.get("retailer_longitude")),
        "owned": owned,
        "region": d.get("retailer_region"),
        "province": d.get("retailer_province"),
        "town": d.get("retailer_town"),
        "number": d.get("retailer_number"),
        "name": d.get("retailer_name"),
        "street": d.get("retailer_street"),
        "street_number": d.get("retailer_street_number"),
        "postal_code": d.get("retailer_postal_code"),
        "telephone": d.get("retailer_telephone"),
        "email": d.get("retailer_email"),
        "lottery_number": d.get("number"),
    }


def _key(d: dict):
    return (str(d.get("retailer_province")), str(d.get("retailer_town")), str(d.get("retailer_number")))


def _owned_rows(session, filters: dict | None = None) -> list[dict]:
    R = db.table("retailers_collection")
    q = session.query(R)
    for k, v in (filters or {}).items():
        col = getattr(R, k, None)
        if col is not None:
            q = q.filter(col == v)
    return [db.row_to_dict(r) for r in q.all()]


def _merge(master: list[dict], owned: list[dict]) -> list[dict]:
    owned_keys = {_key(o) for o in owned}
    markers = [_marker(o, True) for o in owned]
    markers += [_marker(m, False) for m in master if _key(m) not in owned_keys]
    return [m for m in markers if m["lat"] is not None and m["lng"] is not None]


@router.get("/map")
def map_markers(scope: str | None = None,
                region: str | None = None, province: str | None = None,
                town: str | None = None, number: str | None = None,
                session=Depends(db.get_session)):
    if scope == "all":
        return _merge(db.master_retailers(), _owned_rows(session))
    if scope == "owned":
        return _merge([], _owned_rows(session))
    filters: dict = {}
    if region:
        filters["retailer_region"] = region
    if province:
        filters["retailer_province"] = province
    if town:
        filters["retailer_town"] = town
    if number:
        filters["retailer_number"] = number
    return _merge(db.master_retailers(filters), _owned_rows(session, filters))


@router.get("/one")
def get_one(province: str = Query(...), town: str = Query(...), number: str = Query(...),
            region: str | None = None, session=Depends(db.get_session)):
    f = {"retailer_province": province, "retailer_town": town, "retailer_number": number}
    owned = _owned_rows(session, f)
    if owned:
        return _marker(owned[0], True)
    master = db.master_retailers(f)
    return _marker(master[0], False) if master else None


@router.get("/image")
def get_image(province: str = Query(...), town: str = Query(...), number: str = Query(...),
              session=Depends(db.get_session)):
    R = db.table("retailers_collection")
    row = (session.query(R)
           .filter(R.retailer_province == province, R.retailer_town == town,
                   R.retailer_number == number).first())
    if not row:
        return {"image": None, "image_back": None}
    d = db.row_to_dict(row)

    def _dec(v):
        if v is None:
            return None
        return bytes(v).decode("utf-8") if isinstance(v, (bytes, bytearray)) else v

    return {"image": _dec(d.get("image")), "image_back": _dec(d.get("image_back"))}


@router.put("")
def save_retailer(body: dict = Body(...),
                  session=Depends(db.get_session), _: bool = Depends(require_editor)):
    """Upsert if owned == 'Owned', else remove from the collection."""
    R = db.table("retailers_collection")
    owned = body.get("owned")
    # only real columns on the reflected table (graceful if image_back not migrated yet)
    data = {k: v for k, v in body.items() if k in _RETAILER_COLS and hasattr(R, k)}
    q = (session.query(R)
         .filter(R.retailer_region == body.get("retailer_region"),
                 R.retailer_province == body.get("retailer_province"),
                 R.retailer_town == body.get("retailer_town"),
                 R.retailer_number == body.get("retailer_number")))
    existing = q.first()
    if owned == "Owned":
        if existing:
            q.update(data)
        else:
            session.add(R(**data))
        session.commit()
        return {"ok": True, "owned": True}
    if existing:
        q.delete()
        session.commit()
    return {"ok": True, "owned": False}
