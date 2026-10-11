"""Faculty-to-course assignment model."""

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class FacultyCourse(Base, TimestampMixin, TenantMixin):
    __tablename__ = "faculty_courses"

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
    section_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sections.id"), nullable=True
    )

    faculty = relationship("Faculty", back_populates="course_links")
    course = relationship("Course", back_populates="faculty_links")
    semester = relationship("Semester", back_populates="faculty_course_links")
    section = relationship("Section", back_populates="faculty_course_links")
