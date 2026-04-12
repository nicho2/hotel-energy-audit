from uuid import UUID

from app.core.exceptions import NotFoundError
from app.repositories.reference_data_repository import ReferenceDataRepository


class ReferenceDataService:
    def __init__(self, repository: ReferenceDataRepository):
        self.repository = repository

    def list_country_profiles(self):
        return self.repository.list_country_profiles()

    def get_country_profile(self, country_profile_id: UUID):
        country_profile = self.repository.get_country_profile(country_profile_id)
        if country_profile is None:
            raise NotFoundError("Country profile not found")
        return country_profile

    def list_climate_zones(self, country_profile_id: UUID | None = None):
        if country_profile_id is not None:
            self.get_country_profile(country_profile_id)
        return self.repository.list_climate_zones(country_profile_id)

    def get_climate_zone(self, climate_zone_id: UUID):
        climate_zone = self.repository.get_climate_zone(climate_zone_id)
        if climate_zone is None:
            raise NotFoundError("Climate zone not found")
        return climate_zone

    def list_usage_profiles(
        self,
        *,
        country_profile_id: UUID | None = None,
        building_type: str | None = None,
        zone_type: str | None = None,
    ):
        if country_profile_id is not None:
            self.get_country_profile(country_profile_id)
        return self.repository.list_usage_profiles(
            country_profile_id=country_profile_id,
            building_type=building_type,
            zone_type=zone_type,
        )

    def get_usage_profile(self, usage_profile_id: UUID):
        usage_profile = self.repository.get_usage_profile(usage_profile_id)
        if usage_profile is None:
            raise NotFoundError("Usage profile not found")
        return usage_profile
