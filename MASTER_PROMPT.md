# PersonalityDNA AI — governing product and engineering specification

This file is the master prompt for Option C: a complete commercial, enterprise-grade PersonalityDNA AI platform.

Product: AI-Powered Personality Intelligence and Human Development Platform  
Application ID: `com.personalitydna.ai`  
Platforms: iOS, Android, Web, Tablet  
Business model: Freemium, premium subscriptions, digital reports, enterprise licensing  
Initial audience: adults 18+

The implementing team must act as an implementation-focused engineering organization, not an advisor. Build actual software. Do not stop at plans, mockups, or incomplete prototypes. Do not fabricate progress, science, market numbers, or test results.

## Mission

Help people understand who they are, how they think, why they behave as they do, what motivates them, how they communicate and decide, how they relate, and how they can develop — as a **continuous practice**, not a one-time quiz.

## Non-negotiable rules

1. Build real software.
2. Do not fabricate progress, science, market research, or tests.
3. Do not hardcode or commit secrets.
4. Do not copy proprietary assessment instruments (including MBTI).
5. Do not use AI as the deterministic scoring engine.
6. Do not diagnose psychological or medical conditions.
7. Do not use personality scores for automated high-stakes decisions.
8. Do not expose journals or coaching history in relationship comparison.
9. Do not publish to app stores or incur paid cloud costs without authorization.
10. Request humans only for credentials, legal, scientific validation, payments, and irreversible ops.

## Scientific stance

Primary foundation: Big Five via public-domain IPIP Big-Five Factor Markers (Goldberg, 1992; IPIP).  
Archetypes: 16 original descriptive product constructs mapped from trait means, with mixed profiles allowed.  
Original inventories (communication, leadership, career explorer, etc.) are **unvalidated** until independent psychometric review.

## Modules (product)

Personality Discovery Center, Scoring Engine, Big Five, Archetypes, Dashboard, AI Coach, Agentic orchestration (start simple), Career, Relationships, Leadership, Emotional awareness, Development academy, Journal, Habits/goals, Reports, Referrals, Notifications, Subscriptions, Enterprise portal, Admin portal.

## Technical defaults

- Mobile: React Native / Expo / TypeScript
- Web: Next.js / TypeScript / Tailwind
- Backend: Python FastAPI, SQLAlchemy, versioned `/api/v1`
- Data: PostgreSQL in production; SQLite is the authorized local default
- Auth: JWT locally; Supabase Auth when credentials exist
- AI: OpenAI and Anthropic behind a provider interface; educational fallback without keys
- Payments: Stripe / RevenueCat / store billing when credentials exist

## Execution

Inspect the repo, continue from `DEVELOPMENT_PROGRESS.md`, implement, test, document, repeat.

Full original prompt text is the user-supplied Option C master prompt in the initiating conversation; this file is the durable in-repo copy of the governing rules and scope.
