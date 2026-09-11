"""Build unified report context from filtered academic data."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.v1.analytics_filters import AnalyticsFilterParams
from app.api.v1.helpers import parse_uuid
from app.models.academic_year import AcademicYear
from app.models.course import Course
from app.models.department import Department
from app.models.enrollment import Enrollment, SemesterResult
from app.models.institution import Institution
from app.models.prediction import PredictionResult
from app.models.program import Program
from app.models.semester import Semester
from app.models.student import Student
from app.schemas.academic import AtRiskStudentResponse
from app.schemas.report import ReportContext, ReportFilterLabels, ReportHeader, ReportKPIs
from app.services.analytics_aggregations import (
    get_attendance_distribution,
    get_attendance_performance,
    get_average_attendance_filtered,
    get_cgpa_distribution,
    get_course_analytics_filtered,
    get_department_analytics_filtered,
    get_department_risk_stacks,
    get_filtered_overview,
    get_pass_fail_trend,
    get_performance_indicators,
    get_performance_trends_filtered,
    get_prediction_pass_fail_analytics,
    get_prediction_performance_analytics,
    get_prediction_risk_analytics,
    get_risk_distribution_filtered,
    get_risk_factors,
    get_sgpa_distribution,
)
from app.services.report_findings import generate_key_findings


def _resolve_filter_labels(db: Session, institution_id: uuid.UUID, filters: AnalyticsFilterParams) -> ReportFilterLabels:
    labels = ReportFilterLabels()
    if filters.academic_year_id:
        year = db.query(AcademicYear).filter(
            AcademicYear.id == parse_uuid(filters.academic_year_id, "academic_year_id"),
            AcademicYear.institution_id == institution_id,
        ).first()
        if year:
            labels.academic_year = year.name
    if filters.semester_id:
        sem = db.query(Semester).filter(
            Semester.id == parse_uuid(filters.semester_id, "semester_id"),
            Semester.institution_id == institution_id,
        ).first()
        if sem:
            labels.semester = sem.name
    if filters.department_id:
        dept = db.query(Department).filter(
            Department.id == parse_uuid(filters.department_id, "department_id"),
            Department.institution_id == institution_id,
        ).first()
        if dept:
            labels.department = dept.name
    if filters.program_id:
        program = db.query(Program).filter(
            Program.id == parse_uuid(filters.program_id, "program_id"),
            Program.institution_id == institution_id,
        ).first()
        if program:
            labels.program = program.name
    if filters.course_id:
        course = db.query(Course).filter(
            Course.id == parse_uuid(filters.course_id, "course_id"),
            Course.institution_id == institution_id,
        ).first()
        if course:
            labels.course = course.name
    if filters.risk_level:
        labels.risk_level = filters.risk_level
    return labels


def _resolve_scope(filters: AnalyticsFilterParams) -> str:
    if filters.course_id:
        return "course"
    if filters.program_id:
        return "program"
    if filters.department_id:
        return "department"
    if filters.semester_id:
        return "semester"
    return "institution"


def _enrich_at_risk_row(db: Session, student: Student, prediction: PredictionResult) -> AtRiskStudentResponse:
    risk_factors = prediction.risk_factors or {}
    recommendations = prediction.recommendations or {}
    factors = risk_factors if isinstance(risk_factors, list) else list(risk_factors.keys())
    recs = recommendations if isinstance(recommendations, list) else list(recommendations.values())
    enrollment = (
        db.query(Enrollment)
        .filter(Enrollment.student_id == student.id, Enrollment.institution_id == student.institution_id)
        .order_by(Enrollment.created_at.desc())
        .first()
    )
    sem_result = (
        db.query(SemesterResult)
        .filter(SemesterResult.student_id == student.id)
        .order_by(SemesterResult.created_at.desc())
        .first()
    )
    return AtRiskStudentResponse(
        student_id=str(student.id),
        student_name=student.name,
        roll_number=student.roll_number,
        risk_score=prediction.risk_score or 0.0,
        risk_level=prediction.risk_level or "UNKNOWN",
        risk_factors=factors,
        recommendations=recs,
        predicted_at=prediction.created_at,
        department_name=student.department.name if student.department else None,
        program_name=student.program.name if student.program else None,
        semester=student.semester,
        attendance_percentage=enrollment.attendance_percentage if enrollment else None,
        cgpa=sem_result.cgpa if sem_result else None,
        backlog_count=sem_result.backlog_count if sem_result else None,
        performance_trend=sem_result.performance_trend if sem_result else None,
    )


def get_filtered_at_risk_students(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams,
    scope_ids: list[uuid.UUID] | None = None,
    limit: int = 100,
) -> list[AtRiskStudentResponse]:
    from app.services.analytics_aggregations import _latest_predictions, _student_ids_for_filters

    student_ids = _student_ids_for_filters(db, institution_id, filters, scope_ids)
    preds = _latest_predictions(db, institution_id, student_ids)
    risk_levels = {filters.risk_level} if filters.risk_level else {"LOW", "MEDIUM", "HIGH"}
    rows: list[AtRiskStudentResponse] = []
    for pred in sorted(preds, key=lambda p: p.risk_score or 0, reverse=True):
        if pred.risk_level not in risk_levels:
            continue
        student = db.query(Student).filter(Student.id == pred.student_id).first()
        if not student:
            continue
        rows.append(_enrich_at_risk_row(db, student, pred))
        if len(rows) >= limit:
            break
    return rows


def build_report_context(
    db: Session,
    institution_id: uuid.UUID,
    filters: AnalyticsFilterParams | None = None,
    scope_ids: list[uuid.UUID] | None = None,
) -> ReportContext:
    filters = filters or AnalyticsFilterParams()
    institution = db.query(Institution).filter(Institution.id == institution_id).first()
    labels = _resolve_filter_labels(db, institution_id, filters)
    overview = get_filtered_overview(db, institution_id, filters, scope_ids)
    pass_fail = get_pass_fail_trend(db, institution_id, filters, scope_ids)
    total_pass = sum(p.pass_count for p in pass_fail)
    total_fail = sum(p.fail_count for p in pass_fail)
    total_results = total_pass + total_fail
    fail_pct = (total_fail / total_results * 100) if total_results else 0.0
    pred_perf = get_prediction_performance_analytics(db, institution_id, filters, scope_ids)
    pred_pass_fail = get_prediction_pass_fail_analytics(db, institution_id, filters, scope_ids)
    pred_risk = get_prediction_risk_analytics(db, institution_id, filters, scope_ids)

    context = ReportContext(
        header=ReportHeader(
            institution_name=institution.name if institution else "Institution",
            scope=_resolve_scope(filters),
            generated_at=datetime.now(UTC),
            filters=labels,
        ),
        kpis=ReportKPIs(
            overview=overview,
            average_attendance=get_average_attendance_filtered(db, institution_id, filters, scope_ids),
            fail_percentage=round(fail_pct, 2),
            average_predicted_marks=pred_perf.average_predicted_marks,
            average_pass_probability=pred_pass_fail.average_pass_probability,
            average_risk_score=pred_risk.average_risk_score,
        ),
        cgpa_distribution=get_cgpa_distribution(db, institution_id, filters, scope_ids),
        sgpa_distribution=get_sgpa_distribution(db, institution_id, filters, scope_ids),
        performance_trends=get_performance_trends_filtered(db, institution_id, filters, scope_ids),
        course_performance=get_course_analytics_filtered(db, institution_id, filters, scope_ids),
        pass_fail_trend=pass_fail,
        attendance_distribution=get_attendance_distribution(db, institution_id, filters, scope_ids),
        attendance_performance=get_attendance_performance(db, institution_id, filters, scope_ids),
        performance_indicators=get_performance_indicators(db, institution_id, filters, scope_ids),
        prediction_performance=pred_perf,
        prediction_pass_fail=pred_pass_fail,
        prediction_risk=pred_risk,
        risk_distribution=get_risk_distribution_filtered(db, institution_id, filters, scope_ids),
        risk_factors=get_risk_factors(db, institution_id, filters, scope_ids),
        department_analytics=get_department_analytics_filtered(db, institution_id, filters, scope_ids),
        department_risk_stacks=get_department_risk_stacks(db, institution_id, filters, scope_ids),
        at_risk_students=get_filtered_at_risk_students(db, institution_id, filters, scope_ids),
    )
    context.findings = generate_key_findings(context)
    return context
