"""Keep semester_results.backlog_count aligned with course_backlogs."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models.course_backlog import BACKLOG_STATUS_NOT_CLEARED, CourseBacklog
from app.models.enrollment import SemesterResult
from app.models.student import Student


def sync_student_backlog_counts(
    db: Session, institution_id: uuid.UUID, student_id: uuid.UUID
) -> None:
    """Update current-semester SemesterResult backlog fields from course_backlogs."""
    uncleared = (
        db.query(CourseBacklog)
        .filter(
            CourseBacklog.institution_id == institution_id,
            CourseBacklog.student_id == student_id,
            CourseBacklog.status == BACKLOG_STATUS_NOT_CLEARED,
        )
        .count()
    )
    student = (
        db.query(Student)
        .filter(
            Student.id == student_id,
            Student.institution_id == institution_id,
        )
        .first()
    )
    if not student:
        return
    semester_id = student.current_semester_id
    sr = (
        db.query(SemesterResult)
        .filter(
            SemesterResult.institution_id == institution_id,
            SemesterResult.student_id == student_id,
            SemesterResult.semester_id == semester_id,
        )
        .first()
    )
    if sr:
        sr.backlog_count = uncleared
        sr.current_failed_courses = uncleared
    else:
        db.add(
            SemesterResult(
                institution_id=institution_id,
                student_id=student_id,
                semester_id=semester_id,
                sgpa=None,
                cgpa=None,
                backlog_count=uncleared,
                current_failed_courses=uncleared,
                low_performance_course_count=0,
                performance_trend="STABLE",
            )
        )
