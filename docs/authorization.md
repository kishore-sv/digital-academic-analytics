# Authorization

## Overview

Authentication answers: **"Who are you?"**

Authorization answers: **"What are you allowed to access?"**

Authorization is enforced by the backend on every API request. **Authorization has not been implemented yet.**

## Role-Permission Matrix

| Feature | Admin | Student | Faculty | Parent |
|---------|-------|---------|---------|--------|
| Institution Management | ✓ | ✗ | ✗ | ✗ |
| Student Management | ✓ | ✗ | ✗ | ✗ |
| Faculty Management | ✓ | ✗ | ✗ | ✗ |
| Parent Management | ✓ | ✗ | ✗ | ✗ |
| Own Profile | ✓ | ✓ | ✓ | ✓ |
| Student Performance | ✓ | Own | Assigned | Child |
| Predictions | ✓ | Own | Assigned | Child |
| At-Risk Students | ✓ | Own status | Assigned | Child |
| Department Analytics | ✓ | ✗ | ✗ | ✗ |
| Subject Analytics | ✓ | Limited | Assigned | ✗ |
| Institutional Analytics | ✓ | ✗ | ✗ | ✗ |
| Reports | ✓ | Own | Assigned | Child |
| Goal Setting | ✓ | Own | ✗ | ✗ |

## Access Scope Details

### Institution Admin

- Full access to their institution's data
- Can manage all users (students, faculty, parents)
- Can view all analytics, predictions, and reports
- Cannot access other institutions' data

### Student

- Can view only their own academic information
- Can view their own predictions and improvement areas
- Can create and view their own academic goals
- Can view their own reports
- Cannot view other students' data

### Faculty

- Can view only students assigned to them
- Can view assigned students' performance, predictions, at-risk status
- Can view improvement areas and reports for assigned students
- Cannot view institution-wide analytics

### Parent

- Can view only linked child's/children's academic information
- Can view child's performance, predictions, improvement areas
- Can view reports for linked children
- Cannot view other students' data

## Notes

- There is **no HOD role**. Institution Admin directly accesses department-level analytics.
- There is **no platform-admin role**. Each institution is fully independent.
- Faculty "Subject Analytics" is limited to subjects they are assigned to.

## Security Requirements

1. Backend must validate authorization on every request
2. Role checks must use the role from the auth token, not client input
3. Data scope checks (own, assigned, child) must be enforced server-side
4. Disabled users (`is_login_enabled = false`) cannot access any resources

## Related Documentation

- [Authentication](authentication.md)
- [User Roles](user-roles.md)
- [User Management](user-management.md)
- [Multi-Tenancy](multi-tenancy.md)
