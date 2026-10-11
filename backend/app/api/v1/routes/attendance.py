"""Attendance CRUD routes."""

from datetime import date

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


def _roster_row(
    enrollment: Enrollment,
    counts: tuple[int, int] | None,
    *,
    include_percentage: bool,
    attendance_status: str | None,
    window: bool,
) -> AttendanceRosterRow:
    present, absent = counts or (0, 0)
    total = present + absent
    range_pct = (
        round(100.0 * present / total, 1) if window and not attendance_status and total else None
    )
    student = enrollment.student
    return AttendanceRosterRow(
        enrollment_id=str(enrollment.id),
        student_id=str(student.id),
        student_name=student.name,
        roll_number=student.roll_number,
        section=student.section.code if student.section else None,
        attendance_percentage=enrollment.attendance_percentage if include_percentage else None,
        range_present=present if window and attendance_status != "absent" else None,
        range_absent=absent if window and attendance_status != "present" else None,
        range_percentage=range_pct,
    )


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
    course_id: str | None = Query(None),
    academic_year_id: str | None = Query(None),
    semester_id: str | None = Query(None),
    department_id: str | None = Query(None),
    program_id: str | None = Query(None),
    batch_id: str | None = Query(None),
    class_group_id: str | None = Query(None),
    section_id: str | None = Query(None),
    year_number: int | None = Query(None, ge=1, le=8),
    search: str | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    attendance_status: str | None = Query(None, alias="status", pattern="^(present|absent)$"),
):
    from sqlalchemy import case, func

    from app.api.v1.helpers import parse_uuid
    from app.models.faculty import Faculty
    from app.services.authorization_service import get_accessible_student_ids
    from app.services.marks_entry_service import get_assigned_course_ids

    if date_from and date_to and date_from > date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="date_from must be on or before date_to",
        )

    course = None
    course_uuid = parse_uuid(course_id, "course_id") if course_id else None
    if course_uuid:
        course = get_entity_or_404(db, Course, course_uuid, current.institution_id)
    accessible = get_accessible_student_ids(db, current.user)
    faculty_course_ids = None
    if current.user.role == "faculty":
        faculty = (
            db.query(Faculty)
            .filter(
                Faculty.user_id == current.user.id,
                Faculty.institution_id == current.institution_id,
            )
            .first()
        )
        faculty_course_ids = get_assigned_course_ids(db, faculty.id) if faculty else []
        if course_uuid and faculty_course_ids and course_uuid not in faculty_course_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not assigned to this course",
            )

    enrollments = filter_enrollments_query(
        db,
        current.institution_id,
        course_id=course_uuid,
        academic_year_id=(
            parse_uuid(academic_year_id, "academic_year_id") if academic_year_id else None
        ),
        semester_id=parse_uuid(semester_id, "semester_id") if semester_id else None,
        department_id=parse_uuid(department_id, "department_id") if department_id else None,
        program_id=parse_uuid(program_id, "program_id") if program_id else None,
        batch_id=parse_uuid(batch_id, "batch_id") if batch_id else None,
        class_group_id=parse_uuid(class_group_id, "class_group_id") if class_group_id else None,
        section_id=parse_uuid(section_id, "section_id") if section_id else None,
        year_number=year_number,
        search=search,
        accessible_student_ids=accessible,
        course_ids=None if course_uuid or not faculty_course_ids else faculty_course_ids,
        load_marks=False,
    ).all()

    window = date_from is not None or date_to is not None or attendance_status is not None
    counts: dict = {}
    if window and enrollments:
        count_query = (
            db.query(
                Attendance.enrollment_id,
                func.sum(case((Attendance.status == "present", 1), else_=0)),
                func.sum(case((Attendance.status == "absent", 1), else_=0)),
            )
            .filter(
                Attendance.institution_id == current.institution_id,
                Attendance.enrollment_id.in_([e.id for e in enrollments]),
            )
        )
        if date_from:
            count_query = count_query.filter(Attendance.date >= date_from)
        if date_to:
            count_query = count_query.filter(Attendance.date <= date_to)
        if attendance_status:
            count_query = count_query.filter(Attendance.status == attendance_status)
        counts = {
            enrollment_id: (int(present or 0), int(absent or 0))
            for enrollment_id, present, absent in count_query.group_by(
                Attendance.enrollment_id
            ).all()
        }
        enrollments = [e for e in enrollments if e.id in counts]

    if course:
        rows = [
            _roster_row(
                e,
                counts.get(e.id),
                include_percentage=True,
                attendance_status=attendance_status,
                window=window,
            )
            for e in enrollments
        ]
    else:
        grouped: dict = {}
        for enrollment in enrollments:
            bucket = grouped.setdefault(
                enrollment.student_id,
                {
                    "student": enrollment.student,
                    "present": 0,
                    "absent": 0,
                    "seen": False,
                },
            )
            present, absent = counts.get(enrollment.id, (0, 0))
            bucket["present"] += present
            bucket["absent"] += absent
            bucket["seen"] = True
        rows = []
        for bucket in grouped.values():
            student = bucket["student"]
            present = bucket["present"]
            absent = bucket["absent"]
            total = present + absent
            range_pct = (
                round(100.0 * present / total, 1)
                if window and not attendance_status and total
                else None
            )
            rows.append(
                AttendanceRosterRow(
                    enrollment_id=None,
                    student_id=str(student.id),
                    student_name=student.name,
                    roll_number=student.roll_number,
                    section=student.section.code if student.section else None,
                    attendance_percentage=None,
                    range_present=present if window and attendance_status != "absent" else None,
                    range_absent=absent if window and attendance_status != "present" else None,
                    range_percentage=range_pct,
                )
            )
        rows.sort(key=lambda row: row.roll_number)

    return AttendanceRosterResponse(
        course_id=str(course.id) if course else None,
        course_name=course.name if course else None,
        course_code=course.code if course else None,
        date_from=date_from,
        date_to=date_to,
        status=attendance_status,
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
