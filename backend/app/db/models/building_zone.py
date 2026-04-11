from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BuildingZone(Base):
    __tablename__ = "building_zones"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    zone_type: Mapped[str] = mapped_column(String(50), nullable=False)
    orientation: Mapped[str] = mapped_column(String(20), nullable=False, default="mixed")
    area_m2: Mapped[float] = mapped_column(Float, nullable=False)
    room_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    project: Mapped["Project"] = relationship(back_populates="zones")
