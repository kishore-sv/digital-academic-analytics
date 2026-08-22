# User Management

## Overview

The Institution Admin manages all users within their institution. Students, faculty, and parents cannot create their own accounts. **User management has not been implemented yet.**

## Admin Capabilities

The Institution Admin can:

- Create accounts (students, faculty, parents)
- Update account information
- Enable login access
- Disable login access
- Reset credentials
- Assign faculty to students
- Link parents to students

## Student Management

### Create Student

| Field | Description |
|-------|-------------|
| Name | Student full name |
| Roll number | Unique per institution (used for login) |
| Email | Optional, for profile |
| Department | Academic department |
| Program | Degree program |
| Semester | Current semester |
| Password | Initial credentials |
| Login enabled | true/false |

### Update Student

Admin can update any student field including department, program, semester, and credentials.

### Enable/Disable Login

Admin can toggle `is_login_enabled` to control whether a student can log in.

## Faculty Management

### Create Faculty

| Field | Description |
|-------|-------------|
| Name | Faculty full name |
| Email | Login email |
| Department | Academic department |
| Assigned subjects | Subjects taught |
| Assigned students | Students under this faculty |
| Password | Initial credentials |
| Login enabled | true/false |

### Assign Students to Faculty

Admin links faculty members to specific students. Faculty can only view data for assigned students.

```
Faculty
   ↓
Assigned Students
```

## Parent Management

### Create Parent

| Field | Description |
|-------|-------------|
| Name | Parent full name |
| Linked students | One or more children |
| Password | Initial credentials |
| Login enabled | true/false |

### Link Parent to Student

Admin links a parent to one or more students. Parents can only access data for linked children.

```
Parent
   ↓
Child Student(s)
```

## Key Relationships

```
Admin
   ↓
Entire Institution (all users, departments, subjects, data)

Faculty
   ↓
Assigned Students (performance, predictions, at-risk)

Parent
   ↓
Linked Child Student(s) (performance, predictions, reports)

Student
   ↓
Own Records Only (profile, performance, goals, reports)
```

## Credential Reset

Admin can reset passwords for any user. The user receives new initial credentials and must log in with the updated password.

## Account Status

All admin-created users have `is_login_enabled`:

| Status | Behavior |
|--------|----------|
| `true` | User can log in normally |
| `false` | Login attempts are rejected |

## Related Documentation

- [Authentication](authentication.md)
- [Onboarding](onboarding.md)
- [Authorization](authorization.md)
- [User Roles](user-roles.md)
