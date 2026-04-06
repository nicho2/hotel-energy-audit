import uuid

from sqlalchemy import Float, ForeignKey
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
    annual_cost_savings: Mapped[float] = mapped_column(Float, nullable=False)
    simple_payback_years: Mapped[float] = mapped_column(Float, nullable=False)
    npv: Mapped[float] = mapped_column(Float, nullable=False)
    irr: Mapped[float] = mapped_column(Float, nullable=False)

    calculation_run: Mapped["CalculationRun"] = relationship(back_populates="economic_result")
