# Data directories

Large and generated datasets are intentionally excluded from version control.

- `raw/` — immutable source snapshot downloaded from CFPB
- `interim/` — optional temporary transformation artifacts
- `processed/` — analysis-ready Parquet output
- `external/` — optional future enrichment datasets (for example population or market-share denominators)

Run `python scripts/download_data.py` to fetch the official source data.
