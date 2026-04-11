from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CalculationRun(Base):
    __tablename__ = "calculation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scenarios.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed")
    engine_version: Mapped[str] = mapped_column(String(50), nullable=False)
    input_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)
    messages_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    warnings_json: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    project: Mapped["Project"] = relationship(back_populates="calculation_runs")
    scenario: Mapped["Scenario"] = relationship(back_populates="calculation_runs")
    result_summary: Mapped["ResultSummary | None"] = relationship(
        back_populates="calculation_run",
        uselist=False,
        cascade="all, delete-orphan",
    )
    economic_result: Mapped["EconomicResult | None"] = relationship(
        back_populates="calculation_run",
        uselist=False,
        cascade="all, delete-orphan",
    )
    results_by_use: Mapped[list["ResultByUse"]] = relationship(
        back_populates="calculation_run",
        cascade="all, delete-orphan",
        order_by="ResultByUse.usage_type",
    )
    results_by_zone: Mapped[list["ResultByZone"]] = relationship(
        back_populates="calculation_run",
        cascade="all, delete-orphan",
        order_by="ResultByZone.zone_name",
    )
