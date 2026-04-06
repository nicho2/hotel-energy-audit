import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ResultSummary(Base):
    __tablename__ = "result_summaries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    calculation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calculation_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    baseline_energy_kwh_year: Mapped[float] = mapped_column(Float, nullable=False)
    scenario_energy_kwh_year: Mapped[float] = mapped_column(Float, nullable=False)
    energy_savings_percent: Mapped[float] = mapped_column(Float, nullable=False)
    baseline_bacs_class: Mapped[str | None] = mapped_column(String(5), nullable=True)
    scenario_bacs_class: Mapped[str | None] = mapped_column(String(5), nullable=True)

    calculation_run: Mapped["CalculationRun"] = relationship(back_populates="result_summary")
