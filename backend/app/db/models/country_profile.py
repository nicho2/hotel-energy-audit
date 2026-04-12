from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, Integer, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CountryProfile(Base):
    __tablename__ = "country_profiles"
    __table_args__ = (UniqueConstraint("country_code", name="uq_country_profiles_country_code"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_code: Mapped[str] = mapped_column(String(10), nullable=False)
    name_fr: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    regulatory_scope: Mapped[str] = mapped_column(String(50), nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    default_language: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'fr'"))
    default_discount_rate: Mapped[float] = mapped_column(Float, nullable=False)
    default_energy_inflation_rate: Mapped[float] = mapped_column(Float, nullable=False)
    default_analysis_period_years: Mapped[int] = mapped_column(Integer, nullable=False)
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

    climate_zones: Mapped[list["ClimateZone"]] = relationship(
        back_populates="country_profile",
        cascade="all, delete-orphan",
    )
    usage_profiles: Mapped[list["UsageProfile"]] = relationship(
        back_populates="country_profile",
        cascade="all, delete-orphan",
    )
    project_templates: Mapped[list["ProjectTemplate"]] = relationship(
        back_populates="country_profile",
    )
