from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.models.calculation_run import CalculationRun
from app.db.models.generated_report import GeneratedReport
from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.models.scenario import Scenario
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


def test_project_history_returns_scoped_events_in_descending_order(client: TestClient) -> None:
    token, user = _login(client)
    now = datetime.now(UTC)

    with SessionLocal() as db:
        current_user = db.get(User, user["id"])
        assert current_user is not None

        project = Project(
            organization_id=current_user.organization_id,
            created_by_user_id=current_user.id,
            name="History Project",
            building_type="hotel",
            project_goal="traceability",
            created_at=now - timedelta(days=3),
            updated_at=now - timedelta(days=1),
        )
        db.add(project)
        db.flush()

        scenario = Scenario(
            project_id=project.id,
            name="Scenario A",
            scenario_type="custom",
            status="draft",
            created_at=now - timedelta(days=2),
            updated_at=now - timedelta(hours=12),
        )
        db.add(scenario)
        db.flush()

        calculation_run = CalculationRun(
            project_id=project.id,
            scenario_id=scenario.id,
            status="completed",
            engine_version="test",
            input_snapshot={},
            messages_json=[],
            warnings_json=[],
            created_at=now - timedelta(hours=1),
        )
        db.add(calculation_run)
        db.flush()

        report = GeneratedReport(
            organization_id=current_user.organization_id,
            project_id=project.id,
            scenario_id=scenario.id,
            calculation_run_id=calculation_run.id,
            branding_profile_id=None,
            report_type="executive",
            status="generated",
            title="Executive report",
            file_name="report.pdf",
            mime_type="application/pdf",
            storage_path="reports/report.pdf",
            file_size_bytes=128,
            generator_version="test",
            created_at=now,
        )
        db.add(report)
        db.commit()
        project_id = str(project.id)

    response = client.get(
        f"/api/v1/projects/{project_id}/history",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["errors"] == []
    actions = [event["action"] for event in body["data"]]
    assert actions == [
        "report_generated",
        "scenario_updated",
        "project_updated",
        "scenario_created",
        "project_created",
    ]
    assert all("id" not in event for event in body["data"])


def test_project_history_rejects_other_organization_project(client: TestClient) -> None:
    token, _user = _login(client)

    with SessionLocal() as db:
        other_organization = Organization(
            name="Other Organization",
            slug=f"history-other-{uuid4().hex[:8]}",
            default_language="fr",
            is_active=True,
        )
        db.add(other_organization)
        db.flush()

        other_user = User(
            organization_id=other_organization.id,
            email=f"history-{uuid4().hex[:8]}@example.com",
            password_hash="not-used",
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
            name="Hidden History",
            building_type="hotel",
            project_goal="hidden",
        )
        db.add(project)
        db.commit()
        project_id = str(project.id)

    response = client.get(
        f"/api/v1/projects/{project_id}/history",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
