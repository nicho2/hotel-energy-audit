from app.core.exceptions import NotFoundError
from app.repositories.history_repository import HistoryRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.history import ProjectHistoryEventResponse


class HistoryService:
    def __init__(self, project_repository: ProjectRepository, history_repository: HistoryRepository):
        self.project_repository = project_repository
        self.history_repository = history_repository

    def list_project_history(self, project_id, current_user) -> list[ProjectHistoryEventResponse]:
        project = self.project_repository.get_by_id(project_id, current_user.organization_id)
        if project is None:
            raise NotFoundError("Project not found")

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
