#!/usr/bin/env python3
"""Validate committed report evidence without downloading source data."""

from __future__ import annotations

import json
from pathlib import Path

from data_intelligence_platform.validation.evidence import validate_report_evidence

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    result = validate_report_evidence(REPO_ROOT)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
