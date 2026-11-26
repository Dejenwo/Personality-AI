# Row-level security

SQLite does not enforce Postgres RLS. When moving to PostgreSQL, enable RLS on `assessment_results`, `journal_entries`, `ai_messages`, and `assessment_responses` with `user_id = auth.uid()` (Supabase) or equivalent session GUC.

Until then, object-level checks in FastAPI are the authorization layer.
