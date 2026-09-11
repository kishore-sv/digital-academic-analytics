"""Course and semester result calculation from assessment marks."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.enrollment import (
    Assessment,
    AssessmentMark,
    CourseResult,
    Enrollment,
    SemesterResult,
)
from app.models.semester import Semester
from app.models.student import Student

# Grade point mapping (10-point scale)
GRADE_POINTS: dict[str, float] = {
    "O": 10.0,
    "A+": 9.0,
    "A": 8.0,
    "B+": 7.0,
    "B": 6.0,
    "C": 5.0,
    "D": 4.0,
    "F": 0.0,
}

# Assessment weight by type for total marks calculation
ASSESSMENT_WEIGHTS: dict[str, float] = {
    "CA": 0.20,
    "ASSIGNMENT": 0.10,
    "MID": 0.30,
    "FINAL": 0.40,
}

PASS_THRESHOLD = 40.0
LOW_PERFORMANCE_THRESHOLD = 50.0


def marks_to_grade(marks: float) -> str:
    if marks >= 90:
        return "O"
    if marks >= 80:
        return "A+"
    if marks >= 70:
        return "A"
    if marks >= 60:
        return "B+"
    if marks >= 50:
        return "B"
    if marks >= 45:
        return "C"
    if marks >= 40:
        return "D"
    return "F"


def grade_to_point(grade: str) -> float:
    return GRADE_POINTS.get(grade, 0.0)


def compute_weighted_total(
    marks_by_type: dict[str, float],
    assessments: list[Assessment],
) -> float | None:
    """Compute weighted total from available assessment marks."""
    if not marks_by_type:
        return None

    total_weight = 0.0
    weighted_sum = 0.0
    for assessment in assessments:
        atype = assessment.assessment_type.upper()
        if atype not in marks_by_type:
            continue
        weight = ASSESSMENT_WEIGHTS.get(atype, 0.0)
        if weight <= 0:
            continue
        # Normalize mark to percentage of max_marks
        pct = (marks_by_type[atype] / assessment.max_marks) * 100 if assessment.max_marks else 0
        weighted_sum += pct * weight
        total_weight += weight

    if total_weight == 0:
        # Fallback: simple average of available marks
        values = list(marks_by_type.values())
        return sum(values) / len(values) if values else None

    return round(weighted_sum / total_weight * (total_weight / sum(ASSESSMENT_WEIGHTS.values())), 1)


def recalculate_course_result(db: Session, enrollment: Enrollment) -> CourseResult | None:
    """Recalculate and upsert course result for an enrollment."""
    assessments = (
        db.query(Assessment)
        .filter(Assessment.course_id == enrollment.course_id)
        .all()
    )
    marks = (
        db.query(AssessmentMark)
        .filter(AssessmentMark.enrollment_id == enrollment.id)
        .all()
    )
    marks_by_type: dict[str, float] = {}
    for mark in marks:
        atype = mark.assessment.assessment_type.upper()
        marks_by_type[atype] = mark.marks_obtained

    total = compute_weighted_total(marks_by_type, assessments)
    if total is None:
        return enrollment.course_result

    grade = marks_to_grade(total)
    status = "PASS" if total >= PASS_THRESHOLD else "FAIL"

    if enrollment.course_result:
        cr = enrollment.course_result
        cr.end_marks = total
        cr.grade = grade
        cr.status = status
    else:
        cr = CourseResult(
            institution_id=enrollment.institution_id,
            enrollment_id=enrollment.id,
            end_marks=total,
            grade=grade,
            status=status,
        )
        db.add(cr)
    return cr


def recalculate_semester_result(
    db: Session,
    student_id: uuid.UUID,
    semester_id: uuid.UUID,
    institution_id: uuid.UUID,
) -> SemesterResult:
    """Recalculate SGPA, CGPA, backlogs for a student in a semester."""
    enrollments = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student_id,
            Enrollment.semester_id == semester_id,
            Enrollment.institution_id == institution_id,
        )
        .all()
    )

    total_credits = 0
    weighted_points = 0.0
    failed_count = 0
    low_perf_count = 0
    course_marks: list[float] = []

    for enrollment in enrollments:
        cr = enrollment.course_result
        course: Course = enrollment.course
        if not cr or cr.end_marks is None:
            continue
        credits = course.credits
        gp = grade_to_point(cr.grade or "F")
        total_credits += credits
        weighted_points += gp * credits
        course_marks.append(cr.end_marks)
        if cr.status == "FAIL":
            failed_count += 1
        elif cr.end_marks < LOW_PERFORMANCE_THRESHOLD:
            low_perf_count += 1

    sgpa = round(weighted_points / total_credits, 2) if total_credits > 0 else None

    # CGPA across all semesters up to and including this one
    semester = db.query(Semester).filter(Semester.id == semester_id).first()
    all_semester_results = (
        db.query(SemesterResult)
        .join(Semester, SemesterResult.semester_id == Semester.id)
        .filter(
            SemesterResult.student_id == student_id,
            SemesterResult.institution_id == institution_id,
        )
        .order_by(Semester.number)
        .all()
    )

    # Compute cumulative CGPA from all course results up to this semester number
    if semester:
        all_enrollments = (
            db.query(Enrollment)
            .join(Semester, Enrollment.semester_id == Semester.id)
            .filter(
                Enrollment.student_id == student_id,
                Enrollment.institution_id == institution_id,
                Semester.number <= semester.number,
            )
            .all()
        )
        cum_credits = 0
        cum_points = 0.0
        total_backlogs = 0
        for enr in all_enrollments:
            cr = enr.course_result
            if not cr or cr.end_marks is None:
                continue
            cum_credits += enr.course.credits
            cum_points += grade_to_point(cr.grade or "F") * enr.course.credits
            if cr.status == "FAIL":
                total_backlogs += 1
        cgpa = round(cum_points / cum_credits, 2) if cum_credits > 0 else None
    else:
        cgpa = sgpa
        total_backlogs = failed_count

    # Performance trend from previous semester SGPA
    trend = "STABLE"
    if semester and sgpa is not None:
        prev_sr = (
            db.query(SemesterResult)
            .join(Semester, SemesterResult.semester_id == Semester.id)
            .filter(
                SemesterResult.student_id == student_id,
                SemesterResult.institution_id == institution_id,
                Semester.number < semester.number,
            )
            .order_by(Semester.number.desc())
            .first()
        )
        if prev_sr and prev_sr.sgpa is not None:
            diff = sgpa - prev_sr.sgpa
            if diff > 0.15:
                trend = "IMPROVING"
            elif diff < -0.15:
                trend = "DECLINING"

    existing = (
        db.query(SemesterResult)
        .filter(
            SemesterResult.student_id == student_id,
            SemesterResult.semester_id == semester_id,
            SemesterResult.institution_id == institution_id,
        )
        .first()
    )
    if existing:
        sr = existing
        sr.sgpa = sgpa
        sr.cgpa = cgpa
        sr.backlog_count = total_backlogs if semester else failed_count
        sr.current_failed_courses = failed_count
        sr.low_performance_course_count = low_perf_count
        sr.performance_trend = trend
    else:
        sr = SemesterResult(
            institution_id=institution_id,
            student_id=student_id,
            semester_id=semester_id,
            sgpa=sgpa,
            cgpa=cgpa,
            backlog_count=total_backlogs if semester else failed_count,
            current_failed_courses=failed_count,
            low_performance_course_count=low_perf_count,
            performance_trend=trend,
        )
        db.add(sr)

    # Update student current semester
    student = db.query(Student).filter(Student.id == student_id).first()
    if student and semester and semester.number > student.semester:
        student.semester = semester.number

    return sr


def recalculate_after_marks_save(
    db: Session,
    enrollment_ids: list[uuid.UUID],
    institution_id: uuid.UUID,
) -> None:
    """Recalculate course and semester results for affected enrollments."""
    seen_semesters: set[tuple[uuid.UUID, uuid.UUID]] = set()
    for enrollment_id in enrollment_ids:
        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.id == enrollment_id,
                Enrollment.institution_id == institution_id,
            )
            .first()
        )
        if not enrollment:
            continue
        recalculate_course_result(db, enrollment)
        seen_semesters.add((enrollment.student_id, enrollment.semester_id))

    for student_id, semester_id in seen_semesters:
        recalculate_semester_result(db, student_id, semester_id, institution_id)
