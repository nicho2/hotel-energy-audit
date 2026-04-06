"""Add technical systems table

Revision ID: 20260406_1500
Revises: 20260406_1400
Create Date: 2026-04-06 15:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260406_1500"
down_revision = "20260406_1400"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "technical_systems",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("system_type", sa.String(length=50), nullable=False),
        sa.Column("energy_source", sa.String(length=50), nullable=True),
        sa.Column("serves", sa.String(length=255), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("year_installed", sa.Integer(), nullable=True),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("technical_systems")
