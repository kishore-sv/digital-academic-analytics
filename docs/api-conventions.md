# API Conventions

Standard patterns for all FastAPI endpoints. Apply these conventions when implementing any list, detail, or mutation endpoint.

## Base URL

```
http://localhost:8000/api        # development
https://api.example.com/api      # production (future)
```

## Authentication

All endpoints except `/api/auth/login`, `/api/auth/signup`, and `/api/auth/refresh` require a valid `access_token` httpOnly cookie. See [security.md](security.md).

The backend derives `institution_id` and `role` from the JWT — clients must never send these as request parameters.

## Pagination

All list endpoints use offset-based pagination.

### Request

```
GET /api/students?page=1&limit=20
GET /api/attendance?page=2&limit=50&sort=date&order=desc
```

| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| `page` | `1` | — | Page number (1-indexed) |
| `limit` | `20` | `100` | Items per page |
| `sort` | entity default | — | Sort field (optional, v1) |
| `order` | `desc` | — | `asc` or `desc` (optional, v1) |

### Response Envelope

```json
{
  "data": [ ... ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 247,
    "total_pages": 13
  }
}
```

### Endpoints Using Pagination

| Endpoint | Default sort |
|----------|-------------|
| `GET /api/students` | `created_at desc` |
| `GET /api/faculty` | `created_at desc` |
| `GET /api/parents` | `created_at desc` |
| `GET /api/attendance` | `date desc` |
| `GET /api/performance` | `semester desc` |
| `GET /api/analytics/departments` | `name asc` |
| `GET /api/at-risk` | `risk_probability desc` |
| `GET /api/reports` | `created_at desc` |

## Error Responses

All errors follow a consistent format:

```json
{
  "detail": "Human-readable error message",
  "code": "ERROR_CODE"
}
```

### Standard HTTP Status Codes

| Code | Usage |
|------|-------|
| `400` | Validation error, malformed request |
| `401` | Missing or invalid auth token |
| `403` | Authenticated but not authorized for this resource |
| `404` | Resource not found (within tenant scope) |
| `409` | Conflict (e.g. duplicate roll number within institution) |
| `422` | Pydantic validation failure (FastAPI default) |
| `429` | Rate limit exceeded |
| `500` | Unhandled server error |

### Error Codes

| Code | Meaning |
|------|---------|
| `AUTH_INVALID_CREDENTIALS` | Wrong email/roll number or password |
| `AUTH_ACCOUNT_DISABLED` | `is_login_enabled = false` |
| `AUTH_TOKEN_EXPIRED` | Access token expired; use refresh endpoint |
| `TENANT_FORBIDDEN` | Resource belongs to a different institution |
| `ROLE_FORBIDDEN` | User role cannot access this endpoint |
| `DUPLICATE_ROLL_NUMBER` | Roll number already exists in this institution |
| `DUPLICATE_EMAIL` | Email already exists in this institution |

## Tenant Filtering

- Every list and detail query includes `WHERE institution_id = :current_institution_id AND deleted_at IS NULL`
- The `institution_id` is extracted from the JWT by the auth dependency — never from request params
- Returning `404` (not `403`) when a resource exists but belongs to another tenant prevents information leakage

## Single Resource Responses

Detail endpoints return the resource directly (no `data` wrapper):

```json
{
  "id": "uuid",
  "roll_number": "20231CSE0260",
  "name": "Kishore S V",
  ...
}
```

## Mutation Responses

| Operation | Status | Body |
|-----------|--------|------|
| Create | `201 Created` | Created resource |
| Update | `200 OK` | Updated resource |
| Delete (soft) | `204 No Content` | Empty |
| Bulk create | `201 Created` | `{ "created": N, "data": [...] }` |

## Related Documentation

- [API Reference](api.md)
- [Security](security.md)
- [Authorization](authorization.md)
- [Database Constraints](database-constraints.md)
