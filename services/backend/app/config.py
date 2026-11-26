from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../../.env"), extra="ignore")

    app_name: str = "PersonalityDNA AI"
    app_env: str = "development"
    app_debug: bool = True
    app_secret_key: str = "change-me-in-any-non-local-environment"
    app_base_url: str = "http://localhost:3100"
    api_base_url: str = "http://localhost:8080"

    database_url: str = "sqlite:///./data/personalitydna.db"

    jwt_algorithm: str = "HS256"
    jwt_access_token_minutes: int = 30
    jwt_refresh_token_days: int = 14
    demo_user_email: str = "demo@personalitydna.ai"
    demo_user_password: str = "DemoPass123!"

    cors_origins: str = "http://localhost:3100,http://localhost:8081,http://127.0.0.1:3100"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-5"
    ai_provider: str = "auto"
    ai_daily_message_limit_free: int = 8
    ai_daily_message_limit_premium: int = 80

    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""

    assessment_content_dir: Path = ROOT / "assessment-content"
    ai_dir: Path = ROOT / "ai"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


@lru_cache
def get_settings() -> Settings:
    return Settings()
