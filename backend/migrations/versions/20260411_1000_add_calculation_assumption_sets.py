"""Add calculation assumption sets

Revision ID: 20260411_1000
Revises: 20260409_2300
Create Date: 2026-04-11 10:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260411_1000"
down_revision = "20260409_2300"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "calculation_assumption_sets",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("country_profile_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("cloned_from_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column("scope", sa.String(length=50), nullable=False),
        sa.Column("heating_model_json", sa.JSON(), nullable=False),
        sa.Column("cooling_model_json", sa.JSON(), nullable=False),
        sa.Column("ventilation_model_json", sa.JSON(), nullable=False),
        sa.Column("dhw_model_json", sa.JSON(), nullable=False),
        sa.Column("lighting_model_json", sa.JSON(), nullable=False),
        sa.Column("auxiliaries_model_json", sa.JSON(), nullable=False),
        sa.Column("economic_defaults_json", sa.JSON(), nullable=False),
        sa.Column("bacs_rules_json", sa.JSON(), nullable=False),
        sa.Column("co2_factors_json", sa.JSON(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "scope",
            "version",
            "organization_id",
            "country_profile_id",
            name="uq_assumption_set_scope_version",
        ),
    )


def downgrade() -> None:
    op.drop_table("calculation_assumption_sets")
