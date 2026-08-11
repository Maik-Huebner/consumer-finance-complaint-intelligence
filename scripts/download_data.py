#!/usr/bin/env python3
"""Download and extract the official CFPB complaint dataset."""

from __future__ import annotations

import argparse

from data_intelligence_platform.ingestion.download import (
    download_file,
    extract_csv,
    write_download_metadata,
)
from data_intelligence_platform.utils.paths import (
    ensure_project_directories,
    load_config,
    resolve_project_path,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Replace an existing local raw snapshot.")
    args = parser.parse_args()

    config = load_config()
    ensure_project_directories(config)
    data = config["data"]
    raw_dir = resolve_project_path(data["raw_dir"])
    zip_path = raw_dir / data["zip_filename"]

    print(f"Downloading CFPB data to {zip_path} ...")
    download_file(data["source_url"], zip_path, force=args.force)
    csv_path = extract_csv(zip_path, raw_dir, data["csv_filename"])
    metadata = write_download_metadata(
        source_url=data["source_url"],
        zip_path=zip_path,
        csv_path=csv_path,
        metadata_path=raw_dir / "download_metadata.json",
    )
    print(f"Extracted: {csv_path}")
    print(f"SHA-256: {metadata['zip_sha256']}")


if __name__ == "__main__":
    main()
