"""Output-clean notebook smoke execution without a Jupyter runtime dependency."""

from __future__ import annotations

import json
import os
from pathlib import Path


def execute_notebook_smoke(notebook_path: Path, *, repository_root: Path) -> int:
    """Execute all code cells in one namespace and leave the notebook unchanged."""
    notebook = Path(notebook_path).resolve()
    root = Path(repository_root).resolve()
    if not notebook.is_file():
        raise FileNotFoundError(f"Notebook not found: {notebook}")
    if not root.is_dir():
        raise FileNotFoundError(f"Repository root not found: {root}")

    document = json.loads(notebook.read_text(encoding="utf-8"))
    code_cells = [cell for cell in document["cells"] if cell["cell_type"] == "code"]
    for index, cell in enumerate(code_cells, start=1):
        if cell.get("execution_count") is not None or cell.get("outputs"):
            raise ValueError(f"Notebook code cell {index} is not output-clean")

    namespace: dict[str, object] = {"__name__": "__notebook_smoke__"}
    previous = Path.cwd()
    try:
        os.chdir(root)
        for index, cell in enumerate(code_cells, start=1):
            source = "".join(cell["source"])
            exec(compile(source, f"{notebook.name}:cell-{index}", "exec"), namespace)
    finally:
        os.chdir(previous)
    return len(code_cells)
