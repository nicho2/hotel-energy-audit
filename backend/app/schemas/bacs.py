from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

BacsDomain = Literal["monitoring", "heating", "cooling_ventilation", "dhw", "lighting"]
BacsClass = Literal["A", "B", "C", "D", "E"]


class BacsAssessmentUpsert(BaseModel):
    assessor_name: str | None = Field(default=None, max_length=255)
    manual_override_class: BacsClass | None = None
    notes: str | None = None


class BacsCurrentFunctionsUpdate(BaseModel):
    selected_function_ids: list[UUID] = Field(default_factory=list)


class BacsFunctionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    domain: BacsDomain
    name: str
    description: str | None
    weight: float
    order_index: int
    is_selected: bool


class BacsCurrentResponse(BaseModel):
    assessment_id: UUID | None
    project_id: UUID
    version: str
    assessor_name: str | None
    manual_override_class: BacsClass | None
    notes: str | None
    functions: list[BacsFunctionResponse]


class BacsDomainScoreResponse(BaseModel):
    domain: BacsDomain
    score: float
    selected_weight: float
    total_weight: float


class BacsMissingFunctionResponse(BaseModel):
    id: UUID
    code: str
    domain: BacsDomain
    name: str
    description: str | None
    weight: float


class BacsSummaryResponse(BaseModel):
    assessment_id: UUID | None
    project_id: UUID
    version: str
    confidence_score: float
    overall_score: float
    estimated_bacs_class: BacsClass
    manual_override_class: BacsClass | None
    bacs_class: BacsClass
    selected_function_count: int
    total_function_count: int
    domain_scores: list[BacsDomainScoreResponse]
    top_missing_functions: list[BacsMissingFunctionResponse]
