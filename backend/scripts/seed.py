"""Seed database with institution academic data and ML predictions."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.core.seed_data import (
    ADMIN_2_EMAIL,
    ADMIN_2_PASSWORD,
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    FACULTY_EMAIL,
    FACULTY_PASSWORD,
    INSTITUTION_1_NAME,
    INSTITUTION_2_NAME,
    PARENT_EMAIL,
    PARENT_PASSWORD,
    STUDENT_2_ROLL,
    STUDENT_PASSWORD,
    STUDENT_ROLLS,
)
from app.core.security import hash_password
from app.models.academic_year import AcademicYear
from app.models.course import Course
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
from app.models.institution import Institution
from app.models.parent import FacultyStudent, Parent, ParentStudent
from app.models.prediction import PredictionResult
from app.models.program import Program
from app.models.semester import Semester
from app.models.student import Student
from app.models.user import User
from app.services.prediction_storage_service import seed_predictions_for_institution


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


def _create_student(db, institution_id, user, roll_number, name, dept_id, program_id, semester, branch):
    student = Student(
        institution_id=institution_id,
        user_id=user.id,
        roll_number=roll_number,
        name=name,
        department_id=dept_id,
        program_id=program_id,
        semester=semester,
        branch=branch,
    )
    db.add(student)
    db.flush()
    return student


def _create_course_enrollment(
    db,
    institution_id,
    student,
    course,
    semester,
    attendance_pct,
    study_hours,
    assignment_pct,
    ca_mark,
    mid_mark,
    end_marks,
    grade,
    status,
    attendance_dates,
):
    enrollment = Enrollment(
        institution_id=institution_id,
        student_id=student.id,
        course_id=course.id,
        semester_id=semester.id,
        attendance_percentage=attendance_pct,
        study_hours_per_week=study_hours,
        assignment_completion_pct=assignment_pct,
    )
    db.add(enrollment)
    db.flush()

    ca = (
        db.query(Assessment)
        .filter(
            Assessment.course_id == course.id,
            Assessment.assessment_type == "CA",
        )
        .first()
    )
    mid = (
        db.query(Assessment)
        .filter(
            Assessment.course_id == course.id,
            Assessment.assessment_type == "MID",
        )
        .first()
    )
    if ca:
        db.add(
            AssessmentMark(
                institution_id=institution_id,
                enrollment_id=enrollment.id,
                assessment_id=ca.id,
                marks_obtained=ca_mark,
            )
        )
    if mid:
        db.add(
            AssessmentMark(
                institution_id=institution_id,
                enrollment_id=enrollment.id,
                assessment_id=mid.id,
                marks_obtained=mid_mark,
            )
        )

    for att_date, att_status in attendance_dates:
        db.add(
            Attendance(
                institution_id=institution_id,
                enrollment_id=enrollment.id,
                date=att_date,
                status=att_status,
            )
        )

    db.add(
        CourseResult(
            institution_id=institution_id,
            enrollment_id=enrollment.id,
            grade=grade,
            end_marks=end_marks,
            status=status,
        )
    )
    return enrollment


def _ensure_course_assessments(db, institution_id, course):
    existing = (
        db.query(Assessment)
        .filter(Assessment.course_id == course.id)
        .first()
    )
    if existing:
        return
    db.add_all(
        [
            Assessment(
                institution_id=institution_id,
                course_id=course.id,
                name="Continuous Assessment",
                assessment_type="CA",
                max_marks=100,
            ),
            Assessment(
                institution_id=institution_id,
                course_id=course.id,
                name="Mid-Term Exam",
                assessment_type="MID",
                max_marks=100,
            ),
        ]
    )
    db.flush()


def _seed_institution_1(db):
    institution = Institution(name=INSTITUTION_1_NAME)
    db.add(institution)
    db.flush()

    dept = Department(
        institution_id=institution.id,
        name="Computer Science & Engineering",
        code="CSE",
    )
    db.add(dept)
    db.flush()

    program = Program(
        institution_id=institution.id,
        department_id=dept.id,
        name="B.Tech CSE",
        code="BTECH-CSE",
        duration_semesters=8,
    )
    db.add(program)
    db.flush()

    ay = AcademicYear(institution_id=institution.id, name="2024-25", is_current=True)
    db.add(ay)
    db.flush()

    semester = Semester(
        institution_id=institution.id,
        academic_year_id=ay.id,
        number=5,
        name="Semester 5",
    )
    db.add(semester)
    db.flush()

    admin_user = _create_user(db, institution.id, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")
    faculty_user = _create_user(db, institution.id, FACULTY_EMAIL, FACULTY_PASSWORD, "faculty")
    parent_user = _create_user(db, institution.id, PARENT_EMAIL, PARENT_PASSWORD, "parent")

    students = []
    for roll, name in STUDENT_ROLLS:
        user = _create_user(db, institution.id, None, STUDENT_PASSWORD, "student")
        students.append(
            _create_student(
                db, institution.id, user, roll, name, dept.id, program.id, 5, "CSE"
            )
        )

    faculty = Faculty(
        institution_id=institution.id,
        user_id=faculty_user.id,
        name="Dr. Ananya Sharma",
        department_id=dept.id,
    )
    parent = Parent(
        institution_id=institution.id,
        user_id=parent_user.id,
        name="Rajesh Kamble",
    )
    db.add_all([faculty, parent])
    db.flush()

    for student in students:
        db.add(FacultyStudent(faculty_id=faculty.id, student_id=student.id))
    db.add(ParentStudent(parent_id=parent.id, student_id=students[0].id))

    courses = []
    for code, name in [
        ("CS301", "Data Structures"),
        ("CS302", "Database Systems"),
        ("CS303", "Design & Analysis of Algorithms"),
    ]:
        course = Course(
            institution_id=institution.id,
            department_id=dept.id,
            name=name,
            code=code,
            credits=3,
            course_type="THEORY",
        )
        db.add(course)
        db.flush()
        _ensure_course_assessments(db, institution.id, course)
        courses.append(course)

    attendance_good = [
        (date(2025, 1, 6), "present"),
        (date(2025, 1, 8), "present"),
        (date(2025, 1, 10), "present"),
        (date(2025, 1, 13), "present"),
        (date(2025, 1, 15), "absent"),
    ]
    attendance_medium = [
        (date(2025, 1, 6), "present"),
        (date(2025, 1, 8), "absent"),
        (date(2025, 1, 10), "present"),
        (date(2025, 1, 13), "absent"),
        (date(2025, 1, 15), "present"),
    ]
    attendance_poor = [
        (date(2025, 1, 6), "absent"),
        (date(2025, 1, 8), "absent"),
        (date(2025, 1, 10), "present"),
        (date(2025, 1, 13), "absent"),
        (date(2025, 1, 15), "absent"),
    ]

    kishore_data = [
        (82.0, 18.0, 88.0, 72.0, 68.0, 78.0, "A", "PASS", attendance_good),
        (80.0, 17.0, 85.0, 70.0, 66.0, 76.0, "A", "PASS", attendance_good),
        (84.0, 19.0, 90.0, 74.0, 70.0, 80.0, "A", "PASS", attendance_good),
    ]
    for course, row in zip(courses, kishore_data):
        _create_course_enrollment(db, institution.id, students[0], course, semester, *row)

    db.add(
        SemesterResult(
            institution_id=institution.id,
            student_id=students[0].id,
            semester_id=semester.id,
            sgpa=7.8,
            cgpa=7.5,
            backlog_count=0,
            current_failed_courses=0,
            low_performance_course_count=0,
            performance_trend="STABLE",
        )
    )

    srivatsa_data = [
        (72.0, 12.0, 70.0, 58.0, 52.0, 60.0, "B", "PASS", attendance_medium),
        (68.0, 11.0, 65.0, 55.0, 50.0, 58.0, "B", "PASS", attendance_medium),
        (70.0, 13.0, 68.0, 56.0, 48.0, 55.0, "C", "PASS", attendance_medium),
    ]
    for course, row in zip(courses, srivatsa_data):
        _create_course_enrollment(db, institution.id, students[1], course, semester, *row)

    db.add(
        SemesterResult(
            institution_id=institution.id,
            student_id=students[1].id,
            semester_id=semester.id,
            sgpa=6.4,
            cgpa=6.2,
            backlog_count=1,
            current_failed_courses=0,
            low_performance_course_count=1,
            performance_trend="DECLINING",
        )
    )

    mohan_data = [
        (55.0, 6.0, 40.0, 42.0, 38.0, 45.0, "D", "FAIL", attendance_poor),
        (52.0, 5.0, 35.0, 40.0, 36.0, 42.0, "D", "FAIL", attendance_poor),
        (58.0, 7.0, 45.0, 44.0, 40.0, 48.0, "D", "FAIL", attendance_poor),
    ]
    for course, row in zip(courses, mohan_data):
        _create_course_enrollment(db, institution.id, students[2], course, semester, *row)

    db.add(
        SemesterResult(
            institution_id=institution.id,
            student_id=students[2].id,
            semester_id=semester.id,
            sgpa=4.8,
            cgpa=5.0,
            backlog_count=3,
            current_failed_courses=2,
            low_performance_course_count=3,
            performance_trend="DECLINING",
        )
    )

    return institution


def _seed_institution_2(db):
    institution = Institution(name=INSTITUTION_2_NAME)
    db.add(institution)
    db.flush()

    dept = Department(
        institution_id=institution.id,
        name="Electronics & Communication",
        code="ECE",
    )
    db.add(dept)
    db.flush()

    admin_user = _create_user(
        db, institution.id, ADMIN_2_EMAIL, ADMIN_2_PASSWORD, "institution_admin"
    )
    student_user = _create_user(db, institution.id, None, STUDENT_PASSWORD, "student")

    _create_student(
        db,
        institution.id,
        student_user,
        STUDENT_2_ROLL,
        "Priya Nair",
        dept.id,
        None,
        3,
        "ECE",
    )
    return institution


def seed_predictions(db):
    """Generate ML predictions for all seeded students."""
    from app.ml.model_loader import model_loader

    if not model_loader.is_loaded:
        model_loader.load()

    institutions = db.query(Institution).all()
    total = 0
    for institution in institutions:
        total += seed_predictions_for_institution(
            db, institution.id, replace_existing=True
        )
    return total


def seed(force: bool = False, scale: int = 100, cse_demo: bool = False):
    db = SessionLocal()
    try:
        if db.query(Institution).first() and not force:
            if not db.query(PredictionResult).first():
                print("Academic data exists; seeding predictions only...")
                count = seed_predictions(db)
                db.commit()
                print(f"Seeded {count} prediction results.")
            else:
                print("Database already seeded.")
                print("Run `uv run python scripts/reseed.py` for a fresh dataset.")
            return

        if cse_demo:
            from scripts.seed_cse_demo import seed_cse_demo

            seed_cse_demo(db)
        elif scale > 10:
            from scripts.seed_bulk import seed_demo_university

            seed_demo_university(db, scale=scale)
        else:
            _seed_institution_1(db)
        _seed_institution_2(db)
        db.flush()

        count = seed_predictions(db)
        db.commit()

        print("Seed complete.")
        print(f"Institution 1 ({INSTITUTION_1_NAME}):")
        print(f"  Admin:   {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
        print(f"  Faculty: {FACULTY_EMAIL} / {FACULTY_PASSWORD}")
        for roll, name in STUDENT_ROLLS:
            print(f"  Student: {roll} / {STUDENT_PASSWORD} ({name})")
        print(f"  Parent:  {PARENT_EMAIL} / {PARENT_PASSWORD}")
        print(f"Institution 2 ({INSTITUTION_2_NAME}):")
        print(f"  Admin:   {ADMIN_2_EMAIL} / {ADMIN_2_PASSWORD}")
        print(f"  Student: {STUDENT_2_ROLL} / {STUDENT_PASSWORD}")
        print(f"ML predictions stored: {count}")
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Seed academic data and ML predictions for local development"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-seed even if data already exists (does not drop tables)",
    )
    parser.add_argument(
        "--scale",
        type=int,
        default=100,
        help="Total students for Demo University bulk seed (default 100)",
    )
    parser.add_argument(
        "--cse-demo",
        action="store_true",
        help="Seed CSE, ECE, IST branches (60 students each, 4 semesters)",
    )
    args = parser.parse_args()
    seed(force=args.force, scale=args.scale, cse_demo=args.cse_demo)
