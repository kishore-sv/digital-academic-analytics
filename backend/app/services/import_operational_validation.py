"""Database-backed validation for operational academic imports."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models.course_backlog import BACKLOG_STATUS_CLEARED, BACKLOG_STATUS_NOT_CLEARED, CourseBacklog
from app.models.enrollment import (
    Assessment,
    AssessmentMark,
    Attendance,
    CourseResult,
    SemesterResult,
)
from app.services.import_resolvers import (
    ImportResolveError,
    course_by_code,
    enrollment_for,
    parse_date_field,
    semester_for_year,
    student_by_roll,
)

VALID_ASSESSMENT_TYPES = {"CA", "MID", "FINAL", "ASSIGNMENT"}
MAX_ASSESSMENT_MARKS = 100.0


def validate_operational_row(
    db: Session,
    institution_id: uuid.UUID,
    import_type: str,
    row: dict[str, str],
) -> list[str]:
    try:
        match import_type:
            case "attendance":
                return _validate_attendance(db, institution_id, row)
            case "ca_marks" | "mid_term_marks" | "end_sem_marks":
                return _validate_assessment_marks(db, institution_id, import_type, row)
            case "semester_results":
                return _validate_semester_results(db, institution_id, row)
            case "backlogs":
                return _validate_backlog(db, institution_id, row)
            case "backlog_clearance":
                return _validate_backlog_clearance(db, institution_id, row)
    except ImportResolveError as exc:
        return [str(exc)]
    return [f"Unsupported operational import type: {import_type}"]


def _validate_attendance(
    db: Session, institution_id: uuid.UUID, row: dict[str, str]
) -> list[str]:
    errors: list[str] = []
    status = _normalize_attendance_status(row.get("status", ""))
    if status is None:
        errors.append("Status must be present or absent.")
        return errors
    try:
        att_date = parse_date_field(row["attendance_date"], "attendance_date")
    except ImportResolveError as exc:
        return [str(exc)]
    student = student_by_roll(db, institution_id, row["student_roll_number"])
    course = course_by_code(db, institution_id, row["course_code"])
    semester = semester_for_year(
        db, institution_id, row["academic_year_name"], row["semester_number"]
    )
    enrollment = enrollment_for(db, institution_id, student, course, semester)
    existing = (
        db.query(Attendance)
        .filter(
            Attendance.enrollment_id == enrollment.id,
            Attendance.date == att_date,
        )
        .first()
    )
    if existing:
        errors.append("Attendance record already exists for this enrollment and date.")
    return errors


def _validate_assessment_marks(
    db: Session,
    institution_id: uuid.UUID,
    import_type: str,
    row: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    obtained = _parse_float(row.get("obtained_marks", ""), "obtained_marks")
    if obtained is None:
        return ["Obtained marks must be a valid number."]
    if obtained < 0:
        errors.append("Obtained marks cannot be negative.")
    max_marks = 100.0
    if row.get("max_marks", "").strip():
        max_marks = _parse_float(row["max_marks"], "max_marks")
        if max_marks is None:
            errors.append("Max marks must be a valid number.")
            return errors
        if max_marks <= 0 or max_marks > MAX_ASSESSMENT_MARKS:
            errors.append("Max marks must be between 0 and 100.")
    if obtained > max_marks:
        errors.append("Obtained marks exceed maximum marks.")

    atype = _default_assessment_type(import_type, row.get("assessment_type"))
    if import_type == "ca_marks" and atype != "CA":
        errors.append("CA import requires assessment_type CA.")
    if import_type == "mid_term_marks" and atype != "MID":
        errors.append("Mid-term import requires assessment_type MID.")
    if import_type == "end_sem_marks" and atype != "FINAL":
        errors.append("End-semester import requires assessment_type FINAL.")
    if atype not in VALID_ASSESSMENT_TYPES:
        errors.append(f"Unsupported assessment type: {atype}.")

    student = student_by_roll(db, institution_id, row["student_roll_number"])
    course = course_by_code(db, institution_id, row["course_code"])
    semester = semester_for_year(
        db, institution_id, row["academic_year_name"], row["semester_number"]
    )
    enrollment = enrollment_for(db, institution_id, student, course, semester)
    aname = _default_assessment_name(import_type, row.get("assessment_name"))
    assessment = _find_assessment(db, institution_id, course.id, atype, aname)
    if assessment:
        if obtained > assessment.max_marks:
            errors.append("Obtained marks exceed maximum marks for the assessment.")
        existing = (
            db.query(AssessmentMark)
            .filter(
                AssessmentMark.enrollment_id == enrollment.id,
                AssessmentMark.assessment_id == assessment.id,
            )
            .first()
        )
        if existing:
            errors.append("Assessment mark already exists for this student and assessment.")
    return errors


def _validate_semester_results(
    db: Session, institution_id: uuid.UUID, row: dict[str, str]
) -> list[str]:
    errors: list[str] = []
    for forbidden in ("grade_point", "credits", "end_marks"):
        if str(row.get(forbidden, "")).strip():
            errors.append(f"Field '{forbidden}' cannot be imported; it is derived by the system.")
    if errors:
        return errors

    student = student_by_roll(db, institution_id, row["student_roll_number"])
    semester = semester_for_year(
        db, institution_id, row["academic_year_name"], row["semester_number"]
    )
    course_code = row.get("course_code", "").strip()
    if course_code:
        course = course_by_code(db, institution_id, course_code)
        enrollment = enrollment_for(db, institution_id, student, course, semester)
        status = (row.get("result_status") or "PASS").strip().upper()
        if status not in ("PASS", "FAIL"):
            errors.append("Result status must be PASS or FAIL.")
        existing = (
            db.query(CourseResult)
            .filter(CourseResult.enrollment_id == enrollment.id)
            .first()
        )
        if existing:
            errors.append("Course result already exists for this enrollment.")
        return errors

    if not row.get("sgpa", "").strip() and not row.get("cgpa", "").strip():
        errors.append(
            "Provide course_code for course results, or sgpa/cgpa for semester results."
        )
        return errors
    existing_sem = (
        db.query(SemesterResult)
        .filter(
            SemesterResult.student_id == student.id,
            SemesterResult.semester_id == semester.id,
        )
        .first()
    )
    if existing_sem and row.get("sgpa", "").strip() and existing_sem.sgpa is not None:
        errors.append("Semester result already exists for this student and semester.")
    return errors


def _validate_backlog(
    db: Session, institution_id: uuid.UUID, row: dict[str, str]
) -> list[str]:
    status = _normalize_backlog_status(row.get("status", ""))
    if status != BACKLOG_STATUS_NOT_CLEARED:
        return ["Backlog status must be NOT_CLEARED."]
    student = student_by_roll(db, institution_id, row["student_roll_number"])
    course = course_by_code(db, institution_id, row["course_code"])
    semester = semester_for_year(
        db,
        institution_id,
        row["original_academic_year"],
        row["original_semester_number"],
    )
    enrollment_for(db, institution_id, student, course, semester)
    existing = (
        db.query(CourseBacklog)
        .filter(
            CourseBacklog.institution_id == institution_id,
            CourseBacklog.student_id == student.id,
            CourseBacklog.course_id == course.id,
            CourseBacklog.original_semester_id == semester.id,
        )
        .first()
    )
    if existing:
        return ["Backlog record already exists for this student, course, and semester."]
    return []


def _validate_backlog_clearance(
    db: Session, institution_id: uuid.UUID, row: dict[str, str]
) -> list[str]:
    status = row.get("status", "").strip().upper()
    if status not in ("CLEARED", "PASS", "PASSED"):
        return ["Clearance status must be CLEARED."]
    student = student_by_roll(db, institution_id, row["student_roll_number"])
    course = course_by_code(db, institution_id, row["course_code"])
    semester = semester_for_year(
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
            CourseBacklog.original_semester_id == semester.id,
        )
        .first()
    )
    if not backlog:
        return ["Backlog record not found."]
    if backlog.status == BACKLOG_STATUS_CLEARED:
        return ["Backlog already cleared."]
    if row.get("clearance_academic_year", "").strip() and row.get(
        "clearance_semester_number", ""
    ).strip():
        try:
            semester_for_year(
                db,
                institution_id,
                row["clearance_academic_year"],
                row["clearance_semester_number"],
            )
        except ImportResolveError as exc:
            return [str(exc)]
    if row.get("clearance_date", "").strip():
        try:
            parse_date_field(row["clearance_date"], "clearance_date")
        except ImportResolveError as exc:
            return [str(exc)]
    return []


def _normalize_attendance_status(value: str) -> str | None:
    raw = value.strip().lower()
    if raw in ("present", "p"):
        return "present"
    if raw in ("absent", "a"):
        return "absent"
    return None


def _normalize_backlog_status(value: str) -> str:
    raw = value.strip().upper()
    if raw in ("NOT_CLEARED", "FAIL", "FAILED", "ACTIVE", "UNCLEARED"):
        return BACKLOG_STATUS_NOT_CLEARED
    if raw in ("CLEARED", "PASS", "PASSED"):
        return BACKLOG_STATUS_CLEARED
    return raw


def _parse_float(value: str, field: str) -> float | None:
    try:
        return float(value.strip())
    except (ValueError, AttributeError):
        return None


def _default_assessment_type(import_type: str, value: str | None) -> str:
    if value and value.strip():
        return value.strip().upper()
    return {
        "ca_marks": "CA",
        "mid_term_marks": "MID",
        "end_sem_marks": "FINAL",
    }[import_type]


def _default_assessment_name(import_type: str, value: str | None) -> str:
    if value and value.strip():
        return value.strip()
    return {
        "ca_marks": "Continuous Assessment",
        "mid_term_marks": "Mid-Term Exam",
        "end_sem_marks": "End-Term Exam",
    }[import_type]


def _find_assessment(
    db: Session,
    institution_id: uuid.UUID,
    course_id: uuid.UUID,
    atype: str,
    name: str,
) -> Assessment | None:
    return (
        db.query(Assessment)
        .filter(
            Assessment.institution_id == institution_id,
            Assessment.course_id == course_id,
            Assessment.assessment_type == atype,
            Assessment.name == name,
        )
        .first()
    )
