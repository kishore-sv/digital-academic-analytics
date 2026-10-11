"""Persist validated master-data import rows."""

from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.academic_year import AcademicYear
from app.models.batch import Batch
from app.models.class_group import ClassGroup
from app.models.course import Course
from app.models.department import Department
from app.models.enrollment import Enrollment
from app.models.faculty import Faculty
from app.models.faculty_course import FacultyCourse
from app.models.parent import Parent, ParentStudent
from app.models.program import Program
from app.models.program_course import ProgramCourse
from app.models.section import Section
from app.models.semester import Semester
from app.models.student import Student
from app.models.user import User
from app.services.academic_validation_service import validate_student_academic_graph


def commit_master_import(
    db: Session,
    import_type: str,
    institution_id: uuid.UUID,
    valid_rows: list[tuple[int, dict[str, str]]],
    *,
    duplicate_mode: str,
) -> tuple[int, int]:
    created = 0
    failed = 0
    for _row_num, row in valid_rows:
        try:
            with db.begin_nested():
                ok = _commit_row(db, import_type, institution_id, row, duplicate_mode)
            if ok:
                created += 1
            else:
                failed += 1
        except Exception:
            failed += 1
    return created, failed


def _commit_row(
    db: Session,
    import_type: str,
    institution_id: uuid.UUID,
    row: dict[str, str],
    duplicate_mode: str,
) -> bool:
    match import_type:
        case "departments":
            return _commit_department(db, institution_id, row, duplicate_mode)
        case "programs":
            return _commit_program(db, institution_id, row, duplicate_mode)
        case "academic_years":
            return _commit_academic_year(db, institution_id, row, duplicate_mode)
        case "semesters":
            return _commit_semester(db, institution_id, row, duplicate_mode)
        case "courses":
            return _commit_course(db, institution_id, row, duplicate_mode)
        case "program_courses":
            return _commit_program_course(db, institution_id, row, duplicate_mode)
        case "batches":
            return _commit_batch(db, institution_id, row, duplicate_mode)
        case "class_groups":
            return _commit_class_group(db, institution_id, row, duplicate_mode)
        case "sections":
            return _commit_section(db, institution_id, row, duplicate_mode)
        case "faculty":
            return _commit_faculty(db, institution_id, row, duplicate_mode)
        case "students":
            return _commit_student(db, institution_id, row, duplicate_mode)
        case "parents":
            return _commit_parent(db, institution_id, row, duplicate_mode)
        case "enrollments":
            return _commit_enrollment(db, institution_id, row, duplicate_mode)
        case "faculty_courses":
            return _commit_faculty_course(db, institution_id, row, duplicate_mode)
    raise ValueError(f"Unsupported import type: {import_type}")


def _skip_if_exists(exists: bool, duplicate_mode: str) -> bool:
    if not exists:
        return False
    if duplicate_mode == "skip":
        return True
    raise ValueError("duplicate")


