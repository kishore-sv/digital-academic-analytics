"""Bulk seed Demo University with configurable student scale."""

from __future__ import annotations

import random
from datetime import date

from app.core.security import hash_password
from app.core.seed_data import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    DEPARTMENTS,
    FACULTY_EMAIL,
    FACULTY_PASSWORD,
    INSTITUTION_1_NAME,
    PARENT_EMAIL,
    PARENT_PASSWORD,
    STUDENT_PASSWORD,
    STUDENT_ROLLS,
)
from app.models.academic_year import AcademicYear
from app.models.course import Course
from app.models.department import Department
from app.models.enrollment import (
    Assessment,
    AssessmentMark,
    CourseResult,
    Enrollment,
    SemesterResult,
)
from app.models.faculty import Faculty
from app.models.institution import Institution
from app.models.parent import FacultyStudent, Parent, ParentStudent
from app.models.program import Program
from app.models.semester import Semester
from app.models.student import Student
from app.models.user import User


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


def _ensure_assessments(db, institution_id, course):
    if db.query(Assessment).filter(Assessment.course_id == course.id).first():
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


def _seed_student_enrollment(db, institution_id, student, course, semester, rng, cgpa_base):
    att_pct = max(40, min(100, cgpa_base * 10 + rng.uniform(-10, 10)))
    study_hrs = rng.uniform(5, 25)
    assign_pct = rng.uniform(50, 100)
    ca = (
        db.query(Assessment)
        .filter(Assessment.course_id == course.id, Assessment.assessment_type == "CA")
        .first()
    )
    mid = (
        db.query(Assessment)
        .filter(Assessment.course_id == course.id, Assessment.assessment_type == "MID")
        .first()
    )
    end_marks = max(30, min(98, cgpa_base * 10 + rng.uniform(-15, 15)))
    status = "PASS" if end_marks >= 40 else "FAIL"
    grade = (
        "A" if end_marks >= 75
        else "B" if end_marks >= 60
        else "C" if end_marks >= 50
        else "D"
    )
    enrollment = Enrollment(
        institution_id=institution_id,
        student_id=student.id,
        course_id=course.id,
        semester_id=semester.id,
        attendance_percentage=round(att_pct, 1),
        study_hours_per_week=round(study_hrs, 1),
        assignment_completion_pct=round(assign_pct, 1),
    )
    db.add(enrollment)
    db.flush()
    if ca:
        db.add(
            AssessmentMark(
                institution_id=institution_id,
                enrollment_id=enrollment.id,
                assessment_id=ca.id,
                marks_obtained=round(end_marks * 0.4 + rng.uniform(-5, 5), 1),
            )
        )
    if mid:
        db.add(
            AssessmentMark(
                institution_id=institution_id,
                enrollment_id=enrollment.id,
                assessment_id=mid.id,
                marks_obtained=round(end_marks * 0.35 + rng.uniform(-5, 5), 1),
            )
        )
    db.add(
        CourseResult(
            institution_id=institution_id,
            enrollment_id=enrollment.id,
            grade=grade,
            end_marks=round(end_marks, 1),
            status=status,
        )
    )


