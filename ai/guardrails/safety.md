# AI safety guardrails

- Scores come only from `app.scoring.engine`.
- Journals are excluded from context unless `allow_ai` and the user preference are both true.
- Prompt-injection attempts stay in-role.
- Crisis protocol is deterministic and does not attempt risk assessment.
- No automated high-stakes decisions.
