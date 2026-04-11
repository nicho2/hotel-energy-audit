from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    entity_type: str
    entity_id: UUID
    action: str
    before_json: dict | None
    after_json: dict | None
    user_id: UUID | None
    organization_id: UUID
    project_id: UUID | None
    scenario_id: UUID | None
    timestamp: datetime
