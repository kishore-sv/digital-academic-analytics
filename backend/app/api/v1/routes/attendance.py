"""Attendance CRUD routes."""

from app.api.deps import AdminOrFacultyUser, DbSession
from app.api.v1.helpers import PaginationDep, get_entity_or_404, parse_uuid
from app.api.v1.pagination import paginate, paginated_response
from app.models.enrollment import Attendance, Enrollment
from app.models.course import Course
from app.schemas.academic import (
    AttendanceCreate,
    AttendanceResponse,
    AttendanceRosterResponse,
    AttendanceRosterRow,
    AttendanceUpdate,
    BulkAttendanceRequest,
    EnrollmentResponse,
)
from app.services.marks_entry_service import filter_enrollments_query
from fastapi import Query
from app.schemas.common import PaginatedResponse, PaginationParams
from app.services.authorization_service import assert_enrollment_access, assert_student_access
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/attendance", tags=["attendance"])


def _to_response(record: Attendance) -> AttendanceResponse:
    return AttendanceResponse(
        id=str(record.id),
        enrollment_id=str(record.enrollment_id),
        date=record.date,
        status=record.status,
    )


@router.get("", response_model=PaginatedResponse[AttendanceResponse])
def list_attendance(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    enrollment_id: str | None = None,
    student_id: str | None = None,
):
    query = db.query(Attendance).filter(
        Attendance.institution_id == current.institution_id
    )
    if enrollment_id:
        query = query.filter(
            Attendance.enrollment_id == parse_uuid(enrollment_id, "enrollment_id")
        )
    if student_id:
        student_uuid = parse_uuid(student_id, "student_id")
        assert_student_access(db, current.user, student_uuid)
        enrollments = (
            db.query(Enrollment.id)
            .filter(
                Enrollment.institution_id == current.institution_id,
                Enrollment.student_id == student_uuid,
            )
            .all()
        )
        enrollment_ids = [e[0] for e in enrollments]
        if not enrollment_ids:
            items, meta = paginate(query.filter(Attendance.id == None), params)  # noqa: E711
            return paginated_response(items, meta, _to_response)
        query = query.filter(Attendance.enrollment_id.in_(enrollment_ids))
    query = query.order_by(Attendance.date.desc())
    items, meta = paginate(query, params)
    return paginated_response(items, meta, _to_response)


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(body: AttendanceCreate, current: AdminOrFacultyUser, db: DbSession):
    enrollment_id = parse_uuid(body.enrollment_id, "enrollment_id")
    enrollment = get_entity_or_404(db, Enrollment, enrollment_id, current.institution_id)
    assert_student_access(db, current.user, enrollment.student_id)
    record = Attendance(
        institution_id=current.institution_id,
        enrollment_id=enrollment_id,
        date=body.date,
        status=body.status,
    )
    db.add(record)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attendance record already exists for this date",
        )
    db.refresh(record)
    return _to_response(record)


@router.get("/roster", response_model=AttendanceRosterResponse)
def get_attendance_roster(
    current: AdminOrFacultyUser,
    db: DbSession,
    course_id: str = Query(...),
    semester_id: str | None = Query(None),
    department_id: str | None = Query(None),
    program_id: str | None = Query(None),
    section: str | None = Query(None),
    search: str | None = Query(None),
):
    from app.api.v1.helpers import parse_uuid
    from app.services.authorization_service import get_accessible_student_ids

    course_uuid = parse_uuid(course_id, "course_id")
    course = get_entity_or_404(db, Course, course_uuid, current.institution_id)
    accessible = get_accessible_student_ids(db, current.user)

    enrollments = filter_enrollments_query(
        db,
        current.institution_id,
        course_id=course_uuid,
        semester_id=parse_uuid(semester_id, "semester_id") if semester_id else None,
        department_id=parse_uuid(department_id, "department_id") if department_id else None,
        program_id=parse_uuid(program_id, "program_id") if program_id else None,
        section=section,
        search=search,
        accessible_student_ids=accessible,
    ).all()

    rows = [
        AttendanceRosterRow(
            enrollment_id=str(e.id),
            student_id=str(e.student.id),
            student_name=e.student.name,
            roll_number=e.student.roll_number,
            section=e.student.section,
            attendance_percentage=e.attendance_percentage,
        )
        for e in enrollments
    ]
    return AttendanceRosterResponse(
        course_id=str(course.id),
        course_name=course.name,
        course_code=course.code,
        students=rows,
    )


@router.post("/bulk", response_model=list[EnrollmentResponse])
def bulk_update_attendance(
    body: BulkAttendanceRequest,
    current: AdminOrFacultyUser,
    db: DbSession,
):
    updated = []
    for entry in body.entries:
        enrollment_id = parse_uuid(entry.enrollment_id, "enrollment_id")
        enrollment = assert_enrollment_access(db, current.user, enrollment_id)
        enrollment.attendance_percentage = entry.attendance_percentage
        updated.append(enrollment)
    db.commit()
    for e in updated:
        db.refresh(e)
    return [
        EnrollmentResponse(
            id=str(e.id),
            student_id=str(e.student_id),
            course_id=str(e.course_id),
            semester_id=str(e.semester_id),
            attendance_percentage=e.attendance_percentage,
            study_hours_per_week=e.study_hours_per_week,
            assignment_completion_pct=e.assignment_completion_pct,
        )
        for e in updated
    ]


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(attendance_id: str, current: AdminOrFacultyUser, db: DbSession):
    record = get_entity_or_404(
        db, Attendance, parse_uuid(attendance_id), current.institution_id
    )
    enrollment = get_entity_or_404(
        db, Enrollment, record.enrollment_id, current.institution_id
    )
    assert_student_access(db, current.user, enrollment.student_id)
    return _to_response(record)


@router.patch("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: str,
    body: AttendanceUpdate,
    current: AdminOrFacultyUser,
    db: DbSession,
):
    record = get_entity_or_404(
        db, Attendance, parse_uuid(attendance_id), current.institution_id
    )
    enrollment = get_entity_or_404(
        db, Enrollment, record.enrollment_id, current.institution_id
    )
    assert_student_access(db, current.user, enrollment.student_id)
    record.status = body.status
    db.commit()
    db.refresh(record)
    return _to_response(record)


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(attendance_id: str, current: AdminOrFacultyUser, db: DbSession):
    record = get_entity_or_404(
        db, Attendance, parse_uuid(attendance_id), current.institution_id
    )
    enrollment = get_entity_or_404(
        db, Enrollment, record.enrollment_id, current.institution_id
    )
    assert_student_access(db, current.user, enrollment.student_id)
    db.delete(record)
    db.commit()
