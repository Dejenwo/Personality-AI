# Test strategy

## Executed in this increment

`cd services/backend && .venv/bin/pytest -q` → **24 passed** (2026-11-26, this environment).

Coverage includes reverse scoring, min/max/mid profiles, determinism, archetype mapping, Mini-IPIP, auth, consent, IDOR, assessment completion, crisis coach, injection refusal, admin RBAC, relationship non-leak of journals, PDF report, export.

## Not yet executed

Playwright e2e against a running browser, WCAG audit tooling, k6 load tests, SAST beyond ruff/CI placeholders, mobile detox.

Do not claim those passed.
