from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorItem(BaseModel):
    code: str
    message: str
    field: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class MetaPayload(BaseModel):
    version: str | None = None
    warnings: list[str] = Field(default_factory=list)


class ApiResponse(BaseModel, Generic[T]):
    data: T | None
    meta: MetaPayload = Field(default_factory=MetaPayload)
    errors: list[ErrorItem] = Field(default_factory=list)


class HealthPayload(BaseModel):
    status: str


def success_response(
    data: T,
    *,
    meta: MetaPayload | None = None,
) -> ApiResponse[T]:
    return ApiResponse(data=data, meta=meta or MetaPayload(), errors=[])


def error_response(
    *errors: ErrorItem,
    meta: MetaPayload | None = None,
) -> ApiResponse[None]:
    return ApiResponse(data=None, meta=meta or MetaPayload(), errors=list(errors))
