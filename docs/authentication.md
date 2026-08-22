# Authentication

## Overview

The system uses a unified login experience with role-specific credential validation. Authentication is handled by the FastAPI backend. **Authentication has not been implemented yet.**

There is **only one application/client**. There is no platform-admin role and no separate platform-level administration system.

For the full security stack (hashing library, JWT strategy, rate limiting), see [security.md](security.md).

## Signup Policy

**Only Institution Admin can sign up.**

There is NO signup for:
- Students
- Faculty
- Parents

## Admin Signup

1. Admin opens the signup page (`/signup`)
2. Admin enters:
   - Name
   - Email
   - Password
   - University/Institution name
3. Account is created
4. Institution/University tenant is created
5. Admin is authenticated (JWT set in httpOnly cookie)
6. Admin is redirected to institution setup/onboarding

## Login Types

### Institution Admin

- **Credentials:** Email + Password
- **Redirect:** `/admin/dashboard`

### Student

- **Credentials:** Roll Number + Password
- **Example:** Roll Number `20231CSE0260` + Password
- **Redirect:** `/student/dashboard`
- **No signup page**

### Faculty

- **Credentials:** Email + Password
- **Redirect:** `/faculty/dashboard`
- **No signup page**

### Parent

- **Credentials:** Child Roll Number + Password
- **Redirect:** `/parent/dashboard`
- **No signup page**

## Authentication Flow

```
Client
  ↓
Login (/login)
  ↓
FastAPI Authentication API (rate-limited: 5/min per IP)
  ↓
Validate credentials (argon2)
  ↓
Determine user role
  ↓
Determine tenant (institution_id)
  ↓
Check is_login_enabled
  ↓
Issue JWT in httpOnly cookie
  ↓
Client receives authentication state via /api/auth/me
  ↓
Role-based dashboard redirect
```

## Token Storage

JWT tokens are stored in **httpOnly cookies** set by the backend — not in `localStorage`. This prevents XSS from stealing auth tokens.

| Cookie | Lifetime | Purpose |
|--------|----------|---------|
| `access_token` | 15 minutes | API authentication |
| `refresh_token` | 7 days | Obtain new access token |

See [security.md](security.md) for full token specification and [frontend-stack.md](frontend-stack.md) for client-side auth handling.

## Session/Token Payload

| Field | Description |
|-------|-------------|
| `sub` | User UUID |
| `role` | admin, student, faculty, parent |
| `institution_id` | Tenant UUID (always server-derived) |

## Auth Endpoints (planned)

| Method | Path | Rate limited |
|--------|------|-------------|
| POST | `/api/auth/signup` | Yes (3/min) |
| POST | `/api/auth/login` | Yes (5/min) |
| POST | `/api/auth/logout` | No |
| POST | `/api/auth/refresh` | Yes (10/min) |
| GET | `/api/auth/me` | No |

## Logout

Logout clears both `access_token` and `refresh_token` httpOnly cookies and invalidates the session.

## Login Enabled/Disabled

Admin-created users have an `is_login_enabled` status:

- `true` — User can log in
- `false` — User cannot log in (authentication rejected with `AUTH_ACCOUNT_DISABLED`)

This applies to students, faculty, and parents. Admins can enable or disable login access at any time.

## Password Reset

Admin-initiated credential reset only in v1. No self-service "forgot password" flow. See [security.md](security.md).

## Security Requirements

1. Never trust `tenant_id` from the client
2. Never trust role information from the client
3. Backend must validate all credentials with argon2
4. Disabled users must not authenticate
5. Passwords must be hashed — never stored in plain text
6. Rate limiting on all `/api/auth/*` endpoints

## Related Documentation

- [Security](security.md)
- [Onboarding](onboarding.md)
- [Authorization](authorization.md)
- [User Roles](user-roles.md)
- [Multi-Tenancy](multi-tenancy.md)
- [Frontend Stack](frontend-stack.md)
