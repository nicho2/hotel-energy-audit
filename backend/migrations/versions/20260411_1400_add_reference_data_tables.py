"""Add reference data tables

Revision ID: 20260411_1400
Revises: 20260411_1300
Create Date: 2026-04-11 14:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260411_1400"
down_revision = "20260411_1300"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "country_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("country_code", sa.String(length=10), nullable=False),
        sa.Column("name_fr", sa.String(length=255), nullable=False),
        sa.Column("name_en", sa.String(length=255), nullable=False),
        sa.Column("regulatory_scope", sa.String(length=50), nullable=False),
        sa.Column("currency_code", sa.String(length=3), nullable=False),
        sa.Column("default_language", sa.String(length=10), server_default=sa.text("'fr'"), nullable=False),
        sa.Column("default_discount_rate", sa.Float(), nullable=False),
        sa.Column("default_energy_inflation_rate", sa.Float(), nullable=False),
        sa.Column("default_analysis_period_years", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("country_code", name="uq_country_profiles_country_code"),
    )
    op.create_table(
        "climate_zones",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("country_profile_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name_fr", sa.String(length=255), nullable=False),
        sa.Column("name_en", sa.String(length=255), nullable=False),
        sa.Column("heating_severity_index", sa.Float(), nullable=False),
        sa.Column("cooling_severity_index", sa.Float(), nullable=False),
        sa.Column("solar_exposure_index", sa.Float(), nullable=False),
        sa.Column("default_weather_profile_json", sa.JSON(), nullable=False),
        sa.Column("is_default", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["country_profile_id"], ["country_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("country_profile_id", "code", name="uq_climate_zones_country_code"),
    )
    op.create_table(
        "usage_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("country_profile_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name_fr", sa.String(length=255), nullable=False),
        sa.Column("name_en", sa.String(length=255), nullable=False),
        sa.Column("building_type", sa.String(length=50), nullable=False),
        sa.Column("zone_type", sa.String(length=50), nullable=False),
        sa.Column("default_occupancy_rate", sa.Float(), nullable=False),
        sa.Column("seasonality_profile_json", sa.JSON(), nullable=False),
        sa.Column("daily_schedule_json", sa.JSON(), nullable=False),
        sa.Column("ecs_intensity_level", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["country_profile_id"], ["country_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("country_profile_id", "code", name="uq_usage_profiles_country_code"),
    )
    op.create_table(
        "project_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("building_type", sa.String(length=50), nullable=False),
        sa.Column("country_profile_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("default_payload_json", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_by_user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["country_profile_id"], ["country_profiles.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "name", name="uq_project_templates_org_name"),
    )
    op.add_column("projects", sa.Column("template_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        "fk_projects_template_id",
        "projects",
        "project_templates",
        ["template_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_projects_template_id", "projects", type_="foreignkey")
    op.drop_column("projects", "template_id")
    op.drop_table("project_templates")
    op.drop_table("usage_profiles")
    op.drop_table("climate_zones")
    op.drop_table("country_profiles")
