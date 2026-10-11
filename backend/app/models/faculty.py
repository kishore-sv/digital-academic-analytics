"""Faculty model."""

import uuid

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class Faculty(Base, TimestampMixin, TenantMixin):
    __tablename__ = "faculty"
    __table_args__ = (
        UniqueConstraint(
            "institution_id",
            "employee_id",
            name="uq_faculty_institution_employee_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    employee_id: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False
    )
    designation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)

    user = relationship("User", back_populates="faculty")
    department = relationship("Department", back_populates="faculty_members")
    student_links = relationship("FacultyStudent", back_populates="faculty")
    course_links = relationship("FacultyCourse", back_populates="faculty")
