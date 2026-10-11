# End-to-End Testing

## Prerequisites

```bash
docker compose up -d
cd backend && uv run python scripts/reseed.py
uv run uvicorn app.main:app --reload   # port 8000
cd client && cp .env.example .env && bun run dev   # port 3000
```

Pytest reseeds with `scripts/reseed.py --minimal`. The default reseed loads 2,400 students.

## Development Credentials

| Role | Login | Password |
|------|-------|----------|
| Admin | `admin@demo.com` | `admin123` |
| Faculty | `faculty@demo.com` | `faculty123` |
| Student | `26CSE001` | `student123` |
| Parent | `parent@demo.com` | `parent123` |

## Validation Checklist

### Institution Admin

- [ ] Login → dashboard shows KPIs + risk donut + department CGPA chart
- [ ] Analytics → three tabs (Institutional / ML Predictions / At-Risk) with filters
- [ ] Students / Faculty / Departments / Programs / Courses — list + create
- [ ] Predictions — select student → run ML prediction
- [ ] At-Risk — KPIs, charts, enriched table
- [ ] Reports — analytical preview + download HTML/PDF

### Faculty

- [ ] Dashboard shows scoped stats and charts
- [ ] Marks Entry — course → assessment → roster → bulk save
- [ ] Attendance — bulk update attendance %
- [ ] Results — semester results for assigned students
- [ ] At-risk scoped to assigned students

### Student

- [ ] Dashboard with CGPA/SGPA progression and risk chart
- [ ] Performance, predictions, improvement, goals, reports

### Parent

- [ ] Dashboard with child performance and risk overview
- [ ] Performance, predictions, improvement, reports

### Auth

- [ ] Logout clears session; middleware redirects to login
- [ ] Role routes blocked cross-portal
- [ ] Token refresh on 401

## Automated Coverage

Backend pytest covers auth, RBAC, tenant isolation, academic APIs, analytics chart aggregations, goals, reports, scoped analytics, and the full ML integration flow. Pytest reseeds with `--minimal`. Client lint and build run in CI.
