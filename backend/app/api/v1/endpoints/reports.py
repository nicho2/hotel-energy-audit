from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps.auth import get_current_user
from app.api.deps.db import get_db
from app.db.models.user import User
from app.reporting.builders.executive_report_builder import ExecutiveReportBuilder
from app.repositories.branding_repository import BrandingRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.calculation_repository import CalculationRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.common import ApiResponse, success_response
from app.schemas.reports import ExecutiveReportHtmlResponse, GeneratedReportResponse
from app.services.report_service import ReportService, get_reporting_templates_dir

router = APIRouter()


def get_report_service(db: Session) -> ReportService:
    return ReportService(
        project_repository=ProjectRepository(db),
        calculation_repository=CalculationRepository(db),
        building_repository=BuildingRepository(db),
        zone_repository=ZoneRepository(db),
        branding_repository=BrandingRepository(db),
        report_repository=ReportRepository(db),
        builder=ExecutiveReportBuilder(get_reporting_templates_dir()),
    )


@router.get(
    "/projects/{project_id}/reports",
    response_model=ApiResponse[list[GeneratedReportResponse]],
)
def list_generated_reports(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[list[GeneratedReportResponse]]:
    service = get_report_service(db)
    return success_response(service.list_generated_reports(project_id, current_user))


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


@router.post(
    "/reports/executive/{calculation_run_id}/generate",
    response_model=ApiResponse[GeneratedReportResponse],
)
def generate_executive_report(
    calculation_run_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[GeneratedReportResponse]:
    service = get_report_service(db)
    return success_response(service.generate_executive_report(calculation_run_id, current_user))


@router.get("/reports/{report_id}", response_model=ApiResponse[GeneratedReportResponse])
def get_generated_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApiResponse[GeneratedReportResponse]:
    service = get_report_service(db)
    return success_response(service.get_generated_report(report_id, current_user))


@router.get("/reports/{report_id}/download")
def download_generated_report(
    report_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FileResponse:
    service = get_report_service(db)
    report, file_path = service.get_generated_report_file(report_id, current_user)
    return FileResponse(path=file_path, media_type=report.mime_type, filename=report.file_name)
