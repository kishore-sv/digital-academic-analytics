"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.router import api_router
from app.core.brand import API_TITLE
from app.core.config import settings
from app.core.limiter import limiter
from app.ml.model_loader import model_loader
from app.ml_demo.routes import router as ml_demo_router
from app.openapi_meta import OPENAPI_DESCRIPTION, OPENAPI_TAGS

if settings.SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=0.1,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_loader.load()
    yield


app = FastAPI(
    title=API_TITLE,
    description=OPENAPI_DESCRIPTION,
    version="0.1.0",
    lifespan=lifespan,
    openapi_tags=OPENAPI_TAGS,
    servers=[{"url": settings.API_PREFIX, "description": "Version 1 API"}],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

_BACKEND_ROOT = Path(__file__).resolve().parents[1]
app.mount(
    "/static/ml_demo",
    StaticFiles(directory=_BACKEND_ROOT / "static" / "ml_demo"),
    name="ml_demo_static",
)
app.include_router(ml_demo_router)


@app.get("/", tags=["meta"])
def api_index() -> dict:
    """Links to interactive API documentation and health check."""
    return {
        "service": API_TITLE,
        "version": "0.1.0",
        "api_prefix": settings.API_PREFIX,
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json",
        },
        "health": "/health",
        "repository_docs": {
            "backend_api_guide": "docs/backend-api.md",
            "backend_structure": "docs/backend-structure.md",
            "api_reference_generated": "docs/api-reference.generated.md",
        },
    }


@app.get("/health", tags=["meta"])
def health_check() -> dict:
    """Liveness probe and ML model load status."""
    return {"status": "ok", "models_loaded": model_loader.is_loaded}
