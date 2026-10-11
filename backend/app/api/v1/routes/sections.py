"""Section CRUD routes."""

from app.api.deps import AdminOrFacultyUser, AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.class_group import ClassGroup
from app.models.section import Section
from app.schemas.academic import SectionCreate, SectionResponse, SectionUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/sections", tags=["sections"])


def _to_response(section: Section) -> SectionResponse:
    return SectionResponse(
        id=str(section.id),
        class_group_id=str(section.class_group_id),
        code=section.code,
        name=section.name,
        is_active=section.is_active,
    )


@router.get("", response_model=PaginatedResponse[SectionResponse])
def list_sections(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    class_group_id: str | None = Query(None),
):
    query = db.query(Section).filter(Section.institution_id == current.institution_id)
    if class_group_id:
        query = query.filter(
            Section.class_group_id == parse_uuid(class_group_id, "class_group_id")
        )
    query = query.order_by(Section.code)
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
def create_section(body: SectionCreate, current: AdminUser, db: DbSession):
    class_group_id = parse_uuid(body.class_group_id, "class_group_id")
    get_entity_or_404(db, ClassGroup, class_group_id, current.institution_id)
    section = Section(
        institution_id=current.institution_id,
        class_group_id=class_group_id,
        code=body.code,
        name=body.name,
        is_active=body.is_active,
    )
    db.add(section)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Section exists")
    db.refresh(section)
    return _to_response(section)


@router.patch("/{section_id}", response_model=SectionResponse)
def update_section(section_id: str, body: SectionUpdate, current: AdminUser, db: DbSession):
    section = get_entity_or_404(db, Section, parse_uuid(section_id), current.institution_id)
    if body.code is not None:
        section.code = body.code
    if body.name is not None:
        section.name = body.name
    if body.is_active is not None:
        section.is_active = body.is_active
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Section conflict")
    db.refresh(section)
    return _to_response(section)


@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_section(section_id: str, current: AdminUser, db: DbSession):
    section = get_entity_or_404(db, Section, parse_uuid(section_id), current.institution_id)
    db.delete(section)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete section with linked students",
        )
