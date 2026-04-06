import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from scripts.seed_all import seed_dev_auth_data


@pytest.fixture
def client() -> TestClient:
    settings.secret_key = "test-secret-key"
    seed_dev_auth_data()
    return TestClient(app)
