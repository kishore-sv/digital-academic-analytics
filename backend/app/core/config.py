"""Application configuration from environment variables."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings:
    """Application settings loaded from environment."""

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://prj649:prj649_dev@localhost:5432/academic_analytics",
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    ML_MODELS_DIR: str = os.getenv(
        "ML_MODELS_DIR",
        str(_REPO_ROOT / "ml" / "models"),
    )

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    JWT_ALGORITHM: str = "HS256"

    # CORS
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000"
    ).split(",")

    # Cookies
    COOKIE_SECURE: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"

    # Observability
    SENTRY_DSN: str | None = os.getenv("SENTRY_DSN")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")


settings = Settings()
