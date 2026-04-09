"""Add scenario management fields and assignments

Revision ID: 20260409_2300
Revises: 20260409_2200
Create Date: 2026-04-09 23:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260409_2300"
down_revision = "20260409_2200"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("scenarios", sa.Column("scenario_type", sa.String(length=50), nullable=False, server_default="custom"))
    op.add_column("scenarios", sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"))
    op.add_column("scenarios", sa.Column("derived_from_scenario_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("scenarios", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")))

    op.create_table(
        "scenario_solution_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("scenario_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("solution_code", sa.String(length=100), nullable=False),
        sa.Column("target_scope", sa.String(length=20), nullable=False, server_default="project"),
        sa.Column("target_zone_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("target_system_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("quantity", sa.Float(), nullable=True),
        sa.Column("unit_cost_override", sa.Float(), nullable=True),
        sa.Column("capex_override", sa.Float(), nullable=True),
        sa.Column("maintenance_override", sa.Float(), nullable=True),
        sa.Column("gain_override_percent", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("is_selected", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["scenario_id"], ["scenarios.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("scenario_solution_assignments")
    op.drop_column("scenarios", "updated_at")
    op.drop_column("scenarios", "derived_from_scenario_id")
    op.drop_column("scenarios", "status")
    op.drop_column("scenarios", "scenario_type")
