#!/usr/bin/env python3
"""Run transformation and analysis using an existing raw CFPB snapshot."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from data_intelligence_platform.transformation.complaints import transform_complaints
from data_intelligence_platform.utils.paths import (
    ensure_project_directories,
    load_config,
    resolve_project_path,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "configs" / "project.yaml"


def main() -> None:
    config = load_config(CONFIG_PATH)
    ensure_project_directories(config, project_root=REPO_ROOT)
    project = config["project"]
    data = config["data"]

    raw_csv = resolve_project_path(data["raw_dir"], project_root=REPO_ROOT) / data["csv_filename"]
    processed_path = (
        resolve_project_path(data["processed_dir"], project_root=REPO_ROOT)
        / data["processed_filename"]
    )

    if not raw_csv.exists():
        raise FileNotFoundError(
            f"Raw CFPB CSV not found: {raw_csv}. Run scripts/download_data.py first."
        )

    print(
        f"Transforming complaints from {project['analysis_start']} to {project['analysis_end']} ..."
    )
    transform_complaints(
        raw_csv,
        processed_path,
        analysis_start=project["analysis_start"],
        analysis_end=project["analysis_end"],
    )
    print(f"Processed data written to {processed_path}")

    subprocess.run([sys.executable, REPO_ROOT / "scripts" / "run_analysis.py"], check=True)


if __name__ == "__main__":
    main()
