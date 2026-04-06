from pathlib import Path
import shutil

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


@pytest.fixture(autouse=True)
def report_storage_dir() -> None:
    previous = settings.report_storage_dir
    storage_dir = Path("test-artifacts") / "reports"
    if storage_dir.parent.exists():
        shutil.rmtree(storage_dir.parent, ignore_errors=True)
    storage_dir.mkdir(parents=True, exist_ok=True)
    settings.report_storage_dir = str(storage_dir)
    yield
    shutil.rmtree(storage_dir.parent, ignore_errors=True)
    settings.report_storage_dir = previous
