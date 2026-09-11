"""Prediction result and student goal models."""

import uuid

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class PredictionResult(Base, TimestampMixin, TenantMixin):
    __tablename__ = "prediction_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False
    )
    semester_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=True
    )
    predicted_end_marks: Mapped[float | None] = mapped_column(Float, nullable=True)
    pass_fail_prediction: Mapped[str | None] = mapped_column(String(10), nullable=True)
    pass_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    fail_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String(10), nullable=True)
    risk_factors: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    recommendations: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    input_features: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    student = relationship("Student", back_populates="predictions")


class StudentGoal(Base, TimestampMixin, TenantMixin):
    __tablename__ = "student_goals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False
    )
    goal_type: Mapped[str] = mapped_column(String(20), nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    student = relationship("Student", back_populates="goals")
