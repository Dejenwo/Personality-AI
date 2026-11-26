# Technical architecture

PersonalityDNA AI ships as a **modular monolith**.

```
Web / (future) Expo
        |
   REST /api/v1
        |
 FastAPI application
   auth | assessments | scoring | coach | growth | privacy | billing hooks
        |
 SQLite (local) / PostgreSQL (production when provisioned)
```

## Runtime (current)

- Backend: Python 3.12, FastAPI, SQLAlchemy 2, JWT (HS256), PBKDF2 passwords
- Scoring: `services/backend/app/scoring` — pure functions, no I/O, no LLM
- Coach: provider interface (`educational` | `openai` | `anthropic`)
- Web: Next.js 15 App Router, Tailwind, client fetch + bearer token
- Mobile: Expo shell, same five tabs
- Admin / enterprise: route groups on the web app (ADR-003)

## Boundaries

| Module | Owner package | Rule |
| --- | --- | --- |
| Scoring | `app.scoring` | Identical inputs → identical outputs |
| AuthZ | API + user_id filters | Object-level; no cross-user session reads |
| Coach | `app.coaching` | May read authorized results only |
| Journals | `journals` APIs | Never in relationship comparison |

## What is not running yet

Supabase, Stripe, RevenueCat, Sentry, hosted PostgreSQL, app-store builds. Those need credentials and spend approval.
