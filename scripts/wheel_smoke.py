#!/usr/bin/env python3
"""Install the built wheel into an isolated environment and verify metadata."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import venv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LOCK_FILE = (
    REPO_ROOT / "requirements" / f"lock-py{sys.version_info.major}{sys.version_info.minor}.txt"
)


def _run(*args: str | Path) -> None:
    subprocess.run([str(arg) for arg in args], check=True, cwd=REPO_ROOT)


def main() -> None:
    wheels = sorted((REPO_ROOT / "dist").glob("data_intelligence_platform-*.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"Expected exactly one project wheel in dist/, found {len(wheels)}")

    with tempfile.TemporaryDirectory(prefix="data-intelligence-wheel-") as directory:
        environment = Path(directory)
        venv.EnvBuilder(with_pip=True, clear=True).create(environment)
        python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        _run(python, "-m", "pip", "install", "--only-binary=:all:", "-r", LOCK_FILE)
        _run(python, "-m", "pip", "install", "--no-deps", wheels[0])
        smoke = (
            "from importlib.metadata import version; "
            "from pathlib import Path; "
            "import data_intelligence_platform as package; "
            "assert package.__version__ == version('data-intelligence-platform'); "
            "assert 'site-packages' in str(Path(package.__file__).resolve()); "
            "print(package.__version__); print(Path(package.__file__).resolve())"
        )
        _run(python, "-c", smoke)
        _run(python, "-m", "pip", "check")


if __name__ == "__main__":
    main()
