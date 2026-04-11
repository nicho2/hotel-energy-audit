"""Add country/climate reference fields to projects

Revision ID: 20260411_1300
Revises: 20260411_1200
Create Date: 2026-04-11 13:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260411_1300"
down_revision = "20260411_1200"
branch_labels = None
depends_on = None


COUNTRY_FK_NAME = "fk_projects_country_profile_id"
CLIMATE_FK_NAME = "fk_projects_climate_zone_id"


def _table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return inspector.has_table(table_name)


def _foreign_key_exists(table_name: str, fk_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return any(fk.get("name") == fk_name for fk in inspector.get_foreign_keys(table_name))


def upgrade() -> None:
    op.add_column("projects", sa.Column("country_profile_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("projects", sa.Column("climate_zone_id", postgresql.UUID(as_uuid=True), nullable=True))

    if _table_exists("country_profiles"):
        op.create_foreign_key(
            COUNTRY_FK_NAME,
            "projects",
            "country_profiles",
            ["country_profile_id"],
            ["id"],
            ondelete="SET NULL",
        )

    if _table_exists("climate_zones"):
        op.create_foreign_key(
            CLIMATE_FK_NAME,
            "projects",
            "climate_zones",
            ["climate_zone_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    if _foreign_key_exists("projects", CLIMATE_FK_NAME):
        op.drop_constraint(CLIMATE_FK_NAME, "projects", type_="foreignkey")
    if _foreign_key_exists("projects", COUNTRY_FK_NAME):
        op.drop_constraint(COUNTRY_FK_NAME, "projects", type_="foreignkey")

    op.drop_column("projects", "climate_zone_id")
    op.drop_column("projects", "country_profile_id")
