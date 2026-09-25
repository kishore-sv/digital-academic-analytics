# API Reference (generated)

_Auto-generated from the FastAPI OpenAPI schema. Do not edit by hand._

Regenerate:

```bash
cd backend && uv run python scripts/generate_api_docs.py
```

**Interactive UI:** [Swagger](/docs) · [ReDoc](/redoc) (with `uvicorn` on port 8000)

**Base path:** `/api/v1`

## meta

Service index (`GET /`) and health check (`GET /health`).

### `GET` `/`

**Summary:** Api Index

Links to interactive API documentation and health check.

**Responses**

- **200** — Successful Response: `object`

### `GET` `/health`

**Summary:** Health Check

Liveness probe and ML model load status.

**Responses**

- **200** — Successful Response: `object`

## auth

Signup, login, logout, refresh session, and current user (`/auth/me`). Uses httpOnly cookies.

### `POST` `/api/v1/auth/login`

**Summary:** Login

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `identifier` | string | yes | Identifier |
| `password` | string | yes | Password |
| `role` | string | yes | Role |

**Responses**

- **200** — Successful Response: `app__schemas__auth__UserResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/auth/logout`

**Summary:** Logout

**Responses**

- **200** — Successful Response: _empty_

### `GET` `/api/v1/auth/me`

**Summary:** Get Me

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `app__schemas__auth__UserResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/auth/refresh`

**Summary:** Refresh Token

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `refresh_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `app__schemas__auth__UserResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/auth/signup`

**Summary:** Signup

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Name |
| `email` | string | yes | Email |
| `password` | string | yes | Password |
| `institution_name` | string | yes | Institution Name |

**Responses**

- **200** — Successful Response: `app__schemas__auth__UserResponse`
- **422** — Validation Error: `HTTPValidationError`

## users

Institution admin user accounts (create, list, enable/disable).

### `GET` `/api/v1/users`

**Summary:** List Users

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_UserResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/users`

**Summary:** Create User

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | yes | Email |
| `password` | string | yes | Password |
| `role` | string | no | Role |

**Responses**

- **201** — Successful Response: `app__schemas__academic__UserResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/users/{user_id}`

**Summary:** Delete User

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `user_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/users/{user_id}`

**Summary:** Get User

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `user_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `app__schemas__academic__UserResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/users/{user_id}`

**Summary:** Update User

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `user_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `is_login_enabled` | boolean | null | no | Is Login Enabled |

**Responses**

- **200** — Successful Response: `app__schemas__academic__UserResponse`
- **422** — Validation Error: `HTTPValidationError`

## institutions

Institution profile for the current tenant.

### `GET` `/api/v1/institutions/me`

**Summary:** Get My Institution

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `InstitutionResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/institutions/me`

**Summary:** Update My Institution

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | null | no | Name |
| `logo_url` | string | null | no | Logo Url |
| `description` | string | null | no | Description |

**Responses**

- **200** — Successful Response: `InstitutionResponse`
- **422** — Validation Error: `HTTPValidationError`

## departments

Academic departments (CRUD). Scoped to the logged-in institution.

### `GET` `/api/v1/departments`

**Summary:** List Departments

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_DepartmentResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/departments`

**Summary:** Create Department

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Name |
| `code` | string | yes | Code |
| `description` | string | null | no | Description |

**Responses**

- **201** — Successful Response: `DepartmentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/departments/{department_id}`

**Summary:** Delete Department

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `department_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/departments/{department_id}`

**Summary:** Get Department

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `department_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `DepartmentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/departments/{department_id}`

**Summary:** Update Department

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `department_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | null | no | Name |
| `code` | string | null | no | Code |
| `description` | string | null | no | Description |

**Responses**

- **200** — Successful Response: `DepartmentResponse`
- **422** — Validation Error: `HTTPValidationError`

## programs

Degree programs under departments.

### `GET` `/api/v1/programs`

**Summary:** List Programs

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_ProgramResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/programs`

**Summary:** Create Program

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `department_id` | string | yes | Department Id |
| `name` | string | yes | Name |
| `code` | string | yes | Code |
| `duration_semesters` | integer | no | Duration Semesters |

**Responses**

- **201** — Successful Response: `ProgramResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/programs/{program_id}`

**Summary:** Delete Program

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `program_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/programs/{program_id}`

