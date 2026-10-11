# Database Design

PostgreSQL with SQLAlchemy ORM and Alembic migrations.

## Core Entities

- **Institution** — tenant root
- **User** — authentication (roles: institution_admin, student, faculty, parent)
- **Department, Program, AcademicYear, Semester** — academic structure
- **Student, Faculty, Parent** — people
- **ParentStudent, FacultyStudent** — junction tables
- **Course, Enrollment** — course registration
- **Assessment, AssessmentMark, Attendance** — academic data
- **CourseResult, SemesterResult** — outcomes
- **PredictionResult** — stored ML predictions
- **StudentGoal** — student academic goals

## Tenant Isolation

All tenant-owned tables include `institution_id` with indexes. Uniqueness constraints are tenant-scoped (e.g. `UNIQUE (institution_id, roll_number)`).

## Migrations

```bash
cd backend
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
```

## Seed Data

```bash
cd backend
uv run python scripts/reseed.py            # drop, recreate, 2,400-student dataset
uv run python scripts/reseed.py --minimal # small slice for tests
# or, only when the database is empty:
uv run python scripts/seed.py
```

Development credentials (see `app/core/seed_data.py`):

- Admin: `admin@demo.com` / `admin123`
- Faculty: `faculty@demo.com` / `faculty123`
- Student: `26CSE001` / `student123`
- Parent: `parent@demo.com` / `parent123`
