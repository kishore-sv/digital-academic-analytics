"""Course and semester result CRUD routes."""

from app.api.deps import AdminOrFacultyUser, CurrentUserDep, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.enrollment import CourseResult, Enrollment, SemesterResult
from app.models.semester import Semester
from app.models.student import Student
from app.schemas.academic import (
    CourseResultCreate,
    CourseResultResponse,
    CourseResultUpdate,
    EnrollmentCreate,
    EnrollmentResponse,
    EnrollmentUpdate,
    SemesterResultCreate,
    SemesterResultResponse,
    SemesterResultUpdate,
)
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.authorization_service import assert_enrollment_access, assert_student_access
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/results", tags=["results"])


def _to_course_result(result: CourseResult) -> CourseResultResponse:
    return CourseResultResponse(
        id=str(result.id),
        enrollment_id=str(result.enrollment_id),
        grade=result.grade,
        end_marks=result.end_marks,
        status=result.status,
    )


def _to_semester_result(result: SemesterResult) -> SemesterResultResponse:
    return SemesterResultResponse(
        id=str(result.id),
        student_id=str(result.student_id),
        student_name=result.student.name if result.student else None,
        roll_number=result.student.roll_number if result.student else None,
        semester_id=str(result.semester_id),
        sgpa=result.sgpa,
        cgpa=result.cgpa,
        backlog_count=result.backlog_count,
        current_failed_courses=result.current_failed_courses,
        low_performance_course_count=result.low_performance_course_count,
        performance_trend=result.performance_trend,
    )


def _to_enrollment(enrollment: Enrollment) -> EnrollmentResponse:
    return EnrollmentResponse(
        id=str(enrollment.id),
        student_id=str(enrollment.student_id),
        course_id=str(enrollment.course_id),
        semester_id=str(enrollment.semester_id),
        attendance_percentage=enrollment.attendance_percentage,
        study_hours_per_week=enrollment.study_hours_per_week,
        assignment_completion_pct=enrollment.assignment_completion_pct,
    )


# --- Enrollments ---


@router.get("/enrollments", response_model=PaginatedResponse[EnrollmentResponse])
def list_enrollments(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    student_id: str | None = None,
):
    query = db.query(Enrollment).filter(
        Enrollment.institution_id == current.institution_id
    )
    if student_id:
        student_uuid = parse_uuid(student_id, "student_id")
        assert_student_access(db, current.user, student_uuid)
        query = query.filter(Enrollment.student_id == student_uuid)
    query = query.order_by(Enrollment.created_at.desc())
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_enrollment)


@router.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(body: EnrollmentCreate, current: AdminOrFacultyUser, db: DbSession):
    student_id = parse_uuid(body.student_id, "student_id")
    course_id = parse_uuid(body.course_id, "course_id")
    semester_id = parse_uuid(body.semester_id, "semester_id")
    get_entity_or_404(db, Student, student_id, current.institution_id)
    from app.models.course import Course

    get_entity_or_404(db, Course, course_id, current.institution_id)
    get_entity_or_404(db, Semester, semester_id, current.institution_id)
    enrollment = Enrollment(
        institution_id=current.institution_id,
        student_id=student_id,
        course_id=course_id,
        semester_id=semester_id,
        attendance_percentage=body.attendance_percentage,
        study_hours_per_week=body.study_hours_per_week,
        assignment_completion_pct=body.assignment_completion_pct,
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return _to_enrollment(enrollment)


@router.patch("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment(
    enrollment_id: str,
    body: EnrollmentUpdate,
    current: AdminOrFacultyUser,
    db: DbSession,
):
    enrollment = get_entity_or_404(
        db, Enrollment, parse_uuid(enrollment_id), current.institution_id
    )
    assert_enrollment_access(db, current.user, enrollment.id)
    if body.attendance_percentage is not None:
        enrollment.attendance_percentage = body.attendance_percentage
    if body.study_hours_per_week is not None:
        enrollment.study_hours_per_week = body.study_hours_per_week
    if body.assignment_completion_pct is not None:
        enrollment.assignment_completion_pct = body.assignment_completion_pct
    db.commit()
    db.refresh(enrollment)
    return _to_enrollment(enrollment)


# --- Course Results ---


@router.get("/course", response_model=PaginatedResponse[CourseResultResponse])
def list_course_results(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    enrollment_id: str | None = None,
):
    query = db.query(CourseResult).filter(
        CourseResult.institution_id == current.institution_id
    )
    if enrollment_id:
        query = query.filter(
            CourseResult.enrollment_id == parse_uuid(enrollment_id, "enrollment_id")
        )
    query = query.order_by(CourseResult.created_at.desc())
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_course_result)


