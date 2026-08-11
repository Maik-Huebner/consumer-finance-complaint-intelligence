# Consumer Finance Complaint Intelligence Platform v1.0.0

Erster vollständiger Portfolio-Release des Modul-1-Abschlussprojekts **Datenanalyse mit Python / Exploratory Data Analysis**.

## Highlights

- Analyse von **10.269.540** veröffentlichten CFPB-Verbraucherbeschwerden aus den vollständigen Kalenderjahren 2022-2025
- reproduzierbarer CFPB-Download mit Snapshot-Provenienz und SHA-256
- speichereffiziente Multi-Gigabyte-Verarbeitung mit Polars und Parquet
- explizite Datenbereinigung und automatisierte Data Quality Gates
- dokumentierte Harmonisierung historischer CFPB-Produkt- und Issue-Taxonomien
- Zeitreihen-, Produkt-, Issue-, Response- und Korrelationsanalyse
- deskriptiver linearer Zeittrend mit klarer Abgrenzung zu Forecasting
- Segment-Sensitivitätsanalyse des dominanten Credit-Reporting-Segments
- sechs statische Portfolio-Visualisierungen und interaktives Plotly-Dashboard
- deutsche Management Summary, Methodik, Architektur, Datenwörterbuch und Responsible-Interpretation-Dokumentation
- Executive-EDA-Notebook auf Basis der veröffentlichten Report-Snapshots
- Abschlusspräsentation als PPTX und PDF
- **24/24 automatisierte Tests**, `pytest -W error`, Ruff und GitHub Actions für Python 3.11 und 3.13

## Zentrale analytische Erkenntnis

Credit Reporting steigt von **75,3 %** auf **88,4 %** des veröffentlichten Beschwerdeportfolios. Auch ohne dieses Segment wächst das Beschwerdevolumen von 2022 bis 2025 um **220,3 %**, der lineare Monatstrend sinkt jedoch von rund **10.511** auf rund **925** Beschwerden pro Monat. Aggregierte Korrelationsstrukturen verändern sich ebenfalls deutlich.

Die Ergebnisse werden als Segment- beziehungsweise Kompositionseffekt interpretiert und bewusst nicht vorschnell als Simpson-Paradox klassifiziert.

## Responsible Interpretation

Beschwerdevolumen ist keine direkte Qualitätskennzahl. Unternehmensvergleiche benötigen geeignete Exposure-Nenner; Korrelationen sind nicht kausal zu interpretieren und der lineare Trend ist kein Forecast.
