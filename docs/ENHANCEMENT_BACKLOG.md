# Life guidance enhancement backlog

Audit date: 2026-11-26. This is an enhancement of the existing modular monolith, not a rewrite.

## Existing (preserved)

- JWT auth, consent ledger, export/delete
- Deterministic scoring `personalitydna.scoring.v1` (IPIP-50, Mini-IPIP)
- 16 original archetypes from OCEA poles
- Coach with crisis protocol and prompt-injection refusal
- Journals, habits, goals, programs, reports, admin, enterprise
- Backend tests extended to 34 passed; CI green on `cursor/life-guidance-intelligence-49c8`

## Gaps closed in this increment

| ID | Module | Work | Status |
| --- | --- | --- | --- |
| E1 | Encyclopedia | 16 profiles × 60 educational sections, free to browse | Tested |
| E2 | Preference codes | Four-letter educational codes mapped from OCEA; not MBTI | Tested |
| E3 | Personalized intelligence | Who-you-are report from measured scores + user-provided data | Tested |
| E4 | Career | Occupation explorer with O*NET sources; no fabricated wages | Tested |
| E5 | Marriage | Premarital discussion bank; pairing notes without compatibility % | Tested |
| E6 | Parenting | Adult-only educational module; no child typing | Implemented |
| E7 | Finance | Independent money-habit questionnaire; not inferred from type | Tested |
| E8 | Decisions | Weighted decision matrix + private journal | Tested |
| E9 | Values | Values ranking from user input + mission draft | Implemented |
| E10 | Blueprint | Life Blueprint payload + PDF from available data only | Implemented |
| E11 | Coach | Additional educational agents + abuse-safety refusal | Tested |
| E12 | UX | Life Guidance tab, encyclopedia, result intelligence dashboard | Implemented |
| E13 | Assessments | Plain-language Mini-IPIP *adaptation* as a separate instrument | Implemented |

Increment status: **code complete for this slice**. Not a commercial launch. Not independently scientifically reviewed. Not browser-verified on the Windows workstation.

## Still blocked or incomplete

- Independent psychometric review of original instruments and encyclopedia copy
- Licensed official RIASEC (current items remain original/unvalidated)
- Full O*NET/BLS wage ingest (occupations link out; wages are not stored)
- Stripe, RevenueCat, store billing (pricing remains a hypothesis)
- Live LLM keys (educational fallback remains)
- 8,000–12,000 words per type (this increment is structured and original, not a novel-length encyclopedia)
- Translated assessments (locale field only)
- Playwright / native Expo assessment UX
