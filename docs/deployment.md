# Deployment

Production deployment guide for PRJ_649 Academic Analytics.

## Architecture

```
Next.js (Vercel / Node host)  →  FastAPI (Railway / Fly / VPS)  →  Managed PostgreSQL
```

## Backend

1. Provision PostgreSQL and set `DATABASE_URL`
2. Set `SECRET_KEY` (32+ random bytes), `CORS_ORIGINS` (client URL), `COOKIE_SECURE=true`
3. Deploy with uvicorn:

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run python scripts/seed.py   # first deploy only, or import production data
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

4. Optional: set `SENTRY_DSN` for error tracking

## Client

1. Set `NEXT_PUBLIC_API_URL` to your API base (e.g. `https://api.example.com/api/v1`)
2. Build and deploy:

```bash
cd client
bun install --frozen-lockfile
bun run build
bun run start
```

## Health Checks

- Backend: `GET /health` → `{"status":"ok","models_loaded":true}`
- Client: root page loads; login redirects to role dashboard

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on every PR:
- Backend: migrate, seed, ruff, pytest
- Client: lint, build

## Related Documentation

- [Infrastructure](infrastructure.md)
- [Security](security.md)
- [E2E Testing](e2e-testing.md)
