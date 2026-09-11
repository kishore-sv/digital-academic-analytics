"""Shared query filters for analytics endpoints."""

from fastapi import Query
from pydantic import BaseModel


class AnalyticsFilterParams(BaseModel):
    academic_year_id: str | None = None
    semester_id: str | None = None
    department_id: str | None = None
    program_id: str | None = None
    course_id: str | None = None
    risk_level: str | None = None


def analytics_filter_dep(
    academic_year_id: str | None = Query(None),
    semester_id: str | None = Query(None),
    department_id: str | None = Query(None),
    program_id: str | None = Query(None),
    course_id: str | None = Query(None),
    risk_level: str | None = Query(None, pattern="^(LOW|MEDIUM|HIGH)$"),
) -> AnalyticsFilterParams:
    return AnalyticsFilterParams(
        academic_year_id=academic_year_id,
        semester_id=semester_id,
        department_id=department_id,
        program_id=program_id,
        course_id=course_id,
        risk_level=risk_level,
    )
