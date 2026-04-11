from datetime import datetime
from pydantic import BaseModel


class ProjectHistoryEventResponse(BaseModel):
    action: str
    actor: str
    occurred_at: datetime
    summary: str
