from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.schemas.common import ApiResponse, HealthPayload, success_response


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )
    register_exception_handlers(app)

    @app.get("/health", response_model=ApiResponse[HealthPayload])
    def healthcheck() -> ApiResponse[HealthPayload]:
        return success_response(HealthPayload(status="ok"))

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_application()
