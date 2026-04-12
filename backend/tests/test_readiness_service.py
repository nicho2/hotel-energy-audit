from types import SimpleNamespace
from uuid import uuid4

from app.services.readiness_service import ReadinessService


class _StaticProjectService:
    def get_project(self, project_id, current_user):
        return SimpleNamespace(
            id=project_id,
            organization_id=current_user.organization_id,
            country_profile_id=current_user.country_profile_id,
            climate_zone_id=current_user.climate_zone_id,
        )


class _StaticBuildingRepository:
    def __init__(self, building):
        self.building = building

    def get_by_project_id(self, project_id):
        return self.building


class _StaticZoneRepository:
    def __init__(self, zones):
        self.zones = zones

    def list_by_project_id(self, project_id):
        return self.zones


class _StaticTechnicalSystemRepository:
    def __init__(self, systems):
        self.systems = systems

    def list_by_project_id(self, project_id):
        return self.systems


class _StaticPayloadRepository:
    def __init__(self, payloads):
        self.payloads = payloads

    def list_by_project_id(self, project_id):
        return self.payloads


class _StaticBacsRepository:
    def __init__(self, assessment):
        self.assessment = assessment

    def get_assessment_by_project_id(self, project_id):
        return self.assessment


class _StaticScenarioRepository:
    def __init__(self, scenarios):
        self.scenarios = scenarios

    def list_by_project_id(self, project_id):
        return self.scenarios


def test_get_calculation_readiness_reports_missing_blockers_and_low_confidence() -> None:
    service = ReadinessService(
        project_service=_StaticProjectService(),
        building_repository=_StaticBuildingRepository(None),
        zone_repository=_StaticZoneRepository([]),
        technical_system_repository=_StaticTechnicalSystemRepository([]),
        wizard_step_payload_repository=_StaticPayloadRepository([]),
        bacs_repository=_StaticBacsRepository(None),
        scenario_repository=_StaticScenarioRepository([]),
    )

    response = service.get_calculation_readiness(
        uuid4(),
        SimpleNamespace(organization_id=uuid4(), country_profile_id=None, climate_zone_id=None),
    )

    assert response.is_ready is False
    assert response.confidence_level == "low"
    assert [issue.code for issue in response.blocking_issues] == [
        "country_profile_missing",
        "climate_zone_missing",
        "building_missing",
        "zones_missing",
        "usage_occupancy_missing",
        "usage_dhw_intensity_missing",
        "scenario_missing",
    ]
    assert [issue.code for issue in response.warnings] == [
        "systems_missing",
        "bacs_assessment_missing",
    ]


def test_get_calculation_readiness_returns_high_confidence_for_complete_project() -> None:
    service = ReadinessService(
        project_service=_StaticProjectService(),
        building_repository=_StaticBuildingRepository(
            SimpleNamespace(name="Hotel Demo", heated_area_m2=4200, gross_floor_area_m2=5000, number_of_rooms=100)
        ),
        zone_repository=_StaticZoneRepository([SimpleNamespace(name="Rooms", area_m2=1800)]),
        technical_system_repository=_StaticTechnicalSystemRepository(
            [
                SimpleNamespace(system_type="heating"),
                SimpleNamespace(system_type="dhw"),
            ]
        ),
        wizard_step_payload_repository=_StaticPayloadRepository(
            [
                SimpleNamespace(
                    step_code="usage",
                    payload_json={"average_occupancy_rate": 0.72, "ecs_intensity_level": "medium"},
                )
            ]
        ),
        bacs_repository=_StaticBacsRepository(SimpleNamespace(selected_functions=["heating_control"])),
        scenario_repository=_StaticScenarioRepository([SimpleNamespace(name="Reference")]),
    )

    response = service.get_calculation_readiness(
        uuid4(),
        SimpleNamespace(organization_id=uuid4(), country_profile_id=uuid4(), climate_zone_id=uuid4()),
    )

    assert response.is_ready is True
    assert response.blocking_issues == []
    assert response.confidence_level == "high"
    assert response.warnings == []
