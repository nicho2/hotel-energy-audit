"""Add building zones table

Revision ID: 20260406_1400
Revises: 20260406_1300
Create Date: 2026-04-06 14:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260406_1400"
down_revision = "20260406_1300"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "building_zones",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("zone_type", sa.String(length=50), nullable=False),
        sa.Column("orientation", sa.String(length=20), nullable=False),
        sa.Column("area_m2", sa.Float(), nullable=False),
        sa.Column("room_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("building_zones")
