from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.climate_zone import ClimateZone
from app.db.models.country_profile import CountryProfile
from app.db.models.usage_profile import UsageProfile


class ReferenceDataRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_country_profiles(self) -> list[CountryProfile]:
        statement = select(CountryProfile).order_by(CountryProfile.country_code.asc())
        return list(self.db.scalars(statement).all())

    def get_country_profile(self, country_profile_id: UUID) -> CountryProfile | None:
        return self.db.get(CountryProfile, country_profile_id)

    def get_country_profile_by_code(self, country_code: str) -> CountryProfile | None:
        statement = select(CountryProfile).where(CountryProfile.country_code == country_code.upper())
        return self.db.scalar(statement)

    def list_climate_zones(self, country_profile_id: UUID | None = None) -> list[ClimateZone]:
        statement = select(ClimateZone).order_by(ClimateZone.country_profile_id.asc(), ClimateZone.code.asc())
        if country_profile_id is not None:
            statement = statement.where(ClimateZone.country_profile_id == country_profile_id)
        return list(self.db.scalars(statement).all())

    def get_climate_zone(self, climate_zone_id: UUID) -> ClimateZone | None:
        return self.db.get(ClimateZone, climate_zone_id)

    def list_usage_profiles(
        self,
        *,
        country_profile_id: UUID | None = None,
        building_type: str | None = None,
        zone_type: str | None = None,
    ) -> list[UsageProfile]:
        statement = select(UsageProfile).order_by(
            UsageProfile.building_type.asc(),
            UsageProfile.zone_type.asc(),
            UsageProfile.code.asc(),
        )
        if country_profile_id is not None:
            statement = statement.where(UsageProfile.country_profile_id == country_profile_id)
        if building_type is not None:
            statement = statement.where(UsageProfile.building_type == building_type)
        if zone_type is not None:
            statement = statement.where(UsageProfile.zone_type == zone_type)
        return list(self.db.scalars(statement).all())

    def get_usage_profile(self, usage_profile_id: UUID) -> UsageProfile | None:
        return self.db.get(UsageProfile, usage_profile_id)
