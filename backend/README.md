# PRJ_649 Backend

FastAPI backend for the Digital Academic Performance Monitoring and Institutional Analytics System.

## Setup

```bash
cp .env.example .env
uv sync
docker compose up -d   # from repo root
uv run alembic upgrade head
uv run python scripts/reseed.py
```

## Run

```bash
uv run uvicorn app.main:app --reload --port 8000
```

### PDF reports (optional, macOS)

Report PDFs work out of the box via a built-in fallback renderer. For higher-fidelity charts in PDFs (SVG support), install WeasyPrint system libraries:

```bash
brew install pango gdk-pixbuf libffi cairo
```

Restart the API after installing.

API docs: http://localhost:8000/docs

## Test

```bash
uv run pytest
uv run ruff check app tests
```

## Default Development Credentials

After `scripts/reseed.py`:

| Role | Login | Password |
|------|-------|----------|
| Admin | `admin@prj649.edu` | `admin123` |
| Faculty | `faculty@prj649.edu` | `faculty123` |
| Student | `20231CSE0260` | `student123` |
| Parent | `parent@prj649.edu` | `parent123` |

## Structure

- `app/main.py` — FastAPI application entry point
- `app/core/` — Configuration, database, security, seed constants
- `app/models/` — SQLAlchemy models
- `app/schemas/` — Pydantic request/response schemas
- `app/api/v1/` — Versioned API routes
- `app/services/` — Business logic (analytics, predictions, reports, authorization)
- `app/ml/` — ML inference layer
- `alembic/` — Database migrations
- `scripts/seed.py` — Development seed data
- `scripts/reseed.py` — Drop, migrate, and full reseed

## Security Stack

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
- [API Conventions](../docs/api-conventions.md)
- [E2E Testing](../docs/e2e-testing.md)
