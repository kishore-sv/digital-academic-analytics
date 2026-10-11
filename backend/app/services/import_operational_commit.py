"""Commit operational academic import rows."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy.orm import Session

from app.models.course_backlog import (
    BACKLOG_STATUS_CLEARED,
    BACKLOG_STATUS_NOT_CLEARED,
    CourseBacklog,
)
from app.models.enrollment import Assessment, AssessmentMark, Attendance, CourseResult, Enrollment, SemesterResult
from app.services.backlog_sync_service import sync_student_backlog_counts
from app.services.import_operational_validation import (
    _default_assessment_name,
    _default_assessment_type,
    _find_assessment,
    _normalize_attendance_status,
    _normalize_backlog_status,
)
from app.services.import_resolvers import (
    ImportResolveError,
    course_by_code,
    enrollment_for,
    parse_date_field,
    semester_for_year,
    student_by_roll,
)
from app.services.result_calculation_service import recalculate_after_marks_save

_affected_enrollments: set[uuid.UUID] = set()
_affected_mark_enrollments: set[uuid.UUID] = set()
_affected_backlog_students: set[uuid.UUID] = set()


def commit_operational_import(
    db: Session,
    import_type: str,
    institution_id: uuid.UUID,
    valid_rows: list[tuple[int, dict[str, str]]],
    *,
    duplicate_mode: str,
) -> tuple[int, int]:
    global _affected_enrollments, _affected_mark_enrollments, _affected_backlog_students
    _affected_enrollments = set()
    _affected_mark_enrollments = set()
    _affected_backlog_students = set()
    created = 0
    failed = 0
    for _row_num, row in valid_rows:
        try:
            with db.begin_nested():
                ok = _commit_row(db, import_type, institution_id, row, duplicate_mode)
            if ok:
                created += 1
            else:
                failed += 1
        except Exception:
            failed += 1

    if _affected_enrollments:
        for enrollment_id in _affected_enrollments:
            _recalculate_attendance_percentage(db, enrollment_id)

    if _affected_mark_enrollments:
        recalculate_after_marks_save(
            db, list(_affected_mark_enrollments), institution_id
        )

    for student_id in _affected_backlog_students:
        sync_student_backlog_counts(db, institution_id, student_id)

    return created, failed


def _commit_row(
    db: Session,
    import_type: str,
    institution_id: uuid.UUID,
    row: dict[str, str],
    duplicate_mode: str,
) -> bool:
    match import_type:
        case "attendance":
            return _commit_attendance(db, institution_id, row)
        case "ca_marks" | "mid_term_marks" | "end_sem_marks":
            return _commit_assessment_mark(db, institution_id, import_type, row)
        case "semester_results":
            return _commit_semester_results(db, institution_id, row)
        case "backlogs":
            return _commit_backlog(db, institution_id, row)
        case "backlog_clearance":
            return _commit_backlog_clearance(db, institution_id, row)
    raise ValueError(f"Unsupported operational import: {import_type}")


def _commit_attendance(db: Session, institution_id: uuid.UUID, row: dict[str, str]) -> bool:
    status = _normalize_attendance_status(row["status"])
    if not status:
        raise ImportResolveError("Invalid attendance status.")
    att_date = parse_date_field(row["attendance_date"], "attendance_date")
    student = student_by_roll(db, institution_id, row["student_roll_number"])
    course = course_by_code(db, institution_id, row["course_code"])
    semester = semester_for_year(
        db, institution_id, row["academic_year_name"], row["semester_number"]
    )
    enrollment = enrollment_for(db, institution_id, student, course, semester)
    db.add(
        Attendance(
            institution_id=institution_id,
            enrollment_id=enrollment.id,
            date=att_date,
            status=status,
        )
    )
    _affected_enrollments.add(enrollment.id)
    return True


def _commit_assessment_mark(
    db: Session,
    institution_id: uuid.UUID,
    import_type: str,
    row: dict[str, str],
) -> bool:
    obtained = float(row["obtained_marks"].strip())
    student = student_by_roll(db, institution_id, row["student_roll_number"])
    course = course_by_code(db, institution_id, row["course_code"])
    semester = semester_for_year(
        db, institution_id, row["academic_year_name"], row["semester_number"]
    )
    enrollment = enrollment_for(db, institution_id, student, course, semester)
    atype = _default_assessment_type(import_type, row.get("assessment_type"))
    aname = _default_assessment_name(import_type, row.get("assessment_name"))
    max_marks = float(row["max_marks"].strip()) if row.get("max_marks", "").strip() else 100.0
    adate: date | None = None
    date_key = "assessment_date" if import_type != "end_sem_marks" else "exam_date"
    if row.get(date_key, "").strip():
        adate = parse_date_field(row[date_key], date_key)

    assessment = _find_assessment(db, institution_id, course.id, atype, aname)
    if not assessment:
        assessment = Assessment(
            institution_id=institution_id,
            course_id=course.id,
            name=aname,
            assessment_type=atype,
            max_marks=max_marks,
            date=adate,
        )
        db.add(assessment)
        db.flush()
    db.add(
        AssessmentMark(
            institution_id=institution_id,
            enrollment_id=enrollment.id,
            assessment_id=assessment.id,
            marks_obtained=obtained,
        )
    )
    _affected_mark_enrollments.add(enrollment.id)
    return True


def _commit_semester_results(
    db: Session, institution_id: uuid.UUID, row: dict[str, str]
) -> bool:
    student = student_by_roll(db, institution_id, row["student_roll_number"])
    semester = semester_for_year(
        db, institution_id, row["academic_year_name"], row["semester_number"]
    )
    course_code = row.get("course_code", "").strip()
    if course_code:
        course = course_by_code(db, institution_id, course_code)
        enrollment = enrollment_for(db, institution_id, student, course, semester)
        status = (row.get("result_status") or "PASS").strip().upper()
        db.add(
            CourseResult(
                institution_id=institution_id,
                enrollment_id=enrollment.id,
                grade=row.get("grade") or None,
                end_marks=None,
                status=status,
            )
        )
        return True

    existing = (
        db.query(SemesterResult)
        .filter(
            SemesterResult.student_id == student.id,
            SemesterResult.semester_id == semester.id,
        )
        .first()
    )
    if existing:
        if row.get("sgpa", "").strip():
            existing.sgpa = float(row["sgpa"].strip())
        if row.get("cgpa", "").strip():
            existing.cgpa = float(row["cgpa"].strip())
    else:
        db.add(
            SemesterResult(
                institution_id=institution_id,
                student_id=student.id,
                semester_id=semester.id,
                sgpa=_optional_float(row.get("sgpa")),
                cgpa=_optional_float(row.get("cgpa")),
                backlog_count=0,
                current_failed_courses=0,
                low_performance_course_count=0,
                performance_trend="STABLE",
            )
        )
    return True


def _commit_backlog(db: Session, institution_id: uuid.UUID, row: dict[str, str]) -> bool:
    status = _normalize_backlog_status(row.get("status", ""))
    if status != BACKLOG_STATUS_NOT_CLEARED:
        raise ImportResolveError("Backlog status must be NOT_CLEARED.")
    student = student_by_roll(db, institution_id, row["student_roll_number"])
    course = course_by_code(db, institution_id, row["course_code"])
    semester = semester_for_year(
        db,
        institution_id,
        row["original_academic_year"],
        row["original_semester_number"],
    )
    enrollment_for(db, institution_id, student, course, semester)
    attempt = None
    if row.get("attempt_number", "").strip():
        attempt = int(row["attempt_number"].strip())
    db.add(
        CourseBacklog(
            institution_id=institution_id,
            student_id=student.id,
            course_id=course.id,
            original_semester_id=semester.id,
            status=BACKLOG_STATUS_NOT_CLEARED,
            attempt_number=attempt,
        )
    )
    _affected_backlog_students.add(student.id)
    return True


def _commit_backlog_clearance(
    db: Session, institution_id: uuid.UUID, row: dict[str, str]
) -> bool:
    status = row.get("status", "").strip().upper()
    if status not in ("CLEARED", "PASS", "PASSED"):
        raise ImportResolveError("Clearance status must be CLEARED.")
    student = student_by_roll(db, institution_id, row["student_roll_number"])
    course = course_by_code(db, institution_id, row["course_code"])
    original_semester = semester_for_year(
        db,
        institution_id,
        row["original_academic_year"],
        row["original_semester_number"],
    )
    backlog = (
        db.query(CourseBacklog)
        .filter(
            CourseBacklog.institution_id == institution_id,
            CourseBacklog.student_id == student.id,
            CourseBacklog.course_id == course.id,
            CourseBacklog.original_semester_id == original_semester.id,
        )
        .first()
    )
    if not backlog:
        raise ImportResolveError("Backlog record not found.")
    if backlog.status == BACKLOG_STATUS_CLEARED:
        raise ImportResolveError("Backlog already cleared.")
    clearance_semester_id = None
    if row.get("clearance_academic_year", "").strip() and row.get(
        "clearance_semester_number", ""
    ).strip():
        clearance_sem = semester_for_year(
            db,
            institution_id,
            row["clearance_academic_year"],
            row["clearance_semester_number"],
        )
        clearance_semester_id = clearance_sem.id
    clearance_date = None
    if row.get("clearance_date", "").strip():
        clearance_date = parse_date_field(row["clearance_date"], "clearance_date")
    backlog.status = BACKLOG_STATUS_CLEARED
    backlog.clearance_semester_id = clearance_semester_id
    backlog.clearance_date = clearance_date
    if row.get("grade", "").strip():
        backlog.grade = row["grade"].strip()
    _affected_backlog_students.add(student.id)
    return True


def _recalculate_attendance_percentage(db: Session, enrollment_id: uuid.UUID) -> None:
    records = (
        db.query(Attendance).filter(Attendance.enrollment_id == enrollment_id).all()
    )
    if not records:
        return
    present = sum(1 for r in records if r.status.lower() == "present")
    pct = round((present / len(records)) * 100, 2)
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if enrollment:
        enrollment.attendance_percentage = pct


def _optional_float(value: str | None) -> float | None:
    if not value or not str(value).strip():
        return None
    return float(str(value).strip())
