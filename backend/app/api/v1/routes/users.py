"""User management routes (admin only)."""

from app.api.deps import AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.core.security import hash_password
from app.models.user import User
from app.schemas.academic import UserCreate, UserResponse, UserUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=["users"])


def _to_response(user: User) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        role=user.role,
        institution_id=str(user.institution_id),
        is_login_enabled=user.is_login_enabled,
    )


@router.get("", response_model=PaginatedResponse[UserResponse])
def list_users(
    current: AdminUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
):
    query = (
        db.query(User)
        .filter(User.institution_id == current.institution_id)
        .order_by(User.created_at.desc())
    )
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate, current: AdminUser, db: DbSession):
    if body.role != "institution_admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use role-specific endpoints for student, faculty, or parent users",
        )
    existing = (
        db.query(User)
        .filter(
            User.institution_id == current.institution_id,
            User.email == body.email,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    user = User(
        institution_id=current.institution_id,
        email=body.email,
        password_hash=hash_password(body.password),
        role=body.role,
        is_login_enabled=True,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    db.refresh(user)
    return _to_response(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, current: AdminUser, db: DbSession):
    user = get_entity_or_404(db, User, parse_uuid(user_id), current.institution_id)
    return _to_response(user)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, body: UserUpdate, current: AdminUser, db: DbSession):
    user = get_entity_or_404(db, User, parse_uuid(user_id), current.institution_id)
    if body.is_login_enabled is not None:
        user.is_login_enabled = body.is_login_enabled
    db.commit()
    db.refresh(user)
    return _to_response(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, current: AdminUser, db: DbSession):
    user = get_entity_or_404(db, User, parse_uuid(user_id), current.institution_id)
    if user.id == current.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )
    if user.student or user.faculty or user.parent:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Delete the associated profile first (student, faculty, or parent)",
        )
    db.delete(user)
    db.commit()
