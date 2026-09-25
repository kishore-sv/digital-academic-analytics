# Backend API documentation

## Published docs (GitHub Pages)

After enabling GitHub Pages (see [deployment.md](deployment.md)), the backend docs site includes MkDocs pages and static **ReDoc** at `redoc.html` (no running server required).

## Interactive docs UI (local API server)

Start the API server:

```bash
cd backend
uv run uvicorn app.main:app --reload --port 8000
```

Then open:

| UI | URL | Best for |
|----|-----|----------|
| **Swagger UI** | http://localhost:8000/docs | Trying endpoints, seeing request/response schemas |
| **ReDoc** | http://localhost:8000/redoc | Reading grouped reference documentation |
| **OpenAPI JSON** | http://localhost:8000/openapi.json | Codegen, Postman import, CI |

All business routes live under **`http://localhost:8000/api/v1`** (configurable via `API_PREFIX`).

The root http://localhost:8000/ returns links to these UIs and `GET /health` reports ML model load status.

## What each endpoint shows in Swagger

For every operation you get:

- **Summary** — from the route function name / docstring
- **Parameters** — query, path, and headers
- **Request body** — JSON schema from Pydantic models in `backend/app/schemas/`
- **Responses** — status codes and response models (`200`, `201`, `422`, …)

Example: `POST /api/v1/students`

- **Input:** `StudentCreate` — `name`, `roll_number`, `password` (min 6), `department_id`, optional `program_id`, `semester`, `branch`
- **Output:** `201` + `StudentResponse` — `id`, `roll_number`, `name`, `department_id`, `program_id`, `semester`, `branch`, `section`

Schemas are defined once in Python and stay in sync with the running API.

## Authenticated requests in Swagger

1. Call **`POST /api/v1/auth/login`** with JSON body, for example:

```json
{
  "identifier": "admin@demo.com",
  "password": "admin123",
  "role": "institution_admin"
}
```

2. The response sets **httpOnly cookies** in the browser.
3. Other endpoints in the same browser tab use those cookies automatically.

For faculty use `role: "faculty"` and faculty email; for students use `role: "student"` and roll number as `identifier`.

## Static markdown reference

A full endpoint list with parameter and body tables is generated from OpenAPI:

```bash
cd backend
uv run python scripts/generate_api_docs.py
```

Output: [api-reference.generated.md](api-reference.generated.md)

Regenerate after adding or changing routes/schemas.

## Manual overview

Shorter hand-maintained index: [api.md](api.md).

Conventions (pagination, errors, tenancy): [api-conventions.md](api-conventions.md).

Backend layout: [backend-structure.md](backend-structure.md).
