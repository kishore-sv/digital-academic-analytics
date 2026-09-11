"""Prepare ML feature vectors from academic data."""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment, SemesterResult
from app.models.student import Student


def build_features_from_enrollment(
    db: Session, enrollment_id: uuid.UUID, institution_id: uuid.UUID
) -> dict[str, Any]:
    """Build combined feature dict from an enrollment record."""
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.id == enrollment_id,
            Enrollment.institution_id == institution_id,
        )
        .first()
    )
    if not enrollment:
        raise ValueError("Enrollment not found")

    student = enrollment.student
    course = enrollment.course

    ca_mark = 0.0
    mid_mark = 0.0
    for mark in enrollment.assessment_marks:
        atype = mark.assessment.assessment_type.upper()
        if atype == "CA":
            ca_mark = mark.marks_obtained
        elif atype == "MID":
            mid_mark = mark.marks_obtained

    semester_result = (
        db.query(SemesterResult)
        .filter(
            SemesterResult.student_id == student.id,
            SemesterResult.semester_id == enrollment.semester_id,
            SemesterResult.institution_id == institution_id,
        )
        .first()
    )

    prev_sgpa = semester_result.sgpa if semester_result else 0.0
    prev_cgpa = semester_result.cgpa if semester_result else 0.0
    backlog = semester_result.backlog_count if semester_result else 0
    failed = semester_result.current_failed_courses if semester_result else 0
    low_perf = semester_result.low_performance_course_count if semester_result else 0
    trend = semester_result.performance_trend if semester_result else "STABLE"

    attendance = enrollment.attendance_percentage or 0.0
    study_hours = enrollment.study_hours_per_week or 0.0
    assignment_pct = enrollment.assignment_completion_pct or 0.0

    return {
        "CA_mark": ca_mark,
        "MID_mark": mid_mark,
        "attendance_percentage": attendance,
        "study_hours_per_week": study_hours,
        "assignment_completion_pct": assignment_pct,
        "assignment_completion_percentage": assignment_pct,
        "previous_sgpa": prev_sgpa or 0.0,
        "previous_cgpa": prev_cgpa or 0.0,
        "backlog_count": backlog,
        "course_credits": course.credits,
        "course_type": course.course_type,
        "branch": student.branch,
        "semester": student.semester,
        "current_failed_courses": failed,
        "low_performance_course_count": low_perf,
        "performance_trend": trend,
    }


def build_features_from_student(
    db: Session, student_id: uuid.UUID, institution_id: uuid.UUID
) -> dict[str, Any]:
    """Build features from student's latest enrollment."""
    student = (
        db.query(Student)
        .filter(Student.id == student_id, Student.institution_id == institution_id)
        .first()
    )
    if not student:
        raise ValueError("Student not found")

    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student_id,
            Enrollment.institution_id == institution_id,
        )
        .order_by(Enrollment.created_at.desc())
        .first()
    )
    if enrollment:
        return build_features_from_enrollment(db, enrollment.id, institution_id)

    semester_result = (
        db.query(SemesterResult)
        .filter(
            SemesterResult.student_id == student_id,
            SemesterResult.institution_id == institution_id,
        )
        .order_by(SemesterResult.created_at.desc())
        .first()
    )

    return {
        "CA_mark": 0.0,
        "MID_mark": 0.0,
        "attendance_percentage": 0.0,
        "study_hours_per_week": 0.0,
        "assignment_completion_pct": 0.0,
        "assignment_completion_percentage": 0.0,
        "previous_sgpa": semester_result.sgpa if semester_result else 0.0,
        "previous_cgpa": semester_result.cgpa if semester_result else 0.0,
        "backlog_count": semester_result.backlog_count if semester_result else 0,
        "course_credits": 3,
        "course_type": "THEORY",
        "branch": student.branch,
        "semester": student.semester,
        "current_failed_courses": semester_result.current_failed_courses if semester_result else 0,
        "low_performance_course_count": semester_result.low_performance_course_count if semester_result else 0,
        "performance_trend": semester_result.performance_trend if semester_result else "STABLE",
    }
