from collections.abc import Mapping
from http import HTTPStatus
from typing import Any


class AppError(Exception):
    code = "APPLICATION_ERROR"
    message = "Application error"
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(
        self,
        message: str | None = None,
        *,
        code: str | None = None,
        field: str | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        self.message = message or self.message
        self.code = code or self.code
        self.field = field
        self.details = dict(details or {})
        super().__init__(self.message)


class NotFoundError(AppError):
    code = "NOT_FOUND"
    message = "Resource not found"
    status_code = HTTPStatus.NOT_FOUND


class ValidationError(AppError):
    code = "VALIDATION_ERROR"
    message = "Validation failed"
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class BusinessRuleError(AppError):
    code = "BUSINESS_RULE_ERROR"
    message = "Business rule error"
    status_code = HTTPStatus.CONFLICT
