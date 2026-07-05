from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from sqlalchemy import cast, String

from .. import db
from ..security import require_editor

router = APIRouter(prefix="/api/numbers", tags=["numbers"])

# Columns the number form may set (everything else is ignored — no injection of unknown cols).
_NUMBER_COLS = {
    "status", "origin", "lot", "year", "coin", "retailer_region",
    "retailer_province", "retailer_town", "retailer_number", "copies",
}
# Fields whose absence turns a "Perfecto" into "Faltan Datos" (parity with the Flask view).
_DATA_FIELDS = ["origin", "lot", "year", "coin", "retailer_province", "retailer_town", "retailer_number"]


@router.get("/{number}")
def get_number(number: int, session=Depends(db.get_session)):
    N = db.table("numbers_collection")
    row = session.query(N).filter(N.number == number).first()
    return db.row_to_dict(row) if row else None


@router.get("/hundred/{base}")
def get_hundred(base: int, session=Depends(db.get_session)) -> list[str | None]:
    N = db.table("numbers_collection")
    rows = (session.query(N)
            .filter(N.number >= base, N.number < base + 100)
            .order_by(N.number).all())
    out: list[str | None] = []
    for r in rows:
        d = db.row_to_dict(r)
        status = d.get("status")
        if status == "Perfecto" and any(d.get(k) in (None, "") for k in _DATA_FIELDS):
            status = "Faltan Datos"
        out.append(status)
    return out


class FilterItem(BaseModel):
    name: str
    filled: str
    value: str | None = None


class FilteredIn(BaseModel):
    filters: list[FilterItem] = []
    limit: int | None = None


@router.post("/filtered")
def filtered(body: FilteredIn, session=Depends(db.get_session)) -> list[int]:
    N = db.table("numbers_collection")
    q = session.query(N.number)
    for f in body.filters:
        if f.name not in _NUMBER_COLS:
            continue
        col = getattr(N, f.name)
        if f.filled == "0":
            q = q.filter(cast(col, String).is_(None))
        else:
            q = q.filter(cast(col, String).like(f"%{f.value or ''}%"))
    q = q.order_by(N.number)
    if body.limit:
        q = q.limit(body.limit)
    return [row[0] for row in q.all()]


@router.put("/{number}")
def update_number(number: int, data: dict = Body(...),
                  session=Depends(db.get_session), _: bool = Depends(require_editor)):
    N = db.table("numbers_collection")
    clean = {k: v for k, v in data.items() if k in _NUMBER_COLS and v != "Default"}
    if clean:
        session.query(N).filter(N.number == number).update(clean)
        session.commit()
    return {"ok": True}
