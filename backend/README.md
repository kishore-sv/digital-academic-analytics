# PRJ_649 Backend

FastAPI backend for the Digital Academic Performance Monitoring and Institutional Analytics System.

## Setup

```bash
cp .env.example .env
uv sync
```

## Run

```bash
uv run uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

## Test

```bash
uv run pytest
```

## Structure

- `app/main.py` — FastAPI application entry point
- `app/core/` — Configuration, database, security
- `app/models/` — SQLAlchemy models (stubs)
- `app/schemas/` — Pydantic schemas (stubs)
- `app/api/routes/` — API route modules (stubs)
- `app/services/` — Business logic services (stubs)
- `app/ml/` — ML inference layer (stubs)
