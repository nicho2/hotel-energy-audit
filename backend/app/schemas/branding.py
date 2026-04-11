from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BrandingProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    name: str
    company_name: str
    accent_color: str
    logo_text: str | None
    contact_email: str | None
    cover_tagline: str | None
    footer_note: str | None
    is_default: bool
    created_at: datetime
