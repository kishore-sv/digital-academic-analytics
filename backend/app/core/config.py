"""Application configuration from environment variables."""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment."""

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://prj649:prj649_dev@localhost:5432/academic_analytics",
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")


settings = Settings()
