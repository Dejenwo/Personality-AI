.PHONY: backend test-backend web install-web

backend:
	cd services/backend && .venv/bin/python -m uvicorn app.main:app --reload --port 8080

test-backend:
	cd services/backend && .venv/bin/python -m pytest -q

install-web:
	pnpm install

web:
	pnpm --filter @personalitydna/web dev
