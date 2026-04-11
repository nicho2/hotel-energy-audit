"""Add solution catalogs and definitions

Revision ID: 20260411_1100
Revises: 20260411_1000
Create Date: 2026-04-11 11:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260411_1100"
down_revision = "20260411_1000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "solution_catalogs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column("scope", sa.String(length=50), nullable=False),
        sa.Column("country_code", sa.String(length=10), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
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
    )
    op.create_table(
        "solution_definitions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("catalog_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("family", sa.String(length=50), nullable=False),
        sa.Column("target_scopes", sa.JSON(), nullable=False),
        sa.Column("applicable_countries", sa.JSON(), nullable=False),
        sa.Column("applicable_building_types", sa.JSON(), nullable=False),
        sa.Column("applicable_zone_types", sa.JSON(), nullable=False),
        sa.Column("bacs_impact_json", sa.JSON(), nullable=False),
        sa.Column("lifetime_years", sa.Integer(), nullable=True),
        sa.Column("default_quantity", sa.Float(), nullable=True),
        sa.Column("default_unit", sa.String(length=50), nullable=True),
        sa.Column("default_unit_cost", sa.Float(), nullable=True),
        sa.Column("default_capex", sa.Float(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("is_commercial_offer", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("offer_reference", sa.String(length=100), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
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
        sa.ForeignKeyConstraint(["catalog_id"], ["solution_catalogs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_solution_definitions_code"),
    )


def downgrade() -> None:
    op.drop_table("solution_definitions")
    op.drop_table("solution_catalogs")
