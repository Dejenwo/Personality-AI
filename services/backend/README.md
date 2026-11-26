# PersonalityDNA AI backend

Requires Python 3.12 or 3.13. Python 3.14 needs a pydantic version with official `cp314` wheels (this repo now pins pydantic 2.12.4). Do not compile `pydantic-core` from source unless you have a Rust toolchain.

```bash
# macOS / Linux
python3.12 -m venv .venv
source .venv/bin/activate

# Windows (Python Launcher)
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8080
python -m pytest -q
```

If a previous venv was created with Python 3.14 and install failed, delete `.venv` and recreate it.

On Windows, do not run a bare `uvicorn` command. After `.venv\Scripts\activate`, `where uvicorn` often still points at global `Python312\Scripts\uvicorn.exe`, which does not see packages installed in `.venv`. Always use `python -m uvicorn` (or `services\backend\run.cmd`).

OpenAPI: http://localhost:8080/api/docs