@router.post("/course", response_model=CourseResultResponse, status_code=status.HTTP_201_CREATED)
def create_course_result(body: CourseResultCreate, current: AdminOrFacultyUser, db: DbSession):
    enrollment_id = parse_uuid(body.enrollment_id, "enrollment_id")
    assert_enrollment_access(db, current.user, enrollment_id)
    result = CourseResult(
        institution_id=current.institution_id,
        enrollment_id=enrollment_id,
        grade=body.grade,
        end_marks=body.end_marks,
        status=body.status,
    )
    db.add(result)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Course result already exists for this enrollment",
        )
    db.refresh(result)
    return _to_course_result(result)


@router.patch("/course/{result_id}", response_model=CourseResultResponse)
def update_course_result(
    result_id: str,
    body: CourseResultUpdate,
    current: AdminOrFacultyUser,
    db: DbSession,
):
    result = get_entity_or_404(
        db, CourseResult, parse_uuid(result_id), current.institution_id
    )
    assert_enrollment_access(db, current.user, result.enrollment_id)
    if body.grade is not None:
        result.grade = body.grade
    if body.end_marks is not None:
        result.end_marks = body.end_marks
    if body.status is not None:
        result.status = body.status
    db.commit()
    db.refresh(result)
    return _to_course_result(result)


# --- Semester Results ---


@router.get("/semester", response_model=PaginatedResponse[SemesterResultResponse])
def list_semester_results(
    current: CurrentUserDep,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    student_id: str | None = None,
):
    if current.role not in ("institution_admin", "faculty", "student", "parent"):
        from fastapi import HTTPException

        raise HTTPException(status_code=403, detail="Insufficient permissions")

    query = (
        db.query(SemesterResult)
        .options(joinedload(SemesterResult.student))
        .filter(SemesterResult.institution_id == current.institution_id)
    )
    if student_id:
        student_uuid = parse_uuid(student_id, "student_id")
        assert_student_access(db, current.user, student_uuid)
        query = query.filter(SemesterResult.student_id == student_uuid)
    elif current.role != "institution_admin":
        from app.services.authorization_service import filter_students_query

        student_ids = [s.id for s in filter_students_query(db, current.user).all()]
        if not student_ids:
            query = query.filter(SemesterResult.id == None)  # noqa: E711
        else:
            query = query.filter(SemesterResult.student_id.in_(student_ids))
    query = query.order_by(SemesterResult.created_at.desc())
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_semester_result)


@router.post("/semester", response_model=SemesterResultResponse, status_code=status.HTTP_201_CREATED)
def create_semester_result(body: SemesterResultCreate, current: AdminOrFacultyUser, db: DbSession):
    student_id = parse_uuid(body.student_id, "student_id")
    semester_id = parse_uuid(body.semester_id, "semester_id")
    assert_student_access(db, current.user, student_id)
    get_entity_or_404(db, Student, student_id, current.institution_id)
    get_entity_or_404(db, Semester, semester_id, current.institution_id)
    result = SemesterResult(
        institution_id=current.institution_id,
        student_id=student_id,
        semester_id=semester_id,
        sgpa=body.sgpa,
        cgpa=body.cgpa,
        backlog_count=body.backlog_count,
        current_failed_courses=body.current_failed_courses,
        low_performance_course_count=body.low_performance_course_count,
        performance_trend=body.performance_trend,
    )
    db.add(result)
    db.commit()
    db.refresh(result, ["student"])
    return _to_semester_result(result)


@router.patch("/semester/{result_id}", response_model=SemesterResultResponse)
def update_semester_result(
    result_id: str,
    body: SemesterResultUpdate,
    current: AdminOrFacultyUser,
    db: DbSession,
):
    result = get_entity_or_404(
        db, SemesterResult, parse_uuid(result_id), current.institution_id
    )
    assert_student_access(db, current.user, result.student_id)
    if body.sgpa is not None:
        result.sgpa = body.sgpa
    if body.cgpa is not None:
        result.cgpa = body.cgpa
    if body.backlog_count is not None:
        result.backlog_count = body.backlog_count
    if body.current_failed_courses is not None:
        result.current_failed_courses = body.current_failed_courses
    if body.low_performance_course_count is not None:
        result.low_performance_course_count = body.low_performance_course_count
    if body.performance_trend is not None:
        result.performance_trend = body.performance_trend
    db.commit()
    db.refresh(result, ["student"])
    return _to_semester_result(result)
