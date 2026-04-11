from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.exceptions import BusinessRuleError
from app.db.models.calculation_run import CalculationRun
from app.db.models.project import Project
from app.db.models.scenario import Scenario
from app.db.models.user import User
from app.db.session import SessionLocal
from app.repositories.assumption_set_repository import AssumptionSetRepository
from app.schemas.assumption_sets import AssumptionSetCreate, AssumptionSetUpdate
from app.services.assumption_set_service import AssumptionSetService
from test_admin_api import _login


def _valid_payload(version: str = "1.0.0", *, is_active: bool = False) -> dict:
    return {
        "name": f"Default FR {version}",
        "version": version,
        "scope": "organization_override",
        "heating_model_json": {"reference_intensity_kwh_m2": 85},
        "cooling_model_json": {"reference_intensity_kwh_m2": 18},
        "ventilation_model_json": {"reference_intensity_kwh_m2": 12},
        "dhw_model_json": {"reference_intensity_kwh_room": 2200},
        "lighting_model_json": {"reference_intensity_kwh_m2": 28},
        "auxiliaries_model_json": {"reference_intensity_kwh_m2": 8},
        "economic_defaults_json": {
            "discount_rate": 0.06,
            "energy_inflation_rate": 0.03,
            "analysis_period_years": 15,
        },
        "bacs_rules_json": {
            "score_to_class": {
                "A": [85, 100],
                "B": [65, 84],
                "C": [40, 64],
                "D": [0, 39],
            }
        },
        "co2_factors_json": {
            "electricity": 0.055,
            "natural_gas": 0.227,
        },
        "notes": "Managed through admin API",
        "is_active": is_active,
    }


def _create_assumption_set(
    client: TestClient,
    token: str,
    version: str = "1.0.0",
    *,
    is_active: bool = False,
) -> dict:
    response = client.post(
        "/api/v1/admin/assumption-sets",
        headers={"Authorization": f"Bearer {token}"},
        json=_valid_payload(version, is_active=is_active),
    )
    assert response.status_code == 201
    return response.json()["data"]


def _create_historical_run(user: dict, assumption_set: dict) -> None:
    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name=f"Assumption history {uuid4().hex[:8]}",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.flush()
        scenario = Scenario(project_id=project.id, name="Reference", is_reference=True)
        db.add(scenario)
        db.flush()
        db.add(
            CalculationRun(
                project_id=project.id,
                scenario_id=scenario.id,
                status="completed",
                engine_version="placeholder-v1",
                input_snapshot={
                    "assumptions": {
                        "assumption_set_id": assumption_set["id"],
                        "assumption_set_version": assumption_set["version"],
                    }
                },
                messages_json=[],
                warnings_json=[],
            )
        )
        db.commit()


def test_admin_can_create_list_get_and_activate_assumption_sets(client: TestClient) -> None:
    token, _user = _login(client)
    first = _create_assumption_set(client, token, "1.0.0", is_active=True)
    second = _create_assumption_set(client, token, "1.1.0")

    activate_response = client.post(
        f"/api/v1/admin/assumption-sets/{second['id']}/activate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert activate_response.status_code == 200
    assert activate_response.json()["data"]["is_active"] is True

    get_first_response = client.get(
        f"/api/v1/admin/assumption-sets/{first['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_first_response.status_code == 200
    assert get_first_response.json()["data"]["is_active"] is False

    list_response = client.get(
        "/api/v1/admin/assumption-sets",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    versions = {item["version"] for item in list_response.json()["data"]}
    assert versions >= {"1.0.0", "1.1.0"}


def test_admin_can_update_unused_assumption_set(client: TestClient) -> None:
    token, _user = _login(client)
    assumption_set = _create_assumption_set(client, token)

    response = client.patch(
        f"/api/v1/admin/assumption-sets/{assumption_set['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "heating_model_json": {"reference_intensity_kwh_m2": 92},
            "notes": "Updated before use",
        },
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["heating_model_json"]["reference_intensity_kwh_m2"] == 92
    assert body["notes"] == "Updated before use"
    assert body["is_locked"] is False


def test_admin_api_rejects_invalid_json_payloads(client: TestClient) -> None:
    token, _user = _login(client)
    payload = _valid_payload()
    payload["co2_factors_json"] = {"electricity": -0.1}

    response = client.post(
        "/api/v1/admin/assumption-sets",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )

    assert response.status_code == 422


def test_used_assumption_set_is_locked_and_can_be_cloned(client: TestClient) -> None:
    token, user = _login(client)
    assumption_set = _create_assumption_set(client, token)
    _create_historical_run(user, assumption_set)

    update_response = client.patch(
        f"/api/v1/admin/assumption-sets/{assumption_set['id']}",
        headers={"Authorization": f"Bearer {token}"},
        json={"heating_model_json": {"reference_intensity_kwh_m2": 95}},
    )
    assert update_response.status_code == 409
    assert update_response.json()["errors"][0]["details"]["recommended_action"] == "clone"

    clone_response = client.post(
        f"/api/v1/admin/assumption-sets/{assumption_set['id']}/clone",
        headers={"Authorization": f"Bearer {token}"},
        json={"version": "1.0.1", "name": "Default FR 1.0.1"},
    )
    assert clone_response.status_code == 201
    clone = clone_response.json()["data"]
    assert clone["id"] != assumption_set["id"]
    assert clone["cloned_from_id"] == assumption_set["id"]
    assert clone["version"] == "1.0.1"
    assert clone["is_locked"] is False

    locked_response = client.get(
        f"/api/v1/admin/assumption-sets/{assumption_set['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert locked_response.json()["data"]["is_locked"] is True
    assert locked_response.json()["data"]["historical_calculation_count"] == 1


def test_assumption_set_service_blocks_destructive_update_when_used(client: TestClient) -> None:
    _token, user_payload = _login(client)
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.id == user_payload["id"]))
        assert user is not None
        service = AssumptionSetService(AssumptionSetRepository(db))
        created = service.create_assumption_set(
            payload=AssumptionSetCreate(**_valid_payload("2.0.0")),
            current_user=user,
        )

    _create_historical_run(user_payload, {"id": str(created.id), "version": created.version})

    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.id == user_payload["id"]))
        assert user is not None
        service = AssumptionSetService(AssumptionSetRepository(db))
        try:
            service.update_assumption_set(
                created.id,
                AssumptionSetUpdate(heating_model_json={"reference_intensity_kwh_m2": 101}),
                user,
            )
        except BusinessRuleError as exc:
            assert exc.details["recommended_action"] == "clone"
        else:
            raise AssertionError("Expected BusinessRuleError")
