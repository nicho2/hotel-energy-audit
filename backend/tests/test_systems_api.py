from fastapi.testclient import TestClient

from app.db.models.project import Project
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


def _create_project(client: TestClient) -> tuple[str, str]:
    token, user = _login(client)

    with SessionLocal() as db:
        project = Project(
            organization_id=user["organization_id"],
            created_by_user_id=user["id"],
            name="Systems Project",
            building_type="hotel",
            project_goal="baseline",
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        project_id = str(project.id)

    return token, project_id


def test_system_crud_allows_create_update_delete(client: TestClient) -> None:
    token, project_id = _create_project(client)

    create_response = client.post(
        f"/api/v1/projects/{project_id}/systems",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Main boilers",
            "system_type": "heating",
            "energy_source": "natural_gas",
            "technology_type": "gas_boiler",
            "efficiency_level": "standard",
            "serves": "Guest rooms and common areas",
            "quantity": 2,
            "year_installed": 2014,
            "is_primary": True,
            "notes": "Condensing boilers",
            "order_index": 1,
        },
    )
    assert create_response.status_code == 200
    created_body = create_response.json()
    system_id = created_body["data"]["id"]
    assert created_body["data"]["system_type"] == "heating"
    assert created_body["data"]["energy_source"] == "natural_gas"
    assert created_body["data"]["technology_type"] == "gas_boiler"
    assert created_body["data"]["efficiency_level"] == "standard"

    update_response = client.patch(
        f"/api/v1/projects/{project_id}/systems/{system_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Main boiler plant",
            "notes": "Condensing boilers with sequencer",
            "system_type": "control",
            "energy_source": "electricity",
            "technology_type": "bms",
            "efficiency_level": "high",
        },
    )
    assert update_response.status_code == 200
    updated_body = update_response.json()
    assert updated_body["data"]["name"] == "Main boiler plant"
    assert updated_body["data"]["system_type"] == "control"
    assert updated_body["data"]["energy_source"] == "electricity"
    assert updated_body["data"]["technology_type"] == "bms"
    assert updated_body["data"]["efficiency_level"] == "high"

    list_response = client.get(
        f"/api/v1/projects/{project_id}/systems",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    assert len(list_response.json()["data"]) == 1

    delete_response = client.delete(
        f"/api/v1/projects/{project_id}/systems/{system_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200

    final_list_response = client.get(
        f"/api/v1/projects/{project_id}/systems",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert final_list_response.status_code == 200
    assert final_list_response.json()["data"] == []


def test_system_list_orders_by_order_index_then_name(client: TestClient) -> None:
    token, project_id = _create_project(client)

    payloads = [
        {"name": "Secondary chiller", "system_type": "cooling", "order_index": 2},
        {"name": "Primary chiller", "system_type": "cooling", "order_index": 1},
        {"name": "Aux pumps", "system_type": "auxiliaries", "order_index": 1},
    ]
    for payload in payloads:
        response = client.post(
            f"/api/v1/projects/{project_id}/systems",
            headers={"Authorization": f"Bearer {token}"},
            json=payload,
        )
        assert response.status_code == 200

    list_response = client.get(
        f"/api/v1/projects/{project_id}/systems",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    names = [item["name"] for item in list_response.json()["data"]]
    assert names == ["Aux pumps", "Primary chiller", "Secondary chiller"]


def test_system_create_rejects_invalid_quantity(client: TestClient) -> None:
    token, project_id = _create_project(client)

    response = client.post(
        f"/api/v1/projects/{project_id}/systems",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Bad system",
            "system_type": "ventilation",
            "quantity": 0,
        },
    )

    assert response.status_code == 422
    body = response.json()
    assert body["errors"][0]["code"] == "VALIDATION_ERROR"
    assert body["errors"][0]["field"] == "quantity"
