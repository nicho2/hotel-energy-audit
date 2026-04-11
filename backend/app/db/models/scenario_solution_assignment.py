from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ScenarioSolutionAssignment(Base):
    __tablename__ = "scenario_solution_assignments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scenarios.id", ondelete="CASCADE"),
        nullable=False,
    )
    solution_code: Mapped[str] = mapped_column(String(100), nullable=False)
    target_scope: Mapped[str] = mapped_column(String(20), nullable=False, default="project")
    target_zone_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    target_system_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    quantity: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit_cost_override: Mapped[float | None] = mapped_column(Float, nullable=True)
    capex_override: Mapped[float | None] = mapped_column(Float, nullable=True)
    maintenance_override: Mapped[float | None] = mapped_column(Float, nullable=True)
    gain_override_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_selected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    scenario: Mapped["Scenario"] = relationship(back_populates="solution_assignments")
