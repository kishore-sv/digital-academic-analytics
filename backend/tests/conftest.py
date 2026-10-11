"""Pytest configuration and fixtures."""

import warnings

import pytest
from fastapi.testclient import TestClient

warnings.filterwarnings("ignore", category=UserWarning)


@pytest.fixture(scope="session", autouse=True)
def load_ml_models():
    from app.ml.model_loader import model_loader
    if not model_loader.is_loaded:
        model_loader.load()


@pytest.fixture(scope="session", autouse=True)
def disable_rate_limiting():
    from app.core.limiter import limiter
    limiter.enabled = False


@pytest.fixture(scope="session", autouse=True)
def ensure_seeded_database():
    """Reseed a minimal slice in CI only — do not wipe a local 2,400-student dev DB."""
    import os

    if os.environ.get("CI") != "true" and os.environ.get("PYTEST_RESEED") != "1":
        return
    try:
        from scripts.reseed import reseed

        reseed(minimal=True)
    except Exception:
        pass


@pytest.fixture(scope="module")
def client():
    from app.main import app
    with TestClient(app) as c:
        yield c
