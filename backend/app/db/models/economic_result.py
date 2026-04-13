from __future__ import annotations

import uuid

from sqlalchemy import JSON, Boolean, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EconomicResult(Base):
    __tablename__ = "economic_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    calculation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calculation_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    total_capex: Mapped[float] = mapped_column(Float, nullable=False)
    subsidies: Mapped[float | None] = mapped_column(Float, nullable=True)
    net_capex: Mapped[float | None] = mapped_column(Float, nullable=True)
    baseline_opex_year: Mapped[float | None] = mapped_column(Float, nullable=True)
    scenario_opex_year: Mapped[float | None] = mapped_column(Float, nullable=True)
    energy_cost_savings: Mapped[float | None] = mapped_column(Float, nullable=True)
    maintenance_cost_year: Mapped[float | None] = mapped_column(Float, nullable=True)
    maintenance_savings_year: Mapped[float | None] = mapped_column(Float, nullable=True)
    net_annual_savings: Mapped[float | None] = mapped_column(Float, nullable=True)
    annual_cost_savings: Mapped[float] = mapped_column(Float, nullable=False)
    simple_payback_years: Mapped[float | None] = mapped_column(Float, nullable=True)
    npv: Mapped[float] = mapped_column(Float, nullable=False)
    irr: Mapped[float | None] = mapped_column(Float, nullable=True)
    analysis_period_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    discount_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    energy_inflation_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    cash_flows: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    is_roi_calculable: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    calculation_run: Mapped["CalculationRun"] = relationship(back_populates="economic_result")
