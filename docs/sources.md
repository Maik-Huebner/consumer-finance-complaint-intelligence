# Sources and provenance

Verified for this portfolio project on **2026-08-11**.

## Primary data source

**Consumer Financial Protection Bureau (CFPB) — Consumer Complaint Database**

- Database: `https://www.consumerfinance.gov/data-research/consumer-complaints/`
- Bulk CSV ZIP: `https://files.consumerfinance.gov/ccdb/complaints.csv.zip`
- API documentation: `https://cfpb.github.io/api/ccdb/`
- Field reference: `https://cfpb.github.io/api/ccdb/fields.html`

The CFPB states that published complaint data are freely available to use, analyze, and build on, and that the database generally updates daily.

## Methodological constraints taken from the source

The project explicitly preserves the CFPB's own interpretation cautions:

- the database is not a statistical sample of all consumer experiences;
- complaint volume should be interpreted with company size and/or market share in mind;
- geographic volume should be interpreted with population context;
- recent data can be incomplete while publication and narrative-processing rules are applied;
- consumer narratives reflect consumers' descriptions and are not independently verified by the CFPB.

These constraints directly shape the analysis design and the wording of the executive report.