def _commit_department(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    code = row["code"].strip()
    exists = (
        db.query(Department)
        .filter(Department.institution_id == institution_id, Department.code == code)
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    db.add(
        Department(
            institution_id=institution_id,
            name=row["name"].strip(),
            code=code,
            description=row.get("description") or None,
        )
    )
    return True


def _commit_program(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    code = row["code"].strip()
    exists = (
        db.query(Program)
        .filter(Program.institution_id == institution_id, Program.code == code)
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    dept = _dept_by_code(db, institution_id, row["department_code"])
    duration = int(row.get("duration_semesters") or 8)
    db.add(
        Program(
            institution_id=institution_id,
            department_id=dept.id,
            name=row["name"].strip(),
            code=code,
            duration_semesters=duration,
        )
    )
    return True


def _commit_academic_year(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    name = row["name"].strip()
    exists = (
        db.query(AcademicYear)
        .filter(AcademicYear.institution_id == institution_id, AcademicYear.name == name)
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    is_current = _bool(row.get("is_current"))
    if is_current:
        for ay in (
            db.query(AcademicYear)
            .filter(AcademicYear.institution_id == institution_id)
            .all()
        ):
            ay.is_current = False
    db.add(
        AcademicYear(
            institution_id=institution_id,
            name=name,
            is_current=is_current,
        )
    )
    return True


def _commit_semester(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    year = _year_by_name(db, institution_id, row["academic_year_name"])
    number = int(row["number"])
    exists = (
        db.query(Semester)
        .filter(Semester.academic_year_id == year.id, Semester.number == number)
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    db.add(
        Semester(
            institution_id=institution_id,
            academic_year_id=year.id,
            number=number,
            name=row["name"].strip(),
            year_number=int(row["year_number"]),
        )
    )
    return True


def _commit_course(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    code = row["code"].strip()
    exists = (
        db.query(Course)
        .filter(Course.institution_id == institution_id, Course.code == code)
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    dept = _dept_by_code(db, institution_id, row["department_code"])
    course_type = row["course_type"].strip().upper()
    db.add(
        Course(
            institution_id=institution_id,
            department_id=dept.id,
            name=row["name"].strip(),
            code=code,
            credits=int(row["credits"]),
            course_type=course_type,
        )
    )
    return True


def _commit_program_course(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    program = _program_by_code(db, institution_id, row["program_code"])
    course = _course_by_code(db, institution_id, row["course_code"])
    exists = (
        db.query(ProgramCourse)
        .filter(
            ProgramCourse.program_id == program.id,
            ProgramCourse.course_id == course.id,
        )
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    db.add(
        ProgramCourse(
            institution_id=institution_id,
            program_id=program.id,
            course_id=course.id,
            semester_number=int(row["semester_number"]),
        )
    )
    return True


def _commit_batch(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    code = row["code"].strip()
    exists = (
        db.query(Batch)
        .filter(Batch.institution_id == institution_id, Batch.code == code)
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    program = _program_by_code(db, institution_id, row["program_code"])
    db.add(
        Batch(
            institution_id=institution_id,
            program_id=program.id,
            admission_year=int(row["admission_year"]),
            code=code,
            name=row["name"].strip(),
            is_active=_bool(row.get("is_active"), default=True),
        )
    )
    return True


def _commit_class_group(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    batch = _batch_by_code(db, institution_id, row["batch_code"])
    code = row["code"].strip()
    exists = (
        db.query(ClassGroup)
        .filter(ClassGroup.batch_id == batch.id, ClassGroup.code == code)
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    db.add(
        ClassGroup(
            institution_id=institution_id,
            batch_id=batch.id,
            year_number=int(row["year_number"]),
            code=code,
            name=row["name"].strip(),
        )
    )
    return True


def _commit_section(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    class_group = _class_by_code(
        db, institution_id, row["class_code"], row.get("batch_code")
    )
    code = row["code"].strip()
    exists = (
        db.query(Section)
        .filter(Section.class_group_id == class_group.id, Section.code == code)
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    db.add(
        Section(
            institution_id=institution_id,
            class_group_id=class_group.id,
            code=code,
            name=row["name"].strip(),
            is_active=_bool(row.get("is_active"), default=True),
        )
    )
    return True


def _commit_faculty(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    emp = row["employee_id"].strip()
    exists = (
        db.query(Faculty)
        .filter(Faculty.institution_id == institution_id, Faculty.employee_id == emp)
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    dept = _dept_by_code(db, institution_id, row["department_code"])
    email = row["email"].strip()
    user = User(
        institution_id=institution_id,
        email=email,
        password_hash=hash_password(row["password"]),
        role="faculty",
        is_login_enabled=True,
    )
    db.add(user)
    db.flush()
    db.add(
        Faculty(
            institution_id=institution_id,
            user_id=user.id,
            department_id=dept.id,
            name=row["name"].strip(),
            employee_id=emp,
            designation=row.get("designation") or None,
            phone=row.get("phone") or None,
        )
    )
    return True


def _commit_student(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    roll = row["roll_number"].strip()
    exists = (
        db.query(Student)
        .filter(Student.institution_id == institution_id, Student.roll_number == roll)
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    dept = _dept_by_code(db, institution_id, row["department_code"])
    program = _program_by_code(db, institution_id, row["program_code"])
    batch = _batch_by_code(db, institution_id, row["batch_code"])
    class_group = _class_by_code(db, institution_id, row["class_code"], row["batch_code"])
    section = _section_by_code(db, institution_id, row["section_code"], class_group)
    semester = _semester_by_year_and_number(
        db, institution_id, row["current_academic_year"], row["current_semester_number"]
    )
    validate_student_academic_graph(
        db,
        institution_id,
        department_id=dept.id,
        program_id=program.id,
        batch_id=batch.id,
        class_group_id=class_group.id,
        section_id=section.id,
        current_semester_id=semester.id,
    )
    user = User(
        institution_id=institution_id,
        email=None,
        password_hash=hash_password(row["password"]),
        role="student",
        is_login_enabled=True,
    )
    db.add(user)
    db.flush()
    admission = row.get("admission_date")
    admission_date = date.fromisoformat(admission) if admission else None
    db.add(
        Student(
            institution_id=institution_id,
            user_id=user.id,
            roll_number=roll,
            name=row["name"].strip(),
            department_id=dept.id,
            program_id=program.id,
            batch_id=batch.id,
            class_group_id=class_group.id,
            section_id=section.id,
            current_semester_id=semester.id,
            admission_date=admission_date,
        )
    )
    return True


def _commit_parent(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    email = row["email"].strip()
    exists = (
        db.query(User)
        .filter(User.institution_id == institution_id, User.email == email, User.role == "parent")
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    user = User(
        institution_id=institution_id,
        email=email,
        password_hash=hash_password(row["password"]),
        role="parent",
        is_login_enabled=True,
    )
    db.add(user)
    db.flush()
    parent = Parent(
        institution_id=institution_id,
        user_id=user.id,
        name=row["name"].strip(),
        phone=row.get("phone") or None,
    )
    db.add(parent)
    db.flush()
    roll = row.get("student_roll_number", "").strip()
    if roll:
        student = (
            db.query(Student)
            .filter(Student.institution_id == institution_id, Student.roll_number == roll)
            .first()
        )
        if student:
            db.add(
                ParentStudent(
                    parent_id=parent.id,
                    student_id=student.id,
                    relationship_type=row.get("relationship_type") or "GUARDIAN",
                    is_primary_guardian=True,
                )
            )
    return True


def _commit_enrollment(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    student = _student_by_roll(db, institution_id, row["student_roll_number"])
    course = _course_by_code(db, institution_id, row["course_code"])
    semester = _semester_by_year_and_number(
        db, institution_id, row["academic_year_name"], row["semester_number"]
    )
    exists = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student.id,
            Enrollment.course_id == course.id,
            Enrollment.semester_id == semester.id,
        )
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    db.add(
        Enrollment(
            institution_id=institution_id,
            student_id=student.id,
            course_id=course.id,
            semester_id=semester.id,
        )
    )
    return True


def _commit_faculty_course(
    db: Session, institution_id: uuid.UUID, row: dict[str, str], duplicate_mode: str
) -> bool:
    faculty = _faculty_by_employee(db, institution_id, row["employee_id"])
    course = _course_by_code(db, institution_id, row["course_code"])
    semester = _semester_by_year_and_number(
        db, institution_id, row["academic_year_name"], row["semester_number"]
    )
    section_id = None
    if row.get("section_code"):
        batch_code = row.get("batch_code")
        class_code = row.get("class_code")
        if class_code:
            cg = _class_by_code(db, institution_id, class_code, batch_code)
            section = _section_by_code(db, institution_id, row["section_code"], cg)
            section_id = section.id
    exists = (
        db.query(FacultyCourse)
        .filter(
            FacultyCourse.faculty_id == faculty.id,
            FacultyCourse.course_id == course.id,
            FacultyCourse.semester_id == semester.id,
            FacultyCourse.section_id == section_id,
        )
        .first()
    )
    if _skip_if_exists(bool(exists), duplicate_mode):
        return True
    db.add(
        FacultyCourse(
            institution_id=institution_id,
            faculty_id=faculty.id,
            course_id=course.id,
            semester_id=semester.id,
            section_id=section_id,
        )
    )
    return True


def _dept_by_code(db: Session, institution_id: uuid.UUID, code: str) -> Department:
    dept = (
        db.query(Department)
        .filter(
            Department.institution_id == institution_id,
            Department.code == code.strip(),
        )
        .first()
    )
    if not dept:
        raise ValueError(f"Department not found: {code}")
    return dept


def _program_by_code(db: Session, institution_id: uuid.UUID, code: str) -> Program:
    program = (
        db.query(Program)
        .filter(Program.institution_id == institution_id, Program.code == code.strip())
        .first()
    )
    if not program:
        raise ValueError(f"Program not found: {code}")
    return program


def _year_by_name(db: Session, institution_id: uuid.UUID, name: str) -> AcademicYear:
    year = (
        db.query(AcademicYear)
        .filter(AcademicYear.institution_id == institution_id, AcademicYear.name == name.strip())
        .first()
    )
    if not year:
        raise ValueError(f"Academic year not found: {name}")
    return year


def _course_by_code(db: Session, institution_id: uuid.UUID, code: str) -> Course:
    course = (
        db.query(Course)
        .filter(Course.institution_id == institution_id, Course.code == code.strip())
        .first()
    )
    if not course:
        raise ValueError(f"Course not found: {code}")
    return course


def _batch_by_code(db: Session, institution_id: uuid.UUID, code: str) -> Batch:
    batch = (
        db.query(Batch)
        .filter(Batch.institution_id == institution_id, Batch.code == code.strip())
        .first()
    )
    if not batch:
        raise ValueError(f"Batch not found: {code}")
    return batch


def _class_by_code(
    db: Session, institution_id: uuid.UUID, class_code: str, batch_code: str | None
) -> ClassGroup:
    q = db.query(ClassGroup).filter(
        ClassGroup.institution_id == institution_id,
        ClassGroup.code == class_code.strip(),
    )
    if batch_code:
        batch = _batch_by_code(db, institution_id, batch_code)
        q = q.filter(ClassGroup.batch_id == batch.id)
    cg = q.first()
    if not cg:
        raise ValueError(f"Class not found: {class_code}")
    return cg


def _section_by_code(
    db: Session, institution_id: uuid.UUID, section_code: str, class_group: ClassGroup
) -> Section:
    section = (
        db.query(Section)
        .filter(
            Section.institution_id == institution_id,
            Section.class_group_id == class_group.id,
            Section.code == section_code.strip(),
        )
        .first()
    )
    if not section:
        raise ValueError(f"Section not found: {section_code}")
    return section


def _semester_by_year_and_number(
    db: Session, institution_id: uuid.UUID, year_name: str, sem_number: str | int
) -> Semester:
    year = _year_by_name(db, institution_id, year_name)
    number = int(sem_number)
    semester = (
        db.query(Semester)
        .filter(Semester.academic_year_id == year.id, Semester.number == number)
        .first()
    )
    if not semester:
        raise ValueError(f"Semester not found: {year_name} #{number}")
    return semester


def _student_by_roll(db: Session, institution_id: uuid.UUID, roll: str) -> Student:
    student = (
        db.query(Student)
        .filter(
            Student.institution_id == institution_id,
            Student.roll_number == roll.strip(),
        )
        .first()
    )
    if not student:
        raise ValueError(f"Student not found: {roll}")
    return student


def _faculty_by_employee(db: Session, institution_id: uuid.UUID, employee_id: str) -> Faculty:
    faculty = (
        db.query(Faculty)
        .filter(
            Faculty.institution_id == institution_id,
            Faculty.employee_id == employee_id.strip(),
        )
        .first()
    )
    if not faculty:
        raise ValueError(f"Faculty not found: {employee_id}")
    return faculty


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None or str(value).strip() == "":
        return default
    return str(value).strip().lower() in ("1", "true", "yes", "y")
