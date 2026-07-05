from collections import Counter, OrderedDict

from fastapi import APIRouter, Depends

from .. import db

router = APIRouter(prefix="/api/stats", tags=["stats"])


def _count(rows: list[dict], key: str) -> "OrderedDict[str, int]":
    """Counts by value, descending, blanks dropped, names kept VERBATIM."""
    c = Counter()
    for d in rows:
        v = d.get(key)
        if v in (None, ""):
            continue
        c[v] += 1
    return OrderedDict(sorted(c.items(), key=lambda kv: kv[1], reverse=True))


@router.get("/numbers")
def numbers_stats(session=Depends(db.get_session)):
    N = db.table("numbers_collection")
    rows = [db.row_to_dict(r) for r in session.query(N).all()]
    filled = sum(1 for r in rows if r.get("retailer_province") not in (None, ""))
    return {
        "numbers_statuses": dict(Counter(r.get("status") for r in rows if r.get("status"))),
        "numbers_regions": _count(rows, "retailer_region"),
        "numbers_provinces": _count(rows, "retailer_province"),
        "numbers_years": _count(rows, "year"),
        "numbers_origins": _count(rows, "origin"),
        "numbers_coins": _count(rows, "coin"),
        "numbers_filled": {"Por rellenar": len(rows) - filled, "Rellenados": filled},
    }


@router.get("/retailers")
def retailers_stats(session=Depends(db.get_session)):
    R = db.table("retailers_collection")
    rows = [db.row_to_dict(r) for r in session.query(R).all()]
    with_img = sum(1 for r in rows if r.get("image") not in (None, ""))
    return {
        "retailers_regions": _count(rows, "retailer_region"),
        "retailers_provinces": _count(rows, "retailer_province"),
        "retailers_filled": {"Por rellenar": db.master_count(), "Rellenados": len(rows)},
        "retailers_with_image": {"Con imagen": with_img, "Sin imagen": len(rows) - with_img},
    }
