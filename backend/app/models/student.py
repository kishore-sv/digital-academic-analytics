"""Student model."""

import uuid

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class Student(Base, TimestampMixin, TenantMixin):
    __tablename__ = "students"
    __table_args__ = (
        UniqueConstraint("institution_id", "roll_number", name="uq_students_institution_roll"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    roll_number: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False
    )
    program_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("programs.id"), nullable=True
    )
    semester: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    branch: Mapped[str] = mapped_column(String(50), default="CSE", nullable=False)
    section: Mapped[str | None] = mapped_column(String(50), nullable=True)

    user = relationship("User", back_populates="student")
    department = relationship("Department", back_populates="students")
    program = relationship("Program", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
    semester_results = relationship("SemesterResult", back_populates="student")
    goals = relationship("StudentGoal", back_populates="student")
    predictions = relationship("PredictionResult", back_populates="student")
    parent_links = relationship("ParentStudent", back_populates="student")
    faculty_links = relationship("FacultyStudent", back_populates="student")
