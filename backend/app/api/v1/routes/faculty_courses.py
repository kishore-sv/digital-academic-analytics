"""Faculty course assignment CRUD routes."""

from app.api.deps import AdminOrFacultyUser, AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.faculty import Faculty
from app.models.faculty_course import FacultyCourse
from app.schemas.academic import FacultyCourseCreate, FacultyCourseResponse, FacultyCourseUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.academic_validation_service import validate_faculty_course_assignment
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/faculty-courses", tags=["faculty-courses"])


def _to_response(row: FacultyCourse) -> FacultyCourseResponse:
    return FacultyCourseResponse(
        id=str(row.id),
        faculty_id=str(row.faculty_id),
        course_id=str(row.course_id),
        semester_id=str(row.semester_id),
        section_id=str(row.section_id) if row.section_id else None,
    )


@router.get("", response_model=PaginatedResponse[FacultyCourseResponse])
def list_faculty_courses(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    faculty_id: str | None = Query(None),
    course_id: str | None = Query(None),
    semester_id: str | None = Query(None),
):
    query = db.query(FacultyCourse).filter(
        FacultyCourse.institution_id == current.institution_id
    )
    if faculty_id:
        query = query.filter(FacultyCourse.faculty_id == parse_uuid(faculty_id, "faculty_id"))
    if course_id:
        query = query.filter(FacultyCourse.course_id == parse_uuid(course_id, "course_id"))
    if semester_id:
        query = query.filter(
            FacultyCourse.semester_id == parse_uuid(semester_id, "semester_id")
        )
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=FacultyCourseResponse, status_code=status.HTTP_201_CREATED)
def create_faculty_course(body: FacultyCourseCreate, current: AdminUser, db: DbSession):
    faculty_id = parse_uuid(body.faculty_id, "faculty_id")
    course_id = parse_uuid(body.course_id, "course_id")
    semester_id = parse_uuid(body.semester_id, "semester_id")
    section_id = parse_uuid(body.section_id, "section_id") if body.section_id else None
    get_entity_or_404(db, Faculty, faculty_id, current.institution_id)
    validate_faculty_course_assignment(
        db,
        current.institution_id,
        faculty_id=faculty_id,
        course_id=course_id,
        semester_id=semester_id,
        section_id=section_id,
    )
    row = FacultyCourse(
        institution_id=current.institution_id,
        faculty_id=faculty_id,
        course_id=course_id,
        semester_id=semester_id,
        section_id=section_id,
    )
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Assignment exists")
    db.refresh(row)
    return _to_response(row)


@router.patch("/{assignment_id}", response_model=FacultyCourseResponse)
def update_faculty_course(
    assignment_id: str, body: FacultyCourseUpdate, current: AdminUser, db: DbSession
):
    row = get_entity_or_404(
        db, FacultyCourse, parse_uuid(assignment_id), current.institution_id
    )
    section_id = (
        parse_uuid(body.section_id, "section_id") if body.section_id else None
    ) if body.section_id is not None else row.section_id
    if body.section_id is not None and body.section_id == "":
        section_id = None
    validate_faculty_course_assignment(
        db,
        current.institution_id,
        faculty_id=row.faculty_id,
        course_id=row.course_id,
        semester_id=row.semester_id,
        section_id=section_id,
        exclude_id=row.id,
    )
    row.section_id = section_id
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Assignment conflict")
    db.refresh(row)
    return _to_response(row)


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faculty_course(assignment_id: str, current: AdminUser, db: DbSession):
    row = get_entity_or_404(
        db, FacultyCourse, parse_uuid(assignment_id), current.institution_id
    )
    db.delete(row)
    db.commit()
