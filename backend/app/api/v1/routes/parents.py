"""Parent CRUD and child linking routes."""

from app.api.deps import AdminUser, DbSession, ParentUser
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.core.security import hash_password
from app.models.parent import Parent, ParentStudent
from app.models.student import Student
from app.models.user import User
from app.schemas.academic import ParentCreate, ParentResponse, ParentStudentLink, ParentUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.academic_validation_service import (
    validate_parent_student_link,
    validate_relationship_type,
)
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/parents", tags=["parents"])


def _to_response(parent: Parent, db: DbSession) -> ParentResponse:
    links = (
        db.query(ParentStudent)
        .filter(ParentStudent.parent_id == parent.id)
        .all()
    )
    return ParentResponse(
        id=str(parent.id),
        name=parent.name,
        user_id=str(parent.user_id),
        phone=parent.phone,
        linked_student_ids=[str(link.student_id) for link in links],
        student_links=[
            ParentStudentLink(
                student_id=str(link.student_id),
                relationship_type=link.relationship_type,
                is_primary_guardian=link.is_primary_guardian,
            )
            for link in links
        ],
    )


@router.get("", response_model=PaginatedResponse[ParentResponse])
def list_parents(
    current: AdminUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
):
    query = (
        db.query(Parent)
        .filter(Parent.institution_id == current.institution_id)
        .order_by(Parent.created_at.desc())
    )
    items, meta = paginate(query, params)
    return paginated_response(items, meta, lambda p: _to_response(p, db))


@router.post("", response_model=ParentResponse, status_code=status.HTTP_201_CREATED)
def create_parent(body: ParentCreate, current: AdminUser, db: DbSession):
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
        role="parent",
        is_login_enabled=True,
    )
    db.add(user)
    db.flush()

    parent = Parent(
        institution_id=current.institution_id,
        user_id=user.id,
        name=body.name,
        phone=body.phone,
    )
    db.add(parent)
    db.flush()

    for link in body.student_links:
        student = get_entity_or_404(
            db, Student, parse_uuid(link.student_id, "student_id"), current.institution_id
        )
        rel = validate_relationship_type(link.relationship_type)
        db.add(
            ParentStudent(
                parent_id=parent.id,
                student_id=student.id,
                relationship_type=rel,
                is_primary_guardian=link.is_primary_guardian,
            )
        )

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    db.refresh(parent)
    return _to_response(parent, db)


@router.get("/me", response_model=ParentResponse)
def get_my_parent_profile(current: ParentUser, db: DbSession):
    parent = (
        db.query(Parent)
        .filter(
            Parent.user_id == current.id,
            Parent.institution_id == current.institution_id,
        )
        .first()
    )
    if not parent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent profile not found")
    return _to_response(parent, db)


@router.get("/{parent_id}", response_model=ParentResponse)
def get_parent(parent_id: str, current: AdminUser, db: DbSession):
    parent = get_entity_or_404(
        db, Parent, parse_uuid(parent_id), current.institution_id
    )
    return _to_response(parent, db)


@router.patch("/{parent_id}", response_model=ParentResponse)
def update_parent(
    parent_id: str,
    body: ParentUpdate,
    current: AdminUser,
    db: DbSession,
):
    parent = get_entity_or_404(
        db, Parent, parse_uuid(parent_id), current.institution_id
    )
    if body.name is not None:
        parent.name = body.name
    if body.phone is not None:
        parent.phone = body.phone
    db.commit()
    db.refresh(parent)
    return _to_response(parent, db)


@router.delete("/{parent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parent(parent_id: str, current: AdminUser, db: DbSession):
    parent = get_entity_or_404(
        db, Parent, parse_uuid(parent_id), current.institution_id
    )
    db.query(ParentStudent).filter(ParentStudent.parent_id == parent.id).delete()
    user = parent.user
    db.delete(parent)
    if user:
        db.delete(user)
    db.commit()


@router.get("/{parent_id}/children", response_model=list[str])
def list_linked_children(parent_id: str, current: AdminUser, db: DbSession):
    parent = get_entity_or_404(
        db, Parent, parse_uuid(parent_id), current.institution_id
    )
    links = (
        db.query(ParentStudent)
        .filter(ParentStudent.parent_id == parent.id)
        .all()
    )
    return [str(link.student_id) for link in links]


@router.post(
    "/{parent_id}/children/{student_id}",
    status_code=status.HTTP_201_CREATED,
)
def link_child(
    parent_id: str,
    student_id: str,
    current: AdminUser,
    db: DbSession,
    relationship_type: str = "GUARDIAN",
    is_primary_guardian: bool = False,
):
    parent_uuid = parse_uuid(parent_id)
    student_uuid = parse_uuid(student_id)
    validate_parent_student_link(db, current.institution_id, parent_uuid, student_uuid)
    rel = validate_relationship_type(relationship_type)
    existing = (
        db.query(ParentStudent)
        .filter(
            ParentStudent.parent_id == parent_uuid,
            ParentStudent.student_id == student_uuid,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already linked")
    db.add(
        ParentStudent(
            parent_id=parent_uuid,
            student_id=student_uuid,
            relationship_type=rel,
            is_primary_guardian=is_primary_guardian,
        )
    )
    db.commit()
    return {"parent_id": parent_id, "student_id": student_id}


@router.delete(
    "/{parent_id}/children/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def unlink_child(
    parent_id: str,
    student_id: str,
    current: AdminUser,
    db: DbSession,
):
    parent = get_entity_or_404(
        db, Parent, parse_uuid(parent_id), current.institution_id
    )
    student_uuid = parse_uuid(student_id)
    link = (
        db.query(ParentStudent)
        .filter(
            ParentStudent.parent_id == parent.id,
            ParentStudent.student_id == student_uuid,
        )
        .first()
    )
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    db.delete(link)
    db.commit()
