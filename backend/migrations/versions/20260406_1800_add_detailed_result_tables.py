"""Add detailed result tables

Revision ID: 20260406_1800
Revises: 20260406_1700
Create Date: 2026-04-06 18:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260406_1800"
down_revision = "20260406_1700"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "result_by_use",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("calculation_run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("usage_type", sa.String(length=50), nullable=False),
        sa.Column("baseline_energy_kwh_year", sa.Float(), nullable=False),
        sa.Column("scenario_energy_kwh_year", sa.Float(), nullable=False),
        sa.Column("energy_savings_percent", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["calculation_run_id"], ["calculation_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "result_by_zone",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("calculation_run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("zone_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("zone_name", sa.String(length=255), nullable=False),
        sa.Column("zone_type", sa.String(length=50), nullable=False),
        sa.Column("orientation", sa.String(length=20), nullable=False),
        sa.Column("baseline_energy_kwh_year", sa.Float(), nullable=False),
        sa.Column("scenario_energy_kwh_year", sa.Float(), nullable=False),
        sa.Column("energy_savings_percent", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["calculation_run_id"], ["calculation_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("result_by_zone")
    op.drop_table("result_by_use")
