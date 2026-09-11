"""Institutional analytics aggregation service."""

from __future__ import annotations

import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.department import Department
from app.models.enrollment import CourseResult, Enrollment, SemesterResult
from app.models.faculty import Faculty
from app.models.prediction import PredictionResult
from app.models.student import Student
from app.models.user import User
from app.schemas.analytics import (
    CourseAnalytics,
    DepartmentAnalytics,
    OverviewStats,
    PerformanceTrendPoint,
    RiskDistribution,
)


def get_overview(db: Session, institution_id: uuid.UUID) -> OverviewStats:
    total_students = (
        db.query(func.count(Student.id))
        .filter(Student.institution_id == institution_id)
        .scalar()
        or 0
    )
    total_faculty = (
        db.query(func.count(Faculty.id))
        .filter(Faculty.institution_id == institution_id)
        .scalar()
        or 0
    )
    total_departments = (
        db.query(func.count(Department.id))
        .filter(Department.institution_id == institution_id)
        .scalar()
        or 0
    )

    avg_cgpa = (
        db.query(func.avg(SemesterResult.cgpa))
        .filter(SemesterResult.institution_id == institution_id)
        .scalar()
    ) or 0.0

    avg_sgpa = (
        db.query(func.avg(SemesterResult.sgpa))
        .filter(SemesterResult.institution_id == institution_id)
        .scalar()
    ) or 0.0

    total_results = (
        db.query(func.count(CourseResult.id))
        .filter(CourseResult.institution_id == institution_id)
        .scalar()
        or 0
    )
    pass_count = (
        db.query(func.count(CourseResult.id))
        .filter(
            CourseResult.institution_id == institution_id,
            CourseResult.status == "PASS",
        )
        .scalar()
        or 0
    )
    pass_pct = (pass_count / total_results * 100) if total_results > 0 else 0.0

    latest_predictions = (
        db.query(PredictionResult)
        .filter(PredictionResult.institution_id == institution_id)
        .all()
    )
    at_risk = sum(1 for p in latest_predictions if p.risk_level in ("MEDIUM", "HIGH"))
    high_risk = sum(1 for p in latest_predictions if p.risk_level == "HIGH")
    at_risk_pct = (at_risk / len(latest_predictions) * 100) if latest_predictions else 0.0

    return OverviewStats(
        total_students=total_students,
        total_faculty=total_faculty,
        total_departments=total_departments,
        average_cgpa=round(float(avg_cgpa), 2),
        average_sgpa=round(float(avg_sgpa), 2),
        pass_percentage=round(pass_pct, 2),
        at_risk_percentage=round(at_risk_pct, 2),
        high_risk_count=high_risk,
    )


def get_department_analytics(
    db: Session, institution_id: uuid.UUID
) -> list[DepartmentAnalytics]:
    departments = (
        db.query(Department)
        .filter(Department.institution_id == institution_id)
        .all()
    )
    results = []
    for dept in departments:
        students = (
            db.query(Student)
            .filter(Student.department_id == dept.id, Student.institution_id == institution_id)
            .all()
        )
        student_ids = [s.id for s in students]
        avg_cgpa = 0.0
        if student_ids:
            avg_cgpa = (
                db.query(func.avg(SemesterResult.cgpa))
                .filter(SemesterResult.student_id.in_(student_ids))
                .scalar()
            ) or 0.0

        results.append(
            DepartmentAnalytics(
                department_id=str(dept.id),
                department_name=dept.name,
                average_cgpa=round(float(avg_cgpa), 2),
                student_count=len(students),
            )
        )
    return results


def get_risk_distribution(
    db: Session, institution_id: uuid.UUID
) -> RiskDistribution:
    predictions = (
        db.query(PredictionResult)
        .filter(PredictionResult.institution_id == institution_id)
        .all()
    )
    low = sum(1 for p in predictions if p.risk_level == "LOW")
    medium = sum(1 for p in predictions if p.risk_level == "MEDIUM")
    high = sum(1 for p in predictions if p.risk_level == "HIGH")
    return RiskDistribution(low=low, medium=medium, high=high)


def get_performance_trends(
    db: Session, institution_id: uuid.UUID
) -> list[PerformanceTrendPoint]:
    from app.models.semester import Semester

    semesters = (
        db.query(Semester)
        .filter(Semester.institution_id == institution_id)
        .order_by(Semester.number)
        .all()
    )
    trends = []
    for sem in semesters:
        avg_sgpa = (
            db.query(func.avg(SemesterResult.sgpa))
            .filter(
                SemesterResult.semester_id == sem.id,
                SemesterResult.institution_id == institution_id,
            )
            .scalar()
        )
        trends.append(
            PerformanceTrendPoint(
                semester=sem.name,
                average_sgpa=round(float(avg_sgpa), 2) if avg_sgpa is not None else None,
            )
        )
    return trends


def get_course_analytics(
    db: Session, institution_id: uuid.UUID
) -> list[CourseAnalytics]:
    courses = (
        db.query(Course)
        .filter(Course.institution_id == institution_id)
        .all()
    )
    results = []
    for course in courses:
        enrollments = (
            db.query(Enrollment)
            .filter(Enrollment.course_id == course.id)
            .all()
        )
        marks = []
        pass_count = 0
        total = 0
        for e in enrollments:
            if e.course_result:
                total += 1
                if e.course_result.end_marks:
                    marks.append(e.course_result.end_marks)
                if e.course_result.status == "PASS":
                    pass_count += 1
        avg_marks = sum(marks) / len(marks) if marks else 0.0
        pass_pct = (pass_count / total * 100) if total > 0 else 0.0
        results.append(
            CourseAnalytics(
                course_id=str(course.id),
                course_name=course.name,
                average_marks=round(avg_marks, 2),
                pass_percentage=round(pass_pct, 2),
            )
        )
    return results


def _scoped_student_ids(db: Session, user: User) -> list[uuid.UUID]:
    from app.services.authorization_service import filter_students_query

    students = filter_students_query(db, user).all()
    return [s.id for s in students]


def get_scoped_overview(db: Session, user: User) -> OverviewStats:
    institution_id = user.institution_id
    student_ids = _scoped_student_ids(db, user)

    total_faculty = (
        db.query(func.count(Faculty.id))
        .filter(Faculty.institution_id == institution_id)
        .scalar()
        or 0
    )
    total_departments = (
        db.query(func.count(Department.id))
        .filter(Department.institution_id == institution_id)
        .scalar()
        or 0
    )

    if not student_ids:
        return OverviewStats(
            total_students=0,
            total_faculty=total_faculty,
            total_departments=total_departments,
            average_cgpa=0.0,
            average_sgpa=0.0,
            pass_percentage=0.0,
            at_risk_percentage=0.0,
            high_risk_count=0,
        )

    avg_cgpa = (
        db.query(func.avg(SemesterResult.cgpa))
        .filter(SemesterResult.student_id.in_(student_ids))
        .scalar()
    ) or 0.0
    avg_sgpa = (
        db.query(func.avg(SemesterResult.sgpa))
        .filter(SemesterResult.student_id.in_(student_ids))
        .scalar()
    ) or 0.0

    enrollment_ids = [
        row[0]
        for row in db.query(Enrollment.id)
        .filter(Enrollment.student_id.in_(student_ids))
        .all()
    ]
    total_results = 0
    pass_count = 0
    if enrollment_ids:
        total_results = (
            db.query(func.count(CourseResult.id))
            .filter(CourseResult.enrollment_id.in_(enrollment_ids))
            .scalar()
            or 0
        )
        pass_count = (
            db.query(func.count(CourseResult.id))
            .filter(
                CourseResult.enrollment_id.in_(enrollment_ids),
                CourseResult.status == "PASS",
            )
            .scalar()
            or 0
        )
    pass_pct = (pass_count / total_results * 100) if total_results > 0 else 0.0

    predictions = (
        db.query(PredictionResult)
        .filter(
            PredictionResult.institution_id == institution_id,
            PredictionResult.student_id.in_(student_ids),
        )
        .all()
    )
    at_risk = sum(1 for p in predictions if p.risk_level in ("MEDIUM", "HIGH"))
    high_risk = sum(1 for p in predictions if p.risk_level == "HIGH")
    at_risk_pct = (at_risk / len(predictions) * 100) if predictions else 0.0

    return OverviewStats(
        total_students=len(student_ids),
        total_faculty=total_faculty,
        total_departments=total_departments,
        average_cgpa=round(float(avg_cgpa), 2),
        average_sgpa=round(float(avg_sgpa), 2),
        pass_percentage=round(pass_pct, 2),
        at_risk_percentage=round(at_risk_pct, 2),
        high_risk_count=high_risk,
    )


def get_scoped_risk_distribution(db: Session, user: User) -> RiskDistribution:
    student_ids = _scoped_student_ids(db, user)
    if not student_ids:
        return RiskDistribution(low=0, medium=0, high=0)
    predictions = (
        db.query(PredictionResult)
        .filter(
            PredictionResult.institution_id == user.institution_id,
            PredictionResult.student_id.in_(student_ids),
        )
        .all()
    )
    low = sum(1 for p in predictions if p.risk_level == "LOW")
    medium = sum(1 for p in predictions if p.risk_level == "MEDIUM")
    high = sum(1 for p in predictions if p.risk_level == "HIGH")
    return RiskDistribution(low=low, medium=medium, high=high)
