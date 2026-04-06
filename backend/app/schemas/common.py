from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorItem(BaseModel):
    code: str
    message: str
    field: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class MetaPayload(BaseModel):
    warnings: list[str] = Field(default_factory=list)
    version: str | None = None


class ApiResponse(BaseModel, Generic[T]):
    data: T | None
    meta: MetaPayload = Field(default_factory=MetaPayload)
    errors: list[ErrorItem] = Field(default_factory=list)
