from pathlib import Path
from uuid import UUID

from app.core.exceptions import NotFoundError
from app.db.models.user import User
from app.reporting.builders.executive_report_builder import ExecutiveReportBuilder
from app.repositories.building_repository import BuildingRepository
from app.repositories.calculation_repository import CalculationRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.reports import ExecutiveReportHtmlResponse


class ReportService:
    def __init__(
        self,
        project_repository: ProjectRepository,
        calculation_repository: CalculationRepository,
        building_repository: BuildingRepository,
        zone_repository: ZoneRepository,
        builder: ExecutiveReportBuilder,
    ):
        self.project_repository = project_repository
        self.calculation_repository = calculation_repository
        self.building_repository = building_repository
        self.zone_repository = zone_repository
        self.builder = builder

    def build_executive_report_html(
        self,
        calculation_run_id: UUID,
        current_user: User,
    ) -> ExecutiveReportHtmlResponse:
        run = self.calculation_repository.get_by_id(calculation_run_id)
        if run is None:
            raise NotFoundError("Calculation run not found")

        project = self.project_repository.get_by_id(run.project_id, current_user.organization_id)
        if project is None:
            raise NotFoundError("Project not found")

        building = self.building_repository.get_by_project_id(project.id)
        zones = self.zone_repository.list_by_project_id(project.id)
        context = self.builder.build_context(
            project=project,
            scenario=run.scenario,
            calculation_run=run,
            building=building,
            zones=zones,
        )
        html = self.builder.render_html(context)
        return ExecutiveReportHtmlResponse(
            calculation_run_id=run.id,
            project_id=run.project_id,
            scenario_id=run.scenario_id,
            title=context["report"]["title"],
            html=html,
            context=context,
        )


def get_reporting_templates_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "reporting" / "templates"
