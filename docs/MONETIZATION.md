# Monetization

Hypothesis only (not validated):

| Plan | Price | Contents |
| --- | --- | --- |
| Free | $0 | Quick Discovery, Big Five, dashboard, limited coach, card |
| Premium monthly | $9.99 | Reports, extra assessments, career/relationship/leadership, programs, PDF |
| Premium annual | $69.99 | Same |
| À la carte reports | $9.99–$19.99 | As in the master prompt |

Providers: Stripe (web), RevenueCat + store IAP (mobile) — **not configured**. Local development can grant premium via `/api/v1/subscriptions/premium-dev` when `APP_DEBUG=true`.

App store commissions, taxes, refunds, and restoration are unimplemented pending credentials.

Illustrative revenue at $69.99 annual is gross, not profit. See master prompt table; do not treat it as a forecast.
