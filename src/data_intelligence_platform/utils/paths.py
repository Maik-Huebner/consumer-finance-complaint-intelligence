"""Path and configuration helpers used across the project."""

from __future__ import annotations

from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG = PROJECT_ROOT / "configs" / "project.yaml"


def load_config(path: Path | str = DEFAULT_CONFIG) -> dict:
    """Load the YAML project configuration."""
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def resolve_project_path(value: str | Path) -> Path:
    """Resolve a path relative to the repository root."""
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def ensure_project_directories(config: dict) -> None:
    """Create all data and report directories declared in the config."""
    for key in (
        "raw_dir",
        "interim_dir",
        "processed_dir",
        "reports_dir",
        "figures_dir",
    ):
        resolve_project_path(config["data"][key]).mkdir(
            parents=True,
            exist_ok=True,
        )
