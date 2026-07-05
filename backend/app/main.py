"""FastAPI app for "Los décimos de Ildefonso".

Reflects the existing Postgres schema at startup (no DDL, no migrations) and
serves the SQLite reference data read-only. The original Flask app is untouched
and can keep running as a fallback.
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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


# --- Serve the built Vue SPA (frontend/dist), if present -------------------
# Lets nginx proxy everything to this app (no separate static server needed).
# API routes above match first; the catch-all returns index.html for the SPA's
# client-side routes.
_DIST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "frontend", "dist",
)
if os.path.isdir(_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(_DIST, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def spa(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")
        candidate = os.path.normpath(os.path.join(_DIST, full_path))
        if full_path and candidate.startswith(_DIST) and os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(_DIST, "index.html"))
