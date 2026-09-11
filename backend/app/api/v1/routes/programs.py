"""Program CRUD routes."""

from app.api.deps import AdminOrFacultyUser, AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.department import Department
from app.models.program import Program
from app.schemas.academic import ProgramCreate, ProgramResponse, ProgramUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/programs", tags=["programs"])


def _to_response(program: Program) -> ProgramResponse:
    return ProgramResponse(
        id=str(program.id),
        department_id=str(program.department_id),
        name=program.name,
        code=program.code,
        duration_semesters=program.duration_semesters,
    )


@router.get("", response_model=PaginatedResponse[ProgramResponse])
def list_programs(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
):
    query = (
        db.query(Program)
        .filter(Program.institution_id == current.institution_id)
        .order_by(Program.name.asc())
    )
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=ProgramResponse, status_code=status.HTTP_201_CREATED)
def create_program(body: ProgramCreate, current: AdminUser, db: DbSession):
    dept_id = parse_uuid(body.department_id, "department_id")
    get_entity_or_404(db, Department, dept_id, current.institution_id)
    program = Program(
        institution_id=current.institution_id,
        department_id=dept_id,
        name=body.name,
        code=body.code,
        duration_semesters=body.duration_semesters,
    )
    db.add(program)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Program code already exists")
    db.refresh(program)
    return _to_response(program)


@router.get("/{program_id}", response_model=ProgramResponse)
def get_program(program_id: str, current: AdminOrFacultyUser, db: DbSession):
    program = get_entity_or_404(
        db, Program, parse_uuid(program_id), current.institution_id
    )
    return _to_response(program)


@router.patch("/{program_id}", response_model=ProgramResponse)
def update_program(
    program_id: str,
    body: ProgramUpdate,
    current: AdminUser,
    db: DbSession,
):
    program = get_entity_or_404(
        db, Program, parse_uuid(program_id), current.institution_id
    )
    if body.name is not None:
        program.name = body.name
    if body.code is not None:
        program.code = body.code
    if body.duration_semesters is not None:
        program.duration_semesters = body.duration_semesters
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Program code already exists")
    db.refresh(program)
    return _to_response(program)


@router.delete("/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_program(program_id: str, current: AdminUser, db: DbSession):
    program = get_entity_or_404(
        db, Program, parse_uuid(program_id), current.institution_id
    )
    db.delete(program)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete program with linked students",
        )
