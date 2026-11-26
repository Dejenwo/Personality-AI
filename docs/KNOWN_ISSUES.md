# Known issues

- Access tokens stored in `localStorage` (XSS risk).
- Rate limiter is in-memory (not multi-instance).
- Coach crisis detection is keyword-based, not a clinical model.
- Original inventories have no reliability/validity sample.
- Mobile app is a navigation shell; full assessment UX is on web.
- Admin MFA is not implemented.
- Email sending is stubbed (forgot-password returns a dev token when `APP_DEBUG`).
- Social login is disabled until OAuth clients exist.
- Next.js e2e and accessibility automated scans are not in CI yet.
- `hash()` for daily insights is process-randomized; insight text can differ across processes — acceptable for copy rotation.
