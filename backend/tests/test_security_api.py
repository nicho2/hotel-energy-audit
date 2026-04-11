from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import get_password_hash
from app.db.models.calculation_run import CalculationRun
from app.db.models.generated_report import GeneratedReport
from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.models.scenario import Scenario
from app.db.models.user import User
from app.db.session import SessionLocal
from test_admin_api import _login
from test_calculations_api import _create_ready_project_with_scenario


def _create_other_org_user() -> tuple[str, str]:
    email = f"security-other-{uuid4().hex[:8]}@example.com"
    password = "password123"
    with SessionLocal() as db:
        organization = Organization(
            name="Security Other Org",
            slug=f"security-other-{uuid4().hex[:8]}",
            default_language="fr",
            is_active=True,
        )
        db.add(organization)
        db.flush()
        user = User(
            organization_id=organization.id,
            email=email,
            password_hash=get_password_hash(password),
            first_name="Security",
            last_name="Other",
            role="org_admin",
            preferred_language="fr",
            is_active=True,
        )
        db.add(user)
        db.commit()
    return email, password


def _create_other_org_project() -> str:
    email, _password = _create_other_org_user()
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == email).one()
        project = Project(
            organization_id=user.organization_id,
            created_by_user_id=user.id,
            name="Cross Org Project",
            building_type="hotel",
            project_goal="forbidden",
        )
        db.add(project)
        db.commit()
        return str(project.id)


def test_jwt_claims_must_match_current_user_state(client: TestClient) -> None:
    token, user = _login(client)

    with SessionLocal() as db:
        db_user = db.get(User, user["id"])
        assert db_user is not None
        db_user.role = "org_member"
        db.add(db_user)
        db.commit()

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_cross_organization_project_access_is_not_found(client: TestClient) -> None:
    token, _user = _login(client)
    other_project_id = _create_other_org_project()

    response = client.get(
        f"/api/v1/projects/{other_project_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_admin_endpoint_rejects_org_member_role(client: TestClient) -> None:
    _token, admin_user = _login(client)
    email = f"security-member-{uuid4().hex[:8]}@example.com"
    password = "password123"

    with SessionLocal() as db:
        user = User(
            organization_id=admin_user["organization_id"],
            email=email,
            password_hash=get_password_hash(password),
            first_name="Security",
            last_name="Member",
            role="org_member",
            preferred_language="fr",
            is_active=True,
        )
        db.add(user)
        db.commit()

    member_token, _member = _login(client, email, password)
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {member_token}"},
    )

    assert response.status_code == 403


def test_report_download_is_forbidden_outside_organization(client: TestClient) -> None:
    token, _project_id, _scenario_id = _create_ready_project_with_scenario(client)
    calculate_response = client.post(
        f"/api/v1/projects/{_project_id}/scenarios/{_scenario_id}/calculate",
        headers={"Authorization": f"Bearer {token}"},
    )
    calculation_run_id = calculate_response.json()["data"]["calculation_run_id"]
    report_response = client.post(
        f"/api/v1/reports/executive/{calculation_run_id}/generate",
        headers={"Authorization": f"Bearer {token}"},
    )
    report_id = report_response.json()["data"]["id"]

    other_email, other_password = _create_other_org_user()
    other_token, _other_user = _login(client, other_email, other_password)
    response = client.get(
        f"/api/v1/reports/{report_id}/download",
        headers={"Authorization": f"Bearer {other_token}"},
    )

    assert response.status_code == 404


def test_report_download_rejects_path_traversal_storage_path(client: TestClient) -> None:
    token, user = _login(client)
    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Traversal Report Project",
            building_type="hotel",
            project_goal="security",
        )
        db.add(project)
        db.flush()
        scenario = Scenario(project_id=project.id, name="Traversal Scenario")
        db.add(scenario)
        db.flush()
        run = CalculationRun(
            project_id=project.id,
            scenario_id=scenario.id,
            status="completed",
            engine_version="security-test",
            input_snapshot={},
            messages_json=[],
            warnings_json=[],
        )
        db.add(run)
        db.flush()
        report = GeneratedReport(
            organization_id=project.organization_id,
            project_id=project.id,
            scenario_id=scenario.id,
            calculation_run_id=run.id,
            branding_profile_id=None,
            report_type="executive",
            status="generated",
            title="Traversal report",
            file_name="report.pdf",
            mime_type="application/pdf",
            storage_path="../secret.pdf",
            file_size_bytes=12,
            generator_version="security-test",
        )
        db.add(report)
        db.commit()
        report_id = str(report.id)

    response = client.get(
        f"/api/v1/reports/{report_id}/download",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
