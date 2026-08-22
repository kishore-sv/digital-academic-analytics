# User Roles

The system supports exactly **four user roles**. There is no HOD role and no platform-admin role.

## Institution Admin

- Signs up and creates a new institution (tenant)
- Completes institution setup/onboarding
- Manages the entire institution
- Creates and manages students, faculty, and parents
- Views institutional, department, and subject analytics
- Accesses all reports and predictions for the institution

**Login:** Email + Password

## Student

- Views own academic profile and performance
- Views own predictions and improvement areas
- Sets and tracks academic goals
- Views own reports

**Login:** Roll Number + Password

**No signup page.** Accounts are created by the Institution Admin.

## Faculty

- Views assigned students only
- Views performance, predictions, and at-risk status for assigned students
- Views improvement areas and reports for assigned students

**Login:** Email + Password

**No signup page.** Accounts are created by the Institution Admin.

## Parent

- Views linked child's/children's academic information only
- Views performance, predictions, and improvement areas
- Views reports for linked children

**Login:** Child Roll Number + Password

**No signup page.** Accounts are created by the Institution Admin and linked to students.

## Role Summary

| Role | Login Credentials | Signup | Data Scope |
|------|-------------------|--------|------------|
| Institution Admin | Email + Password | Yes (only role) | Entire institution |
| Student | Roll Number + Password | No | Own records |
| Faculty | Email + Password | No | Assigned students |
| Parent | Child Roll Number + Password | No | Linked children |

## Related Documentation

- [Authentication](authentication.md)
- [Authorization](authorization.md)
- [User Management](user-management.md)
