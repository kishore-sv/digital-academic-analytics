# Run ScholarPulse from scratch

Step-by-step guide to run **digital-academic-analytics** (ScholarPulse) on a **new machine** with a **fresh PostgreSQL database**. Commands assume you are in the repository root unless noted.

For a one-command installer, see [setup.md](setup.md) (`python setup.py`).

---

## Prerequisites

Install once:

| Tool | Version | Purpose |
|------|---------|---------|
| [Docker](https://docs.docker.com/get-docker/) | Desktop or Engine | PostgreSQL 16 container |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | latest | Python backend + scripts |
| [Python](https://www.python.org/downloads/) | **3.13+** | Required by `backend/pyproject.toml` |
| [Bun](https://bun.sh/docs/installation) | latest | Next.js client |

Optional:

- **ML training** — `ml/` uses its own `uv sync` (not required to run the app if `ml/models/*.pkl` already exist).

---

## 1. Clone and open the repo

```bash
git clone <your-repo-url> digital-academic-analytics
cd digital-academic-analytics
```

---

## 2. Environment files

Copy templates (skip any file you already customized):

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp client/.env.example client/.env.local
```

**Root `.env`** (used by Docker Compose):

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT`
- Default DB: `postgresql+psycopg://prj649:prj649_dev@localhost:5432/academic_analytics`

**`backend/.env`:**

- `DATABASE_URL` — must match the Postgres container (same host/port/user/password/db)
- `ML_MODELS_DIR=../ml/models` — path to pickle models from `backend/`
- `SECRET_KEY` — change for non-local use

**`client/.env.local`:**

- `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`

---

## 3. Start PostgreSQL (new or reset database)

### First time (empty Docker volume)

```bash
docker pull postgres:16
docker compose up -d
```

Wait until Postgres is healthy:

```bash
docker compose ps
# STATUS should show "healthy" for prj649_postgres
```

### Completely wipe the database and start over

This **deletes all data** in the Postgres volume:

```bash
docker compose down -v
docker compose up -d
```

Again, wait until the health check passes.

---

## 4. Backend dependencies

```bash
cd backend
uv sync
```

This creates `backend/.venv` and installs FastAPI, Alembic, SQLAlchemy, etc.

---

## 5. Database migrations (Alembic)

From `backend/`:

```bash
uv run alembic upgrade head
```

Verify:

```bash
uv run alembic current
```

You should see revision `d4e5f6a7b8c9` (or whatever is **head** in `backend/alembic/versions/`).

**What this does:** creates all tables (`departments`, `students`, `import_jobs`, `course_backlogs`, etc.) via migration scripts. It does **not** load demo users or academic data.

---

## 6. Seed demo data

After migrations, load institutions, users, courses, enrollments, marks, and ML prediction samples:

```bash
uv run python scripts/reseed.py
```

Options:

```bash
# Full deterministic dataset: 2,400 students (default)
uv run python scripts/reseed.py

# Small CSE slice plus a second institution (pytest)
uv run python scripts/reseed.py --minimal
```

**Note:** `reseed.py` drops all tables and recreates schema from SQLAlchemy models, then runs the seed. The project’s `setup.py` runs `alembic upgrade head` first, then `reseed.py` — follow that same order for a full fresh setup.

If you only need data when the schema already exists and is empty:

```bash
uv run python scripts/seed.py
```

Check what is loaded:

```bash
cd backend && uv run python scripts/seed_status.py
```

### Only 2 departments / ~13 students?

That usually means the **minimal** pytest seed ran against your dev database (CSE slice + second tenant), or `reseed.py --minimal` was used.

Restore the full **5 branches × 480 students = 2,400** dataset:

```bash
cd backend && uv run python scripts/reseed.py
```

**Note:** `pytest` only auto-reseeds when `CI=true` (GitHub Actions). Local `uv run pytest` no longer drops your full dev seed.

---

## 7. ML model artifacts

Predictions and reseed require these files under `ml/models/`:

- `model1_endterm_histgradientboosting.pkl`
- `model2_pass_fail_histgradientboosting.pkl`
- `model3_risk_engine_config.json`

They are normally committed or produced by training (see [ml/README.md](ml/README.md)). If the API fails at startup with `FileNotFoundError` for `.pkl` files, train or copy artifacts into `ml/models/` and ensure `ML_MODELS_DIR` in `backend/.env` points there.

---

## 8. Run the API

From `backend/`:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

| URL | Description |
|-----|-------------|
| http://localhost:8000/health | Health check |
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc |

---

## 9. Run the client

In a **second terminal**, from `client/`:

```bash
cd client
bun install
bun run dev
```

Open **http://localhost:3000**.

---

## 10. Sign in (seed credentials)

Use **Institution Admin** role on the login screen.

| Role | Identifier | Password |
|------|------------|----------|
| Institution admin (Demo University) | `admin@demo.com` | `admin123` |
| Faculty | `faculty@demo.com` | `faculty123` |
| Parent | `parent@demo.com` | `parent123` |
| Student | roll number e.g. `26CSE001` | `student123` |

Second tenant (isolation tests): `admin@riverside.edu` / `admin123`.

Admin features include **Imports** at `/admin/imports` (master + operational CSV/XLSX imports).

---

## Quick reference — full fresh stack

```bash
# From repo root
cp .env.example .env
cp backend/.env.example backend/.env
cp client/.env.example client/.env.local

docker pull postgres:16
docker compose down -v    # optional: only when resetting DB
docker compose up -d

cd backend
uv sync
uv run alembic upgrade head
uv run python scripts/reseed.py
uv run uvicorn app.main:app --reload --port 8000
```

Second terminal:

```bash
cd client
bun install
bun run dev
```

Automated equivalent:

```bash
python setup.py --start
```

---

## Tests and quality checks

From `backend/` (Postgres must be running; reseed recommended):

```bash
uv run pytest
uv run ruff check .
```

From `client/`:

```bash
bun run lint
bun run build
```

---

## Troubleshooting

| Problem | What to try |
|---------|-------------|
| `connection refused` on port 5432 | `docker compose up -d`; check `DATABASE_URL` matches `.env` |
| `pull access denied` / image missing | `docker pull postgres:16` (compose uses `pull_policy: never`) |
| Alembic errors after manual schema changes | Fresh DB: `docker compose down -v`, `up -d`, `alembic upgrade head`, `reseed.py` |
| ML `FileNotFoundError` on startup | Add `.pkl` files under `ml/models/` or fix `ML_MODELS_DIR` |
| Client cannot reach API | Confirm `NEXT_PUBLIC_API_URL` and API on port 8000 |
| Login fails after reseed | Use `admin@demo.com` / `admin123` with role **Institution Admin** |

---

## Production

This document is for **local development**. For deployment, env secrets, migrations without `reseed`, and hosting, see [docs/deployment.md](docs/deployment.md) and [docs/infrastructure.md](docs/infrastructure.md).
