"""Deterministic Demo University dataset.

Full spec: 5 departments × 4 batches × 2 sections × 60 students = 2,400.
Historical semesters get CA, MID, and FINAL marks. Grades, SGPA, and CGPA
are produced with result_calculation_service (not a second grading table).
The current odd semester (2026-27) has attendance through 2026-10-07 and CA only.
"""

from __future__ import annotations

import random
import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from types import SimpleNamespace

from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.core.seed_catalog import (
    ACADEMIC_YEARS,
    BATCH_PLAN,
    CURRICULA,
    DEPARTMENTS,
    DESIGNATIONS,
    FACULTY_NAMES,
    FIRST_NAMES,
    LAST_NAMES,
)
from app.core.seed_catalog import program_for
from app.core.seed_data import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    FACULTY_EMAIL,
    FACULTY_PASSWORD,
    INSTITUTION_1_NAME,
    PARENT_EMAIL,
    PARENT_PASSWORD,
    PINNED_PROFILES,
    STUDENT_PASSWORD,
    STUDENT_ROLLS,
)
from app.core.security import hash_password
from app.models.academic_year import AcademicYear
from app.models.batch import Batch
from app.models.class_group import ClassGroup
from app.models.course import Course
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
from app.models.faculty import Faculty
from app.models.faculty_course import FacultyCourse
from app.models.institution import Institution
from app.models.parent import FacultyStudent, Parent, ParentStudent
from app.models.program import Program
from app.models.program_course import ProgramCourse
from app.models.section import Section
from app.models.semester import Semester
from app.models.student import Student
from app.models.user import User
from app.services.result_calculation_service import (
    LOW_PERFORMANCE_THRESHOLD,
    PASS_THRESHOLD,
    compute_weighted_total,
    grade_to_point,
    marks_to_grade,
)
from app.utils.academic_display import format_year_number, semester_year_number

CURRENT_AY = "2026-27"
CURRENT_ATTENDANCE_START = date(2026, 9, 16)
CURRENT_ATTENDANCE_END = date(2026, 10, 7)
SEED = 42
CHUNK = 4000

_WEIGHT_ASSESSMENTS = [
    SimpleNamespace(assessment_type="CA", max_marks=100.0),
    SimpleNamespace(assessment_type="MID", max_marks=100.0),
    SimpleNamespace(assessment_type="FINAL", max_marks=100.0),
]

# attendance rate, mark low, mark high, study hours, assignment pct
# Mark bands stay above the pass line unless a row is explicitly force-failed.
# Weighted CA/MID/FINAL total is about 0.9 × the mark, and pass is 40.
_PROFILES = {
    "high": (0.90, 78, 95, 18.0, 90.0),
    "average": (0.82, 58, 74, 12.0, 72.0),
    "low": (0.66, 50, 64, 8.0, 55.0),
    "at_risk": (0.48, 46, 58, 4.0, 38.0),
}

_PINNED_NAMES = dict(STUDENT_ROLLS)


@dataclass(frozen=True)
class SeedSpec:
    department_codes: tuple[str, ...] = tuple(code for code, _ in DEPARTMENTS)
    sections: tuple[str, ...] = ("A", "B")
    students_per_section: int = 60
    faculty_per_department: int = 10
    historical_class_days: int = 24


FULL_SPEC = SeedSpec()
MINIMAL_SPEC = SeedSpec(
    department_codes=("CSE",),
    sections=("A",),
    students_per_section=3,
    faculty_per_department=2,
    historical_class_days=12,
)


@dataclass
class _Enr:
    id: uuid.UUID
    student_id: uuid.UUID
    student_index: int
    roll: str
    profile: str
    course_id: uuid.UUID
    course_index: int
    credits: int
    semester_id: uuid.UUID
    semester_number: int
    is_current: bool
    force_fail: bool
    ca: float
    mid: float
    final: float


def _ay_name(start_year: int) -> str:
    return f"{start_year}-{str(start_year + 1)[-2:]}"


