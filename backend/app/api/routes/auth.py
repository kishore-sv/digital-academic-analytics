"""Authentication routes (stub). Planned: /api/auth/login, /api/auth/signup, /api/auth/logout"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])
