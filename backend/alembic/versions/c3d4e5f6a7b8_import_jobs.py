"""Import jobs table.

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "c3d4e5f6a7b8"
down_revision = "b2c3d4e5f6a7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "import_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("institution_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("import_type", sa.String(length=64), nullable=False),
        sa.Column("filename", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("uploaded_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("column_mapping", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("raw_rows", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("row_errors", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("total_rows", sa.Integer(), nullable=False),
        sa.Column("valid_rows", sa.Integer(), nullable=False),
        sa.Column("invalid_rows", sa.Integer(), nullable=False),
        sa.Column("duplicate_rows", sa.Integer(), nullable=False),
        sa.Column("created_rows", sa.Integer(), nullable=False),
        sa.Column("failed_rows", sa.Integer(), nullable=False),
        sa.Column("error_summary", sa.Text(), nullable=True),
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
        sa.ForeignKeyConstraint(["uploaded_by_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_import_jobs_import_type", "import_jobs", ["import_type"])
    op.create_index("ix_import_jobs_institution_id", "import_jobs", ["institution_id"])


def downgrade() -> None:
    op.drop_index("ix_import_jobs_institution_id", table_name="import_jobs")
    op.drop_index("ix_import_jobs_import_type", table_name="import_jobs")
    op.drop_table("import_jobs")
