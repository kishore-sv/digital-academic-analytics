"""Course backlogs table.

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "d4e5f6a7b8c9"
down_revision = "c3d4e5f6a7b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "course_backlogs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("institution_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("original_semester_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=True),
        sa.Column("clearance_semester_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("clearance_date", sa.Date(), nullable=True),
        sa.Column("grade", sa.String(length=5), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["institution_id"], ["institutions.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"]),
        sa.ForeignKeyConstraint(["original_semester_id"], ["semesters.id"]),
        sa.ForeignKeyConstraint(["clearance_semester_id"], ["semesters.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "institution_id",
            "student_id",
            "course_id",
            "original_semester_id",
            name="uq_course_backlogs_student_course_original_sem",
        ),
    )
    op.create_index("ix_course_backlogs_institution_id", "course_backlogs", ["institution_id"])
    op.create_index("ix_course_backlogs_student_id", "course_backlogs", ["student_id"])


def downgrade() -> None:
    op.drop_index("ix_course_backlogs_student_id", table_name="course_backlogs")
    op.drop_index("ix_course_backlogs_institution_id", table_name="course_backlogs")
    op.drop_table("course_backlogs")
