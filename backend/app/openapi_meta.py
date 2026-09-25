"""OpenAPI metadata for interactive API documentation (Swagger / ReDoc)."""

OPENAPI_TAGS = [
    {
        "name": "meta",
        "description": "Service index (`GET /`) and health check (`GET /health`).",
    },
    {
        "name": "auth",
        "description": "Signup, login, logout, refresh session, and current user (`/auth/me`). Uses httpOnly cookies.",
    },
    {
        "name": "users",
        "description": "Institution admin user accounts (create, list, enable/disable).",
    },
    {
        "name": "institutions",
        "description": "Institution profile for the current tenant.",
    },
    {
        "name": "departments",
        "description": "Academic departments (CRUD). Scoped to the logged-in institution.",
    },
    {
        "name": "programs",
        "description": "Degree programs under departments.",
    },
    {
        "name": "faculty",
        "description": "Faculty profiles, course assignments, and student mentoring links.",
    },
    {
        "name": "parents",
        "description": "Parent accounts and links to student children.",
    },
    {
        "name": "students",
        "description": "Student profiles, roll numbers, and admin CRUD. Faculty see assigned students only.",
    },
    {
        "name": "student-performance",
        "description": "Per-student performance summaries and improvement insights.",
    },
    {
        "name": "courses",
        "description": "Courses/subjects by department. Faculty lists are limited to assigned courses.",
    },
    {
        "name": "academic",
        "description": "Academic years and semesters.",
    },
    {
        "name": "assessments",
        "description": "Assessments (CA, Mid, End), marks entry grid, bulk save, and rosters.",
    },
    {
        "name": "attendance",
        "description": "Attendance records and bulk entry rosters.",
    },
    {
        "name": "results",
        "description": "Course results, semester results (SGPA/CGPA), and recalculation.",
    },
    {
        "name": "at-risk",
        "description": "At-risk student lists and summary metrics.",
    },
    {
        "name": "predictions",
        "description": "ML predictions (performance, pass/fail, risk) and stored student predictions.",
    },
    {
        "name": "analytics",
        "description": "Institution analytics dashboards (admin). Charts and KPI aggregates.",
    },
    {
        "name": "goals",
        "description": "Student academic goals.",
    },
    {
        "name": "reports",
        "description": "PDF/HTML report generation and download.",
    },
]

OPENAPI_DESCRIPTION = """
ScholarPulse REST API (multi-tenant academic analytics).

## Interactive documentation

| UI | URL (server running on port 8000) |
|----|-----------------------------------|
| **Swagger UI** | [/docs](/docs) — try requests in the browser |
| **ReDoc** | [/redoc](/redoc) — readable reference |
| **OpenAPI JSON** | [/openapi.json](/openapi.json) |

API routes are mounted under **`/api/v1`** (see `API_PREFIX` in config).

## Authentication

Most endpoints require a session established via **`POST /api/v1/auth/login`** (sets httpOnly cookies).
Use the same browser session in Swagger, or call login from the client app first.

Roles: `institution_admin`, `faculty`, `student`, `parent`.

## Conventions

- **List endpoints**: paginated `{ "data": [...], "meta": { page, limit, total, total_pages } }`
- **Errors**: `{ "detail": "..." }` or validation array from FastAPI
- **Tenant scope**: `institution_id` comes from the session — never send it in the body

See repository docs: `docs/api-conventions.md`, `docs/backend-structure.md`, `docs/backend-api.md`.
"""
