# One-command setup (macOS, Linux, Windows)

After cloning the repo, from the project root:

```bash
python setup.py
```

Windows (double-click or CMD):

```bat
setup.bat
```

macOS / Linux:

```bash
chmod +x setup.sh
./setup.sh
```

## What it does

1. Checks **Python 3.13+**, **Docker**, **uv**, and **Bun** (prints install links if missing).
2. Copies env templates when targets are missing:
   - `.env.example` → `.env` (repo root, used by Docker Compose)
   - `backend/.env.example` → `backend/.env`
   - `client/.env.example` → `client/.env.local`
3. Pulls `postgres:16` and runs `docker compose up -d` (compose file uses `pull_policy: never`).
4. Waits until PostgreSQL is ready.
5. **Backend:** `uv sync` (creates `.venv` and installs dependencies).
6. **ML:** `uv sync` in `ml/` (optional training env; API uses `ml/models/*.pkl`).
7. **Database:** `alembic upgrade head`, then `scripts/reseed.py` (fresh demo data).
8. **Client:** `bun install`.

## Run everything (API + UI)

```bash
python setup.py --start
```

- API: http://localhost:8000/docs  
- App: http://localhost:3000  

**Login:** `admin@demo.com` / `admin123` — role **Institution Admin**

## Options

| Flag | Purpose |
|------|---------|
| `--start` | Start `uvicorn` and `bun dev` after setup |
| `--cse-demo` | Larger CSE/ECE/IST seed instead of default bulk seed |
| `--no-seed` | Migrations only, no reseed |
| `--no-docker` | Skip Docker (Postgres already running) |
| `--skip-ml` | Skip `ml/` uv sync |
| `--skip-client` | Backend-only setup |

## Prerequisites (install once per machine)

- [Docker Desktop](https://docs.docker.com/get-docker/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Bun](https://bun.sh/docs/installation)
- [Python 3.13+](https://www.python.org/downloads/)

Manual steps (equivalent to `setup.py`):

```bash
cp .env.example .env
docker pull postgres:16 && docker compose up -d

cd backend && cp .env.example .env && uv sync
uv run alembic upgrade head
uv run python scripts/reseed.py

cd ../ml && uv sync
cd ../client && bun install && bun run dev
```