**Summary:** Get Program

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `program_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `ProgramResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/programs/{program_id}`

**Summary:** Update Program

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `program_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | null | no | Name |
| `code` | string | null | no | Code |
| `duration_semesters` | integer | null | no | Duration Semesters |

**Responses**

- **200** — Successful Response: `ProgramResponse`
- **422** — Validation Error: `HTTPValidationError`

## faculty

Faculty profiles, course assignments, and student mentoring links.

### `GET` `/api/v1/faculty`

**Summary:** List Faculty

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_FacultyResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/faculty`

**Summary:** Create Faculty

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Name |
| `email` | string | yes | Email |
| `password` | string | yes | Password |
| `department_id` | string | yes | Department Id |

**Responses**

- **201** — Successful Response: `FacultyResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/faculty/{faculty_id}`

**Summary:** Delete Faculty

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `faculty_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/faculty/{faculty_id}`

**Summary:** Get Faculty

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `faculty_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `FacultyResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/faculty/{faculty_id}`

**Summary:** Update Faculty

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `faculty_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | null | no | Name |
| `department_id` | string | null | no | Department Id |

**Responses**

- **200** — Successful Response: `FacultyResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/faculty/{faculty_id}/students`

**Summary:** List Assigned Students

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `faculty_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `string`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/faculty/{faculty_id}/students/{student_id}`

**Summary:** Unassign Student

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `faculty_id` | path | yes | string |
| `student_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/faculty/{faculty_id}/students/{student_id}`

**Summary:** Assign Student

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `faculty_id` | path | yes | string |
| `student_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **201** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

## parents

Parent accounts and links to student children.

### `GET` `/api/v1/parents`

**Summary:** List Parents

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_ParentResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/parents`

**Summary:** Create Parent

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Name |
| `email` | string | yes | Email |
| `password` | string | yes | Password |
| `student_ids` | array | no | Student Ids |

**Responses**

- **201** — Successful Response: `ParentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/parents/me`

**Summary:** Get My Parent Profile

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `ParentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/parents/{parent_id}`

**Summary:** Delete Parent

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `parent_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/parents/{parent_id}`

**Summary:** Get Parent

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `parent_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `ParentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/parents/{parent_id}`

**Summary:** Update Parent

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `parent_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | null | no | Name |

**Responses**

- **200** — Successful Response: `ParentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/parents/{parent_id}/children`

**Summary:** List Linked Children

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `parent_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `string`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/parents/{parent_id}/children/{student_id}`

**Summary:** Unlink Child

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `parent_id` | path | yes | string |
| `student_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/parents/{parent_id}/children/{student_id}`

**Summary:** Link Child

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `parent_id` | path | yes | string |
| `student_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **201** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

## students

Student profiles, roll numbers, and admin CRUD. Faculty see assigned students only.

### `GET` `/api/v1/students`

**Summary:** List Students

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_StudentResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/students`

**Summary:** Create Student

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Name |
| `roll_number` | string | yes | Roll Number |
| `password` | string | yes | Password |
| `department_id` | string | yes | Department Id |
| `program_id` | string | null | no | Program Id |
| `semester` | integer | no | Semester |
| `branch` | string | no | Branch |

**Responses**

- **201** — Successful Response: `StudentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/students/me`

**Summary:** Get My Student Profile

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `StudentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/students/{student_id}`

**Summary:** Delete Student

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `student_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/students/{student_id}`

**Summary:** Get Student

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `student_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `StudentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/students/{student_id}`

**Summary:** Update Student

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `student_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | null | no | Name |
| `department_id` | string | null | no | Department Id |
| `program_id` | string | null | no | Program Id |
| `semester` | integer | null | no | Semester |
| `branch` | string | null | no | Branch |

**Responses**

- **200** — Successful Response: `StudentResponse`
- **422** — Validation Error: `HTTPValidationError`

## student-performance

Per-student performance summaries and improvement insights.

### `GET` `/api/v1/students/me/goal-guidance`

**Summary:** Get My Goal Guidance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `target_cgpa` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `GoalGuidanceResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/students/me/performance`

**Summary:** Get My Performance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `StudentPerformanceResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/students/{student_id}/performance`

**Summary:** Get Student Performance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `student_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `StudentPerformanceResponse`
- **422** — Validation Error: `HTTPValidationError`

## courses

Courses/subjects by department. Faculty lists are limited to assigned courses.

### `GET` `/api/v1/courses`

