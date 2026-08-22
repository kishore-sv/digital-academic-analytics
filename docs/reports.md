# Reports and PDF Export

## Overview

The reports feature generates downloadable academic reports for admins, faculty, students, and parents. Reports are generated server-side and delivered as PDF files.

**Reports have not been implemented yet.**

## PDF Library

**WeasyPrint** — converts HTML to PDF on the server.

| Property | Value |
|----------|-------|
| Library | `weasyprint` (Python, backend only) |
| Template engine | Jinja2 (bundled with FastAPI ecosystem) |
| Install (future) | `uv add weasyprint jinja2` |
| Client-side PDF | Not used — all PDF generation is server-side |

### Why WeasyPrint

- Renders HTML/CSS templates — designers can style reports with familiar web technologies
- No client-side PDF library needed
- Works well with FastAPI `StreamingResponse`
- Suitable for capstone-scale report volumes

## Report Generation Flow

```
Client requests report
        ↓
FastAPI /api/reports/{type}
        ↓
Query data (tenant-scoped, role-filtered)
        ↓
Render Jinja2 HTML template
        ↓
WeasyPrint HTML → PDF bytes
        ↓
StreamingResponse with Content-Disposition: attachment
        ↓
Browser downloads PDF
```

## Report Types (planned)

| Report | Available to | Content |
|--------|-------------|---------|
| Student Performance Summary | Admin, Faculty (assigned), Student (own), Parent (child) | Marks, grades, attendance %, CGPA per subject |
| At-Risk Student List | Admin, Faculty (assigned) | Students flagged high/medium risk with top SHAP factors |
| Institutional Analytics Snapshot | Admin | Department-wise averages, at-risk %, pass rate |
| Semester Report Card | Student (own), Parent (child) | Full semester marks and grades |

## API Endpoints (planned)

```
GET /api/reports/student/{student_id}/performance   → PDF
GET /api/reports/at-risk                            → PDF (admin/faculty)
GET /api/reports/institutional                       → PDF (admin only)
GET /api/reports/student/{student_id}/semester       → PDF
```

All report endpoints:
- Require authentication
- Enforce role-based access (see [authorization.md](authorization.md))
- Filter data by `institution_id` from JWT
- Return `Content-Type: application/pdf`

## Template Location (planned)

```
backend/
└── app/
    └── templates/
        └── reports/
            ├── student_performance.html
            ├── at_risk_list.html
            ├── institutional_analytics.html
            └── semester_report.html
```

## Related Documentation

- [API Reference](api.md)
- [API Conventions](api-conventions.md)
- [Authorization](authorization.md)
- [ML Evaluation](ml-evaluation.md) (SHAP factors in at-risk reports)
