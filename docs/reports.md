# Reports

## Report Types

| Report | Endpoint | Format | Roles |
|--------|----------|--------|-------|
| Institutional | `GET /reports/institutional` | HTML | Admin |
| Institutional PDF | `GET /reports/institutional/pdf` | PDF | Admin |
| At-Risk | `GET /reports/at-risk` | HTML | Admin, Faculty |
| Student Prediction | `GET /reports/student/{id}` | HTML | Admin, Faculty, Student, Parent (scoped) |

## Frontend

Admin and faculty report pages use `useReportDownloads()` for one-click downloads.

## Generation

Reports are built in `backend/app/services/report_service.py` using institutional analytics and stored prediction results. PDF export uses WeasyPrint for the institutional report.

## Related Documentation

- [Features](features.md)
- [API](api.md)
