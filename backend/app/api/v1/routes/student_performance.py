"""Student performance and analytics routes."""

from app.api.deps import CurrentUserDep, DbSession, StudentUser
from app.api.v1.helpers import parse_uuid
from app.models.student import Student
from app.schemas.academic import GoalGuidanceResponse, StudentPerformanceResponse
from app.services.authorization_service import assert_student_access
from app.services.student_performance_service import (
    build_goal_guidance,
    build_student_performance,
)
from fastapi import APIRouter, HTTPException, Query, status

router = APIRouter(prefix="/students", tags=["student-performance"])


def _get_student_for_user(db, current) -> Student:
    student = (
        db.query(Student)
        .filter(Student.user_id == current.id, Student.institution_id == current.institution_id)
        .first()
    )
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    return student


@router.get("/me/performance", response_model=StudentPerformanceResponse)
def get_my_performance(current: StudentUser, db: DbSession):
    student = _get_student_for_user(db, current)
    data = build_student_performance(db, student.id, current.institution_id)
    return StudentPerformanceResponse(**data)


@router.get("/{student_id}/performance", response_model=StudentPerformanceResponse)
def get_student_performance(student_id: str, current: CurrentUserDep, db: DbSession):
    sid = parse_uuid(student_id, "student_id")
    assert_student_access(db, current, sid)
    data = build_student_performance(db, sid, current.institution_id)
    return StudentPerformanceResponse(**data)


@router.get("/me/goal-guidance", response_model=GoalGuidanceResponse)
def get_my_goal_guidance(
    current: StudentUser,
    db: DbSession,
    target_cgpa: float | None = Query(None, ge=0, le=10),
):
    student = _get_student_for_user(db, current)
    data = build_goal_guidance(db, student.id, current.institution_id, target_cgpa)
    return GoalGuidanceResponse(**data)
