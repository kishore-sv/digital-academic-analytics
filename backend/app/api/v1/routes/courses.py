"""Course CRUD routes."""

from app.api.deps import AdminOrFacultyUser, AdminUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.course import Course
from app.models.department import Department
from app.schemas.academic import CourseCreate, CourseResponse, CourseUpdate
from app.schemas.common import PaginatedResponse, PaginationParams
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/courses", tags=["courses"])


def _to_response(course: Course) -> CourseResponse:
    return CourseResponse(
        id=str(course.id),
        department_id=str(course.department_id),
        name=course.name,
        code=course.code,
        credits=course.credits,
        course_type=course.course_type,
    )


@router.get("", response_model=PaginatedResponse[CourseResponse])
def list_courses(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
):
    query = (
        db.query(Course)
        .filter(Course.institution_id == current.institution_id)
        .order_by(Course.name.asc())
    )
    if current.user.role == "faculty":
        from app.models.faculty import Faculty
        from app.services.marks_entry_service import get_assigned_course_ids

        faculty = (
            db.query(Faculty)
            .filter(
                Faculty.user_id == current.user.id,
                Faculty.institution_id == current.institution_id,
            )
            .first()
        )
        if faculty:
            course_ids = get_assigned_course_ids(db, faculty.id)
            if course_ids:
                query = query.filter(Course.id.in_(course_ids))
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(body: CourseCreate, current: AdminUser, db: DbSession):
    dept_id = parse_uuid(body.department_id, "department_id")
    get_entity_or_404(db, Department, dept_id, current.institution_id)
    course = Course(
        institution_id=current.institution_id,
        department_id=dept_id,
        name=body.name,
        code=body.code,
        credits=body.credits,
        course_type=body.course_type,
    )
    db.add(course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Course code already exists")
    db.refresh(course)
    return _to_response(course)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: str, current: AdminOrFacultyUser, db: DbSession):
    course = get_entity_or_404(
        db, Course, parse_uuid(course_id), current.institution_id
    )
    return _to_response(course)


@router.patch("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: str,
    body: CourseUpdate,
    current: AdminUser,
    db: DbSession,
):
    course = get_entity_or_404(
        db, Course, parse_uuid(course_id), current.institution_id
    )
    if body.name is not None:
        course.name = body.name
    if body.code is not None:
        course.code = body.code
    if body.credits is not None:
        course.credits = body.credits
    if body.course_type is not None:
        course.course_type = body.course_type
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Course code already exists")
    db.refresh(course)
    return _to_response(course)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: str, current: AdminUser, db: DbSession):
    course = get_entity_or_404(
        db, Course, parse_uuid(course_id), current.institution_id
    )
    db.delete(course)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete course with linked enrollments",
        )
