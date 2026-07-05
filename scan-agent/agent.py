"""LotAlfWeb — local scan agent.

Runs on the machine the Plustek MobileOffice D620 is physically plugged into.
Browsers can't drive a TWAIN scanner directly, so this tiny local service does
the hardware step: the Vue frontend POSTs to it (on localhost) to scan, and
everything else — OCR, database, saving — goes to the remote backend.

It is deliberately minimal: it only shells out to tools/scan_duplex.ps1 (NAPS2)
and returns the two faces as base64 JPEGs. No OCR, no DB, no secrets beyond an
optional shared token. See README.md for install/run/security.

Endpoints:
    GET  /health  → {ok, script_found, script}
    POST /duplex  → {front, back}   (base64 JPEGs; edit-mode token optional)
"""
import base64
import os
import subprocess
import tempfile

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

SCAN_SCRIPT = os.environ.get("SCAN_SCRIPT", "")
SCAN_TOKEN = os.environ.get("SCAN_TOKEN", "")
PORT = int(os.environ.get("PORT", "8765"))
CORS_ORIGINS = [o.strip() for o in os.environ.get(
    "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if o.strip()]

app = FastAPI(title="LotAlfWeb scan agent", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _b64(path: str) -> str | None:
    if os.path.isfile(path):
        with open(path, "rb") as fh:
            return base64.b64encode(fh.read()).decode("ascii")
    return None


def _require_token(token: str) -> None:
    # If SCAN_TOKEN is configured, the frontend must send it as X-Scan-Token.
    # (Also forces a CORS preflight, so only allowed origins can even trigger a scan.)
    if SCAN_TOKEN and token != SCAN_TOKEN:
        raise HTTPException(status_code=401, detail="Token de escaneo inválido.")


@app.get("/health")
def health():
    return {
        "ok": True,
        "script_found": bool(SCAN_SCRIPT and os.path.isfile(SCAN_SCRIPT)),
        "script": SCAN_SCRIPT,
    }


@app.post("/duplex")
def duplex(x_scan_token: str = Header(default="")):
    """Run one duplex scan and return both faces as base64 JPEGs."""
    _require_token(x_scan_token)
    if not SCAN_SCRIPT or not os.path.isfile(SCAN_SCRIPT):
        raise HTTPException(status_code=503,
                            detail=f"SCAN_SCRIPT no configurado o no encontrado: {SCAN_SCRIPT!r}")
    outdir = tempfile.mkdtemp(prefix="lotalf_scan_")
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", SCAN_SCRIPT,
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
    return {"front": front, "back": back}


if __name__ == "__main__":
    import uvicorn
    # Bind to localhost only — the agent must never be reachable from the network.
    uvicorn.run(app, host="127.0.0.1", port=PORT)
