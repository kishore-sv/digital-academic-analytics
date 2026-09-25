# Backend API documentation

Documentation for the **FastAPI** backend (`backend/app/`). Base path: `/api/v1`.

## Quick links

| Resource | Description |
|----------|-------------|
| [Interactive API (ReDoc)](redoc.html) | Browse every endpoint, schemas, and status codes (static; no server required) |
| [API guide](api-guide.md) | Swagger locally, cookies, regenerating the markdown reference |
| [Generated reference](api-reference.md) | Per-endpoint request/response tables |
| [Folder structure](structure.md) | Routes, services, models, and layering |

## Run the live API locally

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

Then use [Swagger UI](http://localhost:8000/docs) to **execute** requests (requires a running server and login cookies).

## Regenerate docs from code

```bash
cd backend
uv run python scripts/generate_api_docs.py
uv run python scripts/export_openapi.py
```

Commit updated `docs/api-reference.generated.md` and `docs/openapi.json` if you want them in git; GitHub Pages CI regenerates them on each deploy.
