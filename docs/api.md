# API Reference

## Overview

The FastAPI backend exposes a REST API. **Endpoints have not been implemented yet.** This document lists the planned API categories.

Base URL: `http://localhost:8000/api`

## Planned API Categories

### Authentication

| Prefix | Description |
|--------|-------------|
| `/api/auth` | Login, signup (admin only), logout, session management |

### Users & Profiles

| Prefix | Description |
|--------|-------------|
| `/api/students` | Student CRUD, profiles, academic info |
| `/api/faculty` | Faculty CRUD, assigned students |
| `/api/parents` | Parent CRUD, linked children |

### Academic Structure

| Prefix | Description |
|--------|-------------|
| `/api/departments` | Department management |
| `/api/subjects` | Subject management |

### Academic Data

| Prefix | Description |
|--------|-------------|
| `/api/attendance` | Attendance records |
| `/api/examinations` | Examination management |
| `/api/performance` | Performance marks and grades |

### Analytics & Predictions

| Prefix | Description |
|--------|-------------|
| `/api/analytics` | Institutional, department, subject analytics |
| `/api/predictions` | ML performance predictions |
| `/api/at-risk` | At-risk student detection |

### Goals & Reports

| Prefix | Description |
|--------|-------------|
| `/api/goals` | Student academic goals |
| `/api/reports` | Academic reports with alerts and trends |

## Authentication Requirements

All endpoints (except `/api/auth/login` and `/api/auth/signup`) require authentication. The backend validates:

- User identity from auth token
- User role for authorization
- `institution_id` from auth token for tenant isolation

## Related Documentation

- [Architecture](architecture.md)
- [Authentication](authentication.md)
- [Authorization](authorization.md)