**Summary:** List Courses

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_CourseResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/courses`

**Summary:** Create Course

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `department_id` | string | yes | Department Id |
| `name` | string | yes | Name |
| `code` | string | yes | Code |
| `credits` | integer | no | Credits |
| `course_type` | string | no | Course Type |

**Responses**

- **201** — Successful Response: `CourseResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/courses/{course_id}`

**Summary:** Delete Course

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `course_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/courses/{course_id}`

**Summary:** Get Course

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `course_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `CourseResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/courses/{course_id}`

**Summary:** Update Course

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `course_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | null | no | Name |
| `code` | string | null | no | Code |
| `credits` | integer | null | no | Credits |
| `course_type` | string | null | no | Course Type |

**Responses**

- **200** — Successful Response: `CourseResponse`
- **422** — Validation Error: `HTTPValidationError`

## academic

Academic years and semesters.

### `GET` `/api/v1/academic/semesters`

**Summary:** List Semesters

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `SemesterResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/academic/years`

**Summary:** List Academic Years

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `AcademicYearResponse`
- **422** — Validation Error: `HTTPValidationError`

## assessments

Assessments (CA, Mid, End), marks entry grid, bulk save, and rosters.

### `GET` `/api/v1/assessments`

**Summary:** List Assessments

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `course_id` | query | no | string |
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_AssessmentResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/assessments`

**Summary:** Create Assessment

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `course_id` | string | yes | Course Id |
| `name` | string | yes | Name |
| `assessment_type` | string | yes | Assessment Type |
| `max_marks` | number | no | Max Marks |
| `date` | string | null | no | Date |

**Responses**

- **201** — Successful Response: `AssessmentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/assessments/marks`

**Summary:** List Marks

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `assessment_id` | query | no | string |
| `enrollment_id` | query | no | string |
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_AssessmentMarkResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/assessments/marks`

**Summary:** Create Mark

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enrollment_id` | string | yes | Enrollment Id |
| `assessment_id` | string | yes | Assessment Id |
| `marks_obtained` | number | yes | Marks Obtained |

**Responses**

- **201** — Successful Response: `AssessmentMarkResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/assessments/marks-grid`

**Summary:** Get Marks Grid

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `course_id` | query | yes | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `section` | query | no | string |
| `search` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `MarksGridResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/assessments/marks/bulk`

**Summary:** Bulk Upsert Marks

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `entries` | array | yes | Entries |

**Responses**

- **200** — Successful Response: array of `AssessmentMarkResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/assessments/marks/bulk-grid`

**Summary:** Bulk Upsert Marks Grid

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `entries` | array | yes | Entries |
| `recalculate_results` | boolean | no | Recalculate Results |
| `trigger_predictions` | boolean | no | Trigger Predictions |

**Responses**

- **200** — Successful Response: array of `AssessmentMarkResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/assessments/marks/{mark_id}`

**Summary:** Delete Mark

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `mark_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/assessments/marks/{mark_id}`

**Summary:** Update Mark

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `mark_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `marks_obtained` | number | yes | Marks Obtained |

**Responses**

- **200** — Successful Response: `AssessmentMarkResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/assessments/roster`

**Summary:** Get Marks Roster

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `course_id` | query | yes | string |
| `assessment_id` | query | yes | string |
| `semester_id` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `MarksRosterResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/assessments/{assessment_id}`

**Summary:** Delete Assessment

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `assessment_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/assessments/{assessment_id}`

**Summary:** Get Assessment

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `assessment_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `AssessmentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/assessments/{assessment_id}`

**Summary:** Update Assessment

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `assessment_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | null | no | Name |
| `assessment_type` | string | null | no | Assessment Type |
| `max_marks` | number | null | no | Max Marks |
| `date` | string | null | no | Date |

**Responses**

- **200** — Successful Response: `AssessmentResponse`
- **422** — Validation Error: `HTTPValidationError`

## attendance

Attendance records and bulk entry rosters.

### `GET` `/api/v1/attendance`

**Summary:** List Attendance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `enrollment_id` | query | no | string |
| `student_id` | query | no | string |
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_AttendanceResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/attendance`

