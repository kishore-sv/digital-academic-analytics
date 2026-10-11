"""Resolve master-data references for operational imports."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy.orm import Session

from app.models.academic_year import AcademicYear
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.semester import Semester
from app.models.student import Student


class ImportResolveError(ValueError):
    pass


def student_by_roll(db: Session, institution_id: uuid.UUID, roll: str) -> Student:
    student = (
        db.query(Student)
        .filter(
            Student.institution_id == institution_id,
            Student.roll_number == roll.strip(),
        )
        .first()
    )
    if not student:
        raise ImportResolveError(f"Student {roll.strip()} not found.")
    return student


def course_by_code(db: Session, institution_id: uuid.UUID, code: str) -> Course:
    course = (
        db.query(Course)
        .filter(
            Course.institution_id == institution_id,
            Course.code == code.strip(),
        )
        .first()
    )
    if not course:
        raise ImportResolveError(f"Course {code.strip()} not found.")
    return course


def academic_year_by_name(db: Session, institution_id: uuid.UUID, name: str) -> AcademicYear:
    year = (
        db.query(AcademicYear)
        .filter(
            AcademicYear.institution_id == institution_id,
            AcademicYear.name == name.strip(),
        )
        .first()
    )
    if not year:
        raise ImportResolveError(f"Academic year {name.strip()} not found.")
    return year


def semester_for_year(
    db: Session, institution_id: uuid.UUID, year_name: str, semester_number: str | int
) -> Semester:
    year = academic_year_by_name(db, institution_id, year_name)
    number = int(semester_number)
    semester = (
        db.query(Semester)
        .filter(
            Semester.institution_id == institution_id,
            Semester.academic_year_id == year.id,
            Semester.number == number,
        )
        .first()
    )
    if not semester:
        raise ImportResolveError(
            f"Semester {number} not found for academic year {year_name.strip()}."
        )
    return semester


def enrollment_for(
    db: Session,
    institution_id: uuid.UUID,
    student: Student,
    course: Course,
    semester: Semester,
) -> Enrollment:
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.institution_id == institution_id,
            Enrollment.student_id == student.id,
            Enrollment.course_id == course.id,
            Enrollment.semester_id == semester.id,
        )
        .first()
    )
    if not enrollment:
        raise ImportResolveError(
            f"Student {student.roll_number} is not enrolled in {course.code} "
            f"for semester {semester.number}."
        )
    return enrollment


def parse_date_field(value: str, field: str) -> date:
    raw = value.strip()
    try:
        return date.fromisoformat(raw)
    except ValueError:
        raise ImportResolveError(f"Invalid date for {field}: {raw}.")
