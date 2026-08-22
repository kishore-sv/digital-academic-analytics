# Database Constraints, Indexes, and Audit Fields

This document extends [database.md](database.md) with concrete indexing rules, tenant-scoped uniqueness constraints, audit fields, and the attendance percentage computation strategy.

## Indexing Strategy

Every tenant-owned table must have an index on `institution_id`. All list and analytics queries filter by tenant, so this index is mandatory on every table that carries `institution_id`.

### Single-Column Indexes

| Table | Column | Reason |
|-------|--------|--------|
| All tenant-owned tables | `institution_id` | Tenant isolation filter on every query |
| All entities | `deleted_at` | Soft-delete filter (`WHERE deleted_at IS NULL`) |

### Composite Indexes

Composite indexes match the most common query patterns. Create these alongside the initial migration.

| Table | Index | Query pattern |
|-------|-------|---------------|
| `users` | `(institution_id, email)` | Login lookup by email within tenant |
| `students` | `(institution_id, roll_number)` | Student login by roll number within tenant |
| `students` | `(institution_id, department_id)` | Department student lists |
| `subjects` | `(institution_id, department_id)` | Department subject lists |
| `attendance` | `(institution_id, student_id)` | Student attendance history |
| `attendance` | `(institution_id, student_id, subject_id)` | Per-subject attendance for a student |
| `performance` | `(institution_id, student_id)` | Student performance records |
| `performance` | `(institution_id, student_id, semester)` | Semester performance lookup |
| `goals` | `(institution_id, student_id)` | Student goal lists |
| `examinations` | `(institution_id, subject_id)` | Subject examination lists |

## Uniqueness Constraints (Tenant-Scoped)

All uniqueness constraints are scoped to `(institution_id, field)`. **Global uniqueness is not used** — it would incorrectly prevent two institutions from having a student with the same roll number or an admin with the same email format.

| Entity | Constraint | SQL |
|--------|-----------|-----|
| `User` | Email unique per institution | `UNIQUE (institution_id, email)` |
| `Student` | Roll number unique per institution | `UNIQUE (institution_id, roll_number)` |
| `Department` | Code unique per institution | `UNIQUE (institution_id, code)` |
| `Subject` | Code unique per institution | `UNIQUE (institution_id, code)` |

### Why Tenant-Scoped Uniqueness Matters

If `email` were globally unique, Institution A creating `admin@college.edu` would block Institution B from using the same email — even though they are completely separate tenants. Tenant-scoped constraints enforce uniqueness only within an institution's data boundary.

## Audit and Soft-Delete Fields

All entities include the following timestamp fields:

| Field | Type | Purpose |
|-------|------|---------|
| `created_at` | `TIMESTAMPTZ` | Record creation time (UTC, server default `now()`) |
| `updated_at` | `TIMESTAMPTZ` | Last modification time (auto-updated on every change) |
| `deleted_at` | `TIMESTAMPTZ NULL` | Soft delete marker; `NULL` = active record |

### Soft Delete Rules

- Deleting a record sets `deleted_at = now()` — the row is never physically removed
- All queries must include `WHERE deleted_at IS NULL` unless explicitly querying deleted records
- Admin can view and restore soft-deleted records (future enhancement)
- Grades, attendance, and performance records use soft delete because they may be disputed and require an audit trail

## Attendance Percentage — Computed, Not Stored

The `Attendance` entity stores individual attendance events only:

| Field | Description |
|-------|-------------|
| `student_id` | FK → Student |
| `subject_id` | FK → Subject |
| `date` | Attendance date |
| `status` | `present` or `absent` |

**`percentage` is not a stored column.** Storing a running percentage alongside raw present/absent records creates drift — the percentage becomes stale whenever a new attendance record is added unless explicitly recomputed.

### Computation Strategy

Attendance percentage is calculated on read:

```sql
SELECT
  student_id,
  subject_id,
  COUNT(*) FILTER (WHERE status = 'present') * 100.0 / COUNT(*) AS attendance_percentage
FROM attendance
WHERE institution_id = :institution_id
  AND student_id = :student_id
  AND deleted_at IS NULL
GROUP BY student_id, subject_id;
```

Filter by semester using a date range on the `date` column when semester boundaries are defined.

### Caching Option (future)

For large institutions where on-read computation is too slow, an `attendance_summary` table or materialized view can cache percentages. Recompute strategy for cached values:

- Recompute on every attendance record insert/update (write-through)
- Or refresh materialized view on a schedule (e.g. nightly)

For the capstone demo, **on-read computation is recommended** for simplicity.

## Related Documentation

- [Database Design](database.md)
- [Migrations](migrations.md)
- [Multi-Tenancy](multi-tenancy.md)
