# PRJ_649 — Digital Academic Performance Monitoring and Institutional Analytics System

**Team:** SMK

**Members:**
- Srivatsa Kamble — 20231CSE0257
- Kishore S V — 20231CSE0260
- Mohan A — 20231CSE0273

**Guide:** Nayeem Akhtar Sholapur

---

## Project Overview

A software-only academic performance monitoring and institutional analytics platform. The system enables universities and institutions to track student performance, generate analytics, predict outcomes, and identify at-risk students using machine learning — all within a secure multi-tenant architecture.

## Problem Statement

Educational institutions struggle to monitor student performance at scale, identify at-risk students early, and provide data-driven insights to administrators, faculty, students, and parents. Manual tracking and fragmented systems make it difficult to deliver timely interventions and institutional analytics.

## Objectives

- Provide a unified platform for academic performance monitoring across an institution
- Enable ML-powered predictions for performance, pass/fail outcomes, and at-risk detection
- Deliver role-specific dashboards for admins, students, faculty, and parents
- Ensure complete data isolation between institutions (multi-tenant)
- Support institutional, department, and subject-level analytics

## Main Features

| Portal | Key Capabilities |
|--------|------------------|
| **Institution Admin** | Analytics dashboard, department/subject analytics, student management, predictions, at-risk detection, reports |
| **Student** | Academic profile, performance, predictions, improvement areas, goal setting, reports |
| **Faculty** | Assigned students, performance tracking, predictions, at-risk students, reports |
| **Parent** | Child performance, predictions, improvement areas, reports |

## Architecture

```
Next.js Client (Bun)
        ↓
FastAPI Backend (uv)
        ↓
PostgreSQL
        ↓
ML Prediction Layer (Pickle models)
```

Each institution operates as an independent tenant with backend-enforced data isolation.

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Client** | Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, react-hook-form, zod, Bun |
| **Backend** | FastAPI, Python, SQLAlchemy, Alembic, argon2-cffi, PyJWT, slowapi, WeasyPrint, uv |
| **Database** | PostgreSQL (Alembic migrations) |
| **ML** | Pandas, NumPy, Scikit-learn, joblib, Jupyter (uv) |
| **CI** | GitHub Actions (pytest, ruff, eslint, build) |
| **Infrastructure** | Docker Compose (PostgreSQL), Sentry (optional) |

## Repository Structure

```
digital-academic-analytics/
├── client/          # Next.js frontend (Bun)
├── backend/         # FastAPI API server (uv)
├── ml/              # ML development & training (uv)
├── docs/            # Project documentation
├── docker-compose.yml
├── .env.example
└── README.md
```

## ML Pipeline

```
UCI student-mat.csv → Training (notebooks) → .pkl / .json artifacts → Python inference → FastAPI (planned)
```

Three components (trained on UCI Student Performance Dataset):
1. **Performance Prediction** — predicted final grade (G3) via HistGradientBoosting regression
2. **Pass/Fail Prediction** — PASS/FAIL classification via Logistic Regression
3. **At-Risk Detection** — rule-based risk scoring (not ML)

See [docs/ml-pipeline.md](docs/ml-pipeline.md) and [ml/README.md](ml/README.md).

## Development Phases

1. Dataset and problem definition
2. Data preprocessing and EDA
3. ML model development
4. Model evaluation and finalization
5. FastAPI backend and academic data system
6. Analytics dashboards
7. Large-scale data testing
8. Integration, testing and deployment

See [docs/development-phases.md](docs/development-phases.md) for details.

## Immediate Next Steps (Phase 0)

Before building Phase 5 backend or Phase 6 dashboards:

1. **Synthetic dataset** — `cd ml && uv run python src/generate_synthetic.py` → [docs/dataset.md](docs/dataset.md)
2. **Alembic init** — `cd backend && uv add alembic && uv run alembic init alembic` → [docs/migrations.md](docs/migrations.md)
3. **Client libraries** — `cd client && bun add @tanstack/react-query react-hook-form zod @hookform/resolvers` → [docs/frontend-stack.md](docs/frontend-stack.md)

## Local Development Setup

### Prerequisites

- [Bun](https://bun.sh) (client)
- [uv](https://docs.astral.sh/uv/) (Python)
- [Docker](https://www.docker.com/) (PostgreSQL)

### 1. Start PostgreSQL

```bash
cp .env.example .env
docker compose up -d
```

### 2. Client (Next.js)

```bash
cd client
bun install
bun run dev
```

Client runs at `http://localhost:3000`.

### 3. Backend (FastAPI)

```bash
cd backend
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

API runs at `http://localhost:8000`. Health check: `GET /health`.

### 4. ML Development

```bash
cd ml
uv sync
```

## Documentation

### Core

| Document | Description |
|----------|-------------|
| [overview.md](docs/overview.md) | Project overview and scope |
| [architecture.md](docs/architecture.md) | System architecture and technology decisions |
| [features.md](docs/features.md) | Feature list by portal |
| [development-phases.md](docs/development-phases.md) | Implementation phases |

### Database & API

| Document | Description |
|----------|-------------|
| [database.md](docs/database.md) | Planned database entities |
| [database-constraints.md](docs/database-constraints.md) | Indexes, uniqueness, audit fields |
| [migrations.md](docs/migrations.md) | Alembic migration strategy |
| [api.md](docs/api.md) | Planned API categories |
| [api-conventions.md](docs/api-conventions.md) | Pagination, errors, response envelopes |

### Auth & Security

| Document | Description |
|----------|-------------|
| [authentication.md](docs/authentication.md) | Authentication flows |
| [security.md](docs/security.md) | argon2, PyJWT, rate limiting |
| [authorization.md](docs/authorization.md) | Role-permission matrix |
| [onboarding.md](docs/onboarding.md) | Admin signup and onboarding |
| [multi-tenancy.md](docs/multi-tenancy.md) | Multi-tenant isolation |
| [user-roles.md](docs/user-roles.md) | User roles and access |
| [user-management.md](docs/user-management.md) | Admin user management |

### ML

| Document | Description |
|----------|-------------|
| [dataset.md](docs/dataset.md) | Dataset strategy (Phase 1 blocker) |
| [ml-pipeline.md](docs/ml-pipeline.md) | ML pipeline and models |
| [ml-evaluation.md](docs/ml-evaluation.md) | Metrics, versioning, SHAP explainability |

### Frontend & Reports

| Document | Description |
|----------|-------------|
| [frontend-stack.md](docs/frontend-stack.md) | TanStack Query, RHF, zod, auth handling |
| [reports.md](docs/reports.md) | PDF export with WeasyPrint |

### Infrastructure & CI

| Document | Description |
|----------|-------------|
| [infrastructure.md](docs/infrastructure.md) | Environments, secrets, Sentry, backup |
| [ci.md](docs/ci.md) | GitHub Actions CI pipeline |

## Scope Exclusions

This project does **not** include: hardware/IoT, ESP32, RFID, sensors, GIS, blockchain, smart contracts, Kubernetes, Kafka, Spark, Redis, or microservices architecture.

## License

Academic project — PRJ_649, SMK Team.
