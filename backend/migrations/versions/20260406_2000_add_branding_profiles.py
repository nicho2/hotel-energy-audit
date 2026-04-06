"""Add branding profiles

Revision ID: 20260406_2000
Revises: 20260406_1900
Create Date: 2026-04-06 20:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260406_2000"
down_revision = "20260406_1900"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "branding_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("accent_color", sa.String(length=20), nullable=False),
        sa.Column("logo_text", sa.String(length=50), nullable=True),
        sa.Column("contact_email", sa.String(length=255), nullable=True),
        sa.Column("cover_tagline", sa.String(length=255), nullable=True),
        sa.Column("footer_note", sa.Text(), nullable=True),
        sa.Column("is_default", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("projects", sa.Column("branding_profile_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        "fk_projects_branding_profile_id_branding_profiles",
        "projects",
        "branding_profiles",
        ["branding_profile_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.add_column("generated_reports", sa.Column("branding_profile_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(
        "fk_generated_reports_branding_profile_id_branding_profiles",
        "generated_reports",
        "branding_profiles",
        ["branding_profile_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_generated_reports_branding_profile_id_branding_profiles", "generated_reports", type_="foreignkey")
    op.drop_column("generated_reports", "branding_profile_id")
    op.drop_constraint("fk_projects_branding_profile_id_branding_profiles", "projects", type_="foreignkey")
    op.drop_column("projects", "branding_profile_id")
    op.drop_table("branding_profiles")
