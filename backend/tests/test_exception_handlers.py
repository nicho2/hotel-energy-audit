from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.exception_handlers import register_exception_handlers
from app.core.exceptions import BusinessRuleError


def test_business_rule_error_returns_standard_response() -> None:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/boom")
    def boom() -> None:
        raise BusinessRuleError(
            "Scenario already finalized",
            field="status",
            details={"current_status": "finalized"},
        )

    client = TestClient(app)
    response = client.get("/boom")

    assert response.status_code == 409
    assert response.json() == {
        "data": None,
        "meta": {"version": None, "warnings": []},
        "errors": [
            {
                "code": "BUSINESS_RULE_ERROR",
                "message": "Scenario already finalized",
                "field": "status",
                "details": {"current_status": "finalized"},
            }
        ],
    }
