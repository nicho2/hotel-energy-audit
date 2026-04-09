from pathlib import Path
from uuid import UUID, uuid4

from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.db.models.branding_profile import BrandingProfile
from app.db.models.generated_report import GeneratedReport
from app.db.models.user import User
from app.reporting.builders.executive_report_builder import ExecutiveReportBuilder
from app.repositories.branding_repository import BrandingRepository
from app.repositories.building_repository import BuildingRepository
from app.repositories.calculation_repository import CalculationRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.zone_repository import ZoneRepository
from app.schemas.reports import ExecutiveReportHtmlResponse, GeneratedReportResponse


class ReportService:
    PLACEHOLDER_PDF_VERSION = "placeholder_pdf_v1"

    def __init__(
        self,
        project_repository: ProjectRepository,
        calculation_repository: CalculationRepository,
        building_repository: BuildingRepository,
        zone_repository: ZoneRepository,
        branding_repository: BrandingRepository,
        report_repository: ReportRepository,
        builder: ExecutiveReportBuilder,
    ):
        self.project_repository = project_repository
        self.calculation_repository = calculation_repository
        self.building_repository = building_repository
        self.zone_repository = zone_repository
        self.branding_repository = branding_repository
        self.report_repository = report_repository
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
        branding_profile, branding_payload = self._resolve_branding(project)
        context = self.builder.build_context(
            project=project,
            scenario=run.scenario,
            calculation_run=run,
            building=building,
            zones=zones,
            branding=branding_payload,
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

    def generate_executive_report(
        self,
        calculation_run_id: UUID,
        current_user: User,
    ) -> GeneratedReportResponse:
        html_report = self.build_executive_report_html(calculation_run_id, current_user)
        storage_root = get_report_storage_dir()
        storage_root.mkdir(parents=True, exist_ok=True)

        report_id = uuid4()
        file_name = f"executive-report-{html_report.calculation_run_id}.pdf"
        relative_storage_path = Path(str(current_user.organization_id)) / str(report_id) / file_name
        absolute_storage_path = storage_root / relative_storage_path
        absolute_storage_path.parent.mkdir(parents=True, exist_ok=True)

        pdf_bytes = self._render_placeholder_pdf(
            title=html_report.title,
            project_id=html_report.project_id,
            scenario_id=html_report.scenario_id,
            calculation_run_id=html_report.calculation_run_id,
        )
        absolute_storage_path.write_bytes(pdf_bytes)
        branding_profile, _ = self._resolve_branding(
            self.project_repository.get_by_id(html_report.project_id, current_user.organization_id)
        )

        report = self.report_repository.create(
            id=report_id,
            organization_id=current_user.organization_id,
            project_id=html_report.project_id,
            scenario_id=html_report.scenario_id,
            calculation_run_id=html_report.calculation_run_id,
            branding_profile_id=branding_profile.id if branding_profile is not None else None,
            report_type="executive",
            status="generated",
            title=html_report.title,
            file_name=file_name,
            mime_type="application/pdf",
            storage_path=relative_storage_path.as_posix(),
            file_size_bytes=len(pdf_bytes),
            generator_version=self.PLACEHOLDER_PDF_VERSION,
        )
        return self._to_generated_report_response(report)

    def get_generated_report(self, report_id: UUID, current_user: User) -> GeneratedReportResponse:
        report = self.report_repository.get_by_id(report_id, current_user.organization_id)
        if report is None:
            raise NotFoundError("Generated report not found")
        return self._to_generated_report_response(report)

    def list_generated_reports(self, project_id: UUID, current_user: User) -> list[GeneratedReportResponse]:
        project = self.project_repository.get_by_id(project_id, current_user.organization_id)
        if project is None:
            raise NotFoundError("Project not found")

        reports = self.report_repository.list_by_project_id(project_id, current_user.organization_id)
        return [self._to_generated_report_response(report) for report in reports]

    def get_generated_report_file(self, report_id: UUID, current_user: User) -> tuple[GeneratedReport, Path]:
        report = self.report_repository.get_by_id(report_id, current_user.organization_id)
        if report is None:
            raise NotFoundError("Generated report not found")

        file_path = _resolve_report_file_path(report.storage_path)
        if not file_path.is_file():
            raise NotFoundError("Generated report file not found")

        return report, file_path

    @staticmethod
    def _to_generated_report_response(report: GeneratedReport) -> GeneratedReportResponse:
        return GeneratedReportResponse(
            id=report.id,
            organization_id=report.organization_id,
            project_id=report.project_id,
            scenario_id=report.scenario_id,
            calculation_run_id=report.calculation_run_id,
            branding_profile_id=report.branding_profile_id,
            report_type=report.report_type,
            status=report.status,
            title=report.title,
            file_name=report.file_name,
            mime_type=report.mime_type,
            file_size_bytes=report.file_size_bytes,
            generator_version=report.generator_version,
            created_at=report.created_at,
        )

    @staticmethod
    def _render_placeholder_pdf(
        *,
        title: str,
        project_id: UUID,
        scenario_id: UUID,
        calculation_run_id: UUID,
    ) -> bytes:
        lines = [
            title,
            "",
            "Executive report placeholder",
            f"Project ID: {project_id}",
            f"Scenario ID: {scenario_id}",
            f"Calculation run ID: {calculation_run_id}",
            "",
            "A richer PDF renderer can replace this placeholder without changing the API contract.",
        ]
        return _build_simple_pdf("\n".join(lines))

    def _resolve_branding(self, project) -> tuple[BrandingProfile | None, dict]:
        if project is None:
            return None, {}

        branding_profile = None
        source = "fallback"
        if project.branding_profile_id is not None:
            branding_profile = self.branding_repository.get_by_id(
                project.branding_profile_id,
                project.organization_id,
            )
            source = "project" if branding_profile is not None else "fallback"

        if branding_profile is None:
            branding_profile = self.branding_repository.get_default_for_organization(project.organization_id)
            if branding_profile is not None:
                source = "organization_default"

        if branding_profile is None:
            return None, {"source": source}

        return branding_profile, {
            "id": str(branding_profile.id),
            "source": source,
            "company_name": branding_profile.company_name,
            "accent_color": branding_profile.accent_color,
            "logo_text": branding_profile.logo_text,
            "contact_email": branding_profile.contact_email,
            "cover_tagline": branding_profile.cover_tagline,
            "footer_note": branding_profile.footer_note,
        }


def get_reporting_templates_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "reporting" / "templates"


def get_report_storage_dir() -> Path:
    return Path(settings.report_storage_dir).resolve()


def _resolve_report_file_path(storage_path: str) -> Path:
    storage_root = get_report_storage_dir()
    file_path = (storage_root / Path(storage_path)).resolve()
    if storage_root not in file_path.parents:
        raise NotFoundError("Generated report file not found")
    return file_path


def _build_simple_pdf(text: str) -> bytes:
    safe_text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    text_commands = "\n".join(
        [
            "BT",
            "/F1 12 Tf",
            "50 780 Td",
            "16 TL",
            *[f"({line}) Tj T*" for line in safe_text.splitlines()],
            "ET",
        ]
    )
    stream = text_commands.encode("latin-1", errors="replace")
    objects = [
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj",
        (
            b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj"
        ),
        b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj",
        f"5 0 obj << /Length {len(stream)} >> stream\n".encode("latin-1") + stream + b"\nendstream endobj",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)
        pdf.extend(b"\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))

    pdf.extend(
        (
            "trailer\n"
            f"<< /Size {len(offsets)} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n"
            "%%EOF\n"
        ).encode("latin-1")
    )
    return bytes(pdf)
