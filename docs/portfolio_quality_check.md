# Portfolio-Qualitätscheck

Dieses Dokument fasst die Qualitätskriterien des veröffentlichten Portfolio-Projekts zusammen.

Ziel ist nicht, möglichst viele Technologien zu verwenden, sondern eine fachlich belastbare, reproduzierbare und professionell präsentierte Exploratory Data Analysis für einen realen Finanzdatensatz umzusetzen.

## Business- und Branchenrelevanz

- realer Finanzdienstleistungsdatensatz einer offiziellen US-Aufsichtsbehörde
- mehr als zehn Millionen analysierte Beschwerden
- klare fachliche Fragestellungen für Customer Operations und Conduct Risk
- übertragbare Methodik für Banking und Finanzdienstleistungen
- übertragbare Methodik für Versicherungsbeschwerden und Schadenprozesse
- klare Technical-AI-Consulting-Perspektive
- Management- und Entscheidungsebene zusätzlich zur technischen Analyse
- keine künstlich hinzugefügte Machine-Learning-Schicht in einem EDA-Modul
- klar dokumentierter Erweiterungspfad zu ML, NLP und AI Engineering

## Datenaufnahme und Provenienz

- automatisierter Download der offiziellen CFPB-Daten
- atomare Download-Logik über temporäre `.part`-Datei
- Schutz vor unvollständigen Downloads
- SHA-256-Prüfsumme des Quelldaten-Snapshots
- Download-Metadaten
- Trennung von Roh-, Zwischen- und Analysedaten
- veröffentlichter Source-Snapshot unter `reports/source_snapshot.json`
- große Rohdaten vollständig aus Git ausgeschlossen

## Verarbeitung großer Datenmengen

- Analyse von 10.269.540 Beschwerden
- Multi-Gigabyte-Rohdatensatz
- Lazy CSV-Verarbeitung mit Polars
- direkte Transformation in Parquet
- keine vollständige Materialisierung der Roh-CSV im Arbeitsspeicher erforderlich
- speichereffiziente analytische Datenebene
- kategorische beziehungsweise Arrow-basierte Datentypen für wiederkehrende Dimensionen

## Datenbereinigung

Datenbereinigung ist ein expliziter Bestandteil der EDA.

Geprüft beziehungsweise behandelt werden:

- fehlende Werte
- leere Textfelder
- Datumsformate
- Datentypen
- doppelte Complaint IDs
- negative Zeitdifferenzen
- unerwartete Response-Werte
- fehlende analytische Kategorien

Fehlende Quellinformationen werden nicht erfunden oder stillschweigend entfernt.

Sechs Beschwerden ohne ursprünglichen Issue-Wert bleiben als:

```text
issue = null
```

erhalten.

Für Aggregationen wird zusätzlich gesetzt:

```text
harmonized_issue = "Issue not provided"
```

Dadurch bleiben Datenherkunft und analytische Vollständigkeit gleichzeitig erhalten.

## Taxonomie-Harmonisierung

Historische CFPB-Klassifikationen werden nicht ungeprüft miteinander verglichen.

Die analytische Ebene enthält:

```text
taxonomy_version
harmonized_product
harmonized_issue
```

während die ursprünglichen Quellwerte erhalten bleiben.

Im verwendeten Analysebestand sind:

```text
1.335.250 Beschwerden
```

beziehungsweise rund:

```text
13,0 %
```

von einer Produktharmonisierung betroffen.

Die Zuordnungen werden vollständig auditiert.

## Automatisierte Datenqualität

Vor der Interpretation prüft die Pipeline unter anderem:

- erwartete Spalten
- eindeutige Complaint IDs
- fehlende Complaint IDs
- harmonisierte Produktwerte
- harmonisierte Issue-Werte
- negative Zeitdifferenzen
- gültige Timely-Response-Werte
- gültige Taxonomieversionen
- Beginn und Ende des Analysezeitraums

Aktueller Qualitätsstatus des realen Analysebestands:

```text
rows = 10.269.540
duplicate_complaint_ids = 0
missing_complaint_ids = 0
missing_harmonized_products = 0
missing_harmonized_issues = 0
negative_days_to_company = 0
passed = true
```

## Analytische Qualität

Die EDA umfasst:

- deskriptive Statistik
- Häufigkeitsanalysen
- Missing-Value-Analyse
- Gruppierung und Aggregation
- Ranking und Filterung
- Pivot-Tabellen
- Produktanalysen
- Issue-Analysen
- Unternehmensscreening
- monatliche Zeitreihen
- vollständigen rollierenden 12-Monats-Durchschnitt
- Pearson-Korrelation
- Spearman-Rangkorrelation
- statistische Signifikanzwerte
- einfache lineare Regression als deskriptiven Trend
- Segmentkontrolle
- Sensitivitätsanalyse

Die lineare Regression wird ausdrücklich nicht als Prognosemodell interpretiert.

## Sensitivitätsanalyse

Das dominante Segment:

```text
Credit reporting or other personal consumer reports
```

macht rund:

```text
85,9 %
```

des gesamten Analysebestands aus.

Deshalb werden zentrale Kennzahlen zusätzlich ohne dieses Segment berechnet.

Die Analyse zeigt unter anderem:

```text
Credit-Reporting-Anteil 2022: 75,3 %
Credit-Reporting-Anteil 2025: 88,4 %
```

Gesamttrend:

```text
+10.511 Beschwerden pro Monat
```

Trend ohne Credit Reporting:

```text
+925 Beschwerden pro Monat
```

