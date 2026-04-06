from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.branding_profile import BrandingProfile


class BrandingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, branding_profile_id: UUID, organization_id: UUID) -> BrandingProfile | None:
        statement = select(BrandingProfile).where(
            BrandingProfile.id == branding_profile_id,
            BrandingProfile.organization_id == organization_id,
        )
        return self.db.scalar(statement)

    def get_default_for_organization(self, organization_id: UUID) -> BrandingProfile | None:
        statement = (
            select(BrandingProfile)
            .where(
                BrandingProfile.organization_id == organization_id,
                BrandingProfile.is_default.is_(True),
            )
            .order_by(BrandingProfile.created_at.desc())
        )
        return self.db.scalar(statement)
