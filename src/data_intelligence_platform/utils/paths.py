"""Path and configuration helpers used across the project."""

from __future__ import annotations

from pathlib import Path

import yaml


def load_config(path: Path | str) -> dict:
    """Load the YAML project configuration."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def resolve_project_path(value: str | Path, *, project_root: Path) -> Path:
    """Resolve a path relative to an explicitly supplied repository root."""
    path = Path(value)
    return path if path.is_absolute() else project_root / path


def ensure_project_directories(config: dict, *, project_root: Path) -> None:
    """Create all data and report directories declared in the config."""
    for key in (
        "raw_dir",
        "interim_dir",
        "processed_dir",
        "reports_dir",
        "figures_dir",
    ):
        resolve_project_path(config["data"][key], project_root=project_root).mkdir(
            parents=True,
            exist_ok=True,
        )