**Summary:** Create Attendance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enrollment_id` | string | yes | Enrollment Id |
| `date` | string | yes | Date |
| `status` | string | yes | Status |

**Responses**

- **201** — Successful Response: `AttendanceResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/attendance/bulk`

**Summary:** Bulk Update Attendance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `entries` | array | yes | Entries |

**Responses**

- **200** — Successful Response: array of `EnrollmentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/attendance/roster`

**Summary:** Get Attendance Roster

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `course_id` | query | yes | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `section` | query | no | string |
| `search` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `AttendanceRosterResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/attendance/{attendance_id}`

**Summary:** Delete Attendance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `attendance_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/attendance/{attendance_id}`

**Summary:** Get Attendance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `attendance_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `AttendanceResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/attendance/{attendance_id}`

**Summary:** Update Attendance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `attendance_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | yes | Status |

**Responses**

- **200** — Successful Response: `AttendanceResponse`
- **422** — Validation Error: `HTTPValidationError`

## results

Course results, semester results (SGPA/CGPA), and recalculation.

### `GET` `/api/v1/results/course`

**Summary:** List Course Results

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `enrollment_id` | query | no | string |
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_CourseResultResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/results/course`

**Summary:** Create Course Result

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enrollment_id` | string | yes | Enrollment Id |
| `grade` | string | null | no | Grade |
| `end_marks` | number | null | no | End Marks |
| `status` | string | no | Status |

**Responses**

- **201** — Successful Response: `CourseResultResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/results/course/{result_id}`

**Summary:** Update Course Result

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `result_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `grade` | string | null | no | Grade |
| `end_marks` | number | null | no | End Marks |
| `status` | string | null | no | Status |

**Responses**

- **200** — Successful Response: `CourseResultResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/results/enrollments`

**Summary:** List Enrollments

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `student_id` | query | no | string |
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_EnrollmentResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/results/enrollments`

**Summary:** Create Enrollment

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `student_id` | string | yes | Student Id |
| `course_id` | string | yes | Course Id |
| `semester_id` | string | yes | Semester Id |
| `attendance_percentage` | number | null | no | Attendance Percentage |
| `study_hours_per_week` | number | null | no | Study Hours Per Week |
| `assignment_completion_pct` | number | null | no | Assignment Completion Pct |

**Responses**

- **201** — Successful Response: `EnrollmentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/results/enrollments/{enrollment_id}`

**Summary:** Update Enrollment

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `enrollment_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `attendance_percentage` | number | null | no | Attendance Percentage |
| `study_hours_per_week` | number | null | no | Study Hours Per Week |
| `assignment_completion_pct` | number | null | no | Assignment Completion Pct |

**Responses**

- **200** — Successful Response: `EnrollmentResponse`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/results/semester`

**Summary:** List Semester Results

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `student_id` | query | no | string |
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_SemesterResultResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/results/semester`

**Summary:** Create Semester Result

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `student_id` | string | yes | Student Id |
| `semester_id` | string | yes | Semester Id |
| `sgpa` | number | null | no | Sgpa |
| `cgpa` | number | null | no | Cgpa |
| `backlog_count` | integer | no | Backlog Count |
| `current_failed_courses` | integer | no | Current Failed Courses |
| `low_performance_course_count` | integer | no | Low Performance Course Count |
| `performance_trend` | string | no | Performance Trend |

**Responses**

