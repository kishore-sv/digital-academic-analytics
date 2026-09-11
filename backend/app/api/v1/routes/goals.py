"""Student goals API routes."""

import uuid

from app.api.deps import DbSession, StudentUser
from app.models.enrollment import SemesterResult
from app.models.prediction import StudentGoal
from app.models.student import Student
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func

router = APIRouter(prefix="/goals", tags=["goals"])


class GoalCreate(BaseModel):
    goal_type: str = Field(..., pattern="^(cgpa|sgpa)$")
    target_value: float = Field(..., ge=0, le=10)
    notes: str | None = None


class GoalUpdate(BaseModel):
    target_value: float | None = Field(default=None, ge=0, le=10)
    status: str | None = Field(default=None, pattern="^(active|completed|cancelled)$")
    notes: str | None = None


class GoalResponse(BaseModel):
    id: str
    goal_type: str
    target_value: float
    current_value: float | None
    status: str
    notes: str | None

    model_config = {"from_attributes": True}


def _get_student_for_user(db, current) -> Student:
    student = (
        db.query(Student)
        .filter(Student.user_id == current.id, Student.institution_id == current.institution_id)
        .first()
    )
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    return student


def _current_metric(db, student_id: uuid.UUID, goal_type: str) -> float | None:
    if goal_type == "cgpa":
        value = (
            db.query(func.max(SemesterResult.cgpa))
            .filter(SemesterResult.student_id == student_id)
            .scalar()
        )
    else:
        value = (
            db.query(func.max(SemesterResult.sgpa))
            .filter(SemesterResult.student_id == student_id)
            .scalar()
        )
    return float(value) if value is not None else None


def _to_response(goal: StudentGoal, current_value: float | None) -> GoalResponse:
    return GoalResponse(
        id=str(goal.id),
        goal_type=goal.goal_type,
        target_value=goal.target_value,
        current_value=current_value,
        status=goal.status,
        notes=goal.notes,
    )


@router.get("", response_model=list[GoalResponse])
def list_goals(current: StudentUser, db: DbSession):
    student = _get_student_for_user(db, current)
    goals = (
        db.query(StudentGoal)
        .filter(
            StudentGoal.student_id == student.id,
            StudentGoal.institution_id == current.institution_id,
        )
        .all()
    )
    return [
        _to_response(g, _current_metric(db, student.id, g.goal_type)) for g in goals
    ]


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(body: GoalCreate, current: StudentUser, db: DbSession):
    student = _get_student_for_user(db, current)
    current_value = _current_metric(db, student.id, body.goal_type)
    goal = StudentGoal(
        institution_id=current.institution_id,
        student_id=student.id,
        goal_type=body.goal_type,
        target_value=body.target_value,
        current_value=current_value,
        notes=body.notes,
        status="active",
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return _to_response(goal, current_value)


@router.patch("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: str, body: GoalUpdate, current: StudentUser, db: DbSession):
    student = _get_student_for_user(db, current)
    goal = (
        db.query(StudentGoal)
        .filter(
            StudentGoal.id == uuid.UUID(goal_id),
            StudentGoal.student_id == student.id,
            StudentGoal.institution_id == current.institution_id,
        )
        .first()
    )
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    if body.target_value is not None:
        goal.target_value = body.target_value
    if body.status is not None:
        goal.status = body.status
    if body.notes is not None:
        goal.notes = body.notes
    current_value = _current_metric(db, student.id, goal.goal_type)
    goal.current_value = current_value
    db.commit()
    db.refresh(goal)
    return _to_response(goal, current_value)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: str, current: StudentUser, db: DbSession):
    student = _get_student_for_user(db, current)
    goal = (
        db.query(StudentGoal)
        .filter(
            StudentGoal.id == uuid.UUID(goal_id),
            StudentGoal.student_id == student.id,
            StudentGoal.institution_id == current.institution_id,
        )
        .first()
    )
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    db.delete(goal)
    db.commit()
