Here’s a minimal **from-scratch** setup (about 15 lines):

```bash
# Prerequisites: Docker, uv, Bun

cp .env.example .env
docker compose up -d

cd backend && cp .env.example .env && uv sync
uv run alembic upgrade head
uv run python scripts/reseed.py --cse-demo   # CSE + ECE + IST (60 students each)
uv run uvicorn app.main:app --reload --port 8000

cd ../client && bun install && bun run dev
```

**URLs**
- App: http://localhost:3000  
- API: http://localhost:8000/docs  

**Login (after seed)**
- Admin: `admin@demo.com` / `admin123`  
- Faculty: `faculty@demo.com` / `faculty123`  
- Student: `20231CSE0260` / `student123`  

**Notes**
- `--cse-demo` drops/recreates data and seeds full demo data (can take ~1–2 min).
- Without `--cse-demo`, `reseed.py` uses the default bulk seed (`scale=100`).
- README still mentions `admin@prj649.edu`; the seed actually uses `admin@demo.com`.

If you want this added to the README as a short block, switch to **Agent mode** and I can update it.