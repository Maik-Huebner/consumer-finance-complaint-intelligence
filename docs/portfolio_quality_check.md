# Portfolio quality check

## Business relevance

- Real financial-services data from an official regulator
- Clear decision questions for customer operations and conduct-risk consulting
- No artificial ML layer added to an EDA module
- Explicit path to later NLP, ML, and AI-engineering extensions

## Data engineering quality

- Automated source download
- Atomic download handling
- SHA-256 snapshot provenance
- Raw / processed separation
- Lazy large-file transformation with Polars
- Parquet analytical layer
- Central YAML configuration

## Analytical quality

- Data-quality audit before interpretation
- Missingness and duplicate checks
- Product, issue, company, channel, and time analysis
- Rolling time-series metrics
- Pearson and Spearman comparison
- Descriptive linear trend with R²
- Minimum-volume thresholds for company comparisons
- Explicit interpretation limitations

## Software quality

- Modular `src/` package
- Type hints and docstrings
- Comments explain decisions rather than narrating obvious syntax
- Automated tests
- Ruff configuration
- GitHub Actions CI
- Reproducible command-line scripts
- Large data excluded from Git

## Communication quality

- Recruiter-readable README
- Consulting-style executive summary generated from real outputs
- Data dictionary
- Methodology
- Architecture documentation
- Limitations / responsible interpretation
- Static figures plus interactive Plotly output
- Narrative notebook without duplicating production logic
