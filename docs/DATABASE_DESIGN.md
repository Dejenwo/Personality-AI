# Database design

SQLAlchemy models in `services/backend/app/models.py` cover users, profiles, preferences, consents, sessions, responses, results, conversations, messages, AI usage, journals, goals, habits, enrollments, relationship invitations, reports, subscriptions, entitlements, organizations, memberships, notifications, referrals, feature flags, audit/security events, export and deletion requests, and feedback.

Local engine: SQLite. Hosted: set `DATABASE_URL` to PostgreSQL. Draft RLS notes live in `database/policies/README.md`.
