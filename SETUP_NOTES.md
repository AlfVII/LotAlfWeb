# LotAlfWeb — validated setup notes & handoff corrections

Companion to the "Handoff to new machine" doc. These are the **deviations, fixes,
and gotchas found while rehearsing the full install** on branch `rebuild`, so the
customer-site install repeats cleanly. Everything below was actually run and verified.

## Status after rehearsal
| Component | State |
|---|---|
| Backend (FastAPI, uvicorn :8000) | ✅ running; `/api/health` → `{"ok":true,"db_ready":false}` |
| Frontend (Vue/Vite :5173) | ✅ running; `/api` proxy → backend OK |
| Auth (`/api/auth/login`) | ✅ token issued for `2Galletas!`; wrong pw → 401 |
| Reference endpoints (SQLite) | ✅ 20 regions served |
| Scan API (`/api/scan/duplex`) | ✅ endpoint works, degrades cleanly (500) until driver installed |
| Scanner hardware | ✅ detected (`USB\VID_07B3&PID_1602` = Plustek D620) |
| Plustek TWAIN driver | ✅ installed on this box (V6.0.2.2); scan verified. **Still a manual step at the customer site** (see §5) |
| Duplex scan (script + `/api/scan/duplex`) | ✅ both faces captured; API returns valid base64 JPEGs |
| Postgres `db_ready:true` | ⚠️ needs the real DB creds (live in hosting platform, not in repo) |

## 1. Python — pin the venv to 3.12
The default `python` may be a bleeding-edge build (3.14 on the rehearsal box) that
lacks prebuilt wheels for `psycopg2-binary`. Create the venv explicitly with 3.12:
```powershell
py -3.12 -m venv .venv       # NOT plain `python -m venv`
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
All deps (incl. `psycopg2-binary` 2.9.12) install cleanly on 3.12. Verified.

## 2. PowerShell execution policy
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` may be **blocked by a
machine/GPO policy** ("overridden by a policy defined at a more specific scope").
This does **not** block the app: the backend invokes the scan script with
`powershell -NoProfile -ExecutionPolicy Bypass -File ...` (see `backend/app/routers/scan.py`),
so the API scan path works regardless. To run the script **manually** when the
policy blocks it:
```powershell
powershell -ExecutionPolicy Bypass -File .\tools\scan_duplex.ps1 -BaseName test
```

## 3. NAPS2 — which asset, where to put it
The 8.x releases have **no asset literally named "portable"**. Use the standalone
zip `naps2-<ver>-win-x64.zip` (v8.2.1 used here). Its root already contains `App\`,
so extract it to `%USERPROFILE%\Tools\naps2\` and you get exactly:
```
C:\Users\<you>\Tools\naps2\App\NAPS2.Console.exe
```
```powershell
$dest = "$env:USERPROFILE\Tools\naps2"
Expand-Archive naps2-8.2.1-win-x64.zip -DestinationPath $dest -Force
& "$dest\App\NAPS2.Console.exe" --version   # sanity check
```

## 4. `tools/scan_duplex.ps1` was hardened (no per-machine edit needed)
The handoff's "edit line 44 to match your username" step is **obsolete**. The
script now auto-detects `NAPS2.Console.exe` in this order:
1. `-Naps2Path 'C:\...\NAPS2.Console.exe'` argument
2. `$env:NAPS2_CONSOLE`
3. `%USERPROFILE%\Tools\naps2\App\NAPS2.Console.exe`  ← works for any username
4. `C:\Program Files\NAPS2\NAPS2.Console.exe` (installer edition)

As long as NAPS2 is extracted to the location in §3, **no edit is required**.
(Also fixed a UTF-8 em-dash in a warning string that could mojibake-corrupt and
break parsing on re-save; the message is now ASCII.)

## 5. Plustek D620 TWAIN driver — the one manual step
Not bundled and not silently installable — it's an interactive, signed GUI
installer. Without it, NAPS2 reports *"The selected scanner could not be found"*
and `/api/scan/duplex` returns 500. On a fresh machine the scanner shows in Device
Manager as **"Sheetfed Scanner" / Error / CM_PROB_FAILED_INSTALL** until installed.

Direct download (verified, signed `CN=PLUSTEK INC.`):
```
https://d3b63i9tvm4mo6.cloudfront.net/downloads/english/driver/MobileOfficeD620_V6022_6L.zip
```
V6.0.2.2, dated 2024-09-27, ~138 MB. Extract and run the single exe inside:
`Release Plustek MobileOffice A6 Duplex BUS Power V6022 WebDriver.exe`
(Install **TWAIN**, not WIA — WIA duplex is broken on this model.) After install,
the TWAIN source is named `Plustek MobileOffice A6 Duplex BU`, which is exactly the
`$device` string the script expects. Reboot/replug if prompted.

Verify the driver took:
```powershell
& "$env:USERPROFILE\Tools\naps2\App\NAPS2.Console.exe" --listdevices --driver twain
# should list: Plustek MobileOffice A6 Duplex BU
```

## 6. Secrets / `.env`
- `EDIT_PASSWORD=2Galletas!` and `SECRET_KEY=you-will-never-guess` are the known
  legacy values (also the code's fallbacks) — fine for a rehearsal box.
- **DB_\*** and **ANTHROPIC_API_KEY** are NOT in the repo; they live in the hosting
  platform's env settings. Backend runs without them: `db_ready:false`, collection
  endpoints 503, but reference + scanner endpoints work. `db_ready:true` and the
  numbers/retailers/stats/comments features need the real Postgres creds.
- `backend/.env` is gitignored — safe to hold values locally.

## 7. Frontend backend URL — handoff is out of date
The handoff says the backend URL is "hardcoded in `frontend/src/api.js`". It is
**not**: `api.js` uses relative `/api` paths (`VITE_API_BASE || ''`) and Vite
proxies `/api → http://localhost:8000` (see `vite.config.js`). No edit needed for
local dev. To point at a different backend host, set `VITE_API_BASE` — don't edit
`api.js`.

## 8. Pre-existing data glitch (not caused by setup)
One region value in the SQLite `towns` table is `Principado De Asturias\tAsturias`
(embedded tab) — it surfaces as a garbled/duplicate región in the dropdown. This is
original Flask reference data; flagging only. Fix belongs in `app/lotalf.db`, out of
scope for setup.
```
