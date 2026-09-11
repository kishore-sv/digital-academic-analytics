"""API v1 router aggregator."""

from app.api.v1.routes import (
    academic,
    analytics,
    assessments,
    at_risk,
    attendance,
    auth,
    courses,
    departments,
    faculty,
    goals,
    institutions,
    parents,
    predictions,
    programs,
    reports,
    results,
    student_performance,
    students,
    users,
)
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(institutions.router)
api_router.include_router(departments.router)
api_router.include_router(programs.router)
api_router.include_router(faculty.router)
api_router.include_router(parents.router)
api_router.include_router(students.router)
api_router.include_router(student_performance.router)
api_router.include_router(courses.router)
api_router.include_router(academic.router)
api_router.include_router(assessments.router)
api_router.include_router(attendance.router)
api_router.include_router(results.router)
api_router.include_router(at_risk.router)
api_router.include_router(predictions.router)
api_router.include_router(analytics.router)
api_router.include_router(goals.router)
api_router.include_router(reports.router)
