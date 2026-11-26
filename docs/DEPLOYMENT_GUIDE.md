# Deployment guide

Do not deploy production or spend cloud budget without authorization.

Local:

1. `uvicorn` on 8080
2. `pnpm --filter @personalitydna/web dev` on 3001
3. Set `NEXT_PUBLIC_API_URL=http://localhost:8080`

Dockerfiles exist under `infrastructure/docker` and `services/backend/Dockerfile`. This environment may not have Docker installed.

Staging/production would add PostgreSQL, secret manager, HTTPS, and a deploy approval job. The GitHub Actions production deploy step is intentionally absent.
