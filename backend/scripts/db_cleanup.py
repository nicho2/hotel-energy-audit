from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.config import settings
from app.db import models  # noqa: F401 - import models so Base metadata is complete.
from app.db.base import Base
from app.db.models.audit_log import AuditLog
from app.db.models.generated_report import GeneratedReport
from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.session import SessionLocal
from scripts.demo_seed_data import DEMO_PROJECT_REFERENCE_CODES
from scripts.seed_all import main as seed_all


PRESERVED_TABLES = {
    "alembic_version",
    "organizations",
    "users",
    "branding_profiles",
    "project_templates",
    "country_profiles",
    "climate_zones",
    "usage_profiles",
    "bacs_function_definitions",
    "calculation_assumption_sets",
    "solution_catalogs",
    "solution_definitions",
}

PROJECT_DATA_TABLES = {
    "projects",
    "buildings",
    "building_zones",
    "technical_systems",
    "bacs_assessments",
    "bacs_selected_functions",
    "scenarios",
    "scenario_solution_assignments",
    "calculation_runs",
    "result_summaries",
    "economic_results",
    "result_by_use",
    "result_by_zone",
    "generated_reports",
    "wizard_step_payloads",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect and clean the local Hotel Energy Audit database.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually modify the database. Without this flag every cleanup command is a dry run.",
    )
    parser.add_argument(
        "--organization-slug",
        help="Limit the cleanup to one organization slug when supported.",
    )
    parser.add_argument(
        "--delete-files",
        action="store_true",
        help="Also delete generated PDF files from REPORT_STORAGE_DIR when reports are removed.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("stats", help="Print row counts for all known tables.")
    subparsers.add_parser(
        "purge-demo-projects",
        help="Remove only seeded demo projects listed in scripts/demo_seed_data.py.",
    )
    subparsers.add_parser(
        "purge-reports",
        help="Remove generated report rows, optionally with their PDF files.",
    )
    subparsers.add_parser(
        "purge-audit-logs",
        help="Remove audit log rows, optionally limited by organization.",
    )
    subparsers.add_parser(
        "purge-projects",
        help="Remove projects and their dependent data, optionally limited by organization.",
    )
    subparsers.add_parser(
        "reset-working-data",
        help="Remove project/report/audit working data but keep users, organizations, reference data and catalogs.",
    )
    subparsers.add_parser(
        "reset-demo",
        help="Remove demo projects and load the current demo seed data again.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    with SessionLocal() as db:
        if args.command == "stats":
            print_stats(db)
            return
        if args.command == "purge-demo-projects":
            purge_demo_projects(db, execute=args.execute, delete_files=args.delete_files)
            return
        if args.command == "purge-reports":
            purge_reports(
                db,
                execute=args.execute,
                organization_slug=args.organization_slug,
                delete_files=args.delete_files,
            )
            return
        if args.command == "purge-audit-logs":
            purge_audit_logs(db, execute=args.execute, organization_slug=args.organization_slug)
            return
        if args.command == "purge-projects":
            purge_projects(
                db,
                execute=args.execute,
                organization_slug=args.organization_slug,
                delete_files=args.delete_files,
            )
            return
        if args.command == "reset-working-data":
            reset_working_data(
                db,
                execute=args.execute,
                organization_slug=args.organization_slug,
                delete_files=args.delete_files,
            )
            return
        if args.command == "reset-demo":
            reset_demo(db, execute=args.execute, delete_files=args.delete_files)
            return
        raise RuntimeError(f"Unsupported command: {args.command}")


def print_stats(db: Session) -> None:
    print(f"Database: {settings.database_url}")
    print("")
    for table_name, count in collect_table_counts(db):
        group = "preserved"
        if table_name in PROJECT_DATA_TABLES:
            group = "project-data"
        elif table_name == "audit_logs":
            group = "audit"
        elif table_name not in PRESERVED_TABLES:
            group = "other"
        print(f"{table_name:36} {count:8}  {group}")


def collect_table_counts(db: Session) -> list[tuple[str, int]]:
    counts: list[tuple[str, int]] = []
    for table in sorted(Base.metadata.sorted_tables, key=lambda item: item.name):
        count = db.scalar(select(func.count()).select_from(table)) or 0
        counts.append((table.name, count))
    return counts


def purge_demo_projects(db: Session, *, execute: bool, delete_files: bool) -> None:
    query = select(Project.id).where(Project.reference_code.in_(DEMO_PROJECT_REFERENCE_CODES))
    project_ids = list(db.scalars(query).all())
    report_paths = _report_paths_for_projects(db, project_ids)
    _print_plan("demo projects", len(project_ids), execute)
    _print_report_file_plan(report_paths, delete_files)
    if not execute:
        return
    _delete_report_files(report_paths, delete_files)
    db.execute(delete(Project).where(Project.id.in_(project_ids)))
    db.commit()
    print("Done.")


def purge_reports(
    db: Session,
    *,
    execute: bool,
    organization_slug: str | None,
    delete_files: bool,
) -> None:
    organization_id = _organization_id_from_slug(db, organization_slug)
    query = select(GeneratedReport)
    if organization_id is not None:
        query = query.where(GeneratedReport.organization_id == organization_id)
    reports = list(db.scalars(query).all())
    report_paths = [report.storage_path for report in reports]
    _print_plan("generated reports", len(reports), execute)
    _print_report_file_plan(report_paths, delete_files)
    if not execute:
        return
    _delete_report_files(report_paths, delete_files)
    statement = delete(GeneratedReport)
    if organization_id is not None:
        statement = statement.where(GeneratedReport.organization_id == organization_id)
    db.execute(statement)
    db.commit()
    print("Done.")


def purge_audit_logs(db: Session, *, execute: bool, organization_slug: str | None) -> None:
    organization_id = _organization_id_from_slug(db, organization_slug)
    query = select(func.count()).select_from(AuditLog)
    if organization_id is not None:
        query = query.where(AuditLog.organization_id == organization_id)
    count = db.scalar(query) or 0
    _print_plan("audit logs", count, execute)
    if not execute:
        return
    statement = delete(AuditLog)
    if organization_id is not None:
        statement = statement.where(AuditLog.organization_id == organization_id)
    db.execute(statement)
    db.commit()
    print("Done.")


def purge_projects(
    db: Session,
    *,
    execute: bool,
    organization_slug: str | None,
    delete_files: bool,
) -> None:
    project_ids = _project_ids(db, organization_slug=organization_slug)
    report_paths = _report_paths_for_projects(db, project_ids)
    _print_plan("projects", len(project_ids), execute)
    _print_report_file_plan(report_paths, delete_files=delete_files)
    if not execute:
        return
    _delete_report_files(report_paths, delete_files)
    db.execute(delete(Project).where(Project.id.in_(project_ids)))
    db.commit()
    print("Done. Generated report rows cascade with projects.")


def reset_working_data(
    db: Session,
    *,
    execute: bool,
    organization_slug: str | None,
    delete_files: bool,
) -> None:
    project_ids = _project_ids(db, organization_slug=organization_slug)
    report_paths = _report_paths_for_projects(db, project_ids)
    report_count = _report_count(db, organization_slug=organization_slug)
    audit_count = _audit_count(db, organization_slug=organization_slug)
    print(f"Projects to delete: {len(project_ids)}")
    print(f"Generated report rows to delete: {report_count}")
    print(f"Audit log rows to delete: {audit_count}")
    _print_report_file_plan(report_paths, delete_files)
    if not execute:
        print("Dry run only. Add --execute to apply this cleanup.")
        return
    _delete_report_files(report_paths, delete_files)
    purge_reports(db, execute=True, organization_slug=organization_slug, delete_files=False)
    purge_audit_logs(db, execute=True, organization_slug=organization_slug)
    db.execute(delete(Project).where(Project.id.in_(project_ids)))
    db.commit()
    print("Done.")


def reset_demo(db: Session, *, execute: bool, delete_files: bool) -> None:
    purge_demo_projects(db, execute=execute, delete_files=delete_files)
    if not execute:
        print("Dry run only. Demo seed was not reloaded.")
        return
    seed_all()


def _project_ids(db: Session, *, organization_slug: str | None) -> list[UUID]:
    organization_id = _organization_id_from_slug(db, organization_slug)
    query = select(Project.id)
    if organization_id is not None:
        query = query.where(Project.organization_id == organization_id)
    return list(db.scalars(query).all())


def _report_count(db: Session, *, organization_slug: str | None) -> int:
    organization_id = _organization_id_from_slug(db, organization_slug)
    query = select(func.count()).select_from(GeneratedReport)
    if organization_id is not None:
        query = query.where(GeneratedReport.organization_id == organization_id)
    return db.scalar(query) or 0


def _audit_count(db: Session, *, organization_slug: str | None) -> int:
    organization_id = _organization_id_from_slug(db, organization_slug)
    query = select(func.count()).select_from(AuditLog)
    if organization_id is not None:
        query = query.where(AuditLog.organization_id == organization_id)
    return db.scalar(query) or 0


def _report_paths_for_projects(db: Session, project_ids: Iterable[UUID]) -> list[str]:
    project_ids = list(project_ids)
    if not project_ids:
        return []
    return list(
        db.scalars(
            select(GeneratedReport.storage_path).where(GeneratedReport.project_id.in_(project_ids))
        ).all()
    )


def _organization_id_from_slug(db: Session, slug: str | None) -> UUID | None:
    if slug is None:
        return None
    organization_id = db.scalar(select(Organization.id).where(Organization.slug == slug))
    if organization_id is None:
        raise SystemExit(f"Organization slug not found: {slug}")
    return organization_id


def _print_plan(label: str, count: int, execute: bool) -> None:
    mode = "EXECUTE" if execute else "DRY RUN"
    print(f"{mode}: {count} {label} will be removed.")
    if not execute:
        print("Add --execute to apply this cleanup.")


def _print_report_file_plan(report_paths: list[str], delete_files: bool) -> None:
    if not report_paths:
        return
    action = "will be deleted" if delete_files else "will be kept"
    print(f"Report files on disk: {len(report_paths)} {action}.")
    if not delete_files:
        print("Add --delete-files with --execute to remove PDF artifacts too.")


def _delete_report_files(report_paths: Iterable[str], delete_files: bool) -> None:
    if not delete_files:
        return
    for storage_path in report_paths:
        path = resolve_report_file_path(storage_path)
        if path.is_file():
            path.unlink()
            _remove_empty_parents(path.parent, get_report_storage_dir())


def get_report_storage_dir() -> Path:
    return Path(settings.report_storage_dir).resolve()


def resolve_report_file_path(storage_path: str) -> Path:
    storage_root = get_report_storage_dir()
    relative_path = Path(storage_path)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError(f"Unsafe report storage path: {storage_path}")
    file_path = (storage_root / relative_path).resolve()
    if storage_root != file_path and storage_root not in file_path.parents:
        raise ValueError(f"Report path escapes storage directory: {storage_path}")
    return file_path


def _remove_empty_parents(path: Path, stop_at: Path) -> None:
    path = path.resolve()
    stop_at = stop_at.resolve()
    while path != stop_at and stop_at in path.parents:
        try:
            path.rmdir()
        except OSError:
            return
        path = path.parent


if __name__ == "__main__":
    main()
