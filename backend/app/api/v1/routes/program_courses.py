"""Program curriculum mapping CRUD routes."""

from app.api.deps import AdminOrFacultyUser, AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.course import Course
from app.models.program import Program
from app.models.program_course import ProgramCourse
from app.schemas.academic import ProgramCourseCreate, ProgramCourseResponse, ProgramCourseUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/program-courses", tags=["program-courses"])


def _to_response(row: ProgramCourse) -> ProgramCourseResponse:
    return ProgramCourseResponse(
        id=str(row.id),
        program_id=str(row.program_id),
        course_id=str(row.course_id),
        semester_number=row.semester_number,
    )


@router.get("", response_model=PaginatedResponse[ProgramCourseResponse])
def list_program_courses(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    program_id: str | None = Query(None),
    semester_number: int | None = Query(None),
):
    query = db.query(ProgramCourse).filter(
        ProgramCourse.institution_id == current.institution_id
    )
    if program_id:
        query = query.filter(ProgramCourse.program_id == parse_uuid(program_id, "program_id"))
    if semester_number is not None:
        query = query.filter(ProgramCourse.semester_number == semester_number)
    query = query.order_by(ProgramCourse.semester_number)
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=ProgramCourseResponse, status_code=status.HTTP_201_CREATED)
def create_program_course(body: ProgramCourseCreate, current: AdminUser, db: DbSession):
    program_id = parse_uuid(body.program_id, "program_id")
    course_id = parse_uuid(body.course_id, "course_id")
    get_entity_or_404(db, Program, program_id, current.institution_id)
    get_entity_or_404(db, Course, course_id, current.institution_id)
    row = ProgramCourse(
        institution_id=current.institution_id,
        program_id=program_id,
        course_id=course_id,
        semester_number=body.semester_number,
    )
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mapping exists")
    db.refresh(row)
    return _to_response(row)


@router.patch("/{mapping_id}", response_model=ProgramCourseResponse)
def update_program_course(
    mapping_id: str, body: ProgramCourseUpdate, current: AdminUser, db: DbSession
):
    row = get_entity_or_404(
        db, ProgramCourse, parse_uuid(mapping_id), current.institution_id
    )
    if body.semester_number is not None:
        row.semester_number = body.semester_number
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Mapping conflict")
    db.refresh(row)
    return _to_response(row)


@router.delete("/{mapping_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_program_course(mapping_id: str, current: AdminUser, db: DbSession):
    row = get_entity_or_404(
        db, ProgramCourse, parse_uuid(mapping_id), current.institution_id
    )
    db.delete(row)
    db.commit()
