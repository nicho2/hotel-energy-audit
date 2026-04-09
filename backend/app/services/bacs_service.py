from collections import defaultdict
from dataclasses import dataclass

from app.core.exceptions import ValidationError
from app.repositories.bacs_repository import BacsRepository
from app.schemas.bacs import (
    BacsCurrentResponse,
    BacsDomainScoreResponse,
    BacsFunctionResponse,
    BacsMissingFunctionResponse,
    BacsSummaryResponse,
)
from app.services.project_service import ProjectService


DOMAIN_ORDER = ("monitoring", "heating", "cooling_ventilation", "dhw", "lighting")
CLASS_THRESHOLDS = (
    (80.0, "A"),
    (65.0, "B"),
    (50.0, "C"),
    (35.0, "D"),
    (0.0, "E"),
)
TOP_MISSING_LIMIT = 5


@dataclass(frozen=True)
class BacsScoringSnapshot:
    overall_score: float
    bacs_class: str
    domain_scores: list[BacsDomainScoreResponse]
    top_missing_functions: list[BacsMissingFunctionResponse]
    selected_function_count: int
    total_function_count: int


class BacsService:
    def __init__(
        self,
        bacs_repository: BacsRepository,
        project_service: ProjectService,
    ):
        self.bacs_repository = bacs_repository
        self.project_service = project_service

    def get_current_assessment(self, project_id, current_user) -> BacsCurrentResponse:
        project = self.project_service.get_project(project_id, current_user)
        return self._build_current_response(project.id)

    def upsert_current_assessment(self, project_id, payload, current_user) -> BacsCurrentResponse:
        project = self.project_service.get_project(project_id, current_user)
        assessment = self.bacs_repository.get_assessment_by_project_id(project.id)
        data = payload.model_dump()

        if assessment is None:
            self.bacs_repository.create_assessment(project_id=project.id, version="v1", **data)
        else:
            self.bacs_repository.update_assessment(assessment, **data)

        return self._build_current_response(project.id)

    def replace_current_functions(self, project_id, payload, current_user) -> BacsCurrentResponse:
        project = self.project_service.get_project(project_id, current_user)
        assessment = self.bacs_repository.get_assessment_by_project_id(project.id)
        if assessment is None:
            assessment = self.bacs_repository.create_assessment(project_id=project.id, version="v1")

        selected_function_ids = list(dict.fromkeys(payload.selected_function_ids))
        definitions = self.bacs_repository.get_function_definitions_by_ids(selected_function_ids)
        if len(definitions) != len(selected_function_ids):
            raise ValidationError(
                "Validation failed",
                field="selected_function_ids",
                details={"reason": "all selected functions must exist in the active BACS V1 catalog"},
            )

        self.bacs_repository.replace_selected_functions(
            assessment.id,
            [definition.id for definition in definitions],
        )
        return self._build_current_response(project.id)

    def get_current_summary(self, project_id, current_user) -> BacsSummaryResponse:
        project = self.project_service.get_project(project_id, current_user)
        assessment = self.bacs_repository.get_assessment_by_project_id(project.id)
        scoring = self._build_scoring_snapshot(assessment.id if assessment is not None else None)

        return BacsSummaryResponse(
            assessment_id=assessment.id if assessment is not None else None,
            project_id=project.id,
            version=assessment.version if assessment is not None else "v1",
            confidence_score=round(
                scoring.selected_function_count / scoring.total_function_count,
                2,
            )
            if scoring.total_function_count > 0
            else 0.0,
            overall_score=scoring.overall_score,
            estimated_bacs_class=scoring.bacs_class,
            manual_override_class=assessment.manual_override_class if assessment is not None else None,
            bacs_class=(assessment.manual_override_class if assessment and assessment.manual_override_class else scoring.bacs_class),
            selected_function_count=scoring.selected_function_count,
            total_function_count=scoring.total_function_count,
            domain_scores=scoring.domain_scores,
            top_missing_functions=scoring.top_missing_functions,
        )

    def _build_current_response(self, project_id) -> BacsCurrentResponse:
        assessment = self.bacs_repository.get_assessment_by_project_id(project_id)
        functions = self._build_function_snapshot(assessment.id if assessment is not None else None)
        return BacsCurrentResponse(
            assessment_id=assessment.id if assessment is not None else None,
            project_id=project_id,
            version=assessment.version if assessment is not None else "v1",
            assessor_name=assessment.assessor_name if assessment is not None else None,
            manual_override_class=assessment.manual_override_class if assessment is not None else None,
            notes=assessment.notes if assessment is not None else None,
            functions=functions,
        )

    def _build_function_snapshot(self, assessment_id) -> list[BacsFunctionResponse]:
        definitions = self.bacs_repository.list_function_definitions()
        selected_ids = set()
        if assessment_id is not None:
            selected_ids = {
                selection.function_definition_id
                for selection in self.bacs_repository.list_selected_for_assessment(assessment_id)
            }

        return [
            BacsFunctionResponse(
                id=definition.id,
                code=definition.code,
                domain=definition.domain,
                name=definition.name,
                description=definition.description,
                weight=definition.weight,
                order_index=definition.order_index,
                is_selected=definition.id in selected_ids,
            )
            for definition in definitions
        ]

    def _build_scoring_snapshot(self, assessment_id) -> BacsScoringSnapshot:
        definitions = self.bacs_repository.list_function_definitions()
        selected_ids = set()
        if assessment_id is not None:
            selected_ids = {
                selection.function_definition_id
                for selection in self.bacs_repository.list_selected_for_assessment(assessment_id)
            }

        total_weight_by_domain: dict[str, float] = defaultdict(float)
        selected_weight_by_domain: dict[str, float] = defaultdict(float)
        total_weight = 0.0
        selected_weight = 0.0
        missing_definitions = []

        for definition in definitions:
            total_weight_by_domain[definition.domain] += definition.weight
            total_weight += definition.weight
            if definition.id in selected_ids:
                selected_weight_by_domain[definition.domain] += definition.weight
                selected_weight += definition.weight
            else:
                missing_definitions.append(definition)

        domain_scores = [
            BacsDomainScoreResponse(
                domain=domain,
                score=round(
                    selected_weight_by_domain[domain] / total_weight_by_domain[domain] * 100.0,
                    1,
                )
                if total_weight_by_domain[domain] > 0
                else 0.0,
                selected_weight=round(selected_weight_by_domain[domain], 2),
                total_weight=round(total_weight_by_domain[domain], 2),
            )
            for domain in DOMAIN_ORDER
            if total_weight_by_domain[domain] > 0
        ]

        overall_score = round(selected_weight / total_weight * 100.0, 1) if total_weight > 0 else 0.0
        top_missing_functions = [
            BacsMissingFunctionResponse(
                id=definition.id,
                code=definition.code,
                domain=definition.domain,
                name=definition.name,
                description=definition.description,
                weight=definition.weight,
            )
            for definition in sorted(
                missing_definitions,
                key=lambda item: (-item.weight, item.name, item.domain, item.order_index),
            )[:TOP_MISSING_LIMIT]
        ]

        return BacsScoringSnapshot(
            overall_score=overall_score,
            bacs_class=self._map_score_to_class(overall_score),
            domain_scores=domain_scores,
            top_missing_functions=top_missing_functions,
            selected_function_count=len(selected_ids),
            total_function_count=len(definitions),
        )

    @staticmethod
    def _map_score_to_class(score: float) -> str:
        for threshold, bacs_class in CLASS_THRESHOLDS:
            if score >= threshold:
                return bacs_class
        return "E"
