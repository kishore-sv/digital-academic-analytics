"""Small tenant slice used by pytest. Not the 2,400-student dataset."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy.orm import Session

from app.core.seed_data import (
    ADMIN_2_EMAIL,
    ADMIN_2_PASSWORD,
    INSTITUTION_2_NAME,
    STUDENT_2_NAME,
    STUDENT_2_ROLL,
    STUDENT_PASSWORD,
)
from app.core.seed_large_dataset import MINIMAL_SPEC, seed_demo_university
from app.core.security import hash_password
from app.models.academic_year import AcademicYear
from app.models.batch import Batch
from app.models.class_group import ClassGroup
from app.models.department import Department
from app.models.institution import Institution
from app.models.program import Program
from app.models.section import Section
from app.models.semester import Semester
from app.models.student import Student
from app.models.user import User
from app.utils.academic_display import semester_year_number


def seed_minimal(db: Session) -> None:
    """Demo University (CSE slice) plus a second institution for tenant tests."""
    seed_demo_university(db, MINIMAL_SPEC)
    _seed_institution_2(db)


def _seed_institution_2(db: Session) -> None:
    institution = Institution(
        name=INSTITUTION_2_NAME,
        description="Second tenant for isolation tests.",
    )
    db.add(institution)
    db.flush()
    iid = institution.id
    db.add(
        User(
            institution_id=iid,
            email=ADMIN_2_EMAIL,
            password_hash=hash_password(ADMIN_2_PASSWORD),
            role="institution_admin",
            is_login_enabled=True,
        )
    )
    dept = Department(
        institution_id=iid,
        code="ECE",
        name="Electronics and Communication Engineering",
    )
    db.add(dept)
    db.flush()
    program = Program(
        institution_id=iid,
        department_id=dept.id,
        name="B.Tech Electronics and Communication Engineering",
        code="BTECH-ECE",
        duration_semesters=8,
    )
    db.add(program)
    db.flush()
    year = AcademicYear(institution_id=iid, name="2026-27", is_current=True)
    db.add(year)
    db.flush()
    semester = Semester(
        institution_id=iid,
        academic_year_id=year.id,
        number=1,
        name="Semester 1",
        year_number=semester_year_number(1),
    )
    db.add(semester)
    db.flush()
    batch = Batch(
        institution_id=iid,
        program_id=program.id,
        admission_year=2026,
        code="2026",
        name="Batch 2026",
        is_active=True,
    )
    db.add(batch)
    db.flush()
    class_group = ClassGroup(
        institution_id=iid,
        batch_id=batch.id,
        year_number=1,
        code="Y1",
        name="ECE 2026 - 1st Year",
    )
    db.add(class_group)
    db.flush()
    section = Section(
        institution_id=iid,
        class_group_id=class_group.id,
        code="A",
        name="Section A",
        is_active=True,
    )
    db.add(section)
    db.flush()
    user = User(
        institution_id=iid,
        email="riverside.student@riverside.edu",
        password_hash=hash_password(STUDENT_PASSWORD),
        role="student",
        is_login_enabled=True,
    )
    db.add(user)
    db.flush()
    db.add(
        Student(
            id=uuid.uuid4(),
            institution_id=iid,
            user_id=user.id,
            roll_number=STUDENT_2_ROLL,
            name=STUDENT_2_NAME,
            department_id=dept.id,
            program_id=program.id,
            batch_id=batch.id,
            class_group_id=class_group.id,
            section_id=section.id,
            current_semester_id=semester.id,
            admission_date=date(2026, 8, 1),
        )
    )
    db.flush()