- **201** — Successful Response: `SemesterResultResponse`
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/results/semester/{result_id}`

**Summary:** Update Semester Result

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `result_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sgpa` | number | null | no | Sgpa |
| `cgpa` | number | null | no | Cgpa |
| `backlog_count` | integer | null | no | Backlog Count |
| `current_failed_courses` | integer | null | no | Current Failed Courses |
| `low_performance_course_count` | integer | null | no | Low Performance Course Count |
| `performance_trend` | string | null | no | Performance Trend |

**Responses**

- **200** — Successful Response: `SemesterResultResponse`
- **422** — Validation Error: `HTTPValidationError`

## at-risk

At-risk student lists and summary metrics.

### `GET` `/api/v1/at-risk`

**Summary:** List At Risk Students

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `department_name` | query | no | string |
| `semester` | query | no | string |
| `risk_level` | query | no | string |
| `performance_trend` | query | no | string |
| `attendance_band` | query | no | string |
| `cgpa_band` | query | no | string |
| `page` | query | no | integer |
| `limit` | query | no | integer |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PaginatedResponse_AtRiskStudentResponse_`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/at-risk/summary`

**Summary:** At Risk Summary

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `AtRiskSummary`
- **422** — Validation Error: `HTTPValidationError`

## predictions

ML predictions (performance, pass/fail, risk) and stored student predictions.

### `POST` `/api/v1/predictions/all`

**Summary:** Predict All Endpoint

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `student_id` | query | no | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `CA_mark` | number | yes | Ca Mark |
| `MID_mark` | number | yes | Mid Mark |
| `attendance_percentage` | number | yes | Attendance Percentage |
| `study_hours_per_week` | number | yes | Study Hours Per Week |
| `assignment_completion_pct` | number | yes | Assignment Completion Pct |
| `previous_sgpa` | number | yes | Previous Sgpa |
| `previous_cgpa` | number | yes | Previous Cgpa |
| `backlog_count` | integer | yes | Backlog Count |
| `course_credits` | integer | yes | Course Credits |
| `course_type` | string | no | Course Type |
| `branch` | string | no | Branch |
| `semester` | integer | yes | Semester |

**Responses**

- **200** — Successful Response: `AllPredictionsResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/predictions/pass-fail`

**Summary:** Predict Pass Fail Endpoint

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `CA_mark` | number | yes | Ca Mark |
| `MID_mark` | number | yes | Mid Mark |
| `attendance_percentage` | number | yes | Attendance Percentage |
| `study_hours_per_week` | number | yes | Study Hours Per Week |
| `assignment_completion_pct` | number | yes | Assignment Completion Pct |
| `previous_sgpa` | number | yes | Previous Sgpa |
| `previous_cgpa` | number | yes | Previous Cgpa |
| `backlog_count` | integer | yes | Backlog Count |
| `course_credits` | integer | yes | Course Credits |
| `branch` | string | no | Branch |
| `semester` | integer | yes | Semester |

**Responses**

- **200** — Successful Response: `PassFailPredictionResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/predictions/performance`

**Summary:** Predict Performance Endpoint

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `CA_mark` | number | yes | Ca Mark |
| `MID_mark` | number | yes | Mid Mark |
| `attendance_percentage` | number | yes | Attendance Percentage |
| `study_hours_per_week` | number | yes | Study Hours Per Week |
| `assignment_completion_pct` | number | yes | Assignment Completion Pct |
| `previous_sgpa` | number | yes | Previous Sgpa |
| `previous_cgpa` | number | yes | Previous Cgpa |
| `backlog_count` | integer | yes | Backlog Count |
| `course_credits` | integer | yes | Course Credits |
| `course_type` | string | no | Course Type |
| `branch` | string | no | Branch |
| `semester` | integer | yes | Semester |

**Responses**

- **200** — Successful Response: `PerformancePredictionResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/predictions/regenerate`

**Summary:** Regenerate Predictions

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `replace_existing` | query | no | boolean |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `RegenerateResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/predictions/risk`

**Summary:** Predict Risk Endpoint

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `attendance_percentage` | number | yes | Attendance Percentage |
| `previous_cgpa` | number | yes | Previous Cgpa |
| `backlog_count` | integer | yes | Backlog Count |
| `current_failed_courses` | integer | yes | Current Failed Courses |
| `low_performance_course_count` | integer | yes | Low Performance Course Count |
| `study_hours_per_week` | number | yes | Study Hours Per Week |
| `assignment_completion_percentage` | number | yes | Assignment Completion Percentage |
| `performance_trend` | string | no | Performance Trend |

**Responses**

- **200** — Successful Response: `RiskPredictionResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/predictions/student`

**Summary:** Predict For Student

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `student_id` | string | yes | Student Id |
| `enrollment_id` | string | null | no | Enrollment Id |

**Responses**

- **200** — Successful Response: `AllPredictionsResponse`
- **422** — Validation Error: `HTTPValidationError`

## analytics

Institution analytics dashboards (admin). Charts and KPI aggregates.

### `GET` `/api/v1/analytics/attendance-performance`

**Summary:** Analytics Attendance Performance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `AttendancePerformancePoint`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/cgpa-distribution`

**Summary:** Analytics Cgpa Distribution

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/courses`

**Summary:** Analytics Courses

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `CourseAnalytics`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/department-risk-stacks`

**Summary:** Analytics Department Risk Stacks

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `DepartmentRiskStack`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/departments`

**Summary:** Analytics Departments

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `DepartmentAnalytics`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/overview`

**Summary:** Analytics Overview

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `OverviewStats`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/pass-fail`

**Summary:** Analytics Pass Fail

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/pass-fail-trend`

