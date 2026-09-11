# API Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/signup` | Institution admin signup |
| POST | `/auth/login` | Role-based login |
| POST | `/auth/logout` | Clear session cookies |
| GET | `/auth/me` | Current user info |

Roles: `institution_admin`, `student`, `faculty`, `parent`

## Predictions

| Method | Path | Description |
|--------|------|-------------|
| POST | `/predictions/performance` | End-term mark prediction |
| POST | `/predictions/pass-fail` | Pass/fail prediction |
| POST | `/predictions/risk` | Risk score and level |
| POST | `/predictions/all` | Combined predictions |
| POST | `/predictions/student` | Predictions from DB data (auth required) |

## Analytics (institution_admin)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/analytics/overview` | Institutional overview stats |
| GET | `/analytics/departments` | Department-wise analytics |
| GET | `/analytics/courses` | Course performance |
| GET | `/analytics/performance-trends` | Semester trends |
| GET | `/analytics/risk-distribution` | Risk level distribution |
| GET | `/analytics/pass-fail` | Pass percentage |

## Students

| Method | Path | Description |
|--------|------|-------------|
| GET | `/students` | List students (admin) |
| GET | `/students/{id}` | Student detail |

## Goals

| Method | Path | Description |
|--------|------|-------------|
| GET | `/goals` | List student goals |
| POST | `/goals` | Create goal |

## Reports

| Method | Path | Description |
|--------|------|-------------|
| GET | `/reports/institutional` | Institutional analytics report (HTML) |

## Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check with model status |
