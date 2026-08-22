# Development Phases

## Phase 0: Foundation Fixes (do before Phase 5)

These three tasks unblock everything in Phases 5–6 and must be completed first:

1. **Synthetic dataset** — run `ml/src/generate_synthetic.py` → `ml/datasets/raw/synthetic_academic_data.csv` (see [dataset.md](dataset.md))
2. **Alembic init** — `uv add alembic && uv run alembic init alembic` in `backend/` (see [migrations.md](migrations.md))
3. **Client libraries** — `bun add @tanstack/react-query react-hook-form zod @hookform/resolvers` (see [frontend-stack.md](frontend-stack.md))

## Phase 1: Dataset and Problem Definition

**Deliverable:** `ml/datasets/raw/synthetic_academic_data.csv` exists and is committed (or gitignored with generation script committed).

- Run synthetic dataset generator (`ml/src/generate_synthetic.py`)
- Verify column schema matches [dataset.md](dataset.md)
- Define ML problem statements (performance, at-risk, pass/fail)
- Document feature requirements and label rules
- Explore data in `ml/notebooks/01_data_exploration.ipynb`

## Phase 2: Data Preprocessing and EDA

- Clean raw academic data
- Exploratory data analysis in Jupyter notebooks
- Identify data quality issues and class distributions
- Document data distributions and patterns
- Produce `ml/datasets/processed/train.csv` and `test.csv` (80/20 stratified split)

## Phase 3: ML Model Development

- Feature engineering (`ml/src/feature_engineering.py`)
- Train performance prediction model (`ml/src/train_performance.py`)
- Train at-risk detection model with `class_weight='balanced'` (`ml/src/train_risk.py`)
- Train pass/fail prediction model (`ml/src/train_pass_fail.py`)
- Export versioned models: `ml/models/{model}_v1.pkl` + metrics JSON

## Phase 4: Model Evaluation and Finalization

- Evaluate models per [ml-evaluation.md](ml-evaluation.md) metrics
- Verify at-risk recall ≥ 0.80 and F1 ≥ 0.70
- Add SHAP explainability to inference
- Finalize and document model performance benchmarks
- Set active model versions in `ml/models/ACTIVE_VERSIONS.json`

## Phase 5: FastAPI Backend and Academic Data System

Complete in this order:

1. **Alembic init** — before writing any SQLAlchemy model (see [migrations.md](migrations.md))
2. **SQLAlchemy models** — with audit fields (`created_at`, `updated_at`, `deleted_at`) and tenant-scoped indexes (see [database-constraints.md](database-constraints.md))
3. **First migration** — `uv run alembic revision --autogenerate -m "initial schema"`
4. **Seed script** — `backend/scripts/seed.py` loads synthetic dataset into PostgreSQL
5. **Auth implementation** — argon2-cffi + PyJWT in httpOnly cookies (see [security.md](security.md))
6. **CRUD APIs** — with pagination per [api-conventions.md](api-conventions.md)
7. **ML inference integration** — load versioned `.pkl` models, return SHAP factors
8. **Admin user management APIs**

## Phase 6: Analytics Dashboards

- Install TanStack Query + react-hook-form + zod on client (if not done in Phase 0)
- Implement Next.js middleware for role-based route protection
- Institution Admin dashboard and analytics
- Student portal with performance and predictions
- Faculty portal with assigned student views
- Parent portal with child performance views
- Reports with PDF export via WeasyPrint (see [reports.md](reports.md))

## Phase 7: Large-Scale Data Testing

- Test with full synthetic dataset (~3,200 records)
- Performance optimization for analytics queries
- Query optimization (verify index usage with `EXPLAIN`)
- Load testing on list endpoints with pagination
- Add Sentry for error tracking (see [infrastructure.md](infrastructure.md))

## Phase 8: Integration, Testing and Deployment

- Set up GitHub Actions CI (see [ci.md](ci.md))
- End-to-end integration testing
- Security testing (tenant isolation, authorization, rate limiting)
- Manual `pg_dump` backup before demo (see [infrastructure.md](infrastructure.md))
- Deployment setup and documentation finalization

## Current Status

**Phase 0** — Repository structure and documentation are complete. Next: synthetic dataset, Alembic init, and client library installation.

## Related Documentation

- [Dataset](dataset.md) — Phase 1 blocker
- [Migrations](migrations.md) — Phase 5 step 1
- [ML Pipeline](ml-pipeline.md)
- [ML Evaluation](ml-evaluation.md)
- [Security](security.md)
- [Frontend Stack](frontend-stack.md)
- [Architecture](architecture.md)
- [Overview](overview.md)
- [CI](ci.md)
