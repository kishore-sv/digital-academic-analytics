# Onboarding

## Overview

After admin signup, the Institution Admin completes institution setup before accessing the full admin dashboard. **Onboarding has not been implemented yet.**

## Onboarding Flow

```
Admin Signup (/signup)
        ↓
Create Institution/Tenant
        ↓
Create Admin Account
        ↓
Institution Setup (/admin/setup)
        ↓
Logo + Institution Details
        ↓
Admin Dashboard (/admin/dashboard)
        ↓
Create Students / Faculty / Parents
        ↓
Enable Login for Users
        ↓
Users Can Login
```

## Step 1: Admin Signup

The Institution Admin signs up with:
- Name
- Email
- Password
- University/Institution name

This creates both the admin account and the institution tenant.

## Step 2: Institution Setup

After signup, the admin completes basic institution setup:

| Field | Description |
|-------|-------------|
| University/Institution name | Display name |
| Institution logo | Upload logo image |
| Short description | Brief institution description |
| Basic details | Additional institution information |

The institution setup is associated with the newly created tenant.

## Step 3: User Creation

After completing setup, the admin creates users:

### Students
- Name, roll number, email, department, program, semester
- Password / initial credentials
- Login enabled/disabled

### Faculty
- Name, email, department, assigned subjects
- Password / initial credentials
- Login enabled/disabled

### Parents
- Name, linked student(s)
- Password / initial credentials
- Login enabled/disabled

## Tenant Association

```
Admin A  →  University A  →  Tenant A
Admin B  →  University B  →  Tenant B
```

Tenant A must NEVER be able to access Tenant B's data.

## Related Documentation

- [Authentication](authentication.md)
- [User Management](user-management.md)
- [Multi-Tenancy](multi-tenancy.md)
