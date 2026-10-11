"""Student intake batch (cohort) model."""

import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class Batch(Base, TimestampMixin, TenantMixin):
    __tablename__ = "batches"
    __table_args__ = (
        UniqueConstraint(
            "institution_id",
            "program_id",
            "admission_year",
            name="uq_batches_institution_program_year",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    program_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("programs.id"), nullable=False
    )
    admission_year: Mapped[int] = mapped_column(Integer, nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    program = relationship("Program", back_populates="batches")
    class_groups = relationship("ClassGroup", back_populates="batch")
    students = relationship("Student", back_populates="batch")
