from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError
from app.schemas.common import ErrorItem, error_response


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        payload = error_response(
            ErrorItem(
                code=exc.code,
                message=exc.message,
                field=exc.field,
                details=exc.details,
            ),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=payload.model_dump(mode="json"),
        )
