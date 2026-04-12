"""Add wizard step payloads

Revision ID: 20260412_1000
Revises: 20260411_1400
Create Date: 2026-04-12 10:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260412_1000"
down_revision = "20260411_1400"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "wizard_step_payloads",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("step_code", sa.String(length=50), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id", "step_code", name="uq_wizard_step_payloads_project_step"),
    )


def downgrade() -> None:
    op.drop_table("wizard_step_payloads")
