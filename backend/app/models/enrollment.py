"""Enrollment and academic data models."""

import uuid
from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class Enrollment(Base, TimestampMixin, TenantMixin):
    __tablename__ = "enrollments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False
    )
    semester_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=False
    )
    attendance_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)
    study_hours_per_week: Mapped[float | None] = mapped_column(Float, nullable=True)
    assignment_completion_pct: Mapped[float | None] = mapped_column(Float, nullable=True)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    semester = relationship("Semester", back_populates="enrollments")
    assessment_marks = relationship("AssessmentMark", back_populates="enrollment")
    course_result = relationship("CourseResult", back_populates="enrollment", uselist=False)
    attendances = relationship("Attendance", back_populates="enrollment")


class Assessment(Base, TimestampMixin, TenantMixin):
    __tablename__ = "assessments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    assessment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    max_marks: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    date: Mapped[date | None] = mapped_column(Date, nullable=True)

    course = relationship("Course", back_populates="assessments")
    marks = relationship("AssessmentMark", back_populates="assessment")


class AssessmentMark(Base, TimestampMixin, TenantMixin):
    __tablename__ = "assessment_marks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    enrollment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("enrollments.id"), nullable=False
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False
    )
    marks_obtained: Mapped[float] = mapped_column(Float, nullable=False)

    enrollment = relationship("Enrollment", back_populates="assessment_marks")
    assessment = relationship("Assessment", back_populates="marks")


class Attendance(Base, TimestampMixin, TenantMixin):
    __tablename__ = "attendances"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    enrollment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("enrollments.id"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    enrollment = relationship("Enrollment", back_populates="attendances")


class CourseResult(Base, TimestampMixin, TenantMixin):
    __tablename__ = "course_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    enrollment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("enrollments.id"), nullable=False, unique=True
    )
    grade: Mapped[str | None] = mapped_column(String(5), nullable=True)
    end_marks: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(10), default="PASS", nullable=False)

    enrollment = relationship("Enrollment", back_populates="course_result")


class SemesterResult(Base, TimestampMixin, TenantMixin):
    __tablename__ = "semester_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False
    )
    semester_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("semesters.id"), nullable=False
    )
    sgpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    cgpa: Mapped[float | None] = mapped_column(Float, nullable=True)
    backlog_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_failed_courses: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    low_performance_course_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    performance_trend: Mapped[str] = mapped_column(String(20), default="STABLE", nullable=False)

    student = relationship("Student", back_populates="semester_results")
    semester = relationship("Semester", back_populates="semester_results")