**Summary:** Analytics Pass Fail Trend

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `PassFailTrendPoint`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/performance-indicators`

**Summary:** Analytics Performance Indicators

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PerformanceIndicators`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/performance-trends`

**Summary:** Analytics Performance Trends

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `PerformanceTrendPoint`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/predictions/actual-vs-predicted`

**Summary:** Analytics Actual Vs Predicted

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `ActualVsPredictedPoint`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/predictions/pass-fail`

**Summary:** Analytics Prediction Pass Fail

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PredictionPassFailAnalytics`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/predictions/performance`

**Summary:** Analytics Prediction Performance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PredictionPerformanceAnalytics`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/predictions/risk`

**Summary:** Analytics Prediction Risk

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PredictionRiskAnalytics`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/risk-distribution`

**Summary:** Analytics Risk Distribution

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `RiskDistribution`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/risk-factors`

**Summary:** Analytics Risk Factors

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `RiskFactorCount`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/scoped/attendance-performance`

**Summary:** Scoped Attendance Performance

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `AttendancePerformancePoint`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/scoped/cgpa-distribution`

**Summary:** Scoped Cgpa Distribution

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/scoped/department-risk-stacks`

**Summary:** Scoped Department Risk Stacks

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `DepartmentRiskStack`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/scoped/departments`

**Summary:** Scoped Departments

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `DepartmentAnalytics`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/scoped/overview`

**Summary:** Scoped Analytics Overview

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `OverviewStats`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/scoped/performance-trends`

**Summary:** Scoped Performance Trends

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `PerformanceTrendPoint`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/scoped/predictions/risk`

**Summary:** Scoped Prediction Risk

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `PredictionRiskAnalytics`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/scoped/risk-distribution`

**Summary:** Scoped Risk Distribution

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `RiskDistribution`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/analytics/scoped/risk-factors`

**Summary:** Scoped Risk Factors

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `RiskFactorCount`
- **422** — Validation Error: `HTTPValidationError`

## goals

Student academic goals.

### `GET` `/api/v1/goals`

**Summary:** List Goals

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: array of `GoalResponse`
- **422** — Validation Error: `HTTPValidationError`

### `POST` `/api/v1/goals`

**Summary:** Create Goal

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `goal_type` | string | yes | Goal Type |
| `target_value` | number | yes | Target Value |
| `notes` | string | null | no | Notes |

**Responses**

- **201** — Successful Response: `GoalResponse`
- **422** — Validation Error: `HTTPValidationError`

### `DELETE` `/api/v1/goals/{goal_id}`

**Summary:** Delete Goal

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `goal_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **204** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `PATCH` `/api/v1/goals/{goal_id}`

**Summary:** Update Goal

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `goal_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Request body** (`application/json`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `target_value` | number | null | no | Target Value |
| `status` | string | null | no | Status |
| `notes` | string | null | no | Notes |

**Responses**

- **200** — Successful Response: `GoalResponse`
- **422** — Validation Error: `HTTPValidationError`

## reports

PDF/HTML report generation and download.

### `GET` `/api/v1/reports/at-risk`

**Summary:** At Risk Report

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `include_charts` | query | no | boolean |
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/reports/at-risk/pdf`

**Summary:** At Risk Report Pdf

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `include_charts` | query | no | boolean |
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/reports/institutional`

**Summary:** Institutional Report

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `include_charts` | query | no | boolean |
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/reports/institutional/data`

**Summary:** Institutional Report Data

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `ReportContext`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/reports/institutional/pdf`

**Summary:** Institutional Report Pdf

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `include_charts` | query | no | boolean |
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/reports/scoped/institutional/data`

**Summary:** Scoped Institutional Report Data

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: `ReportContext`
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/reports/scoped/institutional/pdf`

**Summary:** Scoped Institutional Report Pdf

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `include_charts` | query | no | boolean |
| `academic_year_id` | query | no | string |
| `semester_id` | query | no | string |
| `department_id` | query | no | string |
| `program_id` | query | no | string |
| `course_id` | query | no | string |
| `risk_level` | query | no | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`

### `GET` `/api/v1/reports/student/{student_id}`

**Summary:** Student Prediction Report

**Query / path parameters**

| Name | In | Required | Type |
|------|-----|----------|------|
| `student_id` | path | yes | string |
| `access_token` | cookie | no | string |

**Responses**

- **200** — Successful Response: _empty_
- **422** — Validation Error: `HTTPValidationError`
