"""Authentication routes."""

from uuid import UUID

import jwt
from app.api.deps import CurrentUserDep, DbSession
from app.core.limiter import limiter
from app.core.security import (
    clear_auth_cookies,
    decode_token,
    hash_password,
    set_auth_cookies,
    verify_password,
)
from app.models.institution import Institution
from app.models.student import Student
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest, UserResponse
from fastapi import APIRouter, Cookie, HTTPException, Request, Response, status

router = APIRouter(prefix="/auth", tags=["auth"])


def _user_response(user: User, name: str | None = None) -> UserResponse:
    return UserResponse(
        id=str(user.id),
        email=user.email,
        role=user.role,
        institution_id=str(user.institution_id),
        name=name,
    )


@router.post("/signup", response_model=UserResponse)
@limiter.limit("3/minute")
def signup(request: Request, body: SignupRequest, db: DbSession, response: Response):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    institution = Institution(name=body.institution_name)
    db.add(institution)
    db.flush()

    user = User(
        institution_id=institution.id,
        email=body.email,
        password_hash=hash_password(body.password),
        role="institution_admin",
        is_login_enabled=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    set_auth_cookies(response, str(user.id), user.role, str(user.institution_id))
    return _user_response(user, name=body.name)


@router.post("/login", response_model=UserResponse)
@limiter.limit("5/minute")
def login(request: Request, body: LoginRequest, db: DbSession, response: Response):
    user: User | None = None
    name: str | None = None

    if body.role == "student":
        student = db.query(Student).filter(Student.roll_number == body.identifier).first()
        if student:
            user = (
                db.query(User)
                .filter(
                    User.id == student.user_id,
                    User.role == "student",
                    User.institution_id == student.institution_id,
                )
                .first()
            )
            name = student.name
    else:
        user = (
            db.query(User)
            .filter(User.email == body.identifier, User.role == body.role)
            .first()
        )
        if user and body.role == "faculty" and user.faculty:
            name = user.faculty.name
        elif user and body.role == "parent" and user.parent:
            name = user.parent.name

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_login_enabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account disabled")

    set_auth_cookies(response, str(user.id), user.role, str(user.institution_id))
    return _user_response(user, name=name)


@router.post("/logout")
def logout(response: Response):
    clear_auth_cookies(response)
    return {"message": "Logged out"}


@router.post("/refresh", response_model=UserResponse)
@limiter.limit("10/minute")
def refresh_token(
    request: Request,
    db: DbSession,
    response: Response,
    refresh_token: str | None = Cookie(default=None),
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing"
        )
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type"
            )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    user = db.query(User).filter(User.id == UUID(user_id)).first()
    if not user or not user.is_login_enabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or disabled"
        )

    set_auth_cookies(response, str(user.id), user.role, str(user.institution_id))
    return _user_response(user, name=_resolve_user_name(user))


def _resolve_user_name(user: User) -> str | None:
    if user.student:
        return user.student.name
    if user.faculty:
        return user.faculty.name
    if user.parent:
        return user.parent.name
    return user.email


@router.get("/me", response_model=UserResponse)
def get_me(current: CurrentUserDep):
    return _user_response(current.user, name=_resolve_user_name(current.user))
