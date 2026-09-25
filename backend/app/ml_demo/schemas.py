"""Pydantic validation for ML demo form inputs."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

PerformanceTrend = Literal["IMPROVING", "STABLE", "DECLINING"]
CourseType = Literal["THEORY", "LAB", "PROJECT", "INTERNSHIP", "NON_CREDIT"]


class Model1DemoInput(BaseModel):
    CA_mark: float = Field(ge=0, le=100)
    MID_mark: float = Field(ge=0, le=100)
    attendance_percentage: float = Field(ge=0, le=100)
    study_hours_per_week: float = Field(ge=0, le=80)
    assignment_completion_pct: float = Field(ge=0, le=100)
    previous_sgpa: float = Field(ge=0, le=10)
    previous_cgpa: float = Field(ge=0, le=10)
    backlog_count: int = Field(ge=0, le=20)
    course_credits: int = Field(ge=1, le=10)
    course_type: CourseType = "THEORY"
    branch: str = Field(min_length=2, max_length=20)
    semester: int = Field(ge=1, le=8)


class Model2DemoInput(BaseModel):
    CA_mark: float = Field(ge=0, le=100)
    MID_mark: float = Field(ge=0, le=100)
    attendance_percentage: float = Field(ge=0, le=100)
    study_hours_per_week: float = Field(ge=0, le=80)
    assignment_completion_pct: float = Field(ge=0, le=100)
    previous_sgpa: float = Field(ge=0, le=10)
    previous_cgpa: float = Field(ge=0, le=10)
    backlog_count: int = Field(ge=0, le=20)
    course_credits: int = Field(ge=1, le=10)
    branch: str = Field(min_length=2, max_length=20)
    semester: int = Field(ge=1, le=8)


class Model3DemoInput(BaseModel):
    attendance_percentage: float = Field(ge=0, le=100)
    previous_cgpa: float = Field(ge=0, le=10)
    backlog_count: int = Field(ge=0, le=20)
    current_failed_courses: int = Field(ge=0, le=20)
    low_performance_course_count: int = Field(ge=0, le=20)
    study_hours_per_week: float = Field(ge=0, le=80)
    assignment_completion_percentage: float = Field(ge=0, le=100)
    performance_trend: PerformanceTrend

    @field_validator("performance_trend", mode="before")
    @classmethod
    def normalize_trend(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().upper()
        return value
