"""Cross-entity academic structure validation."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.academic_constants import COURSE_TYPES, PARENT_RELATIONSHIP_TYPES
from app.core.tenant import get_tenant_entity
from app.models.batch import Batch
from app.models.class_group import ClassGroup
from app.models.course import Course
from app.models.department import Department
from app.models.enrollment import Enrollment
from app.models.faculty import Faculty
from app.models.faculty_course import FacultyCourse
from app.models.parent import Parent, ParentStudent
from app.models.program import Program
from app.models.section import Section
from app.models.semester import Semester
from app.models.student import Student


def _ensure(entity, detail: str):
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def validate_program_belongs_to_department(
    db: Session, program_id: uuid.UUID, department_id: uuid.UUID, institution_id: uuid.UUID
) -> Program:
    program = get_tenant_entity(db, Program, program_id, institution_id)
    _ensure(program, "Program not found")
    if program.department_id != department_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Program does not belong to the selected department",
        )
    return program


def validate_batch_belongs_to_program(
    db: Session, batch_id: uuid.UUID, program_id: uuid.UUID, institution_id: uuid.UUID
) -> Batch:
    batch = get_tenant_entity(db, Batch, batch_id, institution_id)
    _ensure(batch, "Batch not found")
    if batch.program_id != program_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Batch does not belong to the selected program",
        )
    return batch


def validate_class_group_belongs_to_batch(
    db: Session, class_group_id: uuid.UUID, batch_id: uuid.UUID, institution_id: uuid.UUID
) -> ClassGroup:
    cg = get_tenant_entity(db, ClassGroup, class_group_id, institution_id)
    _ensure(cg, "Class group not found")
    if cg.batch_id != batch_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class group does not belong to the selected batch",
        )
    return cg


def validate_section_belongs_to_class_group(
    db: Session, section_id: uuid.UUID, class_group_id: uuid.UUID, institution_id: uuid.UUID
) -> Section:
    section = get_tenant_entity(db, Section, section_id, institution_id)
    _ensure(section, "Section not found")
    if section.class_group_id != class_group_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Section does not belong to the selected class group",
        )
    return section


def validate_course_type(course_type: str) -> str:
    normalized = course_type.upper()
    if normalized not in COURSE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"course_type must be one of: {', '.join(sorted(COURSE_TYPES))}",
        )
    return normalized


def validate_relationship_type(relationship_type: str) -> str:
    normalized = relationship_type.upper()
    if normalized not in PARENT_RELATIONSHIP_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"relationship_type must be one of: {', '.join(sorted(PARENT_RELATIONSHIP_TYPES))}",
        )
    return normalized


def validate_student_academic_graph(
    db: Session,
    institution_id: uuid.UUID,
    *,
    department_id: uuid.UUID,
    program_id: uuid.UUID,
    batch_id: uuid.UUID,
    class_group_id: uuid.UUID,
    section_id: uuid.UUID,
    current_semester_id: uuid.UUID,
) -> None:
    get_tenant_entity(db, Department, department_id, institution_id) or _ensure(
        None, "Department not found"
    )
    validate_program_belongs_to_department(db, program_id, department_id, institution_id)
    validate_batch_belongs_to_program(db, batch_id, program_id, institution_id)
    validate_class_group_belongs_to_batch(db, class_group_id, batch_id, institution_id)
    validate_section_belongs_to_class_group(db, section_id, class_group_id, institution_id)
    semester = get_tenant_entity(db, Semester, current_semester_id, institution_id)
    _ensure(semester, "Semester not found")


def validate_enrollment(
    db: Session,
    institution_id: uuid.UUID,
    *,
    student_id: uuid.UUID,
    course_id: uuid.UUID,
    semester_id: uuid.UUID,
    section_id: uuid.UUID | None = None,
) -> Student:
    student = get_tenant_entity(db, Student, student_id, institution_id)
    _ensure(student, "Student not found")
    get_tenant_entity(db, Course, course_id, institution_id) or _ensure(None, "Course not found")
    get_tenant_entity(db, Semester, semester_id, institution_id) or _ensure(
        None, "Semester not found"
    )
    if section_id is not None:
        section = get_tenant_entity(db, Section, section_id, institution_id)
        _ensure(section, "Section not found")
        if section.id != student.section_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Enrollment section must match student's section",
            )
    return student


def validate_faculty_course_assignment(
    db: Session,
    institution_id: uuid.UUID,
    *,
    faculty_id: uuid.UUID,
    course_id: uuid.UUID,
    semester_id: uuid.UUID,
    section_id: uuid.UUID | None = None,
    exclude_id: uuid.UUID | None = None,
) -> None:
    get_tenant_entity(db, Faculty, faculty_id, institution_id) or _ensure(None, "Faculty not found")
    get_tenant_entity(db, Course, course_id, institution_id) or _ensure(None, "Course not found")
    get_tenant_entity(db, Semester, semester_id, institution_id) or _ensure(
        None, "Semester not found"
    )
    if section_id is not None:
        get_tenant_entity(db, Section, section_id, institution_id) or _ensure(
            None, "Section not found"
        )

    query = db.query(FacultyCourse).filter(
        FacultyCourse.institution_id == institution_id,
        FacultyCourse.faculty_id == faculty_id,
        FacultyCourse.course_id == course_id,
        FacultyCourse.semester_id == semester_id,
    )
    if section_id is None:
        query = query.filter(FacultyCourse.section_id.is_(None))
    else:
        query = query.filter(FacultyCourse.section_id == section_id)
    if exclude_id:
        query = query.filter(FacultyCourse.id != exclude_id)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Faculty is already assigned to this course/semester/section",
        )


def validate_parent_student_link(
    db: Session,
    institution_id: uuid.UUID,
    parent_id: uuid.UUID,
    student_id: uuid.UUID,
) -> None:
    parent = get_tenant_entity(db, Parent, parent_id, institution_id)
    student = get_tenant_entity(db, Student, student_id, institution_id)
    _ensure(parent, "Parent not found")
    _ensure(student, "Student not found")


def assert_enrollment_unique(
    db: Session,
    institution_id: uuid.UUID,
    student_id: uuid.UUID,
    course_id: uuid.UUID,
    semester_id: uuid.UUID,
    exclude_id: uuid.UUID | None = None,
) -> None:
    query = db.query(Enrollment).filter(
        Enrollment.institution_id == institution_id,
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id,
        Enrollment.semester_id == semester_id,
    )
    if exclude_id:
        query = query.filter(Enrollment.id != exclude_id)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student is already enrolled in this course for the semester",
        )
