"""Shared helpers for seeding academic master data."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.models.academic_year import AcademicYear
from app.models.batch import Batch
from app.models.class_group import ClassGroup
from app.models.program import Program
from app.models.section import Section
from app.models.semester import Semester
from app.models.student import Student
from app.utils.academic_display import semester_year_number


@dataclass
class ProgramAcademicContext:
    """Cached batch/class/section structure for a program."""

    program: Program
    batches: dict[int, Batch] = field(default_factory=dict)
    class_groups: dict[tuple[int, int], ClassGroup] = field(default_factory=dict)
    sections: dict[tuple[int, int, str], Section] = field(default_factory=dict)


def create_academic_years(
    db: Session,
    institution_id: uuid.UUID,
    year_specs: list[tuple[str, bool]],
) -> list[AcademicYear]:
    years: list[AcademicYear] = []
    for name, is_current in year_specs:
        ay = AcademicYear(
            institution_id=institution_id,
            name=name,
            is_current=is_current,
        )
        db.add(ay)
        db.flush()
        years.append(ay)
    return years


def create_semesters_for_year(
    db: Session,
    institution_id: uuid.UUID,
    academic_year: AcademicYear,
    numbers: range | list[int] | None = None,
) -> dict[int, Semester]:
    nums = list(numbers or range(1, 9))
    by_number: dict[int, Semester] = {}
    for number in nums:
        sem = Semester(
            institution_id=institution_id,
            academic_year_id=academic_year.id,
            number=number,
            name=f"Semester {number}",
            year_number=semester_year_number(number),
        )
        db.add(sem)
        db.flush()
        by_number[number] = sem
    return by_number


def get_or_create_batch(
    db: Session,
    institution_id: uuid.UUID,
    program: Program,
    admission_year: int,
    ctx: ProgramAcademicContext | None = None,
) -> Batch:
    cache = ctx.batches if ctx else {}
    if admission_year in cache:
        return cache[admission_year]
    existing = (
        db.query(Batch)
        .filter(
            Batch.institution_id == institution_id,
            Batch.program_id == program.id,
            Batch.admission_year == admission_year,
        )
        .first()
    )
    if existing:
        if ctx is not None:
            ctx.batches[admission_year] = existing
        return existing
    batch = Batch(
        institution_id=institution_id,
        program_id=program.id,
        admission_year=admission_year,
        code=str(admission_year),
        name=f"Batch {admission_year}",
        is_active=True,
    )
    db.add(batch)
    db.flush()
    if ctx is not None:
        ctx.batches[admission_year] = batch
    return batch


def get_or_create_class_group(
    db: Session,
    institution_id: uuid.UUID,
    batch: Batch,
    year_number: int,
    ctx: ProgramAcademicContext | None = None,
) -> ClassGroup:
    key = (batch.admission_year, year_number)
    cache = ctx.class_groups if ctx else {}
    if key in cache:
        return cache[key]
    existing = (
        db.query(ClassGroup)
        .filter(
            ClassGroup.institution_id == institution_id,
            ClassGroup.batch_id == batch.id,
            ClassGroup.year_number == year_number,
        )
        .first()
    )
    if existing:
        if ctx is not None:
            ctx.class_groups[key] = existing
        return existing
    cg = ClassGroup(
        institution_id=institution_id,
        batch_id=batch.id,
        year_number=year_number,
        code=f"Y{year_number}",
        name=f"Year {year_number}",
    )
    db.add(cg)
    db.flush()
    if ctx is not None:
        ctx.class_groups[key] = cg
    return cg


def get_or_create_section(
    db: Session,
    institution_id: uuid.UUID,
    class_group: ClassGroup,
    code: str,
    ctx: ProgramAcademicContext | None = None,
) -> Section:
    key = (class_group.batch_id, class_group.year_number, code)
    cache = ctx.sections if ctx else {}
    if key in cache:
        return cache[key]
    existing = (
        db.query(Section)
        .filter(
            Section.institution_id == institution_id,
            Section.class_group_id == class_group.id,
            Section.code == code,
        )
        .first()
    )
    if existing:
        if ctx is not None:
            ctx.sections[key] = existing
        return existing
    section = Section(
        institution_id=institution_id,
        class_group_id=class_group.id,
        code=code,
        name=f"Section {code}",
        is_active=True,
    )
    db.add(section)
    db.flush()
    if ctx is not None:
        ctx.sections[key] = section
    return section


def admission_year_for_semester(semester_number: int, anchor_year: int = 2024) -> int:
    """Infer admission year from current semester number (2 semesters per year)."""
    year_of_study = semester_year_number(semester_number)
    return anchor_year - (year_of_study - 1)


def resolve_student_placement(
    db: Session,
    institution_id: uuid.UUID,
    program: Program,
    semester: Semester,
    section_code: str = "A",
    ctx: ProgramAcademicContext | None = None,
    admission_year: int | None = None,
) -> tuple[uuid.UUID, uuid.UUID, uuid.UUID, uuid.UUID]:
    """Return program_id, batch_id, class_group_id, section_id for a student."""
    year_number = semester.year_number
    adm_year = admission_year or admission_year_for_semester(semester.number)
    batch = get_or_create_batch(db, institution_id, program, adm_year, ctx)
    class_group = get_or_create_class_group(
        db, institution_id, batch, year_number, ctx
    )
    section = get_or_create_section(db, institution_id, class_group, section_code, ctx)
    return program.id, batch.id, class_group.id, section.id


def place_student(
    db: Session,
    student: Student,
    program: Program,
    semester: Semester,
    section_code: str = "A",
    ctx: ProgramAcademicContext | None = None,
    admission_year: int | None = None,
) -> None:
    """Assign batch, class group, section, and current semester on a student."""
    program_id, batch_id, class_group_id, section_id = resolve_student_placement(
        db,
        student.institution_id,
        program,
        semester,
        section_code=section_code,
        ctx=ctx,
        admission_year=admission_year,
    )
    student.program_id = program_id
    student.batch_id = batch_id
    student.class_group_id = class_group_id
    student.section_id = section_id
    student.current_semester_id = semester.id
    db.flush()


def create_placed_student(
    db: Session,
    institution_id: uuid.UUID,
    user,
    roll_number: str,
    name: str,
    department_id: uuid.UUID,
    program: Program,
    semester: Semester,
    section_code: str = "A",
    ctx: ProgramAcademicContext | None = None,
    admission_year: int | None = None,
) -> Student:
    """Create a student with full academic placement."""
    program_id, batch_id, class_group_id, section_id = resolve_student_placement(
        db,
        institution_id,
        program,
        semester,
        section_code=section_code,
        ctx=ctx,
        admission_year=admission_year,
    )
    student = Student(
        institution_id=institution_id,
        user_id=user.id,
        roll_number=roll_number,
        name=name,
        department_id=department_id,
        program_id=program_id,
        batch_id=batch_id,
        class_group_id=class_group_id,
        section_id=section_id,
        current_semester_id=semester.id,
    )
    db.add(student)
    db.flush()
    return student
