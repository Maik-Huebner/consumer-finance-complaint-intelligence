"""Robust downloader for the official CFPB bulk complaint dataset."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import UTC, datetime
from pathlib import Path

import requests

CHUNK_SIZE = 1024 * 1024


def sha256_file(path: Path) -> str:
    """Return the SHA-256 checksum of a file without loading it into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_file(url: str, destination: Path, *, force: bool = False) -> Path:
    """Download a URL atomically to ``destination``.

    A temporary ``.part`` file is used so interrupted downloads do not leave a
    corrupted file that looks complete.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        return destination

    temporary = destination.with_suffix(destination.suffix + ".part")
    temporary.unlink(missing_ok=True)

    try:
        with requests.get(url, stream=True, timeout=(10, 120)) as response:
            response.raise_for_status()
            with temporary.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        handle.write(chunk)
        temporary.replace(destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    return destination


def extract_csv(zip_path: Path, destination_dir: Path, csv_filename: str) -> Path:
    """Extract the expected complaint CSV from the CFPB ZIP archive."""
    destination_dir.mkdir(parents=True, exist_ok=True)
    output_path = destination_dir / csv_filename

    with zipfile.ZipFile(zip_path) as archive:
        candidates = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if not candidates:
            raise ValueError(f"No CSV file found inside {zip_path}")

        preferred = next(
            (name for name in candidates if Path(name).name == csv_filename),
            candidates[0],
        )
        with archive.open(preferred) as source, output_path.open("wb") as target:
            shutil.copyfileobj(source, target, length=CHUNK_SIZE)

    return output_path


def write_download_metadata(
    *,
    source_url: str,
    zip_path: Path,
    csv_path: Path,
    metadata_path: Path,
) -> dict:
    """Persist source and checksum metadata for reproducibility."""
    metadata = {
        "source_url": source_url,
        "downloaded_at_utc": datetime.now(UTC).isoformat(),
        "zip_file": zip_path.name,
        "zip_size_bytes": zip_path.stat().st_size,
        "zip_sha256": sha256_file(zip_path),
        "csv_file": csv_path.name,
        "csv_size_bytes": csv_path.stat().st_size,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata
