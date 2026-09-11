"""Extended analytics aggregations for chart endpoints."""

from __future__ import annotations

import uuid
from collections import Counter

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.v1.analytics_filters import AnalyticsFilterParams
from app.api.v1.helpers import parse_uuid
from app.models.department import Department
from app.models.enrollment import CourseResult, Enrollment, SemesterResult
from app.models.prediction import PredictionResult
from app.models.semester import Semester
from app.models.student import Student
from app.models.user import User
from app.models.course import Course
from app.schemas.analytics import (
    ActualVsPredictedPoint,
    AttendancePerformancePoint,
    ChartBucket,
    CourseAnalytics,
    DepartmentAnalytics,
    DepartmentRiskStack,
    OverviewStats,
    PassFailTrendPoint,
    PerformanceIndicators,
    PerformanceTrendPoint,
    PredictionPassFailAnalytics,
    PredictionPerformanceAnalytics,
    PredictionRiskAnalytics,
    RiskDistribution,
    RiskFactorCount,
)
from app.services.analytics_service import get_overview


def _student_ids_for_filters(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[uuid.UUID] | None:
    query = db.query(Student.id).filter(Student.institution_id == institution_id)
    if scope_ids is not None:
        if not scope_ids:
            return []
        query = query.filter(Student.id.in_(scope_ids))
    if filters.department_id:
        query = query.filter(
            Student.department_id == parse_uuid(filters.department_id, "department_id")
        )
    if filters.program_id:
        query = query.filter(
            Student.program_id == parse_uuid(filters.program_id, "program_id")
        )
    if filters.semester_id:
        sem_id = parse_uuid(filters.semester_id, "semester_id")
        enrolled = (
            db.query(Enrollment.student_id)
            .filter(
                Enrollment.institution_id == institution_id,
                Enrollment.semester_id == sem_id,
            )
            .distinct()
        )
        query = query.filter(Student.id.in_(enrolled))
    elif filters.academic_year_id:
        ay_id = parse_uuid(filters.academic_year_id, "academic_year_id")
        sem_ids = [
            row[0]
            for row in db.query(Semester.id)
            .filter(Semester.academic_year_id == ay_id)
            .all()
        ]
        if sem_ids:
            enrolled = (
                db.query(Enrollment.student_id)
                .filter(
                    Enrollment.institution_id == institution_id,
                    Enrollment.semester_id.in_(sem_ids),
                )
                .distinct()
            )
            query = query.filter(Student.id.in_(enrolled))
        else:
            return []
    if filters.course_id:
        course_id = parse_uuid(filters.course_id, "course_id")
        enrolled = (
            db.query(Enrollment.student_id)
            .filter(
                Enrollment.institution_id == institution_id,
                Enrollment.course_id == course_id,
            )
            .distinct()
        )
        query = query.filter(Student.id.in_(enrolled))
    student_ids = [row[0] for row in query.all()]
    if filters.risk_level and student_ids:
        preds = _latest_predictions(db, institution_id, student_ids)
        allowed = {p.student_id for p in preds if p.risk_level == filters.risk_level}
        student_ids = [sid for sid in student_ids if sid in allowed]
    return student_ids


def _latest_predictions(
    db: Session,
    institution_id: uuid.UUID,
    student_ids: list[uuid.UUID] | None,
) -> list[PredictionResult]:
    query = db.query(PredictionResult).filter(
        PredictionResult.institution_id == institution_id
    )
    if student_ids is not None:
        if not student_ids:
            return []
        query = query.filter(PredictionResult.student_id.in_(student_ids))
    predictions = query.order_by(PredictionResult.created_at.desc()).all()
    seen: set[uuid.UUID] = set()
    latest: list[PredictionResult] = []
    for p in predictions:
        if p.student_id not in seen:
            seen.add(p.student_id)
            latest.append(p)
    return latest


def get_filtered_overview(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> OverviewStats:
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    if student_ids is not None and not student_ids:
        return OverviewStats()
    if student_ids is None:
        base = get_overview(db, institution_id)
    else:
        # Recompute with filtered ids
        total_students = len(student_ids)
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
            r[0]
            for r in db.query(Enrollment.id)
            .filter(Enrollment.student_id.in_(student_ids))
            .all()
        ]
        total_results = pass_count = 0
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
        pass_pct = (pass_count / total_results * 100) if total_results else 0.0
        preds = _latest_predictions(db, institution_id, student_ids)
        at_risk = sum(1 for p in preds if p.risk_level in ("MEDIUM", "HIGH"))
        high_risk = sum(1 for p in preds if p.risk_level == "HIGH")
        at_risk_pct = (at_risk / len(preds) * 100) if preds else 0.0
        from app.models.department import Department
        from app.models.faculty import Faculty

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
        base = OverviewStats(
            total_students=total_students,
            total_faculty=total_faculty,
            total_departments=total_departments,
            average_cgpa=round(float(avg_cgpa), 2),
            average_sgpa=round(float(avg_sgpa), 2),
            pass_percentage=round(pass_pct, 2),
            at_risk_percentage=round(at_risk_pct, 2),
            high_risk_count=high_risk,
        )
    return base


def get_department_analytics_filtered(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[DepartmentAnalytics]:
    departments = (
        db.query(Department)
        .filter(Department.institution_id == institution_id)
        .order_by(Department.name)
        .all()
    )
    if filters.department_id:
        dept_uuid = parse_uuid(filters.department_id, "department_id")
        departments = [d for d in departments if d.id == dept_uuid]

    filtered_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    results = []
    for dept in departments:
        student_query = db.query(Student.id).filter(
            Student.department_id == dept.id,
            Student.institution_id == institution_id,
        )
        if scope_ids is not None:
            if not scope_ids:
                continue
            student_query = student_query.filter(Student.id.in_(scope_ids))
        student_ids = [r[0] for r in student_query.all()]
        if filtered_ids is not None:
            allowed = set(filtered_ids)
            student_ids = [sid for sid in student_ids if sid in allowed]
        if not student_ids:
            results.append(
                DepartmentAnalytics(
                    department_id=str(dept.id),
                    department_name=dept.name,
                    average_cgpa=0.0,
                    pass_percentage=0.0,
                    student_count=0,
                )
            )
            continue
        avg_cgpa = (
            db.query(func.avg(SemesterResult.cgpa))
            .filter(SemesterResult.student_id.in_(student_ids))
            .scalar()
        ) or 0.0
        enrollment_ids = [
            r[0]
            for r in db.query(Enrollment.id)
            .filter(Enrollment.student_id.in_(student_ids))
            .all()
        ]
        pass_pct = 0.0
        if enrollment_ids:
            total = (
                db.query(func.count(CourseResult.id))
                .filter(CourseResult.enrollment_id.in_(enrollment_ids))
                .scalar()
                or 0
            )
            passed = (
                db.query(func.count(CourseResult.id))
                .filter(
                    CourseResult.enrollment_id.in_(enrollment_ids),
                    CourseResult.status == "PASS",
                )
                .scalar()
                or 0
            )
            pass_pct = (passed / total * 100) if total else 0.0
        results.append(
            DepartmentAnalytics(
                department_id=str(dept.id),
                department_name=dept.name,
                average_cgpa=round(float(avg_cgpa), 2),
                pass_percentage=round(pass_pct, 2),
                student_count=len(student_ids),
            )
        )
    return results


def get_cgpa_distribution(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[ChartBucket]:
    buckets = [
        ("0-5", 0, 5),
        ("5-6", 5, 6),
        ("6-7", 6, 7),
        ("7-8", 7, 8),
        ("8-9", 8, 9),
        ("9-10", 9, 10.01),
    ]
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    query = db.query(SemesterResult.cgpa).filter(
        SemesterResult.institution_id == institution_id,
        SemesterResult.cgpa.isnot(None),
    )
    if student_ids is not None:
        if not student_ids:
            return [ChartBucket(label=label, value=0) for label, _, _ in buckets]
        query = query.filter(SemesterResult.student_id.in_(student_ids))
    cgpas = [float(r[0]) for r in query.all()]
    counts = {label: 0 for label, _, _ in buckets}
    for cgpa in cgpas:
        for label, low, high in buckets:
            if low <= cgpa < high:
                counts[label] += 1
                break
    return [ChartBucket(label=label, value=counts[label]) for label, _, _ in buckets]


def get_performance_trends_filtered(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[PerformanceTrendPoint]:
    sem_query = db.query(Semester).filter(Semester.institution_id == institution_id)
    if filters.academic_year_id:
        sem_query = sem_query.filter(
            Semester.academic_year_id
            == parse_uuid(filters.academic_year_id, "academic_year_id")
        )
    if filters.semester_id:
        sem_query = sem_query.filter(
            Semester.id == parse_uuid(filters.semester_id, "semester_id")
        )
    semesters = sem_query.order_by(Semester.number).all()
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    trends = []
    for sem in semesters:
        sr_query = db.query(SemesterResult).filter(
            SemesterResult.semester_id == sem.id,
            SemesterResult.institution_id == institution_id,
        )
        if student_ids is not None:
            if not student_ids:
                trends.append(
                    PerformanceTrendPoint(semester=sem.name)
                )
                continue
            sr_query = sr_query.filter(SemesterResult.student_id.in_(student_ids))
        results = sr_query.all()
        if not results:
            trends.append(PerformanceTrendPoint(semester=sem.name))
            continue
        avg_sgpa = sum(r.sgpa or 0 for r in results) / len(results)
        avg_cgpa = sum(r.cgpa or 0 for r in results) / len(results)
        pass_count = sum(1 for r in results if (r.cgpa or 0) >= 5.0)
        pass_pct = pass_count / len(results) * 100
        trends.append(
            PerformanceTrendPoint(
                semester=sem.name,
                average_sgpa=round(avg_sgpa, 2),
                average_cgpa=round(avg_cgpa, 2),
                pass_percentage=round(pass_pct, 2),
            )
        )
    return trends


def get_pass_fail_trend(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[PassFailTrendPoint]:
    sem_query = db.query(Semester).filter(Semester.institution_id == institution_id)
    if filters.academic_year_id:
        sem_query = sem_query.filter(
            Semester.academic_year_id
            == parse_uuid(filters.academic_year_id, "academic_year_id")
        )
    semesters = sem_query.order_by(Semester.number).all()
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    points = []
    for sem in semesters:
        enroll_query = db.query(Enrollment).filter(
            Enrollment.semester_id == sem.id,
            Enrollment.institution_id == institution_id,
        )
        if student_ids is not None:
            if not student_ids:
                points.append(PassFailTrendPoint(semester=sem.name, pass_count=0, fail_count=0))
                continue
            enroll_query = enroll_query.filter(Enrollment.student_id.in_(student_ids))
        enrollments = enroll_query.all()
        pass_count = fail_count = 0
        for e in enrollments:
            if e.course_result:
                if e.course_result.status == "PASS":
                    pass_count += 1
                elif e.course_result.status == "FAIL":
                    fail_count += 1
        points.append(
            PassFailTrendPoint(
                semester=sem.name,
                pass_count=pass_count,
                fail_count=fail_count,
            )
        )
    return points


def get_attendance_performance(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
    limit: int = 200,
) -> list[AttendancePerformancePoint]:
    query = db.query(Enrollment).filter(Enrollment.institution_id == institution_id)
    if scope_ids is not None:
        if not scope_ids:
            return []
        query = query.filter(Enrollment.student_id.in_(scope_ids))
    if filters.semester_id:
        query = query.filter(
            Enrollment.semester_id == parse_uuid(filters.semester_id, "semester_id")
        )
    if filters.course_id:
        query = query.filter(
            Enrollment.course_id == parse_uuid(filters.course_id, "course_id")
        )
    enrollments = query.limit(limit).all()
    points = []
    for e in enrollments:
        if e.attendance_percentage is None:
            continue
        marks = e.course_result.end_marks if e.course_result else None
        if marks is None:
            sr = (
                db.query(SemesterResult.cgpa)
                .filter(
                    SemesterResult.student_id == e.student_id,
                    SemesterResult.institution_id == institution_id,
                )
                .order_by(SemesterResult.created_at.desc())
                .first()
            )
            marks = float(sr[0]) * 10 if sr and sr[0] else None
        if marks is not None:
            points.append(
                AttendancePerformancePoint(
                    attendance_percentage=round(e.attendance_percentage, 2),
                    performance_value=round(float(marks), 2),
                )
            )
    return points


def get_performance_indicators(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> PerformanceIndicators:
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    query = db.query(SemesterResult.performance_trend).filter(
        SemesterResult.institution_id == institution_id
    )
    if student_ids is not None:
        if not student_ids:
            return PerformanceIndicators()
        query = query.filter(SemesterResult.student_id.in_(student_ids))
    trends = [r[0] for r in query.all() if r[0]]
    improving = sum(1 for t in trends if t == "IMPROVING")
    stable = sum(1 for t in trends if t == "STABLE")
    declining = sum(1 for t in trends if t == "DECLINING")
    return PerformanceIndicators(improving=improving, stable=stable, declining=declining)


def get_risk_distribution_filtered(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> RiskDistribution:
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    preds = _latest_predictions(db, institution_id, student_ids)
    low = sum(1 for p in preds if p.risk_level == "LOW")
    medium = sum(1 for p in preds if p.risk_level == "MEDIUM")
    high = sum(1 for p in preds if p.risk_level == "HIGH")
    return RiskDistribution(low=low, medium=medium, high=high)


def get_department_risk_stacks(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[DepartmentRiskStack]:
    departments = (
        db.query(Department)
        .filter(Department.institution_id == institution_id)
        .order_by(Department.name)
        .all()
    )
    if filters.department_id:
        dept_uuid = parse_uuid(filters.department_id, "department_id")
        departments = [d for d in departments if d.id == dept_uuid]
    filtered_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    stacks = []
    for dept in departments:
        student_query = db.query(Student.id).filter(
            Student.department_id == dept.id,
            Student.institution_id == institution_id,
        )
        if scope_ids is not None:
            if not scope_ids:
                continue
            student_query = student_query.filter(Student.id.in_(scope_ids))
        student_ids = [r[0] for r in student_query.all()]
        if filtered_ids is not None:
            allowed = set(filtered_ids)
            student_ids = [sid for sid in student_ids if sid in allowed]
        preds = _latest_predictions(db, institution_id, student_ids if student_ids else [])
        stacks.append(
            DepartmentRiskStack(
                department_id=str(dept.id),
                department_name=dept.name,
                low=sum(1 for p in preds if p.risk_level == "LOW"),
                medium=sum(1 for p in preds if p.risk_level == "MEDIUM"),
                high=sum(1 for p in preds if p.risk_level == "HIGH"),
            )
        )
    return stacks


def get_risk_factors(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[RiskFactorCount]:
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    preds = _latest_predictions(db, institution_id, student_ids)
    counter: Counter[str] = Counter()
    for p in preds:
        factors = p.risk_factors or []
        if isinstance(factors, dict):
            factors = list(factors.keys())
        for f in factors:
            counter[str(f)] += 1
    return [RiskFactorCount(factor=k, count=v) for k, v in counter.most_common(15)]


def get_prediction_performance_analytics(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> PredictionPerformanceAnalytics:
    preds = _latest_predictions(
        db, institution_id, _student_ids_for_filters(db, institution_id, filters, scope_ids)
    )
    marks = [p.predicted_end_marks for p in preds if p.predicted_end_marks is not None]
    avg = sum(marks) / len(marks) if marks else 0.0
    buckets = [("0-40", 0, 40), ("40-60", 40, 60), ("60-75", 60, 75), ("75-90", 75, 90), ("90-100", 90, 100.01)]
    dist = {label: 0 for label, _, _ in buckets}
    for m in marks:
        for label, low, high in buckets:
            if low <= m < high:
                dist[label] += 1
                break
    dept_data = []
    departments = db.query(Department).filter(Department.institution_id == institution_id).all()
    for dept in departments:
        sids = [
            r[0]
            for r in db.query(Student.id)
            .filter(Student.department_id == dept.id, Student.institution_id == institution_id)
            .all()
        ]
        dp = _latest_predictions(db, institution_id, sids)
        dm = [p.predicted_end_marks for p in dp if p.predicted_end_marks is not None]
        if dm:
            dept_data.append(
                ChartBucket(
                    label=dept.name,
                    value=round(sum(dm) / len(dm), 2),
                )
            )
    return PredictionPerformanceAnalytics(
        average_predicted_marks=round(avg, 2),
        distribution=[ChartBucket(label=label, value=dist[label]) for label, _, _ in buckets],
        department_averages=dept_data,
    )


def get_prediction_pass_fail_analytics(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> PredictionPassFailAnalytics:
    preds = _latest_predictions(
        db, institution_id, _student_ids_for_filters(db, institution_id, filters, scope_ids)
    )
    pass_count = sum(1 for p in preds if p.pass_fail_prediction == "PASS")
    fail_count = sum(1 for p in preds if p.pass_fail_prediction == "FAIL")
    probs = [p.pass_probability for p in preds if p.pass_probability is not None]
    avg_pass = sum(probs) / len(probs) * 100 if probs else 0.0
    prob_buckets = [("0-20", 0, 0.2), ("20-40", 0.2, 0.4), ("40-60", 0.4, 0.6), ("60-80", 0.6, 0.8), ("80-100", 0.8, 1.01)]
    dist = {label: 0 for label, _, _ in prob_buckets}
    for pr in probs:
        for label, low, high in prob_buckets:
            if low <= pr < high:
                dist[label] += 1
                break
    dept_rates = []
    for dept in db.query(Department).filter(Department.institution_id == institution_id).all():
        sids = [
            r[0]
            for r in db.query(Student.id)
            .filter(Student.department_id == dept.id)
            .all()
        ]
        dp = _latest_predictions(db, institution_id, sids)
        passed = sum(1 for p in dp if p.pass_fail_prediction == "PASS")
        if dp:
            dept_rates.append(
                ChartBucket(label=dept.name, value=round(passed / len(dp) * 100, 2))
            )
    return PredictionPassFailAnalytics(
        predicted_pass_count=pass_count,
        predicted_fail_count=fail_count,
        average_pass_probability=round(avg_pass, 2),
        probability_distribution=[ChartBucket(label=label, value=dist[label]) for label, _, _ in prob_buckets],
        department_pass_rates=dept_rates,
    )


def get_prediction_risk_analytics(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> PredictionRiskAnalytics:
    preds = _latest_predictions(
        db, institution_id, _student_ids_for_filters(db, institution_id, filters, scope_ids)
    )
    scores = [p.risk_score for p in preds if p.risk_score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0.0
    risk_dist = get_risk_distribution_filtered(db, institution_id, filters, scope_ids)
    dept_stacks = get_department_risk_stacks(db, institution_id, filters, scope_ids)
    score_buckets = [("0-30", 0, 30), ("30-50", 30, 50), ("50-70", 50, 70), ("70-100", 70, 100.01)]
    dist = {label: 0 for label, _, _ in score_buckets}
    for s in scores:
        for label, low, high in score_buckets:
            if low <= s < high:
                dist[label] += 1
                break
    return PredictionRiskAnalytics(
        average_risk_score=round(avg_score, 2),
        risk_distribution=risk_dist,
        department_stacks=dept_stacks,
        score_distribution=[ChartBucket(label=label, value=dist[label]) for label, _, _ in score_buckets],
    )


def get_actual_vs_predicted(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[ActualVsPredictedPoint]:
    preds = _latest_predictions(
        db, institution_id, _student_ids_for_filters(db, institution_id, filters, scope_ids)
    )
    points = []
    for p in preds:
        if p.predicted_end_marks is None:
            continue
        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id == p.student_id,
                Enrollment.institution_id == institution_id,
            )
            .order_by(Enrollment.created_at.desc())
            .first()
        )
        actual = None
        if enrollment and enrollment.course_result and enrollment.course_result.end_marks is not None:
            actual = enrollment.course_result.end_marks
        if actual is not None:
            student = db.query(Student).filter(Student.id == p.student_id).first()
            points.append(
                ActualVsPredictedPoint(
                    student_name=student.name if student else "",
                    actual=round(float(actual), 2),
                    predicted=round(float(p.predicted_end_marks), 2),
                )
            )
    return points[:100]


def get_scoped_ids(db: Session, user: User) -> list[uuid.UUID] | None:
    from app.services.authorization_service import get_accessible_student_ids

    return get_accessible_student_ids(db, user)


def get_sgpa_distribution(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[ChartBucket]:
    buckets = [
        ("0-5", 0, 5),
        ("5-6", 5, 6),
        ("6-7", 6, 7),
        ("7-8", 7, 8),
        ("8-9", 8, 9),
        ("9-10", 9, 10.01),
    ]
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    query = db.query(SemesterResult.sgpa).filter(
        SemesterResult.institution_id == institution_id,
        SemesterResult.sgpa.isnot(None),
    )
    if student_ids is not None:
        if not student_ids:
            return [ChartBucket(label=label, value=0) for label, _, _ in buckets]
        query = query.filter(SemesterResult.student_id.in_(student_ids))
    sgpas = [float(r[0]) for r in query.all()]
    counts = {label: 0 for label, _, _ in buckets}
    for sgpa in sgpas:
        for label, low, high in buckets:
            if low <= sgpa < high:
                counts[label] += 1
                break
    return [ChartBucket(label=label, value=counts[label]) for label, _, _ in buckets]


def get_attendance_distribution(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[ChartBucket]:
    buckets = [
        ("Below 60%", 0, 60),
        ("60-75%", 60, 75),
        ("Above 75%", 75, 101),
    ]
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    query = db.query(Enrollment.attendance_percentage).filter(
        Enrollment.institution_id == institution_id,
        Enrollment.attendance_percentage.isnot(None),
    )
    if student_ids is not None:
        if not student_ids:
            return [ChartBucket(label=label, value=0) for label, _, _ in buckets]
        query = query.filter(Enrollment.student_id.in_(student_ids))
    values = [float(r[0]) for r in query.all()]
    counts = {label: 0 for label, _, _ in buckets}
    for val in values:
        for label, low, high in buckets:
            if low <= val < high:
                counts[label] += 1
                break
    return [ChartBucket(label=label, value=counts[label]) for label, _, _ in buckets]


def get_average_attendance_filtered(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> float:
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    query = db.query(func.avg(Enrollment.attendance_percentage)).filter(
        Enrollment.institution_id == institution_id,
        Enrollment.attendance_percentage.isnot(None),
    )
    if student_ids is not None:
        if not student_ids:
            return 0.0
        query = query.filter(Enrollment.student_id.in_(student_ids))
    return round(float(query.scalar() or 0.0), 2)


def get_course_analytics_filtered(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
) -> list[CourseAnalytics]:
    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    courses = db.query(Course).filter(Course.institution_id == institution_id)
    if filters.course_id:
        courses = courses.filter(
            Course.id == parse_uuid(filters.course_id, "course_id")
        )
    elif filters.department_id:
        courses = courses.filter(
            Course.department_id == parse_uuid(filters.department_id, "department_id")
        )
    results = []
    for course in courses.order_by(Course.name).all():
        enroll_query = db.query(Enrollment).filter(
            Enrollment.course_id == course.id,
            Enrollment.institution_id == institution_id,
        )
        if student_ids is not None:
            if not student_ids:
                continue
            enroll_query = enroll_query.filter(Enrollment.student_id.in_(student_ids))
        enrollments = enroll_query.all()
        marks = []
        pass_count = total = 0
        for enrollment in enrollments:
            if enrollment.course_result:
                total += 1
                if enrollment.course_result.end_marks is not None:
                    marks.append(enrollment.course_result.end_marks)
                if enrollment.course_result.status == "PASS":
                    pass_count += 1
        if not enrollments:
            continue
        avg_marks = sum(marks) / len(marks) if marks else 0.0
        pass_pct = (pass_count / total * 100) if total else 0.0
        results.append(
            CourseAnalytics(
                course_id=str(course.id),
                course_name=course.name,
                average_marks=round(avg_marks, 2),
                pass_percentage=round(pass_pct, 2),
            )
        )
    return results
