# LotAlfWeb — Local Scan Agent

A tiny service that runs the **scanner** on the machine the Plustek MobileOffice
D620 is physically plugged into. Use it when the **backend runs on a remote
server** but the **scanner is on the user's computer**.

---

## 1. Why this exists

Browsers cannot drive a TWAIN scanner directly (they're sandboxed), and the
remote backend has no scanner attached to it. So the work splits by *what needs
the hardware*:

```
   ┌─────────────────────────── user's Windows PC ───────────────────────────┐
   │                                                                          │
   │   Browser (Vue app)                          Scan agent (this)           │
   │   ─────────────────                          ───────────────             │
   │   "Escanear décimo" ──POST /duplex──▶  http://localhost:8765             │
   │        ▲                                     │ runs NAPS2 + Plustek TWAIN │
   │        │ front/back (base64) ◀───────────────┘ via tools/scan_duplex.ps1 │
   │        │                                                                  │
   └────────┼──────────────────────────────────────────────────────────────  ┘
            │
            │ POST /api/scan/read  (the two images → OCR)         everything else:
            ▼                                                     login, map, save…
   ┌───────────────────────── remote server (Linux is fine) ──────────────────┐
   │   FastAPI backend  ──▶  Claude vision (OCR + orientation)                 │
   │                    ──▶  PostgreSQL (collection)                           │
   └──────────────────────────────────────────────────────────────────────── ┘
```

**The scan agent only scans.** It shells out to `tools/scan_duplex.ps1` (NAPS2 →
Plustek TWAIN, with deskew/crop/rotate) and returns the two faces as base64
JPEGs. No OCR, no database, no secrets beyond an optional shared token. All the
intelligence (OCR, orientation correction, black-trim, saving) stays on the
remote backend's `POST /api/scan/read`, which needs no scanner.

> If instead you run the **backend on the same machine as the scanner**, you do
> **not** need this agent — the backend's own `/api/scan/duplex` works, and you
> leave `VITE_SCAN_BASE` empty in the frontend.

---

## 2. Prerequisites on the user's machine

The scanner side is Windows-only (TWAIN). Install, in order:

1. **Plustek MobileOffice D620 TWAIN driver** and **NAPS2 portable**, and set the
   PowerShell execution policy — exactly as in the main `SETUP_NOTES.md`
   (§3–§5, "Scanner software"). The agent reuses the same `tools/scan_duplex.ps1`,
   so if a manual `.\tools\scan_duplex.ps1` scan works, the agent will too.
2. **Python 3.11+** (3.12 recommended). `py --version` should print a version.
3. A **clone of this repo** (the agent needs `tools/scan_duplex.ps1` from it).

Quick check that the scanner itself works before wiring the agent:

```powershell
& "$env:USERPROFILE\Tools\naps2\App\NAPS2.Console.exe" --listdevices --driver twain
# should list: Plustek MobileOffice A6 Duplex BU
```

---

## 3. Install & configure the agent

```powershell
cd scan-agent
py -3.12 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env`:

```env
# Absolute path to the scanner script in your clone (forward slashes are fine):
SCAN_SCRIPT=C:/Users/<you>/LotAlfWeb/tools/scan_duplex.ps1

# Port the agent listens on (localhost only):
PORT=8765

# Origin(s) the browser app is served from — the Vite dev server and/or your
# deployed frontend URL. The agent rejects any origin not listed here.
CORS_ORIGINS=http://localhost:5173,https://your-frontend.example.com

# Optional but recommended shared secret (see §6 Security):
SCAN_TOKEN=choose-a-long-random-string
```

> The agent does **not** need the DB credentials, the Anthropic key, or any of the
> backend's other settings — it only scans.

---

## 4. Run it

```powershell
# from scan-agent\, with .venv active:
python agent.py
```

Or just double-click **`run.bat`** (it creates the venv + installs deps on first
run, then starts the agent).

Verify:

```powershell
Invoke-RestMethod http://localhost:8765/health
# { ok = True; script_found = True; script = C:/Users/.../tools/scan_duplex.ps1 }
```

`script_found: false` means `SCAN_SCRIPT` is wrong — fix the path in `.env`.

### Start it automatically at login (recommended)
Press <kbd>Win</kbd>+<kbd>R</kbd> → `shell:startup` → put a **shortcut to
`run.bat`** in that folder. The agent then starts whenever the user logs in.
(For a headless service, the Windows Task Scheduler "At log on" trigger works too.)

---

## 5. Point the frontend at the agent

In the **frontend** build config (`frontend/.env`, see `frontend/.env.example`):

```env
VITE_API_BASE=https://your-backend.example.com   # the remote backend
VITE_SCAN_BASE=http://localhost:8765             # this agent
VITE_SCAN_TOKEN=choose-a-long-random-string      # must equal the agent's SCAN_TOKEN
```

Rebuild/redeploy the frontend (`npm run build`) — Vite bakes these in at build
time. With `VITE_SCAN_BASE` set, the **scan** button calls the local agent, while
OCR/DB/save calls go to `VITE_API_BASE`. Left empty, everything goes to the
backend (the all-in-one/local-dev mode).

> **Mixed content:** an `https://` frontend calling `http://localhost:8765` is
> allowed by browsers — `localhost` is treated as a secure context. You do **not**
> need TLS on the agent. (A `http://` LAN IP would be blocked; keep it `localhost`.)

---

## 6. Security model

The agent triggers a physical scanner, so treat "who can call it" seriously:

- **Localhost-only.** It binds to `127.0.0.1`, so it is not reachable from the
  network — only software on that same PC can talk to it.
- **CORS allowlist.** Only origins in `CORS_ORIGINS` may read its responses.
- **Shared token (recommended).** Set `SCAN_TOKEN` (and the matching
  `VITE_SCAN_TOKEN`). The frontend then sends it as `X-Scan-Token`; the agent
  rejects requests without it. A custom header also forces a CORS **preflight**,
  which stops a random web page you visit from silently triggering a scan.
- It holds **no secrets** — no DB creds, no API keys. Worst case of a rogue local
  call is a wasted sheet of paper, not data exposure.

For a single-user personal machine, localhost + CORS + token is plenty.

---

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| Frontend: *"¿está el agente de escaneo en marcha?"* | The agent isn't running or `VITE_SCAN_BASE` is wrong. Start `run.bat`; check `http://localhost:8765/health`. |
| `/health` shows `script_found: false` | `SCAN_SCRIPT` path in `.env` is wrong. Use the absolute path to `tools/scan_duplex.ps1`. |
| 503 *"SCAN_SCRIPT no configurado"* | Same as above. |
| 500 *"No se obtuvo imagen (¿hay un décimo…?)"* | Feeder empty or light not solid — load the décimo and push until the light is **solid**. |
| 500 *"Fallo al escanear"* / NAPS2 error | Driver/NAPS2 issue. Run `.\tools\scan_duplex.ps1 -BaseName test` directly and fix that first (see `SETUP_NOTES.md`). |
| 401 *"Token de escaneo inválido"* | `VITE_SCAN_TOKEN` (frontend) ≠ `SCAN_TOKEN` (agent). Make them equal, rebuild the frontend. |
| CORS error in the browser console | Add the frontend's exact origin to `CORS_ORIGINS` and restart the agent. |

---

## 8. Optional: ship it without requiring Python

To avoid installing Python on the customer's PC, freeze the agent to a single
`.exe` with PyInstaller on a build machine:

```powershell
pip install pyinstaller
pyinstaller --onefile --name lotalf-scan-agent agent.py
# dist\lotalf-scan-agent.exe  — copy it + a .env next to it and run it
```

The `.env` (and `tools/scan_duplex.ps1` + NAPS2 + driver) are still required on
the target machine.
