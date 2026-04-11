from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AdminUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    email: str
    first_name: str | None
    last_name: str | None
    role: str
    preferred_language: str
    is_active: bool
    created_at: datetime


class AdminUserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    role: str = Field(default="org_member", pattern="^(org_admin|org_member|member)$")
    preferred_language: str = Field(default="fr", pattern="^(fr|en)$")


class AdminBrandingProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    company_name: str = Field(min_length=1, max_length=255)
    accent_color: str = Field(default="#14365d", pattern="^#[0-9A-Fa-f]{6}$")
    logo_text: str | None = Field(default=None, max_length=50)
    contact_email: EmailStr | None = None
    cover_tagline: str | None = Field(default=None, max_length=255)
    footer_note: str | None = None
    is_default: bool = False


class AdminBrandingProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    company_name: str | None = Field(default=None, min_length=1, max_length=255)
    accent_color: str | None = Field(default=None, pattern="^#[0-9A-Fa-f]{6}$")
    logo_text: str | None = Field(default=None, max_length=50)
    contact_email: EmailStr | None = None
    cover_tagline: str | None = Field(default=None, max_length=255)
    footer_note: str | None = None
    is_default: bool | None = None
