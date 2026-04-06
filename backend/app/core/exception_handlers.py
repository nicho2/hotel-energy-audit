from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
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

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        error_items: list[ErrorItem] = []
        for item in exc.errors():
            location = item.get("loc", ())
            field = location[-1] if location else None
            if field in {"body", "query", "path"}:
                field = None

            error_items.append(
                ErrorItem(
                    code="VALIDATION_ERROR",
                    message="Validation failed",
                    field=str(field) if field is not None else None,
                    details={"reason": item.get("msg", "Invalid value")},
                )
            )

        payload = error_response(*error_items)
        return JSONResponse(status_code=422, content=payload.model_dump(mode="json"))
