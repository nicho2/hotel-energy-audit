"""Add scenarios and calculation result tables

Revision ID: 20260406_1700
Revises: 20260406_1600
Create Date: 2026-04-06 17:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260406_1700"
down_revision = "20260406_1600"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "scenarios",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_reference", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "calculation_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("scenario_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("engine_version", sa.String(length=50), nullable=False),
        sa.Column("input_snapshot", sa.JSON(), nullable=False),
        sa.Column("messages_json", sa.JSON(), nullable=False),
        sa.Column("warnings_json", sa.JSON(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["scenario_id"], ["scenarios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "result_summaries",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("calculation_run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("baseline_energy_kwh_year", sa.Float(), nullable=False),
        sa.Column("scenario_energy_kwh_year", sa.Float(), nullable=False),
        sa.Column("energy_savings_percent", sa.Float(), nullable=False),
        sa.Column("baseline_bacs_class", sa.String(length=5), nullable=True),
        sa.Column("scenario_bacs_class", sa.String(length=5), nullable=True),
        sa.ForeignKeyConstraint(["calculation_run_id"], ["calculation_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("calculation_run_id"),
    )
    op.create_table(
        "economic_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("calculation_run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("total_capex", sa.Float(), nullable=False),
        sa.Column("annual_cost_savings", sa.Float(), nullable=False),
        sa.Column("simple_payback_years", sa.Float(), nullable=False),
        sa.Column("npv", sa.Float(), nullable=False),
        sa.Column("irr", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["calculation_run_id"], ["calculation_runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("calculation_run_id"),
    )


def downgrade() -> None:
    op.drop_table("economic_results")
    op.drop_table("result_summaries")
    op.drop_table("calculation_runs")
    op.drop_table("scenarios")
