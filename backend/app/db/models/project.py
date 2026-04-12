from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    template_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_templates.id", ondelete="SET NULL"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reference_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'draft'"))
    wizard_step: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))
    building_type: Mapped[str] = mapped_column(String(50), nullable=False)
    project_goal: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country_profile_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    climate_zone_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    branding_profile_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("branding_profiles.id", ondelete="SET NULL"),
        nullable=True,
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

    organization: Mapped["Organization"] = relationship(back_populates="projects")
    created_by_user: Mapped["User"] = relationship(back_populates="projects_created")
    branding_profile: Mapped["BrandingProfile | None"] = relationship(back_populates="projects")
    building: Mapped["Building"] = relationship(back_populates="project", uselist=False)
    bacs_assessment: Mapped["BacsAssessment | None"] = relationship(
        back_populates="project",
        uselist=False,
    )
    scenarios: Mapped[list["Scenario"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    calculation_runs: Mapped[list["CalculationRun"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    zones: Mapped[list["BuildingZone"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    technical_systems: Mapped[list["TechnicalSystem"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    wizard_step_payloads: Mapped[list["WizardStepPayload"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
