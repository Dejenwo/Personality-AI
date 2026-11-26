# Threat model (initial)

Date: 2026-11-26  
Method: informal STRIDE on current code, not a certified assessment.

| Asset | Threat | Mitigation now | Residual |
| --- | --- | --- | --- |
| Passwords | Credential stuffing / theft | Hashing, failed-login events, rate limit | No MFA, no lockout policy yet |
| JWT | Token theft from XSS/localStorage | Short access TTL, refresh revocation | Web stores tokens in localStorage — XSS remains a risk; HttpOnly cookies planned |
| Assessment results | IDOR | Session and result lookups scoped by user_id; tests cover cross-user 404 | Admin export paths need continued review |
| Journals | Cross-user read; employer read | Owner checks; excluded from relationship comparison | Need encryption-at-rest in hosted Postgres |
| Coach | Prompt injection; over-trust | Heuristic refusal; educational fallback; no score writes | Heuristics are not a complete LLM firewall |
| Crisis content | Harmful advice | Deterministic redirect to human help | Not a replacement for clinical triage |
| Payments | Webhook forgery | Providers disabled without secrets | Implement signature verify before go-live |
| Tenants | Org admin seeing scores | `results_consent` default false; no score APIs for orgs yet | Must stay false-by-default |
| Supply chain | Dep compromise | Pin requirements; CI gitleaks (non-blocking) | Add blocking SCA |
