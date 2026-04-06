from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, selectinload

from app.db.models.bacs_assessment import BacsAssessment
from app.db.models.bacs_function_definition import BacsFunctionDefinition
from app.db.models.bacs_selected_function import BacsSelectedFunction


class BacsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_assessment_by_project_id(self, project_id: UUID) -> BacsAssessment | None:
        statement = (
            select(BacsAssessment)
            .where(BacsAssessment.project_id == project_id)
            .options(selectinload(BacsAssessment.selected_functions))
        )
        return self.db.scalar(statement)

    def create_assessment(self, **kwargs: object) -> BacsAssessment:
        assessment = BacsAssessment(**kwargs)
        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)
        return assessment

    def update_assessment(self, assessment: BacsAssessment, **kwargs: object) -> BacsAssessment:
        for field, value in kwargs.items():
            setattr(assessment, field, value)

        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)
        return assessment

    def list_function_definitions(self, version: str = "v1") -> list[BacsFunctionDefinition]:
        statement = (
            select(BacsFunctionDefinition)
            .where(
                BacsFunctionDefinition.version == version,
                BacsFunctionDefinition.is_active.is_(True),
            )
            .order_by(
                BacsFunctionDefinition.domain.asc(),
                BacsFunctionDefinition.order_index.asc(),
                BacsFunctionDefinition.name.asc(),
            )
        )
        return list(self.db.scalars(statement).all())

    def get_function_definitions_by_ids(
        self,
        function_ids: list[UUID],
        version: str = "v1",
    ) -> list[BacsFunctionDefinition]:
        if not function_ids:
            return []

        statement = select(BacsFunctionDefinition).where(
            BacsFunctionDefinition.id.in_(function_ids),
            BacsFunctionDefinition.version == version,
            BacsFunctionDefinition.is_active.is_(True),
        )
        return list(self.db.scalars(statement).all())

    def list_selected_for_assessment(self, assessment_id: UUID) -> list[BacsSelectedFunction]:
        statement = (
            select(BacsSelectedFunction)
            .where(BacsSelectedFunction.assessment_id == assessment_id)
            .options(selectinload(BacsSelectedFunction.function_definition))
        )
        return list(self.db.scalars(statement).all())

    def replace_selected_functions(
        self,
        assessment_id: UUID,
        function_definition_ids: list[UUID],
    ) -> list[BacsSelectedFunction]:
        self.db.execute(
            delete(BacsSelectedFunction).where(BacsSelectedFunction.assessment_id == assessment_id)
        )
        selections = [
            BacsSelectedFunction(
                assessment_id=assessment_id,
                function_definition_id=function_definition_id,
            )
            for function_definition_id in function_definition_ids
        ]
        if selections:
            self.db.add_all(selections)
        self.db.commit()
        return self.list_selected_for_assessment(assessment_id)
