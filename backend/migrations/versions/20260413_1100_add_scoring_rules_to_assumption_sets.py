"""Add scoring rules to assumption sets

Revision ID: 20260413_1100
Revises: 20260413_1000
Create Date: 2026-04-13 11:00:00
"""

from alembic import op
import json
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260413_1100"
down_revision = "20260413_1000"
branch_labels = None
depends_on = None


DEFAULT_SCORING_RULES = {
    "version": "comparison-score-v1",
    "weights": {"energy": 0.35, "bacs": 0.20, "roi": 0.25, "capex": 0.20},
    "thresholds": {
        "energy_savings_percent_full_score": 30.0,
        "roi_percent_full_score": 50.0,
        "payback_years_full_score": 3.0,
        "payback_years_zero_score": 12.0,
        "capex_reference": 100000.0,
    },
}


def upgrade() -> None:
    default_json = json.dumps(DEFAULT_SCORING_RULES).replace("'", "''")
    op.add_column(
        "calculation_assumption_sets",
        sa.Column("scoring_rules_json", sa.JSON(), nullable=False, server_default=sa.text(f"'{default_json}'::json")),
    )
    op.alter_column("calculation_assumption_sets", "scoring_rules_json", server_default=None)


def downgrade() -> None:
    op.drop_column("calculation_assumption_sets", "scoring_rules_json")
