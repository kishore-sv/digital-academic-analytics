"""Seed Demo University with CSE, ECE, and IST branches (60 students each, 4 semesters)."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from app.core.security import hash_password
from app.core.seed_data import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    INSTITUTION_1_NAME,
    STUDENT_ROLLS,
)
from app.models.academic_year import AcademicYear
from app.models.course import Course
from app.models.department import Department
from app.models.enrollment import (
    Assessment,
    AssessmentMark,
    Enrollment,
)
from app.models.faculty import Faculty
from app.models.faculty_course import FacultyCourse
from app.models.institution import Institution
from app.models.parent import FacultyStudent, Parent, ParentStudent
from app.models.program import Program
from app.models.semester import Semester
from app.models.student import Student
from app.models.user import User
from app.services.result_calculation_service import (
    recalculate_course_result,
    recalculate_semester_result,
)

THEORY_ASSESSMENTS = [
    ("CA-1", "CA", 20),
    ("CA-2", "CA", 20),
    ("CA-3", "CA", 20),
    ("Mid-Term", "MID", 30),
    ("End-Term", "FINAL", 50),
]
LAB_ASSESSMENTS = [
    ("CA", "CA", 25),
    ("Practical/Internal", "MID", 25),
    ("Final", "FINAL", 50),
]

CourseSpec = tuple[str, str, int, str]
SemesterCourses = dict[int, list[CourseSpec]]


@dataclass
class BranchConfig:
    code: str
    name: str
    program_name: str
    roll_prefix: str
    sections: tuple[str, str]
    courses: SemesterCourses
    faculty: list[tuple[str, str, list[str]]] = field(default_factory=list)


BRANCH_CONFIGS: list[BranchConfig] = [
    BranchConfig(
        code="CSE",
        name="Computer Science & Engineering",
        program_name="B.Tech CSE",
        roll_prefix="20231CSE",
        sections=("CSE-A", "CSE-B"),
        courses={
            1: [
                ("CSE101", "Engineering Mathematics I", 4, "THEORY"),
                ("CSE102", "Engineering Physics", 3, "THEORY"),
                ("CSE103", "Engineering Chemistry", 3, "THEORY"),
                ("CSE104", "Programming Fundamentals", 4, "THEORY"),
                ("CSE105", "Engineering Graphics", 2, "LAB"),
                ("CSE106", "Communication Skills", 2, "THEORY"),
            ],
            2: [
                ("CSE201", "Engineering Mathematics II", 4, "THEORY"),
                ("CSE202", "Data Structures", 4, "THEORY"),
                ("CSE203", "Digital Logic", 3, "THEORY"),
                ("CSE204", "Object Oriented Programming", 4, "THEORY"),
                ("CSE205", "Environmental Studies", 2, "THEORY"),
                ("CSE206", "Discrete Mathematics", 3, "THEORY"),
            ],
            3: [
                ("CSE301", "Database Management Systems", 4, "THEORY"),
                ("CSE302", "Operating Systems", 4, "THEORY"),
                ("CSE303", "Computer Networks", 3, "THEORY"),
                ("CSE304", "Design and Analysis of Algorithms", 4, "THEORY"),
                ("CSE305", "Computer Organization", 3, "THEORY"),
                ("CSE306", "Professional Elective I", 3, "THEORY"),
            ],
            4: [
                ("CSE401", "Software Engineering", 4, "THEORY"),
                ("CSE402", "Theory of Computation", 3, "THEORY"),
                ("CSE403", "Web Technologies", 3, "THEORY"),
                ("CSE404", "Microprocessors", 3, "THEORY"),
                ("CSE405", "Probability and Statistics", 3, "THEORY"),
                ("CSE406", "Professional Elective II", 3, "THEORY"),
            ],
        },
        faculty=[
            ("faculty.cse1@demo.com", "Dr. Priya Nair", ["CSE202", "CSE302"]),
            ("faculty.cse2@demo.com", "Dr. Ravi Kumar", ["CSE301", "CSE303"]),
            ("faculty.cse3@demo.com", "Dr. Meera Patel", ["CSE401", "CSE403"]),
        ],
    ),
    BranchConfig(
        code="ECE",
        name="Electronics & Communication Engineering",
        program_name="B.Tech ECE",
        roll_prefix="20231ECE",
        sections=("ECE-A", "ECE-B"),
        courses={
            1: [
                ("ECE101", "Engineering Mathematics I", 4, "THEORY"),
                ("ECE102", "Engineering Physics", 3, "THEORY"),
                ("ECE103", "Basic Electronics", 4, "THEORY"),
                ("ECE104", "Circuit Theory", 3, "THEORY"),
                ("ECE105", "Electronic Devices Lab", 2, "LAB"),
                ("ECE106", "Communication Skills", 2, "THEORY"),
            ],
            2: [
                ("ECE201", "Engineering Mathematics II", 4, "THEORY"),
                ("ECE202", "Analog Electronics", 4, "THEORY"),
                ("ECE203", "Digital Electronics", 3, "THEORY"),
                ("ECE204", "Signals and Systems", 4, "THEORY"),
                ("ECE205", "Electromagnetic Theory", 3, "THEORY"),
                ("ECE206", "Electronic Circuits Lab", 2, "LAB"),
            ],
            3: [
                ("ECE301", "Microprocessors & Microcontrollers", 4, "THEORY"),
                ("ECE302", "Communication Systems", 4, "THEORY"),
                ("ECE303", "Digital Signal Processing", 3, "THEORY"),
                ("ECE304", "Control Systems", 4, "THEORY"),
                ("ECE305", "VLSI Design", 3, "THEORY"),
                ("ECE306", "Professional Elective I", 3, "THEORY"),
            ],
            4: [
                ("ECE401", "Wireless Communication", 4, "THEORY"),
                ("ECE402", "Embedded Systems", 3, "THEORY"),
                ("ECE403", "Optical Communication", 3, "THEORY"),
                ("ECE404", "Antenna Theory", 3, "THEORY"),
                ("ECE405", "Satellite Communication", 3, "THEORY"),
                ("ECE406", "Professional Elective II", 3, "THEORY"),
            ],
        },
        faculty=[
            ("faculty.ece1@demo.com", "Dr. Suresh Reddy", ["ECE202", "ECE302"]),
            ("faculty.ece2@demo.com", "Dr. Lakshmi Iyer", ["ECE301", "ECE303"]),
            ("faculty.ece3@demo.com", "Dr. Arjun Menon", ["ECE401", "ECE402"]),
        ],
    ),
    BranchConfig(
        code="IST",
        name="Information Science & Technology",
        program_name="B.Tech IST",
        roll_prefix="20231IST",
        sections=("IST-A", "IST-B"),
        courses={
            1: [
                ("IST101", "Engineering Mathematics I", 4, "THEORY"),
                ("IST102", "Engineering Physics", 3, "THEORY"),
                ("IST103", "IT Fundamentals", 3, "THEORY"),
                ("IST104", "Programming in C", 4, "THEORY"),
                ("IST105", "Computer Applications Lab", 2, "LAB"),
                ("IST106", "Communication Skills", 2, "THEORY"),
            ],
            2: [
                ("IST201", "Engineering Mathematics II", 4, "THEORY"),
                ("IST202", "Data Structures", 4, "THEORY"),
                ("IST203", "Digital Systems", 3, "THEORY"),
                ("IST204", "Object Oriented Programming", 4, "THEORY"),
                ("IST205", "Web Design Basics", 3, "THEORY"),
                ("IST206", "Database Fundamentals", 3, "THEORY"),
            ],
            3: [
                ("IST301", "Database Management Systems", 4, "THEORY"),
                ("IST302", "Computer Networks", 4, "THEORY"),
                ("IST303", "Software Engineering", 3, "THEORY"),
                ("IST304", "Operating Systems", 4, "THEORY"),
                ("IST305", "Information Security", 3, "THEORY"),
                ("IST306", "Professional Elective I", 3, "THEORY"),
            ],
            4: [
                ("IST401", "Cloud Computing", 4, "THEORY"),
                ("IST402", "Big Data Analytics", 3, "THEORY"),
                ("IST403", "Mobile Application Development", 3, "THEORY"),
                ("IST404", "Machine Learning Basics", 3, "THEORY"),
                ("IST405", "IT Project Management", 3, "THEORY"),
                ("IST406", "Professional Elective II", 3, "THEORY"),
            ],
        },
        faculty=[
            ("faculty.ist1@demo.com", "Dr. Ananya Sharma", ["IST202", "IST302"]),
            ("faculty.ist2@demo.com", "Dr. Karthik Rao", ["IST301", "IST303"]),
            ("faculty.ist3@demo.com", "Dr. Divya Nambiar", ["IST401", "IST404"]),
        ],
    ),
]

STUDENTS_PER_BRANCH = 60


def _create_user(db, institution_id, email, password, role):
    user = User(
        institution_id=institution_id,
        email=email,
        password_hash=hash_password(password),
        role=role,
        is_login_enabled=True,
    )
    db.add(user)
    db.flush()
    return user


def _ensure_course_assessments(db, institution_id, course: Course):
    if db.query(Assessment).filter(Assessment.course_id == course.id).first():
        return
    specs = LAB_ASSESSMENTS if course.course_type == "LAB" else THEORY_ASSESSMENTS
    for name, atype, max_m in specs:
        db.add(
            Assessment(
                institution_id=institution_id,
                course_id=course.id,
                name=name,
                assessment_type=atype,
                max_marks=float(max_m),
            )
        )
    db.flush()


def _student_profile(idx: int, rng: random.Random) -> dict:
    if idx <= 10:
        return {"base": rng.uniform(8.0, 9.2), "att": rng.uniform(85, 98), "trend": "STABLE"}
    if idx <= 25:
        return {"base": rng.uniform(6.5, 7.8), "att": rng.uniform(70, 88), "trend": "STABLE"}
    if idx <= 35:
        return {"base": rng.uniform(4.5, 5.8), "att": rng.uniform(45, 65), "trend": "DECLINING"}
    if idx <= 45:
        return {"base": rng.uniform(5.5, 7.0), "att": rng.uniform(60, 80), "trend": "IMPROVING"}
    if idx <= 52:
        return {"base": rng.uniform(7.5, 8.5), "att": rng.uniform(55, 70), "trend": "STABLE"}
    return {"base": rng.uniform(5.0, 6.5), "att": rng.uniform(75, 92), "trend": "DECLINING"}


def _seed_branch(
    db,
    institution_id,
    branch: BranchConfig,
    semesters: dict[int, Semester],
    rng: random.Random,
    parent: Parent | None = None,
) -> list[Faculty]:
    dept = Department(
        institution_id=institution_id,
        name=branch.name,
        code=branch.code,
    )
    db.add(dept)
    db.flush()

    program = Program(
        institution_id=institution_id,
        department_id=dept.id,
        name=branch.program_name,
        code=f"BTECH-{branch.code}",
        duration_semesters=8,
    )
    db.add(program)
    db.flush()

    course_by_code: dict[str, Course] = {}
    for sem_num, courses in branch.courses.items():
        for code, name, credits, ctype in courses:
            course = Course(
                institution_id=institution_id,
                department_id=dept.id,
                name=name,
                code=code,
                credits=credits,
                course_type=ctype,
            )
            db.add(course)
            db.flush()
            _ensure_course_assessments(db, institution_id, course)
            course_by_code[code] = course

    faculty_list: list[Faculty] = []
    for email, fname, course_codes in branch.faculty:
        fu = _create_user(db, institution_id, email, "faculty123", "faculty")
        fac = Faculty(
            institution_id=institution_id,
            user_id=fu.id,
            name=fname,
            department_id=dept.id,
        )
        db.add(fac)
        db.flush()
        faculty_list.append(fac)
        for code in course_codes:
            course = course_by_code.get(code)
            if course:
                for sem_num in range(1, 5):
                    db.add(
                        FacultyCourse(
                            institution_id=institution_id,
                            faculty_id=fac.id,
                            course_id=course.id,
                            semester_id=semesters[sem_num].id,
                        )
                    )
    db.flush()

    section_a, section_b = branch.sections
    named_rolls = {idx + 1: (roll, name) for idx, (roll, name) in enumerate(STUDENT_ROLLS)} if branch.code == "CSE" else {}

    for i in range(1, STUDENTS_PER_BRANCH + 1):
        if i in named_rolls:
            roll, student_name = named_rolls[i]
        else:
            roll = f"{branch.roll_prefix}{i:04d}"
            student_name = f"{branch.code} Student {i:03d}"
        section = section_a if i <= 30 else section_b
        profile = _student_profile(i, rng)
        user = _create_user(db, institution_id, None, "student123", "student")
        student = Student(
            institution_id=institution_id,
            user_id=user.id,
            roll_number=roll,
            name=student_name,
            department_id=dept.id,
            program_id=program.id,
            semester=4,
            branch=branch.code,
            section=section,
        )
        db.add(student)
        db.flush()

        fac = faculty_list[i % len(faculty_list)]
        db.add(FacultyStudent(faculty_id=fac.id, student_id=student.id))

        if parent and branch.code == "CSE" and i == 1:
            db.add(ParentStudent(parent_id=parent.id, student_id=student.id))

        for sem_num in range(1, 5):
            sem = semesters[sem_num]
            if profile["trend"] == "IMPROVING":
                sem_cgpa = profile["base"] - 0.4 * (4 - sem_num)
            elif profile["trend"] == "DECLINING" and i > 35:
                sem_cgpa = profile["base"] + 0.3 * (4 - sem_num)
            else:
                sem_cgpa = profile["base"] + rng.uniform(-0.2, 0.2)

            for code, _, _, _ in branch.courses[sem_num]:
                course = course_by_code[code]
                att = max(35, min(100, profile["att"] + rng.uniform(-8, 8)))
                end_marks = max(28, min(98, sem_cgpa * 10 + rng.uniform(-12, 12)))
                if profile["att"] < 60 and rng.random() < 0.3:
                    end_marks = rng.uniform(30, 39)

                enrollment = Enrollment(
                    institution_id=institution_id,
                    student_id=student.id,
                    course_id=course.id,
                    semester_id=sem.id,
                    attendance_percentage=round(att, 1),
                    study_hours_per_week=round(rng.uniform(5, 28), 1),
                    assignment_completion_pct=round(rng.uniform(50, 100), 1),
                )
                db.add(enrollment)
                db.flush()

                assessments = (
                    db.query(Assessment)
                    .filter(Assessment.course_id == course.id)
                    .all()
                )
                for a in assessments:
                    pct = end_marks / 100
                    mark = round(a.max_marks * pct + rng.uniform(-2, 2), 1)
                    mark = max(0, min(a.max_marks, mark))
                    db.add(
                        AssessmentMark(
                            institution_id=institution_id,
                            enrollment_id=enrollment.id,
                            assessment_id=a.id,
                            marks_obtained=mark,
                        )
                    )
                db.flush()
                recalculate_course_result(db, enrollment)

            recalculate_semester_result(db, student.id, sem.id, institution_id)

    return faculty_list


def seed_cse_demo(db) -> Institution:
    """Seed CSE, ECE, and IST branches (60 students each)."""
    rng = random.Random(649)
    institution = Institution(name=INSTITUTION_1_NAME)
    db.add(institution)
    db.flush()

    _create_user(db, institution.id, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")

    ay = AcademicYear(
        institution_id=institution.id, name="2023-24", is_current=True
    )
    db.add(ay)
    db.flush()

    semesters: dict[int, Semester] = {}
    for num in range(1, 5):
        sem = Semester(
            institution_id=institution.id,
            academic_year_id=ay.id,
            number=num,
            name=f"Semester {num}",
        )
        db.add(sem)
        db.flush()
        semesters[num] = sem

    parent_user = _create_user(db, institution.id, "parent@demo.com", "parent123", "parent")
    parent = Parent(
        institution_id=institution.id,
        user_id=parent_user.id,
        name="Rajesh Kamble",
    )
    db.add(parent)
    db.flush()

    # Legacy faculty login for integration tests
    from app.core.seed_data import FACULTY_EMAIL

    legacy_fu = _create_user(db, institution.id, FACULTY_EMAIL, "faculty123", "faculty")

    for branch in BRANCH_CONFIGS:
        faculty_list = _seed_branch(db, institution.id, branch, semesters, rng, parent)
        if branch.code == "CSE" and faculty_list:
            # Link legacy faculty@demo.com to first CSE faculty profile's students
            cse_dept = (
                db.query(Department)
                .filter(
                    Department.institution_id == institution.id,
                    Department.code == "CSE",
                )
                .first()
            )
            if cse_dept:
                legacy_fac = Faculty(
                    institution_id=institution.id,
                    user_id=legacy_fu.id,
                    name="Dr. Ananya Sharma (Legacy)",
                    department_id=cse_dept.id,
                )
                db.add(legacy_fac)
                db.flush()
                cse_students = (
                    db.query(Student)
                    .filter(
                        Student.institution_id == institution.id,
                        Student.branch == "CSE",
                    )
                    .limit(10)
                    .all()
                )
                for s in cse_students:
                    db.add(FacultyStudent(faculty_id=legacy_fac.id, student_id=s.id))

    db.flush()
    return institution
