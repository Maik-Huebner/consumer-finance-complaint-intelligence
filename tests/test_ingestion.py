from __future__ import annotations

import zipfile

from data_intelligence_platform.ingestion.download import extract_csv, sha256_file


def test_sha256_file_is_stable(tmp_path):
    path = tmp_path / "example.txt"
    path.write_text("portfolio-test", encoding="utf-8")

    first = sha256_file(path)
    second = sha256_file(path)

    assert first == second
    assert len(first) == 64


def test_extract_csv(tmp_path):
    zip_path = tmp_path / "complaints.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr("complaints.csv", "Complaint ID,Product\n1,Credit card\n")

    extracted = extract_csv(zip_path, tmp_path / "raw", "complaints.csv")

    assert extracted.exists()
    assert "Credit card" in extracted.read_text(encoding="utf-8")
