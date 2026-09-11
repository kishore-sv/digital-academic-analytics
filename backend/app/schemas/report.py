"""Report preview and export schemas."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.academic import AtRiskStudentResponse
from app.schemas.analytics import (
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


class ReportFilterLabels(BaseModel):
    academic_year: str = "All Academic Years"
    semester: str = "All Semesters"
    department: str = "Institution"
    program: str = "All Programs"
    course: str = "All Courses"
    risk_level: str = "All Risk Levels"


class ReportHeader(BaseModel):
    institution_name: str
    title: str = "Academic Performance Report"
    scope: str = "institution"
    generated_at: datetime
    filters: ReportFilterLabels


class ReportKPIs(BaseModel):
    overview: OverviewStats
    average_attendance: float = 0.0
    fail_percentage: float = 0.0
    average_predicted_marks: float = 0.0
    average_pass_probability: float = 0.0
    average_risk_score: float = 0.0


class ReportContext(BaseModel):
    header: ReportHeader
    kpis: ReportKPIs
    cgpa_distribution: list[ChartBucket] = Field(default_factory=list)
    sgpa_distribution: list[ChartBucket] = Field(default_factory=list)
    performance_trends: list[PerformanceTrendPoint] = Field(default_factory=list)
    course_performance: list[CourseAnalytics] = Field(default_factory=list)
    pass_fail_trend: list[PassFailTrendPoint] = Field(default_factory=list)
    attendance_distribution: list[ChartBucket] = Field(default_factory=list)
    attendance_performance: list[AttendancePerformancePoint] = Field(default_factory=list)
    performance_indicators: PerformanceIndicators = Field(default_factory=PerformanceIndicators)
    prediction_performance: PredictionPerformanceAnalytics = Field(
        default_factory=PredictionPerformanceAnalytics
    )
    prediction_pass_fail: PredictionPassFailAnalytics = Field(
        default_factory=PredictionPassFailAnalytics
    )
    prediction_risk: PredictionRiskAnalytics = Field(default_factory=PredictionRiskAnalytics)
    risk_distribution: RiskDistribution = Field(default_factory=RiskDistribution)
    risk_factors: list[RiskFactorCount] = Field(default_factory=list)
    department_analytics: list[DepartmentAnalytics] = Field(default_factory=list)
    department_risk_stacks: list[DepartmentRiskStack] = Field(default_factory=list)
    at_risk_students: list[AtRiskStudentResponse] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)
