# Infrastructure

Environment configuration, secrets management, observability, and backup strategy.

## Environments

| Environment | Purpose | Database | Config file |
|-------------|---------|----------|-------------|
| `development` | Local development | Docker Compose Postgres (`localhost:5432`) | `.env` |
| `staging` | Pre-production integration | Hosted Postgres (Railway, Supabase, etc.) | `.env.staging` |
| `production` | Live deployment | Managed Postgres | `.env.production` |

All environment files are gitignored. Only `.env.example` is committed.

### Environment Variables

| Variable | Required in | Description |
|----------|------------|-------------|
| `DATABASE_URL` | all | PostgreSQL connection string |
| `SECRET_KEY` | all | JWT signing secret (32+ bytes in production) |
| `POSTGRES_USER` | development | Docker Compose Postgres user |
| `POSTGRES_PASSWORD` | development | Docker Compose Postgres password |
| `POSTGRES_DB` | development | Docker Compose Postgres database name |
| `ENVIRONMENT` | all | `development`, `staging`, or `production` |
| `SENTRY_DSN` | staging, production | Sentry error tracking DSN (optional) |
| `CORS_ORIGINS` | all | Comma-separated allowed origins |

## Secrets Management

- All secrets live in `.env` files — never in source code
- Generate `SECRET_KEY`: `python -c "import secrets; print(secrets.token_hex(32))"`
- Rotating `SECRET_KEY` invalidates all JWTs

## Docker Compose (Development)

```bash
cp .env.example .env
docker compose up -d
cd backend && uv run alembic upgrade head && uv run python scripts/reseed.py
```

## Observability

### Error Tracking (optional)

Set `SENTRY_DSN` in staging/production. The backend initializes Sentry when this variable is present.

### Logging

- Log level: `INFO` in production, `DEBUG` in development
- Never log passwords, JWT tokens, or credential bodies

## PostgreSQL Backup

```bash
# Backup
docker exec prj649_postgres pg_dump -U prj649 academic_analytics > backup_$(date +%Y%m%d).sql

# Restore
docker exec -i prj649_postgres psql -U prj649 academic_analytics < backup_20260415.sql
```

For production, use automated daily backups via your managed database provider.

## Deployment

See [deployment.md](deployment.md) for production deployment steps.

## Related Documentation

- [Deployment](deployment.md)
- [Migrations](migrations.md)
- [Security](security.md)
- [CI](ci.md)
