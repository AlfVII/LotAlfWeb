from fastapi import APIRouter, Query

from .. import db

router = APIRouter(prefix="/api/reference", tags=["reference"])


@router.get("/regions")
def regions() -> list[str]:
    return db.get_regions()


@router.get("/provinces")
def provinces(region: str = Query(...)) -> list[str]:
    return db.get_provinces(region)


@router.get("/towns")
def towns(province: str = Query(...)) -> list[str]:
    return db.get_towns(province)
