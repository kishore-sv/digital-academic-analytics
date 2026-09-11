"""Analytics response schemas."""

from pydantic import BaseModel


class OverviewStats(BaseModel):
    total_students: int = 0
    total_faculty: int = 0
    total_departments: int = 0
    average_cgpa: float = 0.0
    average_sgpa: float = 0.0
    pass_percentage: float = 0.0
    at_risk_percentage: float = 0.0
    high_risk_count: int = 0


class DepartmentAnalytics(BaseModel):
    department_id: str
    department_name: str
    average_cgpa: float = 0.0
    pass_percentage: float = 0.0
    student_count: int = 0


class RiskDistribution(BaseModel):
    low: int = 0
    medium: int = 0
    high: int = 0


class PerformanceTrendPoint(BaseModel):
    semester: str
    average_sgpa: float | None = None
    average_cgpa: float | None = None
    pass_percentage: float | None = None


class CourseAnalytics(BaseModel):
    course_id: str
    course_name: str
    average_marks: float = 0.0
    pass_percentage: float = 0.0


class ChartBucket(BaseModel):
    label: str
    value: float


class PassFailTrendPoint(BaseModel):
    semester: str
    pass_count: int = 0
    fail_count: int = 0


class AttendancePerformancePoint(BaseModel):
    attendance_percentage: float
    performance_value: float


class PerformanceIndicators(BaseModel):
    improving: int = 0
    stable: int = 0
    declining: int = 0


class DepartmentRiskStack(BaseModel):
    department_id: str
    department_name: str
    low: int = 0
    medium: int = 0
    high: int = 0


class RiskFactorCount(BaseModel):
    factor: str
    count: int


class PredictionPerformanceAnalytics(BaseModel):
    average_predicted_marks: float = 0.0
    distribution: list[ChartBucket] = []
    department_averages: list[ChartBucket] = []


class PredictionPassFailAnalytics(BaseModel):
    predicted_pass_count: int = 0
    predicted_fail_count: int = 0
    average_pass_probability: float = 0.0
    probability_distribution: list[ChartBucket] = []
    department_pass_rates: list[ChartBucket] = []


class PredictionRiskAnalytics(BaseModel):
    average_risk_score: float = 0.0
    risk_distribution: RiskDistribution = RiskDistribution()
    department_stacks: list[DepartmentRiskStack] = []
    score_distribution: list[ChartBucket] = []


class ActualVsPredictedPoint(BaseModel):
    student_name: str
    actual: float
    predicted: float


class AtRiskSummary(BaseModel):
    low: int = 0
    medium: int = 0
    high: int = 0
    risk_distribution: RiskDistribution = RiskDistribution()
    department_stacks: list[DepartmentRiskStack] = []
    risk_factors: list[RiskFactorCount] = []
