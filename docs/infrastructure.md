# Infrastructure

Environment configuration, secrets management, observability, and backup strategy.

## Environments

| Environment | Purpose | Database | Config file |
|-------------|---------|----------|-------------|
| `development` | Local development | Docker Compose Postgres (`localhost:5432`) | `.env` |
| `staging` | Pre-demo integration testing | Hosted Postgres (e.g. Railway, Supabase free tier) | `.env.staging` |
| `production` | Capstone demo / evaluation | Managed Postgres | `.env.production` |

All environment files are gitignored. Only `.env.example` is committed, documenting required keys without values.

### Environment Variables

| Variable | Required in | Description |
|----------|------------|-------------|
| `DATABASE_URL` | all | PostgreSQL connection string |
| `SECRET_KEY` | all | JWT signing secret (strong random value in prod) |
| `POSTGRES_USER` | development | Docker Compose Postgres user |
| `POSTGRES_PASSWORD` | development | Docker Compose Postgres password |
| `POSTGRES_DB` | development | Docker Compose Postgres database name |
| `ENVIRONMENT` | all | `development`, `staging`, or `production` |
| `SENTRY_DSN` | staging, production | Sentry error tracking DSN (optional) |
| `RISK_MODEL_VERSION` | all | Active risk model version (e.g. `1`) |
| `PERFORMANCE_MODEL_VERSION` | all | Active performance model version |
| `PASS_FAIL_MODEL_VERSION` | all | Active pass/fail model version |

## Secrets Management

- All secrets live in `.env` files — never in source code or version control
- `.env.example` documents every required key with placeholder values
- `SECRET_KEY` must be a cryptographically random string in staging/production
- Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
- Rotate `SECRET_KEY` invalidates all existing JWTs — plan for this in production

## Docker Compose (Development)

PostgreSQL runs via Docker Compose using the locally available `postgres:16` image:

```bash
cp .env.example .env
docker compose up -d
```

See root `docker-compose.yml`. Uses `pull_policy: never` to avoid downloading images.

## Observability

### Error Tracking (optional, recommended for demo)

**Sentry** free tier for backend exception capture.

| Property | Value |
|----------|-------|
| Library | `sentry-sdk[fastapi]` (future: `uv add sentry-sdk`) |
| When to add | Before Phase 7 (large-scale testing) |
| What it captures | Unhandled exceptions, request context |
| Context tags | `institution_id`, `user_id`, `role` (no PII) |

Sentry is optional for the capstone demo but valuable for debugging once faculty/students are using the system.

### Logging

- FastAPI uses Python `logging` module
- Log level: `INFO` in production, `DEBUG` in development
- Never log passwords, JWT tokens, or full request bodies containing credentials
- Log failed login attempts with IP address and identifier (not password)

## PostgreSQL Backup

For the capstone demo, automated backups are out of scope. Manual backup before demo day:

```bash
# Backup
docker exec prj649_postgres pg_dump -U prj649 academic_analytics > backup_$(date +%Y%m%d).sql

# Restore
docker exec -i prj649_postgres psql -U prj649 academic_analytics < backup_20260415.sql
```

For a production deployment, configure automated daily `pg_dump` via cron or a managed database service with built-in backups.

## Related Documentation

- [Migrations](migrations.md)
- [Security](security.md)
- [CI](ci.md)
- [Development Phases](development-phases.md)
