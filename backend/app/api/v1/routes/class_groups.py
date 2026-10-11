"""Class group CRUD routes."""

from app.api.deps import AdminOrFacultyUser, AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.batch import Batch
from app.models.class_group import ClassGroup
from app.schemas.academic import ClassGroupCreate, ClassGroupResponse, ClassGroupUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from app.utils.academic_display import format_year_number
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/class-groups", tags=["class-groups"])


def _to_response(cg: ClassGroup) -> ClassGroupResponse:
    return ClassGroupResponse(
        id=str(cg.id),
        batch_id=str(cg.batch_id),
        year_number=cg.year_number,
        year_label=format_year_number(cg.year_number),
        code=cg.code,
        name=cg.name,
    )


@router.get("", response_model=PaginatedResponse[ClassGroupResponse])
def list_class_groups(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    batch_id: str | None = Query(None),
    year_number: int | None = Query(None),
):
    query = db.query(ClassGroup).filter(ClassGroup.institution_id == current.institution_id)
    if batch_id:
        query = query.filter(ClassGroup.batch_id == parse_uuid(batch_id, "batch_id"))
    if year_number is not None:
        query = query.filter(ClassGroup.year_number == year_number)
    query = query.order_by(ClassGroup.year_number)
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=ClassGroupResponse, status_code=status.HTTP_201_CREATED)
def create_class_group(body: ClassGroupCreate, current: AdminUser, db: DbSession):
    batch_id = parse_uuid(body.batch_id, "batch_id")
    get_entity_or_404(db, Batch, batch_id, current.institution_id)
    cg = ClassGroup(
        institution_id=current.institution_id,
        batch_id=batch_id,
        year_number=body.year_number,
        code=body.code,
        name=body.name,
    )
    db.add(cg)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Class group exists")
    db.refresh(cg)
    return _to_response(cg)


@router.patch("/{class_group_id}", response_model=ClassGroupResponse)
def update_class_group(
    class_group_id: str, body: ClassGroupUpdate, current: AdminUser, db: DbSession
):
    cg = get_entity_or_404(
        db, ClassGroup, parse_uuid(class_group_id), current.institution_id
    )
    if body.year_number is not None:
        cg.year_number = body.year_number
    if body.code is not None:
        cg.code = body.code
    if body.name is not None:
        cg.name = body.name
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Class group conflict")
    db.refresh(cg)
    return _to_response(cg)


@router.delete("/{class_group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class_group(class_group_id: str, current: AdminUser, db: DbSession):
    cg = get_entity_or_404(
        db, ClassGroup, parse_uuid(class_group_id), current.institution_id
    )
    db.delete(cg)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete class group with linked sections or students",
        )
