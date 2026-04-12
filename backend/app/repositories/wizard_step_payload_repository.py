from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.wizard_step_payload import WizardStepPayload


class WizardStepPayloadRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_project_id(self, project_id: UUID) -> list[WizardStepPayload]:
        statement = (
            select(WizardStepPayload)
            .where(WizardStepPayload.project_id == project_id)
            .order_by(WizardStepPayload.step_code.asc())
        )
        return list(self.db.scalars(statement).all())

    def get_by_project_and_step(self, project_id: UUID, step_code: str) -> WizardStepPayload | None:
        statement = select(WizardStepPayload).where(
            WizardStepPayload.project_id == project_id,
            WizardStepPayload.step_code == step_code,
        )
        return self.db.scalar(statement)

    def upsert(self, project_id: UUID, step_code: str, payload_json: dict) -> WizardStepPayload:
        payload = self.get_by_project_and_step(project_id, step_code)
        if payload is None:
            payload = WizardStepPayload(
                project_id=project_id,
                step_code=step_code,
                payload_json=payload_json,
            )
            self.db.add(payload)
        else:
            payload.payload_json = payload_json
            self.db.add(payload)

        self.db.commit()
        self.db.refresh(payload)
        return payload
