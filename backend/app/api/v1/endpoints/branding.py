from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.branding_repository import BrandingRepository
from app.schemas.branding import BrandingProfileResponse
from app.schemas.common import ApiResponse, success_response

router = APIRouter()


@router.get("", response_model=ApiResponse[list[BrandingProfileResponse]])
def list_branding_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[BrandingProfileResponse]]:
    repository = BrandingRepository(db)
    profiles = repository.list_for_organization(current_user.organization_id)
    data = [BrandingProfileResponse.model_validate(profile) for profile in profiles]
    return success_response(data)
