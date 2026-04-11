from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    default_language: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'fr'"))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=text("CURRENT_TIMESTAMP"),
    )

    users: Mapped[list["User"]] = relationship(back_populates="organization")
    projects: Mapped[list["Project"]] = relationship(back_populates="organization")
    branding_profiles: Mapped[list["BrandingProfile"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )
    calculation_assumption_sets: Mapped[list["CalculationAssumptionSet"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )
