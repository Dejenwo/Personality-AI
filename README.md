# PersonalityDNA AI

**Discover Yourself. Understand Others. Transform Your Life.**

AI-powered personality intelligence and human development platform.

Application ID: `com.personalitydna.ai`  
Repository: Personality-AI / personality-dna-ai

This is a working modular-monolith implementation: FastAPI backend, Next.js web app (consumer, admin, enterprise), Expo mobile shell, deterministic scoring engine, original 16-archetype mapping, educational AI coach, and privacy controls.

It is **not** a finished commercial launch. Independent scientific, legal, and app-store review remain outstanding. Do not treat documentation as certification.

## What works locally (verified)

- Registration, login, JWT sessions, privacy consent
- Assessment marketplace with 16 instruments
- IPIP-50 Big Five and Mini-IPIP scoring (deterministic, reverse-keyed, reproducible hashes)
- Original 16-archetype mapping with mixed-profile handling
- Personality dashboard (radar + bars, not percentiles)
- Educational AI coach with crisis protocol and prompt-injection refusal
- Journal, habits, goals, development programs
- Career, leadership, relationship (consent-based) modules
- HTML/PDF reports
- Development premium entitlements
- Admin overview and enterprise org registration
- Automated backend tests (`24 passed`)

## Quick start

Use **Python 3.12 or 3.13**. Python 3.14 can work with current dependencies, but older pins failed to build `pydantic-core` from source on Windows.

```bash
# Backend (from the repo root)
cd services/backend
python3.12 -m venv .venv
# Windows: py -3.12 -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080

# Web (separate terminal)
pnpm install
pnpm --filter @personalitydna/web dev
```

Open http://localhost:3100 (web uses 3100, API uses 8080). If 3100 is busy: `pnpm --filter @personalitydna/web exec next dev --port 3200`

Demo user: `demo@personalitydna.ai` / `DemoPass123!`  
Admin user: `admin@personalitydna.ai` / `DemoPass123!`

API docs: http://localhost:8080/api/docs

## Architecture

See `docs/TECHNICAL_ARCHITECTURE.md` and `docs/ARCHITECTURE_DECISIONS.md`.

Scoring is never performed by an LLM. The coach may only interpret stored results the user authorized.

## Licensing of assessments

IPIP items are public domain ([permission](https://ipip.ori.org/newPermission.htm)). Original PersonalityDNA inventories are product constructs pending independent psychometric validation and must not be marketed as scientifically validated.

## Non-goals

- Not therapy, not a medical device, not a hiring system
- No automated high-stakes decisions
- No copying of proprietary MBTI instruments or competitor report copy
