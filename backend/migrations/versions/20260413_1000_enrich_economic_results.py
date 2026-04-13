"""Enrich economic results for ROI V1

Revision ID: 20260413_1000
Revises: 20260412_1000
Create Date: 2026-04-13 10:00:00
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260413_1000"
down_revision = "20260412_1000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("economic_results", sa.Column("subsidies", sa.Float(), nullable=True))
    op.add_column("economic_results", sa.Column("net_capex", sa.Float(), nullable=True))
    op.add_column("economic_results", sa.Column("baseline_opex_year", sa.Float(), nullable=True))
    op.add_column("economic_results", sa.Column("scenario_opex_year", sa.Float(), nullable=True))
    op.add_column("economic_results", sa.Column("energy_cost_savings", sa.Float(), nullable=True))
    op.add_column("economic_results", sa.Column("maintenance_cost_year", sa.Float(), nullable=True))
    op.add_column("economic_results", sa.Column("maintenance_savings_year", sa.Float(), nullable=True))
    op.add_column("economic_results", sa.Column("net_annual_savings", sa.Float(), nullable=True))
    op.add_column("economic_results", sa.Column("analysis_period_years", sa.Integer(), nullable=True))
    op.add_column("economic_results", sa.Column("discount_rate", sa.Float(), nullable=True))
    op.add_column("economic_results", sa.Column("energy_inflation_rate", sa.Float(), nullable=True))
    op.add_column("economic_results", sa.Column("cash_flows", sa.JSON(), nullable=True))
    op.add_column("economic_results", sa.Column("is_roi_calculable", sa.Boolean(), nullable=True))
    op.alter_column("economic_results", "simple_payback_years", existing_type=sa.Float(), nullable=True)
    op.alter_column("economic_results", "irr", existing_type=sa.Float(), nullable=True)


def downgrade() -> None:
    op.alter_column("economic_results", "irr", existing_type=sa.Float(), nullable=False)
    op.alter_column("economic_results", "simple_payback_years", existing_type=sa.Float(), nullable=False)
    op.drop_column("economic_results", "is_roi_calculable")
    op.drop_column("economic_results", "cash_flows")
    op.drop_column("economic_results", "energy_inflation_rate")
    op.drop_column("economic_results", "discount_rate")
    op.drop_column("economic_results", "analysis_period_years")
    op.drop_column("economic_results", "net_annual_savings")
    op.drop_column("economic_results", "maintenance_savings_year")
    op.drop_column("economic_results", "maintenance_cost_year")
    op.drop_column("economic_results", "energy_cost_savings")
    op.drop_column("economic_results", "scenario_opex_year")
    op.drop_column("economic_results", "baseline_opex_year")
    op.drop_column("economic_results", "net_capex")
    op.drop_column("economic_results", "subsidies")
