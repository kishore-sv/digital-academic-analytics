"""FastAPI dependencies for auth, DB, and RBAC."""

from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.faculty import Faculty
from app.models.parent import Parent
from app.models.student import Student
from app.models.user import User
from app.services.authorization_service import assert_student_access

DbSession = Annotated[Session, Depends(get_db)]


class CurrentUser:
    def __init__(self, user: User):
        self.user = user
        self.id = user.id
        self.role = user.role
        self.institution_id = user.institution_id
        self.email = user.email


def get_current_user(
    db: DbSession,
    access_token: str | None = Cookie(default=None),
) -> CurrentUser:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = decode_token(access_token)
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.id == UUID(user_id)).first()
    if not user or not user.is_login_enabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or disabled"
        )
    return CurrentUser(user)


def require_role(*roles: str):
    def checker(current: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        if current.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
        return current

    return checker


def get_faculty_profile(
    current: Annotated[CurrentUser, Depends(require_role("institution_admin", "faculty"))],
    db: DbSession,
) -> Faculty:
    faculty = (
        db.query(Faculty)
        .filter(
            Faculty.user_id == current.id,
            Faculty.institution_id == current.institution_id,
        )
        .first()
    )
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Faculty profile not found"
        )
    return faculty


def get_parent_profile(
    current: Annotated[CurrentUser, Depends(require_role("institution_admin", "parent"))],
    db: DbSession,
) -> Parent:
    parent = (
        db.query(Parent)
        .filter(
            Parent.user_id == current.id,
            Parent.institution_id == current.institution_id,
        )
        .first()
    )
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parent profile not found"
        )
    return parent


def require_student_access(
    student_id: Annotated[str, Path()],
    current: Annotated[CurrentUser, Depends(get_current_user)],
    db: DbSession,
) -> Student:
    return assert_student_access(db, current.user, UUID(student_id))


CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]
AdminUser = Annotated[CurrentUser, Depends(require_role("institution_admin"))]
FacultyUser = Annotated[CurrentUser, Depends(require_role("institution_admin", "faculty"))]
StudentUser = Annotated[CurrentUser, Depends(require_role("institution_admin", "student"))]
ParentUser = Annotated[CurrentUser, Depends(require_role("institution_admin", "parent"))]
PredictionToolUser = Annotated[
    CurrentUser, Depends(require_role("institution_admin", "faculty"))
]
AdminOrFacultyUser = Annotated[
    CurrentUser, Depends(require_role("institution_admin", "faculty"))
]
FacultyProfileDep = Annotated[Faculty, Depends(get_faculty_profile)]
ParentProfileDep = Annotated[Parent, Depends(get_parent_profile)]
