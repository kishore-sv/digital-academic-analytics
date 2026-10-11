"""Semester model."""

import uuid

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class Semester(Base, TimestampMixin, TenantMixin):
    __tablename__ = "semesters"
    __table_args__ = (
        UniqueConstraint(
            "institution_id",
            "academic_year_id",
            "number",
            name="uq_semesters_institution_year_number",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    academic_year_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("academic_years.id"), nullable=False
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    year_number: Mapped[int] = mapped_column(Integer, nullable=False)

    academic_year = relationship("AcademicYear", back_populates="semesters")
    enrollments = relationship("Enrollment", back_populates="semester")
    semester_results = relationship("SemesterResult", back_populates="semester")
    current_students = relationship(
        "Student",
        back_populates="current_semester",
        foreign_keys="Student.current_semester_id",
    )
    faculty_course_links = relationship("FacultyCourse", back_populates="semester")
    course_backlogs_originated = relationship(
        "CourseBacklog",
        back_populates="original_semester",
        foreign_keys="CourseBacklog.original_semester_id",
    )
    course_backlogs_cleared = relationship(
        "CourseBacklog",
        back_populates="clearance_semester",
        foreign_keys="CourseBacklog.clearance_semester_id",
    )
