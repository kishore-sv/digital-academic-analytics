# API Reference

## Overview

The FastAPI backend exposes a REST API. **Endpoints have not been implemented yet.** This document lists the planned API categories.

Base URL: `http://localhost:8000/api`

For pagination, error formats, and response envelopes, see [api-conventions.md](api-conventions.md).

## Planned API Categories

### Authentication

| Method | Path | Description | Rate limited |
|--------|------|-------------|-------------|
| POST | `/api/auth/signup` | Admin signup + institution creation | Yes (3/min) |
| POST | `/api/auth/login` | Role-based login | Yes (5/min) |
| POST | `/api/auth/logout` | Clear session cookies | No |
| POST | `/api/auth/refresh` | Refresh access token | Yes (10/min) |
| GET | `/api/auth/me` | Current user info | No |

### Users & Profiles

| Prefix | Description | Paginated |
|--------|-------------|-----------|
| `/api/students` | Student CRUD, profiles, academic info | Yes |
| `/api/faculty` | Faculty CRUD, assigned students | Yes |
| `/api/parents` | Parent CRUD, linked children | Yes |

### Academic Structure

| Prefix | Description | Paginated |
|--------|-------------|-----------|
| `/api/departments` | Department management | Yes |
| `/api/subjects` | Subject management | Yes |

### Academic Data

| Prefix | Description | Paginated |
|--------|-------------|-----------|
| `/api/attendance` | Attendance records | Yes |
| `/api/examinations` | Examination management | Yes |
| `/api/performance` | Performance marks and grades | Yes |

### Analytics & Predictions

| Prefix | Description | Paginated |
|--------|-------------|-----------|
| `/api/analytics` | Institutional, department, subject analytics | Yes |
| `/api/predictions` | ML performance predictions (with SHAP factors) | Yes |
| `/api/at-risk` | At-risk student detection (with SHAP factors) | Yes |

### Goals & Reports

| Prefix | Description | Paginated |
|--------|-------------|-----------|
| `/api/goals` | Student academic goals | Yes |
| `/api/reports` | Academic reports (PDF download) | Yes |

## Authentication Requirements

All endpoints (except `/api/auth/login`, `/api/auth/signup`, and `/api/auth/refresh`) require a valid `access_token` httpOnly cookie. The backend validates:

- User identity from JWT
- User role for authorization
- `institution_id` from JWT for tenant isolation

## Pagination

All list endpoints use offset-based pagination. Default `limit=20`, max `limit=100`.

```
GET /api/students?page=1&limit=20
```

Response envelope:
```json
{ "data": [...], "meta": { "page": 1, "limit": 20, "total": 247, "total_pages": 13 } }
```

See [api-conventions.md](api-conventions.md) for full specification.

## Related Documentation

- [API Conventions](api-conventions.md)
- [Architecture](architecture.md)
- [Authentication](authentication.md)
- [Security](security.md)
- [Authorization](authorization.md)
- [Reports](reports.md)
