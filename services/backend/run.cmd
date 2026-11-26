@echo off
cd /d "%~dp0"
set PYTHONNOUSERSITE=1
if not exist ".venv\Scripts\python.exe" (
  echo Create a Python 3.12 venv first:
  echo   py -3.12 -m venv .venv
  echo   .venv\Scripts\python.exe -m pip install -r requirements.txt
  exit /b 1
)
".venv\Scripts\python.exe" -c "import sys; print('Using', sys.executable, sys.version.split()[0])"
".venv\Scripts\python.exe" -m uvicorn app.main:app --reload --port 8080
