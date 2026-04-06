import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    construction_period: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gross_floor_area_m2: Mapped[float | None] = mapped_column(Float, nullable=True)
    heated_area_m2: Mapped[float | None] = mapped_column(Float, nullable=True)
    cooled_area_m2: Mapped[float | None] = mapped_column(Float, nullable=True)
    number_of_floors: Mapped[int | None] = mapped_column(Integer, nullable=True)
    number_of_rooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    main_orientation: Mapped[str | None] = mapped_column(String(20), nullable=True)
    compactness_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    has_restaurant: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_meeting_rooms: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_spa: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_pool: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    project: Mapped["Project"] = relationship(back_populates="building")
