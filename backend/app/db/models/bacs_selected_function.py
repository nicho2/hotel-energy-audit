from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BacsSelectedFunction(Base):
    __tablename__ = "bacs_selected_functions"
    __table_args__ = (
        UniqueConstraint(
            "assessment_id",
            "function_definition_id",
            name="uq_bacs_selected_functions_assessment_function",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bacs_assessments.id", ondelete="CASCADE"),
        nullable=False,
    )
    function_definition_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bacs_function_definitions.id", ondelete="CASCADE"),
        nullable=False,
    )

    assessment: Mapped["BacsAssessment"] = relationship(back_populates="selected_functions")
    function_definition: Mapped["BacsFunctionDefinition"] = relationship(
        back_populates="selected_in_assessments"
    )
