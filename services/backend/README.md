# PersonalityDNA AI backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
pytest -q
```

OpenAPI: http://localhost:8000/api/docs
