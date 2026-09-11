# Continuous Integration (CI)

## Overview

GitHub Actions runs automated checks on every pull request and on pushes to `main`.

Workflow file: `.github/workflows/ci.yml`

## Jobs

### Backend

| Step | What it does |
|------|----------------|
| Postgres 16 service | Provides test database |
| `uv sync` | Install dependencies |
| `alembic upgrade head` | Apply migrations |
| `python scripts/seed.py` | Load development seed data |
| `ruff check app tests` | Python lint |
| `pytest` | API and integration tests |

### Client

| Step | What it does |
|------|----------------|
| `bun install --frozen-lockfile` | Install dependencies |
| `bun run lint` | ESLint |
| `bun run build` | TypeScript + Next.js build |

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable production-ready code |
| `develop` | Integration branch |
| `feature/*` | Feature branches → PR into `develop` |

## Related Documentation

- [Infrastructure](infrastructure.md)
- [E2E Testing](e2e-testing.md)
