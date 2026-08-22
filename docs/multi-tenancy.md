# Multi-Tenancy

## What is a Tenant?

A tenant represents one university or institution. Each institution that signs up becomes an independent tenant with completely isolated data.

## Tenant Structure

```
Tenant A (University A)
├── Admins
├── Students
├── Faculty
├── Parents
├── Departments
├── Subjects
├── Attendance
├── Exams
├── Marks
└── Analytics

Tenant B (University B)
├── Admins
├── Students
├── Faculty
├── Parents
├── Departments
├── Subjects
├── Attendance
├── Exams
├── Marks
└── Analytics
```

## Tenant Isolation

**Tenant A must never access Tenant B's records.**

Every tenant-owned database record must include an `institution_id` field. All queries must filter by the authenticated user's `institution_id`.

## Backend-Enforced Filtering

The backend determines the authenticated user's tenant from the authenticated session/token. The `institution_id` is embedded in the auth token at login time.

### Why Frontend-Only Filtering is NOT Sufficient

- Clients can be manipulated to send arbitrary `tenant_id` values
- Frontend filtering does not prevent direct API access
- Security must be enforced server-side on every request

### Rules

1. **Never trust `tenant_id` from the client** — always derive from auth token
2. Every database query must include `WHERE institution_id = :current_tenant`
3. Analytics must be calculated only from the current tenant's data
4. Cross-tenant data access must be impossible

## How Users Are Associated with a Tenant

| Event | Association |
|-------|-------------|
| Admin signup | Admin → new Institution → new Tenant |
| Student creation | Student → Admin's Institution → same Tenant |
| Faculty creation | Faculty → Admin's Institution → same Tenant |
| Parent creation | Parent → Admin's Institution → same Tenant |

## Examples

### University A → Tenant A

- Admin A signs up, creates University A
- All students, faculty, parents created by Admin A belong to Tenant A
- Admin A's analytics only show Tenant A data

### University B → Tenant B

- Admin B signs up, creates University B
- All data created by Admin B belongs to Tenant B
- Admin B cannot see, modify, or query any Tenant A data

## Analytics Tenant Boundaries

All analytics queries (institutional, department, subject) must:

1. Extract `institution_id` from the authenticated session
2. Filter all data by that `institution_id`
3. Never aggregate data across tenants

## Related Documentation

- [Authentication](authentication.md)
- [Authorization](authorization.md)
- [Database](database.md)
- [Architecture](architecture.md)
