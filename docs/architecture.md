# Architecture

## Overview

Modular monolith: Next.js frontend → FastAPI backend → PostgreSQL + ML inference.

```
Next.js UI (React + shadcn/ui)
        │
   REST API (/api/v1)
        │
   FastAPI (Auth + RBAC + Services)
      /         \
PostgreSQL    ML Inference
              (Model 1, 2, Risk Engine)
```

## Backend Structure

```
backend/app/
├── api/v1/routes/     # Versioned API endpoints
├── core/              # Config, database, security
├── ml/                # Model loader, inference
├── models/            # SQLAlchemy entities
├── schemas/           # Pydantic request/response
├── services/          # Business logic
└── main.py            # FastAPI app with lifespan
```

## ML Integration

- Models loaded once at startup via `ModelLoader`
- Artifacts in `ml/models/` (configurable via `ML_MODELS_DIR`)
- scikit-learn pinned to 1.6.1 for pickle compatibility
- Risk engine reads `model3_risk_engine_config.json` as source of truth

## Multi-Tenancy

Every tenant-owned record has `institution_id`. All queries filter by the authenticated user's institution. Never trust client-provided tenant IDs.

## Roles

- `institution_admin` — full institution access
- `faculty` — assigned students only
- `student` — own data only
- `parent` — linked child only

No HOD role. No platform-admin role.
