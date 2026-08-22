"""Authentication and security utilities (stub).

Planned token/session payload:
    {
        "user_id": str,
        "role": "admin" | "student" | "faculty" | "parent",
        "institution_id": str,
    }

Security rules:
- Never trust tenant_id or role from the client
- Backend must validate credentials and derive tenant from auth token
- Disabled users (is_login_enabled=False) must not authenticate
"""

# TODO: Implement password hashing, token creation, and verification
