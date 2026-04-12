from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.repositories.reference_data_repository import ReferenceDataRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.reference_data import (
    ClimateZoneResponse,
    CountryProfileResponse,
    UsageProfileResponse,
)
from app.services.reference_data_service import ReferenceDataService

router = APIRouter()


def get_reference_data_service(db: Session) -> ReferenceDataService:
    return ReferenceDataService(ReferenceDataRepository(db))


@router.get("/country-profiles", response_model=ApiResponse[list[CountryProfileResponse]])
def list_country_profiles(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse[list[CountryProfileResponse]]:
    service = get_reference_data_service(db)
    return success_response(service.list_country_profiles())


@router.get("/country-profiles/{country_profile_id}", response_model=ApiResponse[CountryProfileResponse])
def get_country_profile(
    country_profile_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse[CountryProfileResponse]:
    service = get_reference_data_service(db)
    return success_response(service.get_country_profile(country_profile_id))


@router.get("/climate-zones", response_model=ApiResponse[list[ClimateZoneResponse]])
def list_climate_zones(
    country_profile_id: UUID | None = None,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse[list[ClimateZoneResponse]]:
    service = get_reference_data_service(db)
    return success_response(service.list_climate_zones(country_profile_id))


@router.get("/climate-zones/{climate_zone_id}", response_model=ApiResponse[ClimateZoneResponse])
def get_climate_zone(
    climate_zone_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse[ClimateZoneResponse]:
    service = get_reference_data_service(db)
    return success_response(service.get_climate_zone(climate_zone_id))


@router.get("/usage-profiles", response_model=ApiResponse[list[UsageProfileResponse]])
def list_usage_profiles(
    country_profile_id: UUID | None = None,
    building_type: str | None = None,
    zone_type: str | None = None,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse[list[UsageProfileResponse]]:
    service = get_reference_data_service(db)
    return success_response(
        service.list_usage_profiles(
            country_profile_id=country_profile_id,
            building_type=building_type,
            zone_type=zone_type,
        )
    )


@router.get("/usage-profiles/{usage_profile_id}", response_model=ApiResponse[UsageProfileResponse])
def get_usage_profile(
    usage_profile_id: UUID,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
) -> ApiResponse[UsageProfileResponse]:
    service = get_reference_data_service(db)
    return success_response(service.get_usage_profile(usage_profile_id))
