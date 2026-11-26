from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.config import get_settings

PBKDF2_ROUNDS = 210_000


def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), PBKDF2_ROUNDS)
    return f"pbkdf2_sha256${PBKDF2_ROUNDS}${salt}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        scheme, rounds, salt, digest = encoded.split("$", 3)
    except ValueError:
        return False
    if scheme != "pbkdf2_sha256":
        return False
    candidate = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), int(rounds)
    ).hex()
    return hmac.compare_digest(candidate, digest)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_token(subject: str, token_type: str, extra: dict[str, Any] | None = None) -> str:
    settings = get_settings()
    if token_type == "access":
        lifetime = timedelta(minutes=settings.jwt_access_token_minutes)
    else:
        lifetime = timedelta(days=settings.jwt_refresh_token_days)
    payload = {
        "sub": subject,
        "typ": token_type,
        "iat": int(_now().timestamp()),
        "exp": int((_now() + lifetime).timestamp()),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.app_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str, expected_type: str | None = None) -> dict[str, Any]:
    settings = get_settings()
    payload = jwt.decode(token, settings.app_secret_key, algorithms=[settings.jwt_algorithm])
    if expected_type and payload.get("typ") != expected_type:
        raise jwt.InvalidTokenError("Unexpected token type")
    return payload
