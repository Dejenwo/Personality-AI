.PHONY: backend test-backend web install-web

backend:
	cd services/backend && .venv/bin/uvicorn app.main:app --reload --port 8000

test-backend:
	cd services/backend && .venv/bin/pytest -q

install-web:
	pnpm install

web:
	pnpm --filter @personalitydna/web dev
