"""Section model — subdivision of a class group."""

import uuid

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TenantMixin, TimestampMixin, new_uuid


class Section(Base, TimestampMixin, TenantMixin):
    __tablename__ = "sections"
    __table_args__ = (
        UniqueConstraint("class_group_id", "code", name="uq_sections_class_group_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=new_uuid
    )
    class_group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("class_groups.id"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    class_group = relationship("ClassGroup", back_populates="sections")
    students = relationship("Student", back_populates="section")
    enrollments = relationship("Enrollment", back_populates="section")
    faculty_course_links = relationship("FacultyCourse", back_populates="section")
