import pytest

from scripts import db_cleanup


def test_cleanup_parser_is_dry_run_by_default() -> None:
    args = db_cleanup.build_parser().parse_args(["purge-demo-projects"])

    assert args.command == "purge-demo-projects"
    assert args.execute is False
    assert args.delete_files is False


def test_cleanup_parser_requires_explicit_execute() -> None:
    args = db_cleanup.build_parser().parse_args(["--execute", "--delete-files", "purge-reports"])

    assert args.command == "purge-reports"
    assert args.execute is True
    assert args.delete_files is True


def test_resolve_report_file_path_rejects_path_traversal(monkeypatch) -> None:
    storage_root = db_cleanup.BACKEND_ROOT / "storage-test"
    monkeypatch.setattr(db_cleanup.settings, "report_storage_dir", str(storage_root))

    with pytest.raises(ValueError):
        db_cleanup.resolve_report_file_path("../outside.pdf")


def test_resolve_report_file_path_stays_under_storage_root(monkeypatch) -> None:
    storage_root = db_cleanup.BACKEND_ROOT / "storage-test"
    monkeypatch.setattr(db_cleanup.settings, "report_storage_dir", str(storage_root))

    resolved = db_cleanup.resolve_report_file_path("org/report/file.pdf")

    assert resolved == (storage_root / "org" / "report" / "file.pdf").resolve()