Damit entfallen rechnerisch rund:

```text
91,2 %
```

der Steigung des einfachen linearen Gesamttrends auf den Credit-Reporting-Anteil der monatlichen Beschwerdereihe.

Auch Korrelationsstrukturen verändern sich nach der Segmentkontrolle deutlich.

Das Projekt bezeichnet diesen Befund bewusst nicht vorschnell als Simpson-Paradox, sondern als Segment- beziehungsweise Kompositionseffekt.

## Visualisierungsqualität

Das Projekt erzeugt sechs statische Portfolio-Grafiken:

1. monatliche Beschwerdeentwicklung
2. Produktmix
3. Timely-Response-Rate nach Produkt
4. Produkt-Issue-Hotspots
5. jährliche Produktentwicklung als Heatmap
6. Credit-Reporting-Sensitivitätsanalyse

Zusätzlich wird ein interaktives Plotly-Dashboard erzeugt.

Visualisierungen verwenden:

- deutsche Titel und Beschriftungen
- direkte quantitative Werte, wo sinnvoll
- klare Management-Perspektive
- bewusst gewählte Skalen
- eine logarithmische Farbskala für die Produkt-Jahres-Heatmap
- kompakte und verständliche Kategorienamen für die Darstellung

Die Quelldaten selbst werden für Darstellungszwecke nicht verändert.

## Softwarequalität

- modulare `src/`-Paketstruktur
- technische Trennung von Ingestion, Transformation, Validation, Analysis und Visualization
- Type Hints
- Docstrings
- Kommentare für fachliche und technische Entscheidungen
- zentrale YAML-Konfiguration
- reproduzierbare Kommandozeilen-Skripte
- Makefile
- Ruff
- pytest
- Regressionstests
- Warning-as-error-Testlauf
- GitHub Actions CI

Aktueller lokaler Qualitätsstand:

```text
24 Tests
24 bestanden
24 bestanden mit -W error
Ruff: All checks passed
```

GitHub Actions validiert das Projekt zusätzlich auf:

```text
Python 3.11
Python 3.13
```

Beide CI-Jobs sind erfolgreich.

## Reproduzierbarkeit

Der Projektworkflow kann über definierte Befehle ausgeführt werden.

Installation:

```bash
pip install -e ".[dev]"
```

Schnelles Quality Gate:

```bash
make quality
```

Vollständige Reproduktion aus lokalen Rohdaten:

```bash
make reproduce
```

Die große Rohdatenbasis bleibt bewusst außerhalb von Git.

Veröffentlichte Reports, Visualisierungen, Präsentationen und Snapshot-Metadaten ermöglichen trotzdem eine direkte Begutachtung des Projektstands ohne erneuten Multi-Gigabyte-Download.

## Kommunikation und Dokumentation

Das Repository enthält:

- kompakte Recruiter-Landingpage als `README.md`
- Executive EDA Notebook
- Management Summary
- Architektur-Dokumentation
- Methodik-Dokumentation
- Datenwörterbuch
- Quellen- und Provenienz-Dokumentation
- Limitations-Dokumentation
- Portfolio-Qualitätscheck
- Report-Dokumentation
- maschinenlesbare Analyseoutputs
- statische Visualisierungen
- interaktives Dashboard
- deutschsprachige Abschlusspräsentation
- PDF-Version der Abschlusspräsentation
- Release Notes

## Präsentation

Die Kursanforderung einer eigenständigen EDA mit Präsentation wird zusätzlich über eine eigenständige deutschsprachige Abschlusspräsentation erfüllt.

Veröffentlichte Dateien:

```text
presentation/consumer_finance_complaint_intelligence_presentation.pptx
presentation/consumer_finance_complaint_intelligence_presentation.pdf
```

Die Präsentation behandelt:

- Business-Problem
- Datenquelle und Analyseumfang
- Architektur und Datenverarbeitung
- Datenbereinigung
- Taxonomie-Harmonisierung
- zentrale EDA-Ergebnisse
- Response Operations
- Sensitivitätsanalyse
- methodische Einschränkungen
- Management- und Consulting-Implikationen

## Verantwortungsvolle Interpretation

Das Projekt dokumentiert ausdrücklich, dass:

- Beschwerdevolumen keine direkte Unternehmensqualität misst
- CFPB-Beschwerden keine repräsentative Stichprobe sämtlicher Kundenerfahrungen darstellen
- Unternehmensvergleiche zusätzliche Exposure-Nenner benötigen
- Korrelation keine Kausalität beweist
- die lineare Regression keine Prognose darstellt
- ein Segmenteffekt nicht automatisch ein Simpson-Paradox ist
- externe Beschwerdedaten allein keine regulatorische Entscheidung rechtfertigen

## Portfolio-Fazit

Das Repository demonstriert nicht nur die technische Durchführung einer EDA.

Es zeigt einen vollständigen analytischen Arbeitsprozess:

```text
Business Problem
        ↓
Data Ingestion
        ↓
Data Profiling
        ↓
Data Cleaning
        ↓
Taxonomy Harmonization
        ↓
Quality Gates
        ↓
Exploratory Analysis
        ↓
Statistical Analysis
        ↓
Segment Sensitivity
        ↓
Visualization
        ↓
Management Interpretation
        ↓
Recommended Next Steps
```

Damit verbindet das Projekt Datenanalyse, Softwarequalität, fachliche Interpretation und consultingorientierte Kommunikation in einem reproduzierbaren Financial-Services-Anwendungsfall.
