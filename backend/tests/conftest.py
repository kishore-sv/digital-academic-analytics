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


@pytest.fixture(scope="module")
def client():
    from app.main import app
    with TestClient(app) as c:
        yield c
