"""Faculty-to-course assignment model."""

import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class FacultyCourse(Base, TimestampMixin, TenantMixin):
    __tablename__ = "faculty_courses"
    __table_args__ = (
        UniqueConstraint(
            "faculty_id", "course_id", "semester_id",
            name="uq_faculty_course_semester",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    faculty_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("faculty.id"), nullable=False
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False
    )
    semester_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=False
    )
    section: Mapped[str | None] = mapped_column(String(50), nullable=True)

    faculty = relationship("Faculty", back_populates="course_links")
    course = relationship("Course", back_populates="faculty_links")
    semester = relationship("Semester")
