# Architecture decision records

## ADR-001 — SQLite locally, PostgreSQL when hosted

Status: Accepted  
Local development and CI use SQLite so the product runs without Docker or cloud accounts. SQLAlchemy models stay dialect-portable. Production should switch `DATABASE_URL` to PostgreSQL; RLS policies in `database/policies` are documented for that stage.

## ADR-002 — Educational AI fallback

Status: Accepted  
When OpenAI/Anthropic keys are absent, a deterministic educational provider answers from authorized context. Tests and demos must not require paid APIs.

## ADR-003 — Single Next.js web surface

Status: Accepted  
Consumer, admin (`/admin`), and enterprise (`/enterprise`) share `apps/web` until traffic, compliance, or separate deploy cadences justify extraction. `apps/admin` and `apps/enterprise` remain workspace packages that point at those routes.

## ADR-004 — JWT instead of Supabase Auth in this increment

Status: Accepted  
Supabase requires a project URL and keys. JWT + hashed passwords unblock the product. A later adapter can wrap Supabase Auth without changing public `/api/v1/auth` shapes.

## ADR-005 — Original RIASEC items, not O*NET Interest Profiler copy

Status: Accepted  
O*NET Career Exploration Tools are CC BY-ND or Developer License with attribution and, if modified, validation. This increment uses original interest items and cites Holland theoretically.
