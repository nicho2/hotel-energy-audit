"""Add BACS tables

Revision ID: 20260406_1600
Revises: 20260406_1500
Create Date: 2026-04-06 16:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260406_1600"
down_revision = "20260406_1500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "bacs_assessments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version", sa.String(length=20), nullable=False),
        sa.Column("assessor_name", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id"),
    )
    op.create_table(
        "bacs_function_definitions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("domain", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("version", sa.String(length=20), nullable=False, server_default=sa.text("'v1'")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "bacs_selected_functions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("assessment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("function_definition_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["assessment_id"], ["bacs_assessments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["function_definition_id"],
            ["bacs_function_definitions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "assessment_id",
            "function_definition_id",
            name="uq_bacs_selected_functions_assessment_function",
        ),
    )


def downgrade() -> None:
    op.drop_table("bacs_selected_functions")
    op.drop_table("bacs_function_definitions")
    op.drop_table("bacs_assessments")
