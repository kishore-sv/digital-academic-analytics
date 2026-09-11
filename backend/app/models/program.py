"""Academic program model."""

import uuid

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class Program(Base, TimestampMixin, TenantMixin):
    __tablename__ = "programs"
    __table_args__ = (
        UniqueConstraint("institution_id", "code", name="uq_programs_institution_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    duration_semesters: Mapped[int] = mapped_column(Integer, default=8, nullable=False)

    department = relationship("Department", back_populates="programs")
    students = relationship("Student", back_populates="program")
