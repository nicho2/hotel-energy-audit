from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppError, UnauthorizedError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError):
        status = 401 if isinstance(exc, UnauthorizedError) else 422
        return JSONResponse(
            status_code=status,
            content={
                "data": None,
                "meta": {},
                "errors": [
                    {
                        "code": exc.code,
                        "message": exc.message,
                        "field": exc.field,
                        "details": exc.details,
                    }
                ],
            },
        )
