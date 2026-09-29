#!/usr/bin/env python3
"""Run the lightweight repository hygiene audit."""

from __future__ import annotations

from pathlib import Path

from data_intelligence_platform.validation.repository import audit_repository

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    findings = audit_repository(REPO_ROOT)
    if findings:
        details = "\n".join(f"- {item.path}: {item.reason}" for item in findings)
        raise SystemExit(f"Repository audit failed:\n{details}")
    print("Repository audit passed (lightweight guard; not a professional secret scanner).")


if __name__ == "__main__":
    main()
