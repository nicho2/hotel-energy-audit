from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.core.security import get_password_hash
from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.models.wizard_step_payload import WizardStepPayload
from app.db.models.user import User
from app.db.session import SessionLocal
from scripts.seed_all import DEV_USER_EMAIL, DEV_USER_PASSWORD


def _login(client: TestClient) -> tuple[str, dict]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": DEV_USER_EMAIL, "password": DEV_USER_PASSWORD},
    )
    assert response.status_code == 200
    body = response.json()
    return body["data"]["access_token"], body["data"]["user"]


def test_get_wizard_state_returns_full_stepper_for_project(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Wizard Project",
            building_type="hotel",
            project_goal="baseline",
            wizard_step=4,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    response = client.get(
        f"/api/v1/projects/{project_id}/wizard",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["errors"] == []
    assert body["data"]["project_id"] == project_id
    assert body["data"]["current_step"] == 4
    assert len(body["data"]["steps"]) == 10
    assert body["data"]["steps"][0]["status"] == "completed"
    assert body["data"]["steps"][3]["status"] == "current"
    assert body["data"]["steps"][9]["status"] == "not_started"
    assert body["data"]["step_payloads"]["project"]["name"] == "Wizard Project"
    assert body["data"]["readiness"]["can_calculate"] is False
    assert body["data"]["readiness"]["status"] == "not_ready"
    assert 4 in body["data"]["readiness"]["blocking_steps"]


def test_get_wizard_state_is_scoped_to_current_organization(client: TestClient) -> None:
    token, _ = _login(client)

    with SessionLocal() as db:
        other_organization = Organization(
            name="Other Organization",
            slug=f"wizard-other-org-{uuid4().hex[:8]}",
            default_language="fr",
            is_active=True,
        )
        db.add(other_organization)
        db.flush()

        other_user = User(
            organization_id=other_organization.id,
            email=f"wizard-other-{uuid4().hex[:8]}@example.com",
            password_hash=get_password_hash("password123"),
            first_name="Other",
            last_name="User",
            role="org_admin",
            preferred_language="fr",
            is_active=True,
        )
        db.add(other_user)
        db.flush()

        project = Project(
            organization_id=other_organization.id,
            created_by_user_id=other_user.id,
            name="Foreign Project",
            building_type="hotel",
            project_goal="baseline",
            wizard_step=2,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    response = client.get(
        f"/api/v1/projects/{project_id}/wizard",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_save_wizard_usage_step_persists_payload_and_round_trips(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Usage Wizard Project",
            building_type="hotel",
            project_goal="baseline",
            wizard_step=5,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    payload = {
        "average_occupancy_rate": 0.72,
        "seasonality_profile": "seasonal",
        "room_usage_intensity": "standard",
        "ecs_intensity_level": "medium",
        "restaurant_active": True,
    }
    response = client.put(
        f"/api/v1/projects/{project_id}/wizard/steps/usage",
        json={"payload": payload},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["errors"] == []
    assert body["data"]["saved"] is True
    assert body["data"]["payload"] == payload

    state_response = client.get(
        f"/api/v1/projects/{project_id}/wizard",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert state_response.status_code == 200
    assert state_response.json()["data"]["step_payloads"]["usage"] == payload

    with SessionLocal() as db:
        saved_payload = db.query(WizardStepPayload).filter_by(
            project_id=UUID(project_id),
            step_code="usage",
        ).one()
        assert saved_payload.payload_json == payload


def test_validate_wizard_usage_step_blocks_missing_minimum_fields(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Invalid Usage Wizard Project",
            building_type="hotel",
            project_goal="baseline",
            wizard_step=5,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    response = client.post(
        f"/api/v1/projects/{project_id}/wizard/steps/usage/validate",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["data"] is None
    assert body["errors"][0]["code"] == "VALIDATION_ERROR"
    assert body["errors"][0]["details"]["step_code"] == "usage"


def test_validate_wizard_usage_step_advances_resume_step_when_valid(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Valid Usage Wizard Project",
            building_type="hotel",
            project_goal="baseline",
            wizard_step=5,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    save_response = client.put(
        f"/api/v1/projects/{project_id}/wizard/steps/usage",
        json={"payload": {"average_occupancy_rate": 0.66, "ecs_intensity_level": "medium"}},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert save_response.status_code == 200

    validate_response = client.post(
        f"/api/v1/projects/{project_id}/wizard/steps/usage/validate",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert validate_response.status_code == 200
    assert validate_response.json()["data"]["valid"] is True

    with SessionLocal() as db:
        refreshed = db.get(Project, UUID(project_id))
        assert refreshed is not None
        assert refreshed.wizard_step == 6


def test_save_wizard_usage_step_accepts_user_facing_percent(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Percent Usage Wizard Project",
            building_type="hotel",
            project_goal="baseline",
            wizard_step=5,
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    response = client.put(
        f"/api/v1/projects/{project_id}/wizard/steps/usage",
        json={"payload": {"average_occupancy_rate": 56, "ecs_intensity_level": "medium"}},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["payload"]["average_occupancy_rate"] == 0.56

    validate_response = client.post(
        f"/api/v1/projects/{project_id}/wizard/steps/usage/validate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert validate_response.status_code == 200
