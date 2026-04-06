"""Add buildings table

Revision ID: 20260406_1300
Revises: 20260406_1200
Create Date: 2026-04-06 13:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260406_1300"
down_revision = "20260406_1200"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "buildings",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("construction_period", sa.String(length=50), nullable=True),
        sa.Column("gross_floor_area_m2", sa.Float(), nullable=True),
        sa.Column("heated_area_m2", sa.Float(), nullable=True),
        sa.Column("cooled_area_m2", sa.Float(), nullable=True),
        sa.Column("number_of_floors", sa.Integer(), nullable=True),
        sa.Column("number_of_rooms", sa.Integer(), nullable=True),
        sa.Column("main_orientation", sa.String(length=20), nullable=True),
        sa.Column("compactness_level", sa.String(length=50), nullable=True),
        sa.Column("has_restaurant", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("has_meeting_rooms", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("has_spa", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("has_pool", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id"),
    )


def downgrade() -> None:
    op.drop_table("buildings")
