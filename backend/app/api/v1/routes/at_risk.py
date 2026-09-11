"""At-risk student listing routes."""

import math

from app.api.deps import AdminOrFacultyUser, DbSession
from app.api.v1.analytics_filters import AnalyticsFilterParams, analytics_filter_dep
from app.api.v1.helpers import PaginationDep
from app.models.enrollment import Enrollment, SemesterResult
from app.models.prediction import PredictionResult
from app.models.student import Student
from app.schemas.academic import AtRiskStudentResponse
from app.schemas.analytics import AtRiskSummary
from app.schemas.common import PaginatedResponse, PaginationMeta, PaginationParams
from app.services.analytics_aggregations import (
    get_department_risk_stacks,
    get_risk_distribution_filtered,
    get_risk_factors,
    get_scoped_ids,
)
from app.services.authorization_service import get_accessible_student_ids
from fastapi import APIRouter, Depends, Query

router = APIRouter(prefix="/at-risk", tags=["at-risk"])

RISK_LEVELS = ("HIGH", "MEDIUM")


def _enrich_student(db, student: Student, prediction: PredictionResult) -> AtRiskStudentResponse:
    risk_factors = prediction.risk_factors or {}
    recommendations = prediction.recommendations or {}
    factors = risk_factors if isinstance(risk_factors, list) else list(risk_factors.keys())
    recs = recommendations if isinstance(recommendations, list) else list(recommendations.values())

    dept_name = student.department.name if student.department else None
    program_name = student.program.name if student.program else None
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student.id,
            Enrollment.institution_id == student.institution_id,
        )
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
        department_name=dept_name,
        program_name=program_name,
        semester=student.semester,
        attendance_percentage=enrollment.attendance_percentage if enrollment else None,
        cgpa=sem_result.cgpa if sem_result else None,
        backlog_count=sem_result.backlog_count if sem_result else None,
        performance_trend=sem_result.performance_trend if sem_result else None,
    )


@router.get("/summary", response_model=AtRiskSummary)
def at_risk_summary(
    current: AdminOrFacultyUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    dist = get_risk_distribution_filtered(
        db, current.institution_id, filters, scope_ids
    )
    return AtRiskSummary(
        low=dist.low,
        medium=dist.medium,
        high=dist.high,
        risk_distribution=dist,
        department_stacks=get_department_risk_stacks(
            db, current.institution_id, filters, scope_ids
        ),
        risk_factors=get_risk_factors(
            db, current.institution_id, filters, scope_ids
        ),
    )


def _apply_at_risk_filters(
    query,
    db: DbSession,
    department_name: str | None,
    semester: int | None,
    risk_level: str | None,
    performance_trend: str | None,
    attendance_band: str | None,
    cgpa_band: str | None,
):
    from sqlalchemy import func

    from app.models.department import Department

    if department_name:
        query = query.join(Department, Student.department_id == Department.id).filter(
            Department.name == department_name
        )
    if semester is not None:
        query = query.filter(Student.semester == semester)
    if risk_level:
        query = query.filter(PredictionResult.risk_level == risk_level)

    if performance_trend or cgpa_band:
        latest_sr = (
            db.query(
                SemesterResult.student_id,
                func.max(SemesterResult.created_at).label("max_created"),
            )
            .group_by(SemesterResult.student_id)
            .subquery()
        )
        query = query.join(
            SemesterResult,
            Student.id == SemesterResult.student_id,
        ).join(
            latest_sr,
            (SemesterResult.student_id == latest_sr.c.student_id)
            & (SemesterResult.created_at == latest_sr.c.max_created),
        )
        if performance_trend:
            query = query.filter(SemesterResult.performance_trend == performance_trend)
        if cgpa_band == "low":
            query = query.filter(SemesterResult.cgpa < 6.0)
        elif cgpa_band == "medium":
            query = query.filter(
                SemesterResult.cgpa >= 6.0, SemesterResult.cgpa <= 7.5
            )
        elif cgpa_band == "high":
            query = query.filter(SemesterResult.cgpa > 7.5)

    if attendance_band:
        latest_enr = (
            db.query(
                Enrollment.student_id,
                func.max(Enrollment.created_at).label("max_created"),
            )
            .group_by(Enrollment.student_id)
            .subquery()
        )
        query = query.join(
            Enrollment,
            Student.id == Enrollment.student_id,
        ).join(
            latest_enr,
            (Enrollment.student_id == latest_enr.c.student_id)
            & (Enrollment.created_at == latest_enr.c.max_created),
        )
        if attendance_band == "low":
            query = query.filter(Enrollment.attendance_percentage < 60)
        elif attendance_band == "medium":
            query = query.filter(
                Enrollment.attendance_percentage >= 60,
                Enrollment.attendance_percentage <= 75,
            )
        elif attendance_band == "high":
            query = query.filter(Enrollment.attendance_percentage > 75)

    return query


@router.get("", response_model=PaginatedResponse[AtRiskStudentResponse])
def list_at_risk_students(
    current: AdminOrFacultyUser,
    db: DbSession,
    params: PaginationParams = PaginationDep,
    department_name: str | None = Query(None),
    semester: int | None = Query(None, ge=1, le=8),
    risk_level: str | None = Query(None, pattern="^(HIGH|MEDIUM)$"),
    performance_trend: str | None = Query(
        None, pattern="^(IMPROVING|STABLE|DECLINING)$"
    ),
    attendance_band: str | None = Query(None, pattern="^(low|medium|high)$"),
    cgpa_band: str | None = Query(None, pattern="^(low|medium|high)$"),
):
    accessible = get_accessible_student_ids(db, current.user)

    from sqlalchemy import func

    latest_subq = (
        db.query(
            PredictionResult.student_id,
            func.max(PredictionResult.created_at).label("max_created"),
        )
        .filter(PredictionResult.institution_id == current.institution_id)
        .group_by(PredictionResult.student_id)
        .subquery()
    )
    query = (
        db.query(PredictionResult, Student)
        .join(Student, PredictionResult.student_id == Student.id)
        .join(
            latest_subq,
            (PredictionResult.student_id == latest_subq.c.student_id)
            & (PredictionResult.created_at == latest_subq.c.max_created),
        )
        .filter(
            PredictionResult.institution_id == current.institution_id,
            PredictionResult.risk_level.in_(RISK_LEVELS),
        )
    )

    if accessible is not None:
        if not accessible:
            query = query.filter(PredictionResult.id == None)  # noqa: E711
        else:
            query = query.filter(PredictionResult.student_id.in_(accessible))

    query = _apply_at_risk_filters(
        query,
        db,
        department_name,
        semester,
        risk_level,
        performance_trend,
        attendance_band,
        cgpa_band,
    )

    query = query.order_by(PredictionResult.risk_score.desc())
    total = query.count()
    offset = (params.page - 1) * params.limit
    rows = query.offset(offset).limit(params.limit).all()

    total_pages = max(1, math.ceil(total / params.limit)) if total else 0
    meta = PaginationMeta(
        page=params.page,
        limit=params.limit,
        total=total,
        total_pages=total_pages,
    )
    data = [_enrich_student(db, student, pred) for pred, student in rows]
    return PaginatedResponse(data=data, meta=meta)
