"""Add faculty_courses table and student section column."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "4ce6162e84c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("students", sa.Column("section", sa.String(50), nullable=True))
    op.create_table(
        "faculty_courses",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("faculty_id", sa.UUID(), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=False),
        sa.Column("semester_id", sa.UUID(), nullable=False),
        sa.Column("section", sa.String(50), nullable=True),
        sa.Column("institution_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"]),
        sa.ForeignKeyConstraint(["faculty_id"], ["faculty.id"]),
        sa.ForeignKeyConstraint(["institution_id"], ["institutions.id"]),
        sa.ForeignKeyConstraint(["semester_id"], ["semesters.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("faculty_id", "course_id", "semester_id", name="uq_faculty_course_semester"),
    )


def downgrade() -> None:
    op.drop_table("faculty_courses")
    op.drop_column("students", "section")
