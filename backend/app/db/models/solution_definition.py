from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SolutionDefinition(Base):
    __tablename__ = "solution_definitions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    catalog_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("solution_catalogs.id", ondelete="CASCADE"),
        nullable=False,
    )
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    family: Mapped[str] = mapped_column(String(50), nullable=False)
    target_scopes: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    applicable_countries: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    applicable_building_types: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    applicable_zone_types: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    bacs_impact_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    lifetime_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    default_quantity: Mapped[float | None] = mapped_column(Float, nullable=True)
    default_unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    default_unit_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    default_capex: Mapped[float | None] = mapped_column(Float, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    is_commercial_offer: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
    offer_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
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

    catalog: Mapped["SolutionCatalog"] = relationship(back_populates="solutions")
