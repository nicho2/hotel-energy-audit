from app.core.exceptions import NotFoundError
from app.repositories.audit_repository import AuditRepository
from app.repositories.history_repository import HistoryRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.history import ProjectHistoryEventResponse


class HistoryService:
    def __init__(
        self,
        project_repository: ProjectRepository,
        history_repository: HistoryRepository,
        audit_repository: AuditRepository,
    ):
        self.project_repository = project_repository
        self.history_repository = history_repository
        self.audit_repository = audit_repository

    def list_project_history(self, project_id, current_user) -> list[ProjectHistoryEventResponse]:
        project = self.project_repository.get_by_id(project_id, current_user.organization_id)
        if project is None:
            raise NotFoundError("Project not found")

        audit_logs = self.audit_repository.list_for_project(project.id, current_user.organization_id)
        if audit_logs:
            return [_audit_log_to_history_event(item) for item in audit_logs]

        return self._list_legacy_project_history(project, current_user)

    def list_scenario_history(
        self,
        project_id,
        scenario_id,
        current_user,
    ) -> list[ProjectHistoryEventResponse]:
        project = self.project_repository.get_by_id(project_id, current_user.organization_id)
        if project is None:
            raise NotFoundError("Project not found")
        scenario = next(
            (item for item in self.history_repository.list_scenarios(project.id) if item.id == scenario_id),
            None,
        )
        if scenario is None:
            raise NotFoundError("Scenario not found")

        audit_logs = self.audit_repository.list_for_scenario(
            project_id=project.id,
            scenario_id=scenario.id,
            organization_id=current_user.organization_id,
        )
        if audit_logs:
            return [_audit_log_to_history_event(item) for item in audit_logs]

        events = [
            ProjectHistoryEventResponse(
                action="scenario_created",
                actor="System",
                occurred_at=scenario.created_at,
                summary=scenario.name,
            )
        ]
        if scenario.updated_at and scenario.updated_at != scenario.created_at:
            events.append(
                ProjectHistoryEventResponse(
                    action="scenario_updated",
                    actor="System",
                    occurred_at=scenario.updated_at,
                    summary=scenario.name,
                )
            )
        return sorted(events, key=lambda event: event.occurred_at, reverse=True)

    def _list_legacy_project_history(self, project, current_user) -> list[ProjectHistoryEventResponse]:
        actor = self._format_actor(project.created_by_user)
        events = [
            ProjectHistoryEventResponse(
                action="project_created",
                actor=actor,
                occurred_at=project.created_at,
                summary=project.name,
            )
        ]

        if project.updated_at and project.updated_at != project.created_at:
            events.append(
                ProjectHistoryEventResponse(
                    action="project_updated",
                    actor=actor,
                    occurred_at=project.updated_at,
                    summary=project.name,
                )
            )

        for scenario in self.history_repository.list_scenarios(project.id):
            events.append(
                ProjectHistoryEventResponse(
                    action="scenario_created",
                    actor="System",
                    occurred_at=scenario.created_at,
                    summary=scenario.name,
                )
            )
            if scenario.updated_at and scenario.updated_at != scenario.created_at:
                events.append(
                    ProjectHistoryEventResponse(
                        action="scenario_updated",
                        actor="System",
                        occurred_at=scenario.updated_at,
                        summary=scenario.name,
                    )
                )

        for report in self.history_repository.list_reports(project.id, current_user.organization_id):
            events.append(
                ProjectHistoryEventResponse(
                    action="report_generated",
                    actor="System",
                    occurred_at=report.created_at,
                    summary=report.title,
                )
            )

        return sorted(events, key=lambda event: event.occurred_at, reverse=True)

    @staticmethod
    def _format_actor(user) -> str:
        if user is None:
            return "System"

        full_name = " ".join(part for part in [user.first_name, user.last_name] if part)
        return full_name or user.email


def _audit_log_to_history_event(item) -> ProjectHistoryEventResponse:
    payload = item.after_json or item.before_json or {}
    summary = (
        payload.get("name")
        or payload.get("title")
        or payload.get("code")
        or payload.get("status")
        or str(item.entity_id)
    )
    actor = "System" if item.user_id is None else str(item.user_id)
    return ProjectHistoryEventResponse(
        action=item.action,
        actor=actor,
        occurred_at=item.timestamp,
        summary=summary,
    )
