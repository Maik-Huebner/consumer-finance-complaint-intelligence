"""Lightweight repository hygiene checks for CI and local audits."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepositoryFinding:
    """One repository hygiene finding."""

    path: str
    reason: str


FORBIDDEN_NAMES = {
    ".DS_Store",
    ".env",
    ".idea",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    ".vscode",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
}
FORBIDDEN_SUFFIXES = {".part", ".pyc", ".pyo", ".tmp"}
RAW_DATA_SUFFIXES = {".parquet", ".zip"}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[ps]_[A-Za-z0-9]{30,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}
MAX_TRACKED_BINARY_BYTES = 5 * 1024 * 1024
TEXT_SUFFIXES = {
    ".cfg",
    ".csv",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


def _candidate_files(root: Path) -> list[Path]:
    """Return tracked and non-ignored untracked files when Git is available."""
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode == 0:
        return [root / item.decode() for item in result.stdout.split(b"\0") if item]
    return [path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts]


def audit_repository(repository_root: Path) -> list[RepositoryFinding]:
    """Inspect versionable files for common accidental repository artifacts.

    This is intentionally a small guard, not a professional secret scanner.
    """
    root = Path(repository_root).resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Repository root not found: {root}")

    findings: list[RepositoryFinding] = []
    for path in _candidate_files(root):
        relative = path.relative_to(root)
        parts = set(relative.parts)
        forbidden = sorted(parts & FORBIDDEN_NAMES)
        if forbidden:
            findings.append(
                RepositoryFinding(str(relative), f"forbidden repository artifact: {forbidden[0]}")
            )
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(RepositoryFinding(str(relative), "temporary or cache file"))
            continue
        if relative.parts and relative.parts[0] == "data" and path.name != ".gitkeep":
            if len(relative.parts) > 1 and relative.parts[1] in {
                "raw",
                "interim",
                "processed",
                "external",
            }:
                findings.append(
                    RepositoryFinding(str(relative), "local data must not be versioned")
                )
                continue
        if path.suffix.lower() in RAW_DATA_SUFFIXES and relative.parts[0] != "presentation":
            findings.append(RepositoryFinding(str(relative), "unexpected archive or data binary"))
            continue
        if path.is_file() and path.stat().st_size > MAX_TRACKED_BINARY_BYTES:
            findings.append(RepositoryFinding(str(relative), "unexpected file larger than 5 MiB"))
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    findings.append(RepositoryFinding(str(relative), f"possible {label}"))
    return findings