def _weekdays_between(start: date, end: date) -> list[date]:
    days: list[date] = []
    cursor = start
    while cursor <= end:
        if cursor.weekday() < 5:
            days.append(cursor)
        cursor += timedelta(days=1)
    return days


def _weekdays_from(start: date, count: int) -> list[date]:
    days: list[date] = []
    cursor = start
    while len(days) < count:
        if cursor.weekday() < 5:
            days.append(cursor)
        cursor += timedelta(days=1)
    return days


def _hist_start(admission_year: int, semester_number: int) -> date:
    ay = admission_year + (semester_number - 1) // 2
    if semester_number % 2 == 1:
        return date(ay, 8, 4)
    return date(ay + 1, 1, 6)


def _profile_name(index: int, roll: str) -> str:
    pinned = PINNED_PROFILES.get(roll)
    if pinned:
        return pinned
    bucket = index % 100
    if bucket < 20:
        return "high"
    if bucket < 75:
        return "average"
    if bucket < 90:
        return "low"
    return "at_risk"


def _student_name(index: int, roll: str) -> str:
    if roll in _PINNED_NAMES:
        return _PINNED_NAMES[roll]
    first = FIRST_NAMES[index % len(FIRST_NAMES)]
    last = LAST_NAMES[(index * 7) % len(LAST_NAMES)]
    return f"{first} {last}"


def _bulk(db: Session, model, rows: list[dict]) -> None:
    for offset in range(0, len(rows), CHUNK):
        db.execute(insert(model), rows[offset : offset + CHUNK])
    if rows:
        db.flush()


def _user_row(institution_id, email, password_hash, role) -> dict:
    return {
        "id": uuid.uuid4(),
        "institution_id": institution_id,
        "email": email,
        "password_hash": password_hash,
        "role": role,
        "is_login_enabled": True,
    }


