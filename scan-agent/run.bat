@echo off
REM Launch the LotAlfWeb local scan agent. Double-click this, or add a shortcut
REM to it in shell:startup so it runs at login. See README.md.
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo [scan-agent] Creating virtual environment...
  py -3.12 -m venv .venv || python -m venv .venv
  call ".venv\Scripts\activate.bat"
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt
) else (
  call ".venv\Scripts\activate.bat"
)
echo [scan-agent] Starting on http://127.0.0.1 (see .env PORT)...
python agent.py
