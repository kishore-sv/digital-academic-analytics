"""Shared academic API response builders."""

from app.models.semester import Semester
from app.models.student import Student
from app.schemas.academic import SemesterResponse, StudentResponse
from app.utils.academic_display import format_year_number


def semester_response(semester: Semester) -> SemesterResponse:
    return SemesterResponse(
        id=str(semester.id),
        academic_year_id=str(semester.academic_year_id),
        number=semester.number,
        name=semester.name,
        year_number=semester.year_number,
        year_label=format_year_number(semester.year_number),
    )


def student_response(student: Student) -> StudentResponse:
    sem = student.current_semester
    section = student.section
    batch = student.batch
    return StudentResponse(
        id=str(student.id),
        roll_number=student.roll_number,
        name=student.name,
        department_id=str(student.department_id),
        program_id=str(student.program_id),
        batch_id=str(student.batch_id),
        class_group_id=str(student.class_group_id),
        section_id=str(student.section_id),
        current_semester_id=str(student.current_semester_id),
        admission_date=student.admission_date,
        semester_number=sem.number if sem else None,
        year_number=sem.year_number if sem else None,
        year_label=format_year_number(sem.year_number) if sem else None,
        section_code=section.code if section else None,
        batch_name=batch.name if batch else None,
    )
