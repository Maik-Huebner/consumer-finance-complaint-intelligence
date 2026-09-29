#!/usr/bin/env python3
"""Smoke-execute the committed output-clean executive EDA notebook."""

from __future__ import annotations

from pathlib import Path

from data_intelligence_platform.validation.notebook import execute_notebook_smoke

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = REPO_ROOT / "notebooks" / "01_executive_eda.ipynb"


def main() -> None:
    cell_count = execute_notebook_smoke(NOTEBOOK, repository_root=REPO_ROOT)
    print(f"Notebook smoke passed: {cell_count} output-clean code cells executed.")


if __name__ == "__main__":
    main()
