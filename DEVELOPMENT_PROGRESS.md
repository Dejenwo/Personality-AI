# Development progress tracker

Statuses: Not Started · In Progress · Implemented · Tested · Verified · Blocked

| Task ID | Module | Description | Priority | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| P1-01 | Product | Market research with sources/dates | P0 | Implemented | docs/MARKET_RESEARCH.md |
| P1-02 | Product | Competitor matrix + 20 differentiators | P0 | Implemented | docs/COMPETITOR_ANALYSIS.md |
| P1-03 | Science | IPIP license + methodology | P0 | Tested | docs/ASSESSMENT_LICENSES.md; pytest scoring |
| P2-01 | Architecture | Modular monolith ADRs | P0 | Implemented | docs/ARCHITECTURE_DECISIONS.md |
| P3-01 | Repo | Monorepo, CI, Docker files | P0 | Implemented | pnpm-workspace, .github/workflows/ci.yml |
| P4-01 | Design | Tokens, distinctive UI, 5-tab nav | P0 | Implemented | AppShell: Home, Discover, Guidance, AI Coach, My Growth |
| P5-01 | Auth | Register/login/refresh/consent | P0 | Tested | tests/test_api.py |
| P6-01 | Scoring | IPIP-50 + Mini-IPIP engine | P0 | Tested | tests/test_scoring.py; suite now 34 passed |
| P6-02 | Assessments | Sessions, resume, completion | P0 | Tested | test_assessment_completion_and_reproducible_result |
| P7-01 | Archetypes | 16 original mappings + mixed | P0 | Tested | test_archetype_strategist_pattern |
| P7-02 | Dashboard | Radar/bar, strengths, history | P0 | Implemented | apps/web/src/app/app/page.tsx |
| P8-01 | Coach | Provider abstraction + safety | P0 | Tested | crisis, injection, abuse-not-personality |
| P9-01 | Career | RIASEC + O*NET occupation explorer | P1 | Tested | /app/guidance/career; no fabricated wages |
| P10-01 | Relationships | Invite, consent, no journal leak | P1 | Tested | test_relationship_does_not_leak_journal |
| P11-01 | Leadership | Preferences + insights | P1 | Implemented | /app/leadership |
| P12-01 | Emotions | Educational activities | P1 | Implemented | /app/emotions |
| P13-01 | Academy | Programs 7–365 days | P1 | Implemented | content.PROGRAMS + enroll API |
| P14-01 | Journal/habits/goals | Private journal, habits, goals | P1 | Implemented | APIs + screens |
| P15-01 | Reports | JSON + PDF | P1 | Tested | test_export_and_report |
| P16-01 | Monetization | Plans + local premium grant | P1 | Implemented | /app/premium; Stripe Blocked |
| P17-01 | Admin | Overview + user list | P1 | Tested | test_admin_ok_for_admin |
| P18-01 | Enterprise | Org create, consent default off | P1 | Implemented | /enterprise |
| P19-01 | i18n | English first + locale field | P2 | Implemented | en.json; other locales Not Started |
| P20-01 | Growth | Referrals, marketing pages | P1 | Implemented | /app/referrals + marketing routes |
| P21-01 | Security | Threat model + authZ tests | P0 | Implemented | docs/THREAT_MODEL.md |
| P22-01 | QA | Backend pytest | P0 | Tested | 34 passed; CI green on life-guidance PR |
| P23-01 | Performance | Load testing | P2 | Not Started | |
| P24-01 | Beta | External beta | P2 | Blocked | Needs product owner |
| P25-01 | Launch | Stores + production | P2 | Blocked | Credentials, legal, science review |
| E1 | Encyclopedia | 16 profiles × 60 sections | P0 | Tested | GET /api/v1/life/encyclopedia |
| E2 | Preference codes | Educational four-letter labels from OCEA | P0 | Tested | test_preference_code_for_strategist_pattern |
| E3 | Who you are | Personalized report from measured scores | P0 | Tested | /api/v1/life/who-you-are |
| E4 | Occupations | O*NET explorer, wages not stored | P0 | Tested | test_occupations_do_not_fabricate_wages |
| E5 | Marriage | 150 discussion questions, no compatibility % | P0 | Tested | test_premarital_bank_has_one_hundred_fifty |
| E6 | Parenting | Adult-only; no child typing | P1 | Implemented | /app/guidance/family |
| E7 | Finance | Independent money-habit questionnaire | P0 | Tested | test_finance_independent_of_personality |
| E8 | Decisions | Weighted matrix + journal | P0 | Tested | test_decision_matrix_is_transparent_and_user_weighted |
| E9 | Values | User-ranked values + mission draft | P1 | Implemented | /app/guidance/purpose |
| E10 | Blueprint | Life Blueprint from available data | P1 | Implemented | /app/blueprint |
| E11 | Coach agents | Marriage, finance, parenting, abuse safety | P0 | Tested | test_abuse_is_not_personality |
| E12 | Guidance UX | Guidance tab + intelligence dashboard | P1 | Implemented | AppShell + /app/results/[id] |
| E13 | Plain Mini-IPIP | Separate unvalidated wording adaptation | P1 | Implemented | catalog slug quick-discovery-plain |

## External blockers

- Supabase project, Stripe, RevenueCat, OpenAI, Anthropic, Apple/Google store accounts
- Independent psychometrics review
- Legal review (privacy/terms)
- Production hosting authorization
