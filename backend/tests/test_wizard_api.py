from fastapi.testclient import TestClient

from app.core.security import get_password_hash
from app.db.models.organization import Organization
from app.db.models.project import Project
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
    assert body["data"]["readiness"]["can_calculate"] is False
    assert body["data"]["readiness"]["status"] == "not_ready"
    assert body["data"]["readiness"]["blocking_steps"] == [4, 5, 6, 7, 8, 9, 10]


def test_get_wizard_state_is_scoped_to_current_organization(client: TestClient) -> None:
    token, _ = _login(client)

    with SessionLocal() as db:
        other_organization = Organization(
            name="Other Organization",
            slug="wizard-other-org",
            default_language="fr",
            is_active=True,
        )
        db.add(other_organization)
        db.flush()

        other_user = User(
            organization_id=other_organization.id,
            email="wizard-other@example.com",
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
