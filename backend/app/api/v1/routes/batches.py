"""Batch CRUD routes."""

from app.api.deps import AdminOrFacultyUser, AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.batch import Batch
from app.models.program import Program
from app.schemas.academic import BatchCreate, BatchResponse, BatchUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/batches", tags=["batches"])


def _to_response(batch: Batch) -> BatchResponse:
    return BatchResponse(
        id=str(batch.id),
        program_id=str(batch.program_id),
        admission_year=batch.admission_year,
        code=batch.code,
        name=batch.name,
        is_active=batch.is_active,
    )


@router.get("", response_model=PaginatedResponse[BatchResponse])
def list_batches(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    program_id: str | None = Query(None),
):
    query = db.query(Batch).filter(Batch.institution_id == current.institution_id)
    if program_id:
        query = query.filter(Batch.program_id == parse_uuid(program_id, "program_id"))
    query = query.order_by(Batch.admission_year.desc())
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=BatchResponse, status_code=status.HTTP_201_CREATED)
def create_batch(body: BatchCreate, current: AdminUser, db: DbSession):
    program_id = parse_uuid(body.program_id, "program_id")
    get_entity_or_404(db, Program, program_id, current.institution_id)
    batch = Batch(
        institution_id=current.institution_id,
        program_id=program_id,
        admission_year=body.admission_year,
        code=body.code,
        name=body.name,
        is_active=body.is_active,
    )
    db.add(batch)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Batch already exists")
    db.refresh(batch)
    return _to_response(batch)


@router.patch("/{batch_id}", response_model=BatchResponse)
def update_batch(batch_id: str, body: BatchUpdate, current: AdminUser, db: DbSession):
    batch = get_entity_or_404(db, Batch, parse_uuid(batch_id), current.institution_id)
    if body.admission_year is not None:
        batch.admission_year = body.admission_year
    if body.code is not None:
        batch.code = body.code
    if body.name is not None:
        batch.name = body.name
    if body.is_active is not None:
        batch.is_active = body.is_active
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Batch conflict")
    db.refresh(batch)
    return _to_response(batch)


@router.delete("/{batch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_batch(batch_id: str, current: AdminUser, db: DbSession):
    batch = get_entity_or_404(db, Batch, parse_uuid(batch_id), current.institution_id)
    db.delete(batch)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete batch with linked students or class groups",
        )
