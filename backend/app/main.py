"""FastAPI app for "Los décimos de Ildefonso".

Reflects the existing Postgres schema at startup (no DDL, no migrations) and
serves the SQLite reference data read-only. The original Flask app is untouched
and can keep running as a fallback.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import db
from .config import get_settings
from .routers import auth, reference, comments, numbers, retailers, stats, scan


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_postgres()  # reflect once; never raises
    if db.pg.ready:
        print("[lotalf] Postgres connected and schema reflected.")
    else:
        print(f"[lotalf] WARNING: Postgres not connected: {db.pg.error}\n"
              "         Reference endpoints work; collection endpoints return 503 until DB_* are set.")
    yield


app = FastAPI(title="Los décimos de Ildefonso — API", version="1.0.0", lifespan=lifespan)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for module in (auth, reference, comments, numbers, retailers, stats, scan):
    app.include_router(module.router)


@app.get("/api/health")
def health():
    return {"ok": True, "db_ready": db.pg.ready, "db_error": db.pg.error}
