import uuid

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ResultByZone(Base):
    __tablename__ = "result_by_zone"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    calculation_run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calculation_runs.id", ondelete="CASCADE"),
        nullable=False,
    )
    zone_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    zone_name: Mapped[str] = mapped_column(String(255), nullable=False)
    zone_type: Mapped[str] = mapped_column(String(50), nullable=False)
    orientation: Mapped[str] = mapped_column(String(20), nullable=False, default="mixed")
    baseline_energy_kwh_year: Mapped[float] = mapped_column(Float, nullable=False)
    scenario_energy_kwh_year: Mapped[float] = mapped_column(Float, nullable=False)
    energy_savings_percent: Mapped[float] = mapped_column(Float, nullable=False)

    calculation_run: Mapped["CalculationRun"] = relationship(back_populates="results_by_zone")
