# Security architecture

Implemented now:

- Password hashing: PBKDF2-HMAC-SHA256 (210k rounds)
- JWT access + refresh with hash-stored refresh tokens and revocation
- Object-level authorization on sessions, results, journals, comparisons
- CORS allowlist
- In-memory rate limits (auth 30/min, default 120/min)
- Input validation via Pydantic
- Parameterized SQL via SQLAlchemy
- Audit and security event tables
- Admin routes role-gated
- Webhook/payment providers not enabled without secrets
- Coach prompt-injection and crisis heuristics

Not claimed: SOC2, ISO 27001, penetration-test sign-off, RLS on SQLite.

Production must add: PostgreSQL RLS, secret manager, WAF, Sentry, dependency scanning in a blocking gate, MFA for admins.
