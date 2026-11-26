from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

os.environ.setdefault("APP_SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("APP_DEBUG", "true")
os.environ.setdefault("AI_PROVIDER", "educational")
os.environ.setdefault("DATABASE_URL", "sqlite:///" + str(BACKEND_ROOT / "data" / "test.db"))

from app.config import get_settings  # noqa: E402

get_settings.cache_clear()


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    get_settings.cache_clear()

    import app.database as database
    from app import models  # noqa: F401
    from app.database import Base

    engine = database.build_engine()
    database.engine = engine
    database.SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    from app.seed import seed_if_needed

    db = database.SessionLocal()
    seed_if_needed(db)
    db.close()

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
    get_settings.cache_clear()


def auth_header(client: TestClient, email: str = "demo@personalitydna.ai", password: str = "DemoPass123!") -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
