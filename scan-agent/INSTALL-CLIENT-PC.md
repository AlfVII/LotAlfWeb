# Client PC setup — scanner for the deployed app

Step-by-step to prepare the **user's Windows PC** (the one the Plustek D620 is
plugged into) so the scanner works from the **live site**
`https://losdecimosdeildefonso.com`. Written to be executed by an install agent.

> **There is nothing to install for the UI itself** — the app is hosted; the user
> just opens `https://losdecimosdeildefonso.com` in a browser. This guide only
> sets up the **scanner + local scan agent**, because a browser cannot drive a
> TWAIN scanner directly. OCR, the database, and the Anthropic API key all live
> on the server — **this PC holds no secrets.**

Architecture recap (details in `README.md`):
```
Browser @ losdecimosdeildefonso.com  ──/duplex──▶  scan agent (this PC, localhost:8765) ──▶ NAPS2 ──▶ Plustek D620
                                     ──everything else──▶ server (OCR, DB, save)
```

---

## Prerequisites — install in this order

### 1. Plustek D620 TWAIN driver
- Connect the Plustek MobileOffice D620 by USB.
- Download the driver (V6.0.2.2, ~138 MB, signed by PLUSTEK INC.):
  `https://d3b63i9tvm4mo6.cloudfront.net/downloads/english/driver/MobileOfficeD620_V6022_6L.zip`
  (or from the Plustek D620 support page → Windows driver).
- Extract it and run the single installer inside
  (`Release Plustek MobileOffice A6 Duplex BUS Power V6022 WebDriver.exe`).
  Install the **TWAIN** driver (not WIA). Reboot/replug if prompted.
- Verify: Device Manager shows the sheetfed scanner **OK** (not "Error /
  CM_PROB_FAILED_INSTALL").

### 2. NAPS2 (portable)
- Download `naps2-<version>-win-x64.zip` from `https://www.naps2.com` (or the
  NAPS2 GitHub releases). The `-win-x64.zip` is the portable build.
- Extract to `%USERPROFILE%\Tools\naps2\` so the console is at
  `%USERPROFILE%\Tools\naps2\App\NAPS2.Console.exe`.
- Verify the scanner is visible through NAPS2:
  ```powershell
  & "$env:USERPROFILE\Tools\naps2\App\NAPS2.Console.exe" --listdevices --driver twain
  # expected: Plustek MobileOffice A6 Duplex BU
  ```

### 3. Python 3.12 (3.11+ works) — `https://www.python.org` (tick "Add to PATH").
### 4. Git — `https://git-scm.com`.

---

## Install & configure the scan agent

```powershell
git clone https://github.com/AlfVII/LotAlfWeb.git
cd LotAlfWeb\scan-agent
py -3.12 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `scan-agent\.env` (adjust the username in the path):
```env
SCAN_SCRIPT=C:/Users/<you>/LotAlfWeb/tools/scan_duplex.ps1
PORT=8765
CORS_ORIGINS=https://losdecimosdeildefonso.com,https://www.losdecimosdeildefonso.com
SCAN_TOKEN=
```
> **Leave `SCAN_TOKEN` empty.** The deployed frontend was built without a scan
> token, so the agent must not require one. (To add a token later you must set it
> here *and* have the frontend rebuilt with a matching `VITE_SCAN_TOKEN` — see
> README §6.)
>
> `SCAN_SCRIPT` must point at `tools/scan_duplex.ps1` inside this clone. No DB
> credentials or API keys go in this file — the agent only scans.

PowerShell execution policy (only needed for running the scan script manually;
the agent already invokes it with `-ExecutionPolicy Bypass`):
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## Run it

```powershell
# from scan-agent\, with .venv active:
python agent.py
```
or double-click **`run.bat`** (creates the venv + installs deps on first run).

**Autostart at login:** press <kbd>Win</kbd>+<kbd>R</kbd> → `shell:startup` → put a
**shortcut to `run.bat`** there.

---

## Verify end-to-end

1. Agent health: open `http://localhost:8765/health` →
   `{"ok":true,"script_found":true,...}` (`script_found:false` ⇒ fix `SCAN_SCRIPT`).
2. Open `https://losdecimosdeildefonso.com`, enter **edit mode** (the edit-mode
   password is configured on the server), go to **Colección de administraciones**.
3. Load a décimo (short edge first, wait for the **solid** light), click
   **"Escanear décimo"**. Expected: status shows *Escaneando…* then *Leyendo…*,
   both faces appear **upright**, and the ficha auto-fills for review → **Guardar**.

---

## Notes

- **No secrets on this PC.** The agent has no DB access and no Anthropic key; OCR
  runs on the server. The only optional secret is `SCAN_TOKEN` (left empty here).
- The agent binds to `127.0.0.1` (not reachable from the network) and only serves
  the origins listed in `CORS_ORIGINS`.
- `https://` page → `http://localhost:8765` is allowed by browsers (localhost is a
  secure context) — no TLS needed on the agent.
- Full reference, security model, and troubleshooting: **`scan-agent/README.md`**.
