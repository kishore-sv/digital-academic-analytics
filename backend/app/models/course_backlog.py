"""Course-level backlog lifecycle (original semester through clearance)."""

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid

BACKLOG_STATUS_NOT_CLEARED = "NOT_CLEARED"
BACKLOG_STATUS_CLEARED = "CLEARED"


class CourseBacklog(Base, TimestampMixin, TenantMixin):
    __tablename__ = "course_backlogs"
    __table_args__ = (
        UniqueConstraint(
            "institution_id",
            "student_id",
            "course_id",
            "original_semester_id",
            name="uq_course_backlogs_student_course_original_sem",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False, index=True
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False, index=True
    )
    original_semester_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=BACKLOG_STATUS_NOT_CLEARED)
    attempt_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    clearance_semester_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=True
    )
    clearance_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    grade: Mapped[str | None] = mapped_column(String(5), nullable=True)

    student = relationship("Student", back_populates="course_backlogs")
    course = relationship("Course", back_populates="course_backlogs")
    original_semester = relationship(
        "Semester", foreign_keys=[original_semester_id], back_populates="course_backlogs_originated"
    )
    clearance_semester = relationship(
        "Semester", foreign_keys=[clearance_semester_id], back_populates="course_backlogs_cleared"
    )
