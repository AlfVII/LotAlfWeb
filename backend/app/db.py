"""Data layer.

Two backends, exactly as in the original app — but hardened:

* SQLite (read-only reference data: ``towns`` + ``lottery_retailers``).
  Queries are PARAMETERIZED (no f-string interpolation) and matched
  case-insensitively (``COLLATE NOCASE``), which fixes the SQL-injection risk
  AND the recurring apostrophe/diacritic bug (L'Alfàs del Pi, A Coruña…).
  Place names are returned VERBATIM as stored — never ``.title()``-mangled.

* Postgres (the mutable collection). The schema is reflected ONCE at startup
  via ``automap`` (not per-request), and NO DDL is ever issued — the new app
  reads/writes the same tables the Flask app does. Nothing is migrated.
"""
import os
import sqlite3
from contextlib import contextmanager

from fastapi import HTTPException
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

from .config import get_settings

LOCAL_RETAILER_COLS = [
    "id", "retailer_number", "retailer_street", "retailer_street_number",
    "retailer_postal_code", "retailer_town", "retailer_telephone",
    "retailer_longitude", "retailer_latitude", "retailer_province",
    "retailer_region", "retailer_name", "retailer_email",
]

# --------------------------------------------------------------------------
# SQLite (read-only reference data)
# --------------------------------------------------------------------------
def _local_path() -> str:
    s = get_settings()
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/
    return os.path.normpath(os.path.join(base, s.LOCAL_DB_PATH))


@contextmanager
def local_conn():
    """Open the bundled SQLite file read-only (cannot modify reference data)."""
    path = _local_path()
    uri = f"file:{path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()


def get_regions() -> list[str]:
    with local_conn() as c:
        rows = c.execute("SELECT DISTINCT region FROM towns ORDER BY region").fetchall()
    return [r[0] for r in rows]


def get_provinces(region: str) -> list[str]:
    with local_conn() as c:
        rows = c.execute(
            "SELECT DISTINCT province FROM towns WHERE region = ? COLLATE NOCASE ORDER BY province",
            (region,),
        ).fetchall()
    return [r[0] for r in rows]


def get_towns(province: str) -> list[str]:
    with local_conn() as c:
        rows = c.execute(
            "SELECT DISTINCT town FROM towns WHERE province = ? COLLATE NOCASE ORDER BY town",
            (province,),
        ).fetchall()
    return [r[0] for r in rows]


def _master_query(filters: dict, like: bool = False) -> list[dict]:
    """Master retailers from SQLite with an optional equality/LIKE filter set.

    ``filters`` maps column -> value; only whitelisted reference columns are
    allowed (the keys can never reach SQL as text). Values are parameterized.
    """
    sql = ("SELECT * FROM lottery_retailers "
           "WHERE retailer_latitude != '' AND retailer_number != ''")
    params: list = []
    for field, value in filters.items():
        if field not in LOCAL_RETAILER_COLS:
            continue  # ignore anything not a known reference column
        if like:
            sql += f" AND {field} LIKE ? COLLATE NOCASE"
            params.append(f"%{value}%")
        else:
            sql += f" AND {field} = ? COLLATE NOCASE"
            params.append(value)
    with local_conn() as c:
        rows = c.execute(sql, params).fetchall()
    return [dict(zip(LOCAL_RETAILER_COLS, r)) for r in rows]


def master_retailers(filters: dict | None = None, like: bool = False) -> list[dict]:
    return _master_query(filters or {}, like=like)


def lookup_town(town: str) -> tuple[str | None, str | None]:
    """Reverse-lookup a town in the reference data → (region, province), verbatim.

    Lets OCR fill Comunidad + Provincia for free from just the town on the seal.
    """
    if not town:
        return (None, None)
    with local_conn() as c:
        # Seals usually name a city, most often a provincial capital. Try the
        # province name first (resolves 'Madrid', 'A Coruña' unambiguously — town
        # names like 'Madrid' also exist as tiny villages elsewhere), then fall
        # back to a town match for ordinary localities.
        row = c.execute(
            "SELECT region, province FROM towns WHERE province = ? COLLATE NOCASE LIMIT 1",
            (town,),
        ).fetchone()
        if not row:
            row = c.execute(
                "SELECT region, province FROM towns WHERE town = ? COLLATE NOCASE LIMIT 1",
                (town,),
            ).fetchone()
    return (row[0], row[1]) if row else (None, None)


def master_count() -> int:
    with local_conn() as c:
        (n,) = c.execute(
            "SELECT COUNT(*) FROM lottery_retailers "
            "WHERE retailer_latitude != '' AND retailer_number != ''"
        ).fetchone()
    return n


# --------------------------------------------------------------------------
# Postgres (mutable collection) — reflected once, no DDL
# --------------------------------------------------------------------------
class _PG:
    engine = None
    Session = None
    classes = None
    ready = False
    error: str | None = None


pg = _PG()
_PG_TABLES = ["comments", "numbers_collection", "retailers_collection"]


def init_postgres() -> None:
    """Reflect the live schema once. Safe to call at startup; never raises."""
    s = get_settings()
    url = s.postgres_url
    if not url:
        pg.error = "DB_* environment variables are not set"
        return
    try:
        engine = create_engine(url, connect_args={"connect_timeout": 10}, pool_pre_ping=True)
        metadata = MetaData()
        metadata.reflect(engine, only=_PG_TABLES)
        Base = automap_base(metadata=metadata)
        Base.prepare()
        pg.engine = engine
        pg.Session = sessionmaker(bind=engine)
        pg.classes = Base.classes
        pg.ready = True
        pg.error = None
    except Exception as exc:  # connection/reflection failure — degrade gracefully
        pg.error = str(exc)
        pg.ready = False


def require_pg():
    if not pg.ready:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {pg.error}")


def get_session():
    """FastAPI dependency: a short-lived session, always closed."""
    require_pg()
    db = pg.Session()
    try:
        yield db
    finally:
        db.close()


def table(name: str):
    require_pg()
    return getattr(pg.classes, name)


def row_to_dict(row) -> dict:
    """Serialize a reflected ORM row to a plain dict (schema-agnostic)."""
    return {c.name: getattr(row, c.name) for c in row.__table__.columns}
