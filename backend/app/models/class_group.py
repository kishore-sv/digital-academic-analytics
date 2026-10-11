"""Class group model — batch + year of study."""

import uuid

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class ClassGroup(Base, TimestampMixin, TenantMixin):
    __tablename__ = "class_groups"
    __table_args__ = (
        UniqueConstraint("batch_id", "year_number", name="uq_class_groups_batch_year"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    batch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("batches.id"), nullable=False
    )
    year_number: Mapped[int] = mapped_column(Integer, nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    batch = relationship("Batch", back_populates="class_groups")
    sections = relationship("Section", back_populates="class_group")
    students = relationship("Student", back_populates="class_group")
