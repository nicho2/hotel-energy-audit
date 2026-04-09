"""Add manual override class to BACS assessments

Revision ID: 20260409_2200
Revises: 20260409_2100
Create Date: 2026-04-09 22:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260409_2200"
down_revision = "20260409_2100"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("bacs_assessments", sa.Column("manual_override_class", sa.String(length=1), nullable=True))


def downgrade() -> None:
    op.drop_column("bacs_assessments", "manual_override_class")
