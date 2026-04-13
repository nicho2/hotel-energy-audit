from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CalculationAssumptionSet(Base):
    __tablename__ = "calculation_assumption_sets"
    __table_args__ = (
        UniqueConstraint(
            "scope",
            "version",
            "organization_id",
            "country_profile_id",
            name="uq_assumption_set_scope_version",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
    )
    country_profile_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    cloned_from_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    scope: Mapped[str] = mapped_column(String(50), nullable=False)
    heating_model_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    cooling_model_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    ventilation_model_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    dhw_model_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    lighting_model_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    auxiliaries_model_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    economic_defaults_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    bacs_rules_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    scoring_rules_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    co2_factors_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
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

    organization: Mapped["Organization | None"] = relationship(
        back_populates="calculation_assumption_sets"
    )