def seed_demo_university(db, scale: int = 500) -> Institution:
    """Seed Demo University with `scale` total students across departments."""
    rng = random.Random(649)
    institution = Institution(name=INSTITUTION_1_NAME)
    db.add(institution)
    db.flush()

    admin_user = _create_user(db, institution.id, ADMIN_EMAIL, ADMIN_PASSWORD, "institution_admin")
    faculty_user = _create_user(db, institution.id, FACULTY_EMAIL, FACULTY_PASSWORD, "faculty")
    parent_user = _create_user(db, institution.id, PARENT_EMAIL, PARENT_PASSWORD, "parent")

    years = []
    for yr_name, is_current in [("2022-23", False), ("2023-24", False), ("2024-25", True)]:
        ay = AcademicYear(
            institution_id=institution.id, name=yr_name, is_current=is_current
        )
        db.add(ay)
        db.flush()
        years.append(ay)

    semesters = []
    for ay in years:
        for num in range(1, 9):
            sem = Semester(
                institution_id=institution.id,
                academic_year_id=ay.id,
                number=num,
                name=f"Semester {num}",
            )
            db.add(sem)
            db.flush()
            semesters.append(sem)

    current_semester = semesters[-2]

    departments: list[Department] = []
    programs: dict[str, Program] = {}
    courses: dict[str, list[Course]] = {}
    faculty_list: list[Faculty] = []

    for code, name in DEPARTMENTS:
        dept = Department(
            institution_id=institution.id, name=name, code=code
        )
        db.add(dept)
        db.flush()
        departments.append(dept)

        program = Program(
            institution_id=institution.id,
            department_id=dept.id,
            name=f"B.Tech {code}",
            code=f"BTECH-{code}",
            duration_semesters=8,
        )
        db.add(program)
        db.flush()
        programs[code] = program

        dept_courses = []
        for i, cname in enumerate(
            ["Engineering Mathematics", "Core Subject I", "Core Subject II", "Lab Course"],
            start=1,
        ):
            course = Course(
                institution_id=institution.id,
                department_id=dept.id,
                name=cname,
                code=f"{code}10{i}",
                credits=3 if i < 4 else 2,
                course_type="THEORY" if i < 4 else "LAB",
            )
            db.add(course)
            db.flush()
            _ensure_assessments(db, institution.id, course)
            dept_courses.append(course)
        courses[code] = dept_courses

        for f_idx in range(3):
            email = f"faculty.{code.lower()}.{f_idx + 1}@demo.com"
            fu = _create_user(db, institution.id, email, "faculty123", "faculty")
            fac = Faculty(
                institution_id=institution.id,
                user_id=fu.id,
                name=f"Prof. {code} Faculty {f_idx + 1}",
                department_id=dept.id,
            )
            db.add(fac)
            db.flush()
            faculty_list.append(fac)

    primary_faculty = Faculty(
        institution_id=institution.id,
        user_id=faculty_user.id,
        name="Dr. Ananya Sharma",
        department_id=departments[0].id,
    )
    db.add(primary_faculty)
    db.flush()
    faculty_list.append(primary_faculty)

    parent = Parent(
        institution_id=institution.id,
        user_id=parent_user.id,
        name="Rajesh Kamble",
    )
    db.add(parent)
    db.flush()

    students_per_dept = max(1, scale // len(DEPARTMENTS))
    all_students: list[Student] = []
    roll_counter = 20240001

    # Named seed students for integration tests (CSE)
    cse_dept = departments[0]
    cse_program = programs["CSE"]
    for roll, name in STUDENT_ROLLS:
        user = _create_user(db, institution.id, None, STUDENT_PASSWORD, "student")
        student = Student(
            institution_id=institution.id,
            user_id=user.id,
            roll_number=roll,
            name=name,
            department_id=cse_dept.id,
            program_id=cse_program.id,
            semester=5,
            branch="CSE",
        )
        db.add(student)
        db.flush()
        all_students.append(student)
        db.add(FacultyStudent(faculty_id=primary_faculty.id, student_id=student.id))
        if roll == STUDENT_ROLLS[0][0]:
            db.add(ParentStudent(parent_id=parent.id, student_id=student.id))
        cgpa_base = 7.5 if roll == STUDENT_ROLLS[0][0] else 6.2 if roll == STUDENT_ROLLS[1][0] else 5.0
        for course in courses["CSE"][:3]:
            _seed_student_enrollment(
                db, institution.id, student, course, current_semester,
                rng, cgpa_base,
            )
        db.add(
            SemesterResult(
                institution_id=institution.id,
                student_id=student.id,
                semester_id=current_semester.id,
                sgpa=round(cgpa_base, 2),
                cgpa=round(cgpa_base, 2),
                backlog_count=0 if cgpa_base >= 6 else 2,
                current_failed_courses=0 if cgpa_base >= 6 else 1,
                low_performance_course_count=0,
                performance_trend="STABLE" if cgpa_base >= 7 else "DECLINING",
            )
        )

    for dept_idx, (code, _) in enumerate(DEPARTMENTS):
        dept = departments[dept_idx]
        program = programs[code]
        dept_faculty = [f for f in faculty_list if f.department_id == dept.id]

        for i in range(students_per_dept):
            roll = f"{roll_counter + dept_idx * 10000 + i:08d}"
            roll_counter += 1
            user = _create_user(db, institution.id, None, STUDENT_PASSWORD, "student")
            sem_num = rng.randint(1, 8)
            cgpa_base = rng.uniform(4.5, 9.5)
            trend = rng.choice(["IMPROVING", "STABLE", "DECLINING"])
            backlogs = max(0, int((6.0 - cgpa_base) * 2))

            student = Student(
                institution_id=institution.id,
                user_id=user.id,
                roll_number=roll,
                name=f"Student {roll}",
                department_id=dept.id,
                program_id=program.id,
                semester=sem_num,
                branch=code,
            )
            db.add(student)
            db.flush()
            all_students.append(student)

            fac = dept_faculty[i % len(dept_faculty)]
            db.add(FacultyStudent(faculty_id=fac.id, student_id=student.id))

            if rng.random() < 0.3:
                pu = _create_user(
                    db,
                    institution.id,
                    f"parent.{roll}@demo.com",
                    "parent123",
                    "parent",
                )
                p = Parent(
                    institution_id=institution.id,
                    user_id=pu.id,
                    name=f"Parent of {roll}",
                )
                db.add(p)
                db.flush()
                db.add(ParentStudent(parent_id=p.id, student_id=student.id))

            att_pct = max(40, min(100, cgpa_base * 10 + rng.uniform(-10, 10)))
            study_hrs = rng.uniform(5, 25)
            assign_pct = rng.uniform(50, 100)

            for course in courses[code][:3]:
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
                end_marks = max(30, min(98, cgpa_base * 10 + rng.uniform(-15, 15)))
                status = "PASS" if end_marks >= 40 else "FAIL"
                grade = "A" if end_marks >= 75 else "B" if end_marks >= 60 else "C" if end_marks >= 50 else "D"

                enrollment = Enrollment(
                    institution_id=institution.id,
                    student_id=student.id,
                    course_id=course.id,
                    semester_id=current_semester.id,
                    attendance_percentage=round(att_pct, 1),
                    study_hours_per_week=round(study_hrs, 1),
                    assignment_completion_pct=round(assign_pct, 1),
                )
                db.add(enrollment)
                db.flush()

                if ca:
                    db.add(
                        AssessmentMark(
                            institution_id=institution.id,
                            enrollment_id=enrollment.id,
                            assessment_id=ca.id,
                            marks_obtained=round(end_marks * 0.4 + rng.uniform(-5, 5), 1),
                        )
                    )
                if mid:
                    db.add(
                        AssessmentMark(
                            institution_id=institution.id,
                            enrollment_id=enrollment.id,
                            assessment_id=mid.id,
                            marks_obtained=round(end_marks * 0.35 + rng.uniform(-5, 5), 1),
                        )
                    )
                db.add(
                    CourseResult(
                        institution_id=institution.id,
                        enrollment_id=enrollment.id,
                        grade=grade,
                        end_marks=round(end_marks, 1),
                        status=status,
                    )
                )

            db.add(
                SemesterResult(
                    institution_id=institution.id,
                    student_id=student.id,
                    semester_id=current_semester.id,
                    sgpa=round(cgpa_base + rng.uniform(-0.3, 0.3), 2),
                    cgpa=round(cgpa_base, 2),
                    backlog_count=backlogs,
                    current_failed_courses=min(backlogs, 2),
                    low_performance_course_count=max(0, backlogs - 1),
                    performance_trend=trend,
                )
            )

    db.flush()
    return institution
