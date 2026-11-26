from __future__ import annotations

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import (
    Entitlement,
    FeatureFlag,
    Referral,
    Subscription,
    User,
    UserPreference,
    UserProfile,
)
from app.security import hash_password


def seed_if_needed(db: Session) -> None:
    settings = get_settings()
    defaults = {
        "social_login": False,
        "push_notifications": False,
        "enterprise": True,
        "stripe": False,
    }
    for key, enabled in defaults.items():
        if not db.get(FeatureFlag, key):
            db.add(FeatureFlag(key=key, enabled=enabled, description=f"Default flag {key}"))

    existing = db.query(User).filter(User.email == settings.demo_user_email).first()
    if existing:
        db.commit()
        return

    demo = User(
        email=settings.demo_user_email,
        password_hash=hash_password(settings.demo_user_password),
        role="user",
        email_verified=True,
    )
    admin = User(
        email="admin@personalitydna.ai",
        password_hash=hash_password(settings.demo_user_password),
        role="admin",
        email_verified=True,
    )
    db.add_all([demo, admin])
    db.flush()
    for user, name in ((demo, "Alex Rivera"), (admin, "Jordan Admin")):
        db.add(UserProfile(user_id=user.id, display_name=name, headline="Exploring PersonalityDNA AI"))
        db.add(UserPreference(user_id=user.id))
        db.add(Subscription(user_id=user.id, plan="premium" if user.role == "user" else "staff", provider="internal"))
        db.add(Entitlement(user_id=user.id, code="premium", active=True, source="seed"))
        db.add(Referral(referrer_id=user.id, code=user.id[:8].upper(), status="issued"))
    db.commit()