def seed_demo_university(db: Session, spec: SeedSpec = FULL_SPEC) -> Institution:
    """Insert one internally consistent Demo University dataset. Caller commits."""
    rng = random.Random(SEED)
    institution = Institution(
        name=INSTITUTION_1_NAME,
        description="Deterministic engineering college dataset for local development.",
    )
    db.add(institution)
    db.flush()
    institution_id = institution.id

    admin_hash = hash_password(ADMIN_PASSWORD)
    faculty_hash = hash_password(FACULTY_PASSWORD)
    student_hash = hash_password(STUDENT_PASSWORD)
    parent_hash = hash_password(PARENT_PASSWORD)

    db.add(
        User(
            institution_id=institution_id,
            email=ADMIN_EMAIL,
            password_hash=admin_hash,
            role="institution_admin",
            is_login_enabled=True,
        )
    )
    db.flush()

    dept_by_code: dict[str, Department] = {}
    for code, name in DEPARTMENTS:
        if code not in spec.department_codes:
            continue
        dept = Department(
            institution_id=institution_id, code=code, name=name, description=name
        )
        db.add(dept)
        dept_by_code[code] = dept
    db.flush()

    program_by_code: dict[str, Program] = {}
    for code in spec.department_codes:
        pcode, pname = program_for(code)
        program = Program(
            institution_id=institution_id,
            department_id=dept_by_code[code].id,
            name=pname,
            code=pcode,
            duration_semesters=8,
        )
        db.add(program)
        program_by_code[code] = program
    db.flush()

    years: dict[str, AcademicYear] = {}
    for name, is_current in ACADEMIC_YEARS:
        ay = AcademicYear(
            institution_id=institution_id, name=name, is_current=is_current
        )
        db.add(ay)
        years[name] = ay
    db.flush()

    semesters: dict[tuple[str, int], Semester] = {}
    for name, ay in years.items():
        for number in range(1, 9):
            sem = Semester(
                institution_id=institution_id,
                academic_year_id=ay.id,
                number=number,
                name=f"Semester {number}",
                year_number=semester_year_number(number),
            )
            db.add(sem)
            semesters[(name, number)] = sem
    db.flush()

    course_by_code: dict[str, Course] = {}
    course_credits: dict[uuid.UUID, int] = {}
    for dept_code in spec.department_codes:
        for semester_courses in CURRICULA[dept_code]:
            for code, name, credits, ctype in semester_courses:
                course = Course(
                    institution_id=institution_id,
                    department_id=dept_by_code[dept_code].id,
                    code=code,
                    name=name,
                    credits=credits,
                    course_type=ctype,
                )
                db.add(course)
                course_by_code[code] = course
    db.flush()
    for course in course_by_code.values():
        course_credits[course.id] = course.credits

    for dept_code in spec.department_codes:
        program = program_by_code[dept_code]
        for sem_index, semester_courses in enumerate(CURRICULA[dept_code], start=1):
            for code, _name, _credits, _ctype in semester_courses:
                db.add(
                    ProgramCourse(
                        institution_id=institution_id,
                        program_id=program.id,
                        course_id=course_by_code[code].id,
                        semester_number=sem_index,
                    )
                )
    db.flush()

    # Assessments are course-level and shared by every enrollment.
    assessment_ids: dict[tuple[uuid.UUID, str], uuid.UUID] = {}
    assessment_rows: list[dict] = []
    for course in course_by_code.values():
        for atype, aname in (
            ("CA", "Continuous Assessment"),
            ("MID", "Mid-Term Exam"),
            ("FINAL", "End-Term Exam"),
        ):
            aid = uuid.uuid4()
            assessment_ids[(course.id, atype)] = aid
            assessment_rows.append(
                {
                    "id": aid,
                    "institution_id": institution_id,
                    "course_id": course.id,
                    "name": aname,
                    "assessment_type": atype,
                    "max_marks": 100.0,
                    "date": None,
                }
            )
    _bulk(db, Assessment, assessment_rows)

    # Batches, classes, sections — one class per batch (current year of study).
    section_of: dict[tuple[str, int, str], Section] = {}
    batch_of: dict[tuple[str, int], Batch] = {}
    for dept_code in spec.department_codes:
        program = program_by_code[dept_code]
        for admission, _current_sem, year_number in BATCH_PLAN:
            batch = Batch(
                institution_id=institution_id,
                program_id=program.id,
                admission_year=admission,
                code=str(admission),
                name=f"Batch {admission}",
                is_active=True,
            )
            db.add(batch)
            db.flush()
            batch_of[(dept_code, admission)] = batch
            class_group = ClassGroup(
                institution_id=institution_id,
                batch_id=batch.id,
                year_number=year_number,
                code=f"Y{year_number}",
                name=f"{dept_code} {admission} - {format_year_number(year_number)}",
            )
            db.add(class_group)
            db.flush()
            for section_code in spec.sections:
                section = Section(
                    institution_id=institution_id,
                    class_group_id=class_group.id,
                    code=section_code,
                    name=f"Section {section_code}",
                    is_active=True,
                )
                db.add(section)
                section_of[(dept_code, admission, section_code)] = section
    db.flush()

    faculty_by_dept: dict[str, list[Faculty]] = defaultdict(list)
    faculty_rows_users: list[dict] = []
    faculty_pending: list[tuple[dict, str]] = []
    name_cursor = 0
    for dept_code in spec.department_codes:
        for n in range(1, spec.faculty_per_department + 1):
            employee_id = f"FAC-{dept_code}-{n:02d}"
            if dept_code == "CSE" and n == 1:
                email = FACULTY_EMAIL
            else:
                email = f"faculty-{dept_code.lower()}-{n:02d}@demo.com"
            user = _user_row(institution_id, email, faculty_hash, "faculty")
            faculty_rows_users.append(user)
            faculty_pending.append(
                (
                    {
                        "id": uuid.uuid4(),
                        "institution_id": institution_id,
                        "user_id": user["id"],
                        "employee_id": employee_id,
                        "name": FACULTY_NAMES[name_cursor % len(FACULTY_NAMES)],
                        "department_id": dept_by_code[dept_code].id,
                        "designation": DESIGNATIONS[(n - 1) % len(DESIGNATIONS)],
                        "phone": f"98{name_cursor:08d}"[:10],
                    },
                    dept_code,
                )
            )
            name_cursor += 1
    _bulk(db, User, faculty_rows_users)
    _bulk(db, Faculty, [row for row, _dept in faculty_pending])
    for row, dept_code in faculty_pending:
        faculty_by_dept[dept_code].append(row["id"])  # type: ignore[arg-type]

    # Students, parents, and section placement.
    student_users: list[dict] = []
    parent_users: list[dict] = []
    student_rows: list[dict] = []
    parent_rows: list[dict] = []
    parent_links: list[dict] = []
    placed: list[dict] = []
    index = 0
    relationships = ("FATHER", "MOTHER", "GUARDIAN")
    for dept_code in spec.department_codes:
        program = program_by_code[dept_code]
        for admission, current_sem, _year in BATCH_PLAN:
            current_semester = semesters[(CURRENT_AY, current_sem)]
            batch = batch_of[(dept_code, admission)]
            for section_code in spec.sections:
                section = section_of[(dept_code, admission, section_code)]
                section_base = 1 if section_code == "A" else 61
                for offset in range(spec.students_per_section):
                    seq = section_base + offset
                    roll = f"{admission % 100:02d}{dept_code}{seq:03d}"
                    profile = _profile_name(index, roll)
                    user = _user_row(
                        institution_id,
                        f"{roll.lower()}@students.demo.edu",
                        student_hash,
                        "student",
                    )
                    student_users.append(user)
                    student_id = uuid.uuid4()
                    student_rows.append(
                        {
                            "id": student_id,
                            "institution_id": institution_id,
                            "user_id": user["id"],
                            "roll_number": roll,
                            "name": _student_name(index, roll),
                            "department_id": dept_by_code[dept_code].id,
                            "program_id": program.id,
                            "batch_id": batch.id,
                            "class_group_id": section.class_group_id,
                            "section_id": section.id,
                            "current_semester_id": current_semester.id,
                            "admission_date": date(admission, 8, 1),
                        }
                    )
                    if roll == "26CSE001":
                        parent_email = PARENT_EMAIL
                    else:
                        parent_email = f"p-{roll.lower()}@demo.edu"
                    parent_user = _user_row(
                        institution_id, parent_email, parent_hash, "parent"
                    )
                    parent_users.append(parent_user)
                    parent_id = uuid.uuid4()
                    last = _student_name(index, roll).split()[-1]
                    rel = relationships[index % 3]
                    prefix = {"FATHER": "Mr.", "MOTHER": "Mrs.", "GUARDIAN": "Mx."}[rel]
                    parent_rows.append(
                        {
                            "id": parent_id,
                            "institution_id": institution_id,
                            "user_id": parent_user["id"],
                            "name": f"{prefix} {last}",
                            "phone": f"97{index:08d}"[:10],
                        }
                    )
                    parent_links.append(
                        {
                            "parent_id": parent_id,
                            "student_id": student_id,
                            "relationship_type": rel,
                            "is_primary_guardian": True,
                        }
                    )
                    placed.append(
                        {
                            "id": student_id,
                            "index": index,
                            "roll": roll,
                            "profile": profile,
                            "dept": dept_code,
                            "admission": admission,
                            "current_sem": current_sem,
                            "section_id": section.id,
                            "section_code": section_code,
                        }
                    )
                    index += 1

    print(f"  inserting {len(student_rows)} students and parents...")
    _bulk(db, User, student_users)
    _bulk(db, User, parent_users)
    _bulk(db, Student, student_rows)
    _bulk(db, Parent, parent_rows)
    _bulk(db, ParentStudent, parent_links)

    mentor_links: list[dict] = []
    for student in placed:
        mentors = faculty_by_dept[student["dept"]]
        slot = 0 if student["section_code"] == "A" else 1
        mentor_links.append(
            {
                "faculty_id": mentors[slot % len(mentors)],
                "student_id": student["id"],
            }
        )
    _bulk(db, FacultyStudent, mentor_links)

    faculty_course_rows: list[dict] = []
    for dept_code in spec.department_codes:
        mentors = faculty_by_dept[dept_code]
        cursor_f = 0
        for admission, current_sem, _year in BATCH_PLAN:
            semester = semesters[(CURRENT_AY, current_sem)]
            for course_spec in CURRICULA[dept_code][current_sem - 1]:
                course = course_by_code[course_spec[0]]
                for section_code in spec.sections:
                    section = section_of[(dept_code, admission, section_code)]
                    faculty_course_rows.append(
                        {
                            "id": uuid.uuid4(),
                            "institution_id": institution_id,
                            "faculty_id": mentors[cursor_f % len(mentors)],
                            "course_id": course.id,
                            "semester_id": semester.id,
                            "section_id": section.id,
                        }
                    )
                    cursor_f += 1
    _bulk(db, FacultyCourse, faculty_course_rows)

    current_days = _weekdays_between(CURRENT_ATTENDANCE_START, CURRENT_ATTENDANCE_END)
    hist_cache: dict[tuple[int, int], list[date]] = {}

    def hist_days(admission: int, semester_number: int) -> list[date]:
        key = (admission, semester_number)
        if key not in hist_cache:
            hist_cache[key] = _weekdays_from(
                _hist_start(admission, semester_number), spec.historical_class_days
            )
        return hist_cache[key]

    enrollments: list[_Enr] = []
    enrollment_rows: list[dict] = []
    print("  building enrollments, attendance, and marks...")
    attendance_buf: list[dict] = []
    mark_buf: list[dict] = []

    def flush_streams() -> None:
        nonlocal enrollment_rows, attendance_buf, mark_buf
        if enrollment_rows:
            _bulk(db, Enrollment, enrollment_rows)
            enrollment_rows = []
        if attendance_buf:
            _bulk(db, Attendance, attendance_buf)
            attendance_buf = []
        if mark_buf:
            _bulk(db, AssessmentMark, mark_buf)
            mark_buf = []

    for student in placed:
        profile = student["profile"]
        rate, lo, hi, study, assignment = _PROFILES[profile]
        dept_code = student["dept"]
        admission = student["admission"]
        current_sem = student["current_sem"]
        for sem_num in range(1, current_sem + 1):
            ay = _ay_name(admission + (sem_num - 1) // 2)
            semester = semesters[(ay, sem_num)]
            is_current = sem_num == current_sem
            days = current_days if is_current else hist_days(admission, sem_num)
            courses = CURRICULA[dept_code][sem_num - 1]
            for course_index, spec_row in enumerate(courses):
                course = course_by_code[spec_row[0]]
                force_fail = _should_fail(student, sem_num, course_index, is_current)
                if force_fail:
                    ca = mid = final = 22.0
                else:
                    ca = float(rng.randint(lo, hi))
                    mid = float(rng.randint(lo, hi))
                    final = float(rng.randint(lo, hi))
                statuses = [
                    "present" if rng.random() < rate else "absent" for _ in days
                ]
                present = sum(1 for status in statuses if status == "present")
                pct = round(100.0 * present / len(statuses), 1) if statuses else 0.0
                enr_id = uuid.uuid4()
                enrollment_rows.append(
                    {
                        "id": enr_id,
                        "institution_id": institution_id,
                        "student_id": student["id"],
                        "course_id": course.id,
                        "semester_id": semester.id,
                        "section_id": student["section_id"],
                        "attendance_percentage": pct,
                        "study_hours_per_week": study,
                        "assignment_completion_pct": assignment,
                    }
                )
                enrollments.append(
                    _Enr(
                        id=enr_id,
                        student_id=student["id"],
                        student_index=student["index"],
                        roll=student["roll"],
                        profile=profile,
                        course_id=course.id,
                        course_index=course_index,
                        credits=course_credits[course.id],
                        semester_id=semester.id,
                        semester_number=sem_num,
                        is_current=is_current,
                        force_fail=force_fail,
                        ca=ca,
                        mid=mid,
                        final=final,
                    )
                )
                for day, status in zip(days, statuses, strict=True):
                    attendance_buf.append(
                        {
                            "id": uuid.uuid4(),
                            "institution_id": institution_id,
                            "enrollment_id": enr_id,
                            "date": day,
                            "status": status,
                        }
                    )
                mark_buf.append(
                    {
                        "id": uuid.uuid4(),
                        "institution_id": institution_id,
                        "enrollment_id": enr_id,
                        "assessment_id": assessment_ids[(course.id, "CA")],
                        "marks_obtained": ca,
                    }
                )
                if not is_current:
                    mark_buf.append(
                        {
                            "id": uuid.uuid4(),
                            "institution_id": institution_id,
                            "enrollment_id": enr_id,
                            "assessment_id": assessment_ids[(course.id, "MID")],
                            "marks_obtained": mid,
                        }
                    )
                    mark_buf.append(
                        {
                            "id": uuid.uuid4(),
                            "institution_id": institution_id,
                            "enrollment_id": enr_id,
                            "assessment_id": assessment_ids[(course.id, "FINAL")],
                            "marks_obtained": final,
                        }
                    )
                if len(attendance_buf) >= CHUNK or len(enrollment_rows) >= CHUNK:
                    flush_streams()
    flush_streams()

    print("  calculating historical results and backlogs...")
    _write_results_and_backlogs(db, institution_id, enrollments, semesters)
    db.flush()
    print(f"  Demo University ready ({index} students).")
    return institution


def _should_fail(student: dict, sem_num: int, course_index: int, is_current: bool) -> bool:
    if is_current:
        return False
    profile = student["profile"]
    index = student["index"]
    if profile == "at_risk" and sem_num == 2 and course_index == 0:
        return True
    if profile == "at_risk" and index % 5 == 0 and sem_num == 4 and course_index == 1:
        return True
    if profile == "low" and index % 2 == 0 and sem_num == 2 and course_index == 0:
        return True
    return False


def _write_results_and_backlogs(db, institution_id, enrollments: list[_Enr], semesters) -> None:
    historical = [row for row in enrollments if not row.is_current]
    course_rows: list[dict] = []
    fails: list[_Enr] = []
    for row in historical:
        total = compute_weighted_total(
            {"CA": row.ca, "MID": row.mid, "FINAL": row.final},
            _WEIGHT_ASSESSMENTS,
        )
        assert total is not None
        grade = marks_to_grade(total)
        status = "PASS" if total >= PASS_THRESHOLD else "FAIL"
        course_rows.append(
            {
                "id": uuid.uuid4(),
                "institution_id": institution_id,
                "enrollment_id": row.id,
                "grade": grade,
                "end_marks": total,
                "status": status,
            }
        )
        if status == "FAIL":
            fails.append(row)
    _bulk(db, CourseResult, course_rows)

    # Backlogs follow actual FAIL course results. Clear a subset in a later semester.
    backlog_rows: list[dict] = []
    # (student_id, original_sem_number, clearance_sem_number or None)
    backlog_events: list[tuple[uuid.UUID, int, int | None]] = []
    semester_for_student: dict[tuple[uuid.UUID, int], uuid.UUID] = {}
    historical_sems: set[tuple[uuid.UUID, int]] = set()
    for row in enrollments:
        semester_for_student[(row.student_id, row.semester_number)] = row.semester_id
        if not row.is_current:
            historical_sems.add((row.student_id, row.semester_number))

    for row in fails:
        clearance_sem = None
        later = row.semester_number + 2
        # Clear only in a completed semester the student already attended.
        if (row.student_id, later) in historical_sems and row.student_index % 5 < 2:
            clearance_sem = later
        if clearance_sem is not None:
            status = BACKLOG_STATUS_CLEARED
            clearance_id = semester_for_student[(row.student_id, clearance_sem)]
            clearance_date = date(2026, 1, 15) if clearance_sem % 2 == 0 else date(2025, 12, 10)
            grade = "B"
            attempt = 2
        else:
            status = BACKLOG_STATUS_NOT_CLEARED
            clearance_id = None
            clearance_date = None
            grade = None
            attempt = 1
        backlog_rows.append(
            {
                "id": uuid.uuid4(),
                "institution_id": institution_id,
                "student_id": row.student_id,
                "course_id": row.course_id,
                "original_semester_id": row.semester_id,
                "status": status,
                "attempt_number": attempt,
                "clearance_semester_id": clearance_id,
                "clearance_date": clearance_date,
                "grade": grade,
            }
        )
        backlog_events.append((row.student_id, row.semester_number, clearance_sem))
    _bulk(db, CourseBacklog, backlog_rows)

    by_student_sem: dict[tuple[uuid.UUID, int], list[_Enr]] = defaultdict(list)
    sem_id_of: dict[tuple[uuid.UUID, int], uuid.UUID] = {}
    for row in historical:
        by_student_sem[(row.student_id, row.semester_number)].append(row)
        sem_id_of[(row.student_id, row.semester_number)] = row.semester_id

    events_by_student: dict[uuid.UUID, list[tuple[int, int | None]]] = defaultdict(list)
    for student_id, origin, clearance in backlog_events:
        events_by_student[student_id].append((origin, clearance))

    semester_rows: list[dict] = []
    for student_id, sem_numbers in _grouped_students(by_student_sem):
        cum_credits = 0
        cum_points = 0.0
        prev_sgpa = None
        for sem_num in sem_numbers:
            rows = by_student_sem[(student_id, sem_num)]
            credits = 0
            points = 0.0
            failed = 0
            low = 0
            for row in rows:
                total = compute_weighted_total(
                    {"CA": row.ca, "MID": row.mid, "FINAL": row.final},
                    _WEIGHT_ASSESSMENTS,
                )
                assert total is not None
                grade = marks_to_grade(total)
                status = "PASS" if total >= PASS_THRESHOLD else "FAIL"
                credits += row.credits
                points += grade_to_point(grade) * row.credits
                if status == "FAIL":
                    failed += 1
                elif total < LOW_PERFORMANCE_THRESHOLD:
                    low += 1
            sgpa = round(points / credits, 2) if credits else None
            cum_credits += credits
            cum_points += points
            cgpa = round(cum_points / cum_credits, 2) if cum_credits else None
            if prev_sgpa is None or sgpa is None:
                trend = "STABLE"
            elif sgpa - prev_sgpa > 0.15:
                trend = "IMPROVING"
            elif sgpa - prev_sgpa < -0.15:
                trend = "DECLINING"
            else:
                trend = "STABLE"
            prev_sgpa = sgpa
            uncleared = 0
            for origin, clearance in events_by_student.get(student_id, []):
                if origin > sem_num:
                    continue
                if clearance is None or clearance > sem_num:
                    uncleared += 1
            semester_rows.append(
                {
                    "id": uuid.uuid4(),
                    "institution_id": institution_id,
                    "student_id": student_id,
                    "semester_id": sem_id_of[(student_id, sem_num)],
                    "sgpa": sgpa,
                    "cgpa": cgpa,
                    "backlog_count": uncleared,
                    "current_failed_courses": failed,
                    "low_performance_course_count": low,
                    "performance_trend": trend,
                }
            )
    _bulk(db, SemesterResult, semester_rows)
    del semesters


def _grouped_students(by_student_sem):
    students: dict[uuid.UUID, list[int]] = defaultdict(list)
    for student_id, sem_num in by_student_sem:
        students[student_id].append(sem_num)
    for student_id, numbers in students.items():
        yield student_id, sorted(set(numbers))
