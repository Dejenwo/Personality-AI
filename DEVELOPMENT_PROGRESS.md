# Development progress tracker

Statuses: Not Started · In Progress · Implemented · Tested · Verified · Blocked

| Task ID | Module | Description | Priority | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| P1-01 | Product | Market research with sources/dates | P0 | Implemented | docs/MARKET_RESEARCH.md |
| P1-02 | Product | Competitor matrix + 20 differentiators | P0 | Implemented | docs/COMPETITOR_ANALYSIS.md |
| P1-03 | Science | IPIP license + methodology | P0 | Tested | docs/ASSESSMENT_LICENSES.md; pytest scoring |
| P2-01 | Architecture | Modular monolith ADRs | P0 | Implemented | docs/ARCHITECTURE_DECISIONS.md |
| P3-01 | Repo | Monorepo, CI, Docker files | P0 | Implemented | pnpm-workspace, .github/workflows/ci.yml |
| P4-01 | Design | Tokens, distinctive UI, 5-tab nav | P0 | Implemented | apps/web design tokens + AppShell |
| P5-01 | Auth | Register/login/refresh/consent | P0 | Tested | tests/test_api.py |
| P6-01 | Scoring | IPIP-50 + Mini-IPIP engine | P0 | Tested | tests/test_scoring.py 24 tests in suite |
| P6-02 | Assessments | Sessions, resume, completion | P0 | Tested | test_assessment_completion_and_reproducible_result |
| P7-01 | Archetypes | 16 original mappings + mixed | P0 | Tested | test_archetype_strategist_pattern |
| P7-02 | Dashboard | Radar/bar, strengths, history | P0 | Implemented | apps/web/src/app/app/page.tsx |
| P8-01 | Coach | Provider abstraction + safety | P0 | Tested | test_coach_crisis_protocol, test_coach_prompt_injection_refused |
| P9-01 | Career | Original RIASEC explorer | P1 | Implemented | API + /app/career |
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
| P22-01 | QA | Backend pytest | P0 | Tested | 24 passed |
| P23-01 | Performance | Load testing | P2 | Not Started | |
| P24-01 | Beta | External beta | P2 | Blocked | Needs product owner |
| P25-01 | Launch | Stores + production | P2 | Blocked | Credentials, legal, science review |

## External blockers

- Supabase project, Stripe, RevenueCat, OpenAI, Anthropic, Apple/Google store accounts
- Independent psychometrics review
- Legal review (privacy/terms)
- Production hosting authorization
