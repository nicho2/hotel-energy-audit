from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.reporting.builders.executive_report_builder import ExecutiveReportBuilder
from app.repositories.building_repository import BuildingRepository
from app.repositories.calculation_repository import CalculationRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.reports import ExecutiveReportHtmlResponse
from app.services.report_service import ReportService, get_reporting_templates_dir

router = APIRouter()


def get_report_service(db: Session) -> ReportService:
    return ReportService(
        project_repository=ProjectRepository(db),
        calculation_repository=CalculationRepository(db),
        building_repository=BuildingRepository(db),
        zone_repository=ZoneRepository(db),
        builder=ExecutiveReportBuilder(get_reporting_templates_dir()),
    )


@router.get(
    "/reports/executive/{calculation_run_id}/html",
    response_model=ApiResponse[ExecutiveReportHtmlResponse],
)
def get_executive_report_html(
    calculation_run_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[ExecutiveReportHtmlResponse]:
    service = get_report_service(db)
    return success_response(service.build_executive_report_html(calculation_run_id, current_user))
