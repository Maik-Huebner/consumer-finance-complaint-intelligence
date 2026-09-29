from __future__ import annotations

import json
import os
import shutil
import tomllib
from importlib import metadata
from pathlib import Path

import pytest

import data_intelligence_platform
from data_intelligence_platform.utils.paths import load_config, resolve_project_path
from data_intelligence_platform.validation.evidence import (
    EvidenceValidationError,
    validate_report_evidence,
)
from data_intelligence_platform.validation.notebook import execute_notebook_smoke
from data_intelligence_platform.validation.repository import audit_repository

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_package_version_matches_distribution_and_pyproject() -> None:
    project = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    expected = project["project"]["version"]
    assert data_intelligence_platform.__version__ == expected
    assert metadata.version("data-intelligence-platform") == expected


def test_python_support_contract() -> None:
    project = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["requires-python"] == ">=3.11,<3.14"


def test_lock_is_exact_and_covers_direct_dependencies() -> None:
    project = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    direct = {
        dependency.split(">=", maxsplit=1)[0].lower().replace("_", "-")
        for dependency in project["project"]["dependencies"]
    }
    for filename in ("lock-py311.txt", "lock-py313.txt"):
        lock_lines = [
            line.strip()
            for line in (REPO_ROOT / "requirements" / filename)
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip() and not line.startswith("#")
        ]
        assert lock_lines
        assert all("==" in line for line in lock_lines)
        locked_names = {
            line.split("==", maxsplit=1)[0].lower().replace("_", "-") for line in lock_lines
        }
        assert direct <= locked_names
        assert {"build", "pytest", "ruff", "setuptools", "wheel"} <= locked_names


def test_report_evidence_is_consistent() -> None:
    result = validate_report_evidence(REPO_ROOT)
    assert result == {
        "status": "passed",
        "analysis_rows": 10_269_540,
        "analysis_months": 48,
        "products": 11,
        "quality_passed": True,
    }


def test_report_evidence_rejects_tampered_metric(tmp_path: Path) -> None:
    for name in ("configs", "reports", "docs", "notebooks", "presentation"):
        shutil.copytree(REPO_ROOT / name, tmp_path / name)
    shutil.copy2(REPO_ROOT / "README.md", tmp_path / "README.md")

    path = tmp_path / "reports" / "linear_trend.json"
    content = json.loads(path.read_text(encoding="utf-8"))
    content["r2"] = 0.5
    path.write_text(json.dumps(content), encoding="utf-8")

    with pytest.raises(EvidenceValidationError, match="R-squared"):
        validate_report_evidence(tmp_path)


def test_report_evidence_missing_path_is_clear(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Project configuration not found"):
        validate_report_evidence(tmp_path)


def test_repository_audit_passes_for_versionable_tree() -> None:
    assert audit_repository(REPO_ROOT) == []


def test_repository_audit_detects_unignored_raw_data(tmp_path: Path) -> None:
    raw = tmp_path / "data" / "raw"
    raw.mkdir(parents=True)
    (raw / "complaints.csv").write_text("Complaint ID\n1\n", encoding="utf-8")
    findings = audit_repository(tmp_path)
    assert any(item.path == "data/raw/complaints.csv" for item in findings)


def test_notebook_is_output_clean_and_executes_from_another_cwd(tmp_path: Path) -> None:
    previous = Path.cwd()
    try:
        os.chdir(tmp_path)
        count = execute_notebook_smoke(
            REPO_ROOT / "notebooks" / "01_executive_eda.ipynb",
            repository_root=REPO_ROOT,
        )
    finally:
        os.chdir(previous)
    assert count == 8


def test_explicit_project_paths_do_not_depend_on_cwd(tmp_path: Path) -> None:
    config = load_config(REPO_ROOT / "configs" / "project.yaml")
    previous = Path.cwd()
    try:
        os.chdir(tmp_path)
        resolved = resolve_project_path(config["data"]["reports_dir"], project_root=REPO_ROOT)
    finally:
        os.chdir(previous)
    assert resolved == REPO_ROOT / "reports"
