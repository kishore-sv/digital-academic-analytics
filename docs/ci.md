# Continuous Integration (CI)

## Overview

GitHub Actions runs automated checks on every pull request. CI catches regressions early — especially important with three team members committing concurrently.

**The CI workflow file has not been created yet.** This document specifies the planned pipeline.

## Planned Workflow

File: `.github/workflows/ci.yml` (to be created in a future implementation task)

```yaml
name: CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  backend:
    name: Backend (Python)
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run pytest

  client:
    name: Client (Next.js)
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: client
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile
      - run: bun run lint
      - run: bun run build
```

## Checks Per Job

### Backend

| Step | Tool | What it catches |
|------|------|----------------|
| `uv sync` | uv | Dependency resolution failures |
| `ruff check .` | ruff | Python linting and style issues |
| `pytest` | pytest | Broken API endpoints, failed unit tests |

`ruff` will be added as a dev dependency: `uv add --dev ruff`

### Client

| Step | Tool | What it catches |
|------|------|----------------|
| `bun install --frozen-lockfile` | Bun | Lockfile drift |
| `bun run lint` | ESLint | TypeScript/React lint issues |
| `bun run build` | Next.js | TypeScript errors, broken routes, build failures |

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable, demo-ready code |
| `develop` | Integration branch for active development |
| `feature/*` | Individual feature branches; PR into `develop` |

All merges to `main` and `develop` require a passing CI run.

## What CI Does Not Cover (yet)

- Database migration tests (requires Postgres service in CI — add later)
- End-to-end browser tests (out of scope for capstone)
- ML model training validation (manual for now)
- Security scanning (optional future addition)

## Adding Postgres to CI (future)

When Alembic migrations exist, add a Postgres service to the backend job:

```yaml
services:
  postgres:
    image: postgres:16
    env:
      POSTGRES_USER: prj649
      POSTGRES_PASSWORD: test
      POSTGRES_DB: test_db
    ports:
      - 5432:5432
```

## Related Documentation

- [Infrastructure](infrastructure.md)
- [Migrations](migrations.md)
- [Development Phases](development-phases.md)
