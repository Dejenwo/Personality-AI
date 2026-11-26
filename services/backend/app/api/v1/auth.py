from __future__ import annotations

import hashlib
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.deps import get_current_user
from app.models import (
    AuditEvent,
    ConsentRecord,
    RefreshToken,
    SecurityEvent,
    Subscription,
    User,
    UserPreference,
    UserProfile,
    utcnow,
)
from app.security import create_token, decode_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10)
    display_name: str = Field(min_length=1, max_length=120)
    consent_privacy: bool
    consent_research: bool = False
    locale: str = "en"


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class RefreshIn(BaseModel):
    refresh_token: str


class PasswordIn(BaseModel):
    email: EmailStr


class ResetIn(BaseModel):
    token: str
    password: str = Field(min_length=10)


def _user_public(user: User, db: Session) -> dict:
    profile = db.get(UserProfile, user.id)
    sub = db.get(Subscription, user.id)
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "email_verified": user.email_verified,
        "locale": user.locale,
        "display_name": profile.display_name if profile else "",
        "plan": sub.plan if sub else "free",
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


def _issue(user: User, db: Session, request: Request | None = None) -> TokenOut:
    access = create_token(user.id, "access", extra={"role": user.role})
    refresh = create_token(user.id, "refresh")
    token_hash = hashlib.sha256(refresh.encode()).hexdigest()
    db.add(
        RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=utcnow() + timedelta(days=get_settings().jwt_refresh_token_days),
        )
    )
    db.add(AuditEvent(actor_id=user.id, action="auth.issue", resource="user", resource_id=user.id))
    if request:
        db.add(SecurityEvent(user_id=user.id, kind="login", ip=request.client.host if request.client else None))
    db.commit()
    return TokenOut(access_token=access, refresh_token=refresh, user=_user_public(user, db))


@router.post("/register", response_model=TokenOut, status_code=201)
def register(payload: RegisterIn, request: Request, db: Session = Depends(get_db)):
    if not payload.consent_privacy:
        raise HTTPException(status_code=400, detail="Privacy consent is required")
    if db.query(User).filter(User.email == payload.email.lower()).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        locale=payload.locale,
        email_verified=False,
    )
    db.add(user)
    db.flush()
    db.add(UserProfile(user_id=user.id, display_name=payload.display_name))
    db.add(UserPreference(user_id=user.id))
    db.add(Subscription(user_id=user.id, plan="free"))
    db.add(
        ConsentRecord(
            user_id=user.id,
            kind="privacy",
            granted=True,
            version="1.0",
            text_snapshot="Privacy notice accepted at registration.",
        )
    )
    if payload.consent_research:
        db.add(ConsentRecord(user_id=user.id, kind="research", granted=True, version="1.0"))
    return _issue(user, db, request)


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        db.add(SecurityEvent(kind="failed_login", ip=request.client.host if request.client else None, detail=payload.email.lower()))
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return _issue(user, db, request)


@router.post("/refresh", response_model=TokenOut)
def refresh(payload: RefreshIn, db: Session = Depends(get_db)):
    try:
        data = decode_token(payload.refresh_token, expected_type="refresh")
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail="Invalid refresh token") from exc
    token_hash = hashlib.sha256(payload.refresh_token.encode()).hexdigest()
    stored = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash, RefreshToken.revoked.is_(False)).first()
    if not stored:
        raise HTTPException(status_code=401, detail="Refresh token revoked")
    stored.revoked = True
    user = db.get(User, data["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return _issue(user, db)


@router.post("/logout")
def logout(payload: RefreshIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(payload.refresh_token.encode()).hexdigest()
    stored = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash, RefreshToken.user_id == user.id).first()
    if stored:
        stored.revoked = True
        db.commit()
    return {"ok": True}


@router.post("/forgot-password")
def forgot_password(payload: PasswordIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    # Always succeed to avoid account enumeration.
    token = None
    if user:
        token = create_token(user.id, "access", extra={"purpose": "reset"})
    return {
        "ok": True,
        "message": "If an account exists, a reset token was issued. In local development the token is returned.",
        "dev_token": token if get_settings().app_debug else None,
    }


@router.post("/reset-password")
def reset_password(payload: ResetIn, db: Session = Depends(get_db)):
    try:
        data = decode_token(payload.token, expected_type="access")
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid reset token") from exc
    if data.get("purpose") != "reset":
        raise HTTPException(status_code=400, detail="Invalid reset token")
    user = db.get(User, data["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password_hash = hash_password(payload.password)
    db.commit()
    return {"ok": True}


@router.post("/verify-email")
def verify_email(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.email_verified = True
    db.commit()
    return {"ok": True, "email_verified": True}


@router.get("/social-login")
def social_login():
    return {
        "enabled": False,
        "providers": ["google", "apple"],
        "reason": "OAuth client credentials are an external blocker. Email registration is available.",
    }
