from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ResultByUse(Base):
    __tablename__ = "result_by_use"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    calculation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calculation_runs.id", ondelete="CASCADE"),
        nullable=False,
    )
    usage_type: Mapped[str] = mapped_column(String(50), nullable=False)
    baseline_energy_kwh_year: Mapped[float] = mapped_column(Float, nullable=False)
    scenario_energy_kwh_year: Mapped[float] = mapped_column(Float, nullable=False)
    energy_savings_percent: Mapped[float] = mapped_column(Float, nullable=False)

    calculation_run: Mapped["CalculationRun"] = relationship(back_populates="results_by_use")
