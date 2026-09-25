# Backend folder structure

FastAPI application root: `backend/`. Python package: `app/`.

```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, routers, /health
│   ├── openapi_meta.py      # Swagger/ReDoc tag descriptions
│   ├── api/
│   │   ├── deps.py          # Auth dependencies (AdminUser, DbSession, …)
│   │   └── v1/
│   │       ├── router.py    # Aggregates all route modules
│   │       ├── pagination.py
│   │       ├── helpers.py   # parse_uuid, get_entity_or_404, pagination dep
│   │       ├── analytics_filters.py
│   │       └── routes/      # One file per domain (see table below)
│   ├── core/
│   │   ├── config.py        # Settings from .env
│   │   ├── database.py      # SQLAlchemy engine & session
│   │   ├── security.py      # Password hashing, JWT, cookies
│   │   ├── tenant.py        # institution_id scoping helpers
│   │   ├── limiter.py       # slowapi rate limits
│   │   └── seed_data.py     # Demo credential constants
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response models (OpenAPI schemas)
│   ├── services/            # Business logic (analytics, marks, reports, ML bridge)
│   └── ml/                  # Model loading & inference wrappers used by API
├── alembic/                 # Database migrations
├── scripts/                 # seed, reseed, generate_api_docs.py
├── tests/                   # pytest API & service tests
└── pyproject.toml           # uv / dependencies
```

## Route modules (`app/api/v1/routes/`)

| Module | Prefix | Purpose |
|--------|--------|---------|
| `auth.py` | `/auth` | Login, signup, logout, refresh, `/me` |
| `users.py` | `/users` | Institution admin users |
| `institutions.py` | `/institutions` | Tenant profile |
| `departments.py` | `/departments` | Departments CRUD |
| `programs.py` | `/programs` | Programs CRUD |
| `faculty.py` | `/faculty` | Faculty CRUD, assignments |
| `parents.py` | `/parents` | Parents & child links |
| `students.py` | `/students` | Students CRUD, `/students/me` |
| `student_performance.py` | `/students` | Performance & improvement endpoints |
| `courses.py` | `/courses` | Courses CRUD |
| `academic.py` | `/academic` | Academic years & semesters |
| `assessments.py` | `/assessments` | Assessments, marks grid, bulk marks |
| `attendance.py` | `/attendance` | Attendance & rosters |
| `results.py` | `/results` | Course/semester results |
| `at_risk.py` | `/at-risk` | At-risk lists |
| `predictions.py` | `/predictions` | ML prediction endpoints |
| `analytics.py` | `/analytics` | Dashboard analytics |
| `goals.py` | `/goals` | Student goals |
| `reports.py` | `/reports` | Report generation |

## Layering

1. **Routes** — HTTP, status codes, call services, map ORM → Pydantic responses.
2. **Schemas** (`schemas/`) — Input validation and OpenAPI models (`StudentCreate`, `MarksGridResponse`, …).
3. **Services** (`services/`) — Queries, aggregations, marks calculation, PDF reports, authorization helpers.
4. **Models** (`models/`) — Tables and relationships; all tenant data includes `institution_id`.

## Auth & multi-tenancy

- Session: httpOnly cookies set by `auth/login` (see `core/security.py`).
- Dependencies in `api/deps.py` enforce role (`AdminUser`, `FacultyUser`, …).
- `services/authorization_service.py` scopes students/courses for faculty and parents.
- Every query filters by `current.institution_id` from the session.

## Related docs

- [Backend API guide](backend-api.md) — Swagger/ReDoc and trying endpoints
- [API conventions](api-conventions.md) — Pagination, errors, tenants
- [API reference (generated)](api-reference.generated.md) — Per-endpoint I/O tables
- [Architecture](architecture.md)
