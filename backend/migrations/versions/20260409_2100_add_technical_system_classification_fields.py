"""Add technology and efficiency fields to technical systems

Revision ID: 20260409_2100
Revises: 20260406_2000
Create Date: 2026-04-09 21:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260409_2100"
down_revision = "20260406_2000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("technical_systems", sa.Column("technology_type", sa.String(length=50), nullable=True))
    op.add_column("technical_systems", sa.Column("efficiency_level", sa.String(length=50), nullable=True))


def downgrade() -> None:
    op.drop_column("technical_systems", "efficiency_level")
    op.drop_column("technical_systems", "technology_type")
