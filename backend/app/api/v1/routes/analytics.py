"""Analytics API routes."""

from app.api.deps import AdminUser, CurrentUserDep, DbSession
from app.api.v1.analytics_filters import AnalyticsFilterParams, analytics_filter_dep
from app.schemas.analytics import (
    ActualVsPredictedPoint,
    AttendancePerformancePoint,
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
from app.services.analytics_aggregations import (
    get_actual_vs_predicted,
    get_attendance_performance,
    get_cgpa_distribution,
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
    get_scoped_ids,
)
from app.services.analytics_service import get_course_analytics
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=OverviewStats)
def analytics_overview(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_filtered_overview(db, current.institution_id, filters)


@router.get("/departments", response_model=list[DepartmentAnalytics])
def analytics_departments(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_department_analytics_filtered(db, current.institution_id, filters)


@router.get("/courses", response_model=list[CourseAnalytics])
def analytics_courses(current: AdminUser, db: DbSession):
    return get_course_analytics(db, current.institution_id)


@router.get("/performance-trends", response_model=list[PerformanceTrendPoint])
def analytics_performance_trends(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_performance_trends_filtered(db, current.institution_id, filters)


@router.get("/risk-distribution", response_model=RiskDistribution)
def analytics_risk_distribution(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_risk_distribution_filtered(db, current.institution_id, filters)


@router.get("/pass-fail")
def analytics_pass_fail(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    overview = get_filtered_overview(db, current.institution_id, filters)
    return {"pass_percentage": overview.pass_percentage}


@router.get("/cgpa-distribution")
def analytics_cgpa_distribution(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_cgpa_distribution(db, current.institution_id, filters)


@router.get("/pass-fail-trend", response_model=list[PassFailTrendPoint])
def analytics_pass_fail_trend(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_pass_fail_trend(db, current.institution_id, filters)


@router.get("/attendance-performance", response_model=list[AttendancePerformancePoint])
def analytics_attendance_performance(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_attendance_performance(db, current.institution_id, filters)


@router.get("/performance-indicators", response_model=PerformanceIndicators)
def analytics_performance_indicators(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_performance_indicators(db, current.institution_id, filters)


@router.get("/department-risk-stacks", response_model=list[DepartmentRiskStack])
def analytics_department_risk_stacks(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_department_risk_stacks(db, current.institution_id, filters)


@router.get("/risk-factors", response_model=list[RiskFactorCount])
def analytics_risk_factors(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_risk_factors(db, current.institution_id, filters)


@router.get("/predictions/performance", response_model=PredictionPerformanceAnalytics)
def analytics_prediction_performance(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_prediction_performance_analytics(db, current.institution_id, filters)


@router.get("/predictions/pass-fail", response_model=PredictionPassFailAnalytics)
def analytics_prediction_pass_fail(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_prediction_pass_fail_analytics(db, current.institution_id, filters)


@router.get("/predictions/risk", response_model=PredictionRiskAnalytics)
def analytics_prediction_risk(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_prediction_risk_analytics(db, current.institution_id, filters)


@router.get("/predictions/actual-vs-predicted", response_model=list[ActualVsPredictedPoint])
def analytics_actual_vs_predicted(
    current: AdminUser,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    return get_actual_vs_predicted(db, current.institution_id, filters)


# --- Scoped endpoints for faculty/student/parent ---


@router.get("/scoped/overview", response_model=OverviewStats)
def scoped_analytics_overview(
    current: CurrentUserDep,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    return get_filtered_overview(db, current.institution_id, filters, scope_ids)


@router.get("/scoped/risk-distribution", response_model=RiskDistribution)
def scoped_risk_distribution(
    current: CurrentUserDep,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    return get_risk_distribution_filtered(
        db, current.institution_id, filters, scope_ids
    )


@router.get("/scoped/departments", response_model=list[DepartmentAnalytics])
def scoped_departments(
    current: CurrentUserDep,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    return get_department_analytics_filtered(
        db, current.institution_id, filters, scope_ids
    )


@router.get("/scoped/performance-trends", response_model=list[PerformanceTrendPoint])
def scoped_performance_trends(
    current: CurrentUserDep,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    return get_performance_trends_filtered(
        db, current.institution_id, filters, scope_ids
    )


@router.get("/scoped/cgpa-distribution")
def scoped_cgpa_distribution(
    current: CurrentUserDep,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    return get_cgpa_distribution(db, current.institution_id, filters, scope_ids)


@router.get("/scoped/attendance-performance", response_model=list[AttendancePerformancePoint])
def scoped_attendance_performance(
    current: CurrentUserDep,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    return get_attendance_performance(
        db, current.institution_id, filters, scope_ids
    )


@router.get("/scoped/predictions/risk", response_model=PredictionRiskAnalytics)
def scoped_prediction_risk(
    current: CurrentUserDep,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    return get_prediction_risk_analytics(
        db, current.institution_id, filters, scope_ids
    )


@router.get("/scoped/department-risk-stacks", response_model=list[DepartmentRiskStack])
def scoped_department_risk_stacks(
    current: CurrentUserDep,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    return get_department_risk_stacks(
        db, current.institution_id, filters, scope_ids
    )


@router.get("/scoped/risk-factors", response_model=list[RiskFactorCount])
def scoped_risk_factors(
    current: CurrentUserDep,
    db: DbSession,
    filters: AnalyticsFilterParams = Depends(analytics_filter_dep),
):
    scope_ids = get_scoped_ids(db, current.user)
    return get_risk_factors(db, current.institution_id, filters, scope_ids)
