from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UsageProfile(Base):
    __tablename__ = "usage_profiles"
    __table_args__ = (
        UniqueConstraint("country_profile_id", "code", name="uq_usage_profiles_country_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("country_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    name_fr: Mapped[str] = mapped_column(String(255), nullable=False)
    name_en: Mapped[str] = mapped_column(String(255), nullable=False)
    building_type: Mapped[str] = mapped_column(String(50), nullable=False)
    zone_type: Mapped[str] = mapped_column(String(50), nullable=False)
    default_occupancy_rate: Mapped[float] = mapped_column(Float, nullable=False)
    seasonality_profile_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    daily_schedule_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    ecs_intensity_level: Mapped[str] = mapped_column(String(50), nullable=False)
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

    country_profile: Mapped["CountryProfile"] = relationship(back_populates="usage_profiles")
