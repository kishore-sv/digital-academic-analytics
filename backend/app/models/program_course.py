"""Program curriculum mapping — program, course, semester number."""

import uuid

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class ProgramCourse(Base, TimestampMixin, TenantMixin):
    __tablename__ = "program_courses"
    __table_args__ = (
        UniqueConstraint(
            "program_id",
            "course_id",
            "semester_number",
            name="uq_program_courses_program_course_semester",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    program_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("programs.id"), nullable=False
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False
    )
    semester_number: Mapped[int] = mapped_column(Integer, nullable=False)

    program = relationship("Program", back_populates="program_courses")
    course = relationship("Course", back_populates="program_courses")
