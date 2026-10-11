"""Operational academic import validation tests."""

import pytest

from app.core.import_constants import IMPORT_TYPES, COMING_SOON_IMPORT_COUNT
from app.models.course_backlog import BACKLOG_STATUS_NOT_CLEARED, CourseBacklog
from app.services.import_job_service import create_job_from_upload, validate_job
from app.services.import_operational_validation import validate_operational_row

API = "/api/v1"


def _admin_login(client):
    res = client.post(
        f"{API}/auth/login",
        json={
            "identifier": "admin@demo.com",
            "password": "admin123",
            "role": "institution_admin",
        },
    )
    assert res.status_code == 200, res.text


def _enrollment_context(client, db):
    from app.models.academic_year import AcademicYear
    from app.models.course import Course
    from app.models.enrollment import Enrollment
    from app.models.semester import Semester
    from app.models.student import Student

    _admin_login(client)
    enrollment = db.query(Enrollment).first()
    if not enrollment:
        pytest.skip("Seeded enrollment required")
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    semester = db.query(Semester).filter(Semester.id == enrollment.semester_id).first()
    year = (
        db.query(AcademicYear)
        .filter(AcademicYear.id == semester.academic_year_id)
        .first()
    )
    return {
        "roll": student.roll_number,
        "course_code": course.code,
        "year_name": year.name,
        "semester_number": str(semester.number),
        "institution_id": enrollment.institution_id,
        "student_id": student.id,
        "course_id": course.id,
        "semester_id": semester.id,
    }


@pytest.fixture
def db_session():
    from app.core.database import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_operational_types_registered():
    for key in (
        "attendance",
        "ca_marks",
        "mid_term_marks",
        "end_sem_marks",
        "semester_results",
        "backlogs",
        "backlog_clearance",
    ):
        assert key in IMPORT_TYPES
    assert COMING_SOON_IMPORT_COUNT == 0


def test_attendance_invalid_status(client, db_session):
    ctx = _enrollment_context(client, db_session)
    errors = validate_operational_row(
        db_session,
        ctx["institution_id"],
        "attendance",
        {
            "student_roll_number": ctx["roll"],
            "course_code": ctx["course_code"],
            "academic_year_name": ctx["year_name"],
            "semester_number": ctx["semester_number"],
            "attendance_date": "2026-01-15",
            "status": "LATE",
        },
    )
    assert any("present or absent" in e.lower() for e in errors)


def test_ca_marks_exceed_max(client, db_session):
    ctx = _enrollment_context(client, db_session)
    errors = validate_operational_row(
        db_session,
        ctx["institution_id"],
        "ca_marks",
        {
            "student_roll_number": ctx["roll"],
            "course_code": ctx["course_code"],
            "academic_year_name": ctx["year_name"],
            "semester_number": ctx["semester_number"],
            "obtained_marks": "150",
            "max_marks": "30",
        },
    )
    assert any("exceed" in e.lower() for e in errors)


def test_semester_results_rejects_grade_point(client, db_session):
    ctx = _enrollment_context(client, db_session)
    errors = validate_operational_row(
        db_session,
        ctx["institution_id"],
        "semester_results",
        {
            "student_roll_number": ctx["roll"],
            "academic_year_name": ctx["year_name"],
            "semester_number": ctx["semester_number"],
            "course_code": ctx["course_code"],
            "grade": "A",
            "result_status": "PASS",
            "grade_point": "8",
        },
    )
    assert any("grade_point" in e for e in errors)


def test_backlog_persists_course_backlog(client, db_session):
    ctx = _enrollment_context(client, db_session)
    from app.models.user import User

    admin = (
        db_session.query(User).filter(User.email == "admin@demo.com").first()
    )
    if not admin:
        pytest.skip("admin required")
    csv = (
        "student_roll_number,course_code,original_academic_year,original_semester_number,status\n"
        f"{ctx['roll']},{ctx['course_code']},{ctx['year_name']},"
        f"{ctx['semester_number']},NOT_CLEARED\n"
    )
    job, _ = create_job_from_upload(
        db_session,
        institution_id=admin.institution_id,
        user_id=admin.id,
        import_type="backlogs",
        filename="backlogs.csv",
        content=csv.encode(),
    )
    validate_job(db_session, job)
    assert job.valid_rows >= 1
    from app.services.import_operational_commit import commit_operational_import

    mapped = job.raw_rows or []
    valid = [(2, mapped[0])] if mapped else []
    commit_operational_import(
        db_session,
        "backlogs",
        admin.institution_id,
        valid,
        duplicate_mode="reject",
    )
    backlog = (
        db_session.query(CourseBacklog)
        .filter(
            CourseBacklog.student_id == ctx["student_id"],
            CourseBacklog.course_id == ctx["course_id"],
            CourseBacklog.original_semester_id == ctx["semester_id"],
        )
        .first()
    )
    assert backlog is not None
    assert backlog.status == BACKLOG_STATUS_NOT_CLEARED


def test_template_download(client):
    _admin_login(client)
    res = client.get(f"{API}/imports/types/attendance/template.csv")
    assert res.status_code == 200
    assert "student_roll_number" in res.text
