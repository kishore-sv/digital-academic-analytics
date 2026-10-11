"""Post-seed consistency checks for the full Demo University dataset."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.seed_large_dataset import CURRENT_ATTENDANCE_END, CURRENT_ATTENDANCE_START
from app.models.batch import Batch
from app.models.class_group import ClassGroup
from app.models.course_backlog import (
    BACKLOG_STATUS_CLEARED,
    BACKLOG_STATUS_NOT_CLEARED,
    CourseBacklog,
)
from app.models.department import Department
from app.models.enrollment import (
    Assessment,
    AssessmentMark,
    Attendance,
    CourseResult,
    Enrollment,
    SemesterResult,
)
from app.models.faculty_course import FacultyCourse
from app.models.parent import ParentStudent
from app.models.program import Program
from app.models.section import Section
from app.models.semester import Semester
from app.models.student import Student
from app.models.academic_year import AcademicYear

FULL_DATASET_DEPARTMENTS = 5
FULL_DATASET_STUDENTS = 2400
FULL_DATASET_BRANCH_CODES = ("CSE", "ECE", "EEE", "ME", "CE")
STUDENTS_PER_BRANCH = 480


def validate_large_dataset(db: Session, institution_id: uuid.UUID) -> dict[str, int]:
    """Raise AssertionError when the full dataset is internally inconsistent."""
    inst = institution_id

    def count(model) -> int:
        return db.query(model).filter(model.institution_id == inst).count()

    departments = count(Department)
    programs = count(Program)
    batches = count(Batch)
    classes = count(ClassGroup)
    sections = count(Section)
    students = count(Student)
    assert departments == FULL_DATASET_DEPARTMENTS, departments
    assert programs == FULL_DATASET_DEPARTMENTS, programs
    assert batches == 20, batches
    assert classes == 20, classes
    assert sections == 40, sections
    assert students == FULL_DATASET_STUDENTS, students

    by_dept = dict(
        db.query(Department.code, func.count(Student.id))
        .join(Student, Student.department_id == Department.id)
        .filter(Student.institution_id == inst)
        .group_by(Department.code)
        .all()
    )
    for code in FULL_DATASET_BRANCH_CODES:
        assert by_dept.get(code) == STUDENTS_PER_BRANCH, (code, by_dept.get(code))

    current_year = (
        db.query(AcademicYear)
        .filter(AcademicYear.institution_id == inst, AcademicYear.name == "2026-27")
        .one()
    )
    assert current_year.is_current is True
    old_current = (
        db.query(AcademicYear)
        .filter(
            AcademicYear.institution_id == inst,
            AcademicYear.name != "2026-27",
            AcademicYear.is_current.is_(True),
        )
        .count()
    )
    assert old_current == 0

    year_counts = dict(
        db.query(ClassGroup.year_number, func.count(Student.id))
        .join(Student, Student.class_group_id == ClassGroup.id)
        .filter(Student.institution_id == inst)
        .group_by(ClassGroup.year_number)
        .all()
    )
    for year in (1, 2, 3, 4):
        assert year_counts.get(year) == 600, (year, year_counts.get(year))

    section_sizes = (
        db.query(func.count(Student.id))
        .filter(Student.institution_id == inst)
        .group_by(Student.section_id)
        .all()
    )
    assert len(section_sizes) == 40
    assert all(size == 60 for (size,) in section_sizes)

    current_sem_counts = dict(
        db.query(Semester.number, func.count(Student.id))
        .join(Student, Student.current_semester_id == Semester.id)
        .filter(
            Student.institution_id == inst,
            Semester.academic_year_id == current_year.id,
        )
        .group_by(Semester.number)
        .all()
    )
    for number in (1, 3, 5, 7):
        assert current_sem_counts.get(number) == 600, (number, current_sem_counts)

    current_sem_ids = [
        row[0]
        for row in db.query(Semester.id)
        .filter(
            Semester.institution_id == inst,
            Semester.academic_year_id == current_year.id,
            Semester.number.in_((1, 3, 5, 7)),
        )
        .all()
    ]
    att_bounds = (
        db.query(func.min(Attendance.date), func.max(Attendance.date))
        .join(Enrollment, Attendance.enrollment_id == Enrollment.id)
        .filter(Enrollment.semester_id.in_(current_sem_ids))
        .one()
    )
    assert att_bounds[0] == CURRENT_ATTENDANCE_START, att_bounds
    assert att_bounds[1] == CURRENT_ATTENDANCE_END, att_bounds

    future = (
        db.query(Attendance)
        .join(Enrollment, Attendance.enrollment_id == Enrollment.id)
        .filter(
            Enrollment.semester_id.in_(current_sem_ids),
            Attendance.date > date(2026, 10, 7),
        )
        .count()
    )
    assert future == 0

    mid_or_final = (
        db.query(AssessmentMark)
        .join(Assessment, AssessmentMark.assessment_id == Assessment.id)
        .join(Enrollment, AssessmentMark.enrollment_id == Enrollment.id)
        .filter(
            Enrollment.semester_id.in_(current_sem_ids),
            Assessment.assessment_type.in_(("MID", "FINAL")),
        )
        .count()
    )
    assert mid_or_final == 0, mid_or_final

    current_ca = (
        db.query(AssessmentMark)
        .join(Assessment, AssessmentMark.assessment_id == Assessment.id)
        .join(Enrollment, AssessmentMark.enrollment_id == Enrollment.id)
        .filter(
            Enrollment.semester_id.in_(current_sem_ids),
            Assessment.assessment_type == "CA",
        )
        .count()
    )
    current_enrollments = (
        db.query(Enrollment).filter(Enrollment.semester_id.in_(current_sem_ids)).count()
    )
    assert current_ca == current_enrollments > 0

    current_results = (
        db.query(SemesterResult)
        .filter(
            SemesterResult.institution_id == inst,
            SemesterResult.semester_id.in_(current_sem_ids),
            SemesterResult.sgpa.isnot(None),
        )
        .count()
    )
    assert current_results == 0

    historical_results = (
        db.query(SemesterResult)
        .filter(
            SemesterResult.institution_id == inst,
            SemesterResult.semester_id.notin_(current_sem_ids),
            SemesterResult.sgpa.isnot(None),
        )
        .count()
    )
    assert historical_results > 0

    historical_courses = (
        db.query(CourseResult).filter(CourseResult.institution_id == inst).count()
    )
    assert historical_courses > 0

    uncleared = (
        db.query(CourseBacklog)
        .filter(
            CourseBacklog.institution_id == inst,
            CourseBacklog.status == BACKLOG_STATUS_NOT_CLEARED,
        )
        .count()
    )
    cleared = (
        db.query(CourseBacklog)
        .filter(
            CourseBacklog.institution_id == inst,
            CourseBacklog.status == BACKLOG_STATUS_CLEARED,
        )
        .count()
    )
    assert uncleared > 0, uncleared
    assert cleared > 0, cleared

    # Cleared backlogs still have a FAIL course result on the original enrollment.
    sample = (
        db.query(CourseBacklog)
        .filter(
            CourseBacklog.institution_id == inst,
            CourseBacklog.status == BACKLOG_STATUS_CLEARED,
        )
        .first()
    )
    assert sample is not None
    failed = (
        db.query(CourseResult)
        .join(Enrollment, CourseResult.enrollment_id == Enrollment.id)
        .filter(
            Enrollment.student_id == sample.student_id,
            Enrollment.course_id == sample.course_id,
            Enrollment.semester_id == sample.original_semester_id,
            CourseResult.status == "FAIL",
        )
        .count()
    )
    assert failed == 1

    assert count(FacultyCourse) > 0
    parent_links = db.query(ParentStudent).join(Student, ParentStudent.student_id == Student.id).filter(
        Student.institution_id == inst
    ).count()
    assert parent_links == 2400

    sample_enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.semester_id.in_(current_sem_ids))
        .first()
    )
    assert sample_enrollment is not None
    rows = (
        db.query(Attendance)
        .filter(Attendance.enrollment_id == sample_enrollment.id)
        .all()
    )
    present = sum(1 for row in rows if row.status == "present")
    expected = round(100.0 * present / len(rows), 1)
    assert sample_enrollment.attendance_percentage == expected

    summary = {
        "departments": departments,
        "programs": programs,
        "batches": batches,
        "classes": classes,
        "sections": sections,
        "students": students,
        "enrollments": count(Enrollment),
        "attendance": count(Attendance),
        "assessments": count(Assessment),
        "assessment_marks": count(AssessmentMark),
        "course_results": historical_courses,
        "semester_results": count(SemesterResult),
        "backlogs_uncleared": uncleared,
        "backlogs_cleared": cleared,
        "faculty_courses": count(FacultyCourse),
        "parent_links": parent_links,
        "current_ca": current_ca,
    }
    print("Seed validation passed.")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    return summary
