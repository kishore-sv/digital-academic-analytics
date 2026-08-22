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

## Migrations (planned — set up before writing models)

Alembic must be initialized before the first SQLAlchemy model is written.

```bash
# Future implementation:
uv add alembic
uv run alembic init alembic
uv run alembic revision --autogenerate -m "initial schema"
uv run alembic upgrade head
```

See [docs/migrations.md](../docs/migrations.md).

## Seed Data (planned)

After migrations, load synthetic dataset into PostgreSQL for local development:

```bash
# Future implementation:
uv run python scripts/seed.py
```

See [docs/dataset.md](../docs/dataset.md).

## Structure

- `app/main.py` — FastAPI application entry point
- `app/core/` — Configuration, database, security
- `app/models/` — SQLAlchemy models (stubs — write only after Alembic init)
- `app/schemas/` — Pydantic schemas (stubs)
- `app/api/routes/` — API route modules (stubs)
- `app/services/` — Business logic services (stubs)
- `app/ml/` — ML inference layer (stubs)
- `alembic/` — Migration files (to be created)

## Security Stack (planned)

| Concern | Library |
|---------|---------|
| Password hashing | argon2-cffi |
| Auth tokens | PyJWT in httpOnly cookies |
| Rate limiting | slowapi |

See [docs/security.md](../docs/security.md).

## Related Documentation

- [Security](../docs/security.md)
- [Migrations](../docs/migrations.md)
- [Database Design](../docs/database.md)
- [Database Constraints](../docs/database-constraints.md)
- [API Conventions](../docs/api-conventions.md)
- [Development Phases](../docs/development-phases.md)
