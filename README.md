# Consumer Finance Complaint Intelligence Platform

Eine reproduzierbare **Exploratory-Data-Analysis-Plattform für Finanzbeschwerden**, die mehr als zehn Millionen veröffentlichte Verbraucherbeschwerden des U.S. Consumer Financial Protection Bureau (CFPB) in eine belastbare Analyse- und Entscheidungsgrundlage überführt.

Das Projekt verbindet **Datenaufnahme, Datenbereinigung, Datenqualitätskontrollen, Taxonomie-Harmonisierung, statistische Exploration, Zeitreihenanalyse, Sensitivitätsanalyse und Visualisierung** in einer modularen Python-Pipeline.

Der fachliche Fokus liegt auf übertragbaren Anwendungsfällen aus **Banking, Finanzdienstleistungen, Versicherungen, Conduct Risk, Customer Operations und Technical AI Consulting**.

> **Projektumfang:** Abschlussprojekt Modul 1 – Datenanalyse mit Python / Exploratory Data Analysis (EDA).
> Der Schwerpunkt liegt bewusst auf Datenqualität, Datenaufbereitung, statistischer Exploration und Entscheidungsunterstützung – nicht auf prädiktivem Machine Learning.

---

## Projektziel

Finanzinstitute verarbeiten große Mengen an Kundenbeschwerden zu Produkten und Prozessen wie:

- Kreditkarten,
- Giro- und Sparkonten,
- Hypotheken,
- Konsumentenkrediten,
- Inkasso,
- Zahlungsdiensten,
- Studentenkrediten,
- Credit Reporting und Bonitätsinformationen.

Reine Beschwerdezahlen reichen für eine belastbare Bewertung jedoch nicht aus.

Eine professionelle EDA muss zunächst beantworten:

1. **In welchen Produkten konzentriert sich das Beschwerdevolumen?**
2. **Welche Produkt-Issue-Kombinationen bilden die größten Hotspots?**
3. **Wie verändert sich das Beschwerdevolumen im Zeitverlauf?**
4. **Wo zeigen sich auffällige Unterschiede bei zeitnahen Unternehmensreaktionen?**
5. **Welche Veränderungen entstehen möglicherweise nur durch historische Änderungen der Datenklassifikation?**
6. **Welche Datenqualitätsprobleme müssen vor einer Interpretation behandelt werden?**
7. **Wie stark werden aggregierte Portfolio-Kennzahlen durch ein dominantes Produktsegment beeinflusst?**

Die Plattform überführt den öffentlichen CFPB-Rohdatensatz deshalb in einen nachvollziehbaren Analyseprozess, der als Grundlage für weiterführende Untersuchungen in **Customer Operations, Conduct Risk, Operational Risk und Data/AI Consulting** dienen kann.

---

# Zentrale Ergebnisse

Die aktuelle Analyse umfasst vollständige Kalenderjahre von **2022 bis 2025** und verarbeitet:

- **10.269.540 Beschwerden**,
- **5.601 Unternehmen**,
- **11 harmonisierte Produktgruppen**.

## Starkes Wachstum des veröffentlichten Beschwerdevolumens

Das veröffentlichte Beschwerdevolumen steigt von:

```text
800.245 Beschwerden im Jahr 2022
```

auf:

```text
5.442.977 Beschwerden im Jahr 2025
```

Dies entspricht einer Veränderung von rund:

```text
+580,2 %
```

über den betrachteten Zeitraum.

Der einfache deskriptive lineare Zeittrend entspricht durchschnittlich rund:

```text
+10.511 Beschwerden pro Monat
```

bei:

```text
R² = 0,877
```

Dieser Trend beschreibt ausschließlich den beobachteten Zeitraum und stellt keine Prognose dar.

---

## Dominanz von Credit Reporting

Die größte harmonisierte Produktgruppe:

```text
Credit reporting or other personal consumer reports
```

umfasst:

```text
8.824.129 Beschwerden
```

beziehungsweise rund:

```text
85,9 %
```

aller Beschwerden im gesamten Analysezeitraum.

Der Anteil dieses Segments verändert sich zusätzlich deutlich:

```text
2022: 75,3 %
2023: 80,9 %
2024: 86,5 %
2025: 88,4 %
```

Damit verändert sich nicht nur das Gesamtvolumen, sondern auch der Produktmix des veröffentlichten CFPB-Datensatzes erheblich.

---

## Größter Produkt-Issue-Hotspot

Der volumenstärkste harmonisierte Hotspot ist:

```text
Credit reporting or other personal consumer reports
→ Incorrect information on your report
```

mit:

```text
4.653.591 Beschwerden
```

Weitere besonders große Credit-Reporting-Hotspots sind:

```text
Improper use of your report
2.344.426 Beschwerden
```

und:

```text
Problem with a company's investigation into an existing problem
1.727.343 Beschwerden
```

Damit konzentriert sich ein erheblicher Teil des gesamten Datensatzes auf wenige Credit-Reporting-Issues.

---

## Response Operations

Die veröffentlichte Timely-Response-Rate liegt über den gesamten Datensatz bei rund:

```text
99,6 %
```

Zwischen Produktgruppen bestehen jedoch deutliche Unterschiede.

Besonders auffällig ist:

```text
Student loan: 84,8 %
```

Unternehmensbezogene Response-Kennzahlen werden im Projekt ausschließlich als **explorative Screening-Signale** verwendet.

Ohne zusätzliche Bezugsgrößen wie Kundenanzahl, Marktanteil oder Produkt-Exposure stellen sie keine faire Performance-Rangliste dar.

---

# Sensitivitätsanalyse

Eine zentrale Erkenntnis der EDA ist, dass aggregierte Portfolio-Kennzahlen stark vom Produktmix beeinflusst werden.

Da Credit Reporting im Gesamtportfolio dominiert, wurde deshalb zusätzlich geprüft, wie sich zentrale Ergebnisse verändern, wenn dieses Segment aus der Aggregation entfernt wird.

## Beschwerdewachstum ohne Credit Reporting

Auch ohne Credit Reporting steigt das veröffentlichte Beschwerdevolumen deutlich:

```text
2022: 197.553
2025: 632.673
```

Das entspricht:

```text
+220,3 %
```

Das Wachstum des Gesamtportfolios ist damit nicht ausschließlich auf Credit Reporting zurückzuführen.

Die Größenordnung verändert sich jedoch erheblich.

---

## Einfluss auf den linearen Zeittrend

Gesamtportfolio:

```text
+10.511 Beschwerden pro Monat
```

Portfolio ohne Credit Reporting:

```text
+925 Beschwerden pro Monat
```

Rechnerisch entfallen damit rund:

```text
91,2 %
```

der Steigung des einfachen linearen Gesamttrends auf den Credit-Reporting-Anteil der monatlichen Beschwerdereihe.

---

## Einfluss auf Korrelationsstrukturen

Für das Gesamtportfolio ergibt sich zwischen monatlichem Beschwerdevolumen und Narrative-Anteil:

```text
Pearson r = -0,891
```

Ohne Credit Reporting:

```text
Pearson r = -0,227
```

Auch die Beziehung zwischen Beschwerdevolumen und Timely-Response-Rate verändert sich:

```text
Gesamtportfolio:
r = +0,343

ohne Credit Reporting:
r = -0,297
```

Die Richtung des aggregierten Zusammenhangs wechselt damit in dieser Sensitivitätsanalyse.

Das Projekt klassifiziert dies bewusst **nicht vorschnell als Simpson-Paradox**.

Die Ergebnisse zeigen jedoch einen deutlichen **Segment- beziehungsweise Kompositionseffekt**.

Damit wird sichtbar, warum aggregierte Portfolio-KPIs nicht ohne Segmentkontrolle interpretiert werden sollten.

---

# Warum dieses Projekt über eine klassische Notebook-EDA hinausgeht

Reale Analysedaten sind selten bereits sauber, stabil klassifiziert und unmittelbar vergleichbar.

Der CFPB-Datensatz enthält innerhalb des Untersuchungszeitraums historische Veränderungen von Produkt- und Issue-Bezeichnungen.

Werden solche Änderungen ignoriert, können scheinbare Wachstumssprünge oder Rückgänge entstehen, obwohl sich teilweise lediglich die Taxonomie der Quelle verändert hat.

Das Projekt behandelt deshalb die gesamte analytische Datenkette:

```text
Offizielle Datenquelle
        ↓
Reproduzierbarer Download
        ↓
Datenprofiling
        ↓
Datenbereinigung
        ↓
Taxonomie-Harmonisierung
        ↓
Automatisierte Quality Gates
        ↓
Explorative Datenanalyse
        ↓
Zeitreihenanalyse
        ↓
Statistische Zusammenhangsanalyse
        ↓
Segment- und Sensitivitätsanalyse
        ↓
Visualisierung
        ↓
Management-Interpretation
        ↓
Consulting-Handlungsempfehlungen
```

Die ursprünglichen Quelldaten werden dabei nicht überschrieben.

---

# Datenquelle

**Quelle:** U.S. Consumer Financial Protection Bureau – Consumer Complaint Database

**Offizieller Bulk-Datensatz:**

```text
https://files.consumerfinance.gov/ccdb/complaints.csv.zip
```

Die Rohdaten werden **nicht in Git gespeichert**.

Das Ingestion-Skript lädt den offiziellen CFPB-Datensatz herunter und speichert ihn lokal unter:

```text
data/raw/
```

Zusätzlich werden Download-Metadaten und ein SHA-256-Hash erzeugt, damit nachvollziehbar bleibt, auf welchem lokalen Snapshot eine Analyse basiert.

---

## Reproduzierbarkeit und Datenprovenienz

Für jeden lokalen Download werden unter anderem dokumentiert:

- Datenquelle,
- Downloadzeitpunkt,
- Dateiname,
- Dateigröße,
- SHA-256-Prüfsumme.

Die Metadaten werden gespeichert unter:

```text
data/raw/download_metadata.json
```

Damit lässt sich nachvollziehen, mit welchem Quelldatensatz ein bestimmter Analyse- und Reporting-Stand erzeugt wurde.

---

# Wichtiger Interpretationshinweis

Die CFPB Consumer Complaint Database ist **keine repräsentative Stichprobe aller Kundenerfahrungen**.

Beschwerdevolumen kann unter anderem beeinflusst werden durch:

- Unternehmensgröße,
- Marktanteil,
- Anzahl der Kunden,
- Produktnutzung,
- Bekanntheit des Beschwerdekanals,
- individuelles Meldeverhalten,
- externe Dienstleister,
- Veränderungen von Erfassungs- oder Einreichungsprozessen.

Deshalb wird ein Unternehmen oder Finanzprodukt in diesem Projekt **nicht allein aufgrund hoher Beschwerdezahlen als gut oder schlecht bewertet**.

Für faire Unternehmensvergleiche wären zusätzliche Bezugsgrößen erforderlich, beispielsweise:

- Kundenanzahl,
- Konten,
- Verträge,
- Transaktionsvolumen,
- Marktanteil.

---

# Projektarchitektur

```text
data-intelligence-platform/
├── .github/
│   └── workflows/
│       └── ci.yml
├── configs/
│   └── project.yaml
├── data/
│   ├── external/
│   ├── interim/
│   ├── processed/
│   └── raw/
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── limitations.md
│   └── methodology.md
├── notebooks/
│   └── 01_executive_eda.ipynb
├── reports/
│   ├── figures/
│   └── README.md
├── scripts/
│   ├── download_data.py
│   ├── run_analysis.py
│   └── run_pipeline.py
├── src/
│   └── data_intelligence_platform/
│       ├── analysis/
│       ├── ingestion/
│       ├── transformation/
│       ├── utils/
│       ├── validation/
│       └── visualization/
├── tests/
├── .gitignore
├── Makefile
└── pyproject.toml
```

Die Architektur trennt bewusst:

```text
Rohdaten
→ Transformation
→ Datenbereinigung
→ Taxonomie-Harmonisierung
→ Datenqualität
→ Analyse
→ Sensitivitätsanalyse
→ Visualisierung
→ Reporting
```

Dadurch bleibt der Analyseprozess reproduzierbar, testbar und erweiterbar.

---

# Technologie-Stack

## Python

**Python 3.11+** bildet die technische Grundlage des Projekts.

## Polars

Polars verarbeitet den Multi-Millionen-Zeilen-Rohdatensatz speichereffizient.

Die CSV-Datei wird lazy eingelesen und die transformierte Datenmenge direkt als Parquet geschrieben.

Dadurch muss der vollständige Rohbestand nicht gleichzeitig im Arbeitsspeicher materialisiert werden.

## Pandas

Pandas wird in der analytischen Ebene eingesetzt für:

- Gruppierungen,
- Aggregationen,
- Pivot-Tabellen,
- Zeitreihen,
- Management-Tabellen,
- Reporting.

Wiederkehrende Textdimensionen werden als kategorische Datentypen repräsentiert, um den Speicherbedarf der mehr als zehn Millionen Analysezeilen zu reduzieren.

## NumPy

Für numerische Berechnungen und analytische Hilfsoperationen.

## Matplotlib und Seaborn

Für statische, GitHub- und reportfähige Visualisierungen.

## Plotly

Für ein interaktives HTML-Dashboard.

## SciPy

Für:

- Pearson-Korrelation,
- Spearman-Rangkorrelation,
- statistische Signifikanzwerte.

## scikit-learn

Für eine einfache lineare Regression als **deskriptive Trendanalyse**.

Sie wird ausdrücklich nicht als Prognosemodell verwendet.

## PyArrow und Parquet

Für eine kompakte und speichereffiziente analytische Datenebene.

## pytest und Ruff

Für automatisierte:

- Unit Tests,
- Regressionstests,
- Quality Gates,
- Warning-as-error-Prüfungen,
- Linting.

---

# Reproduzierbarer Workflow

## 1. Python-Umgebung erstellen

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

---

## 2. CFPB-Daten herunterladen

```bash
python scripts/download_data.py
```

Der Downloader:

- lädt den offiziellen CFPB-ZIP-Datensatz,
- schreibt zunächst in eine temporäre `.part`-Datei,
- verhindert dadurch scheinbar vollständige, aber abgebrochene Downloads,
- extrahiert die CSV,
- berechnet einen SHA-256-Hash,
- schreibt Download-Metadaten,
- überschreibt einen bestehenden Snapshot nur bei expliziter Anforderung.

---

## 3. Gesamte Pipeline ausführen

```bash
python scripts/run_pipeline.py
```

Standardmäßig werden vollständige Kalenderjahre von:

```text
2022-01-01
bis
2025-12-31
```

analysiert.

Die Pipeline übernimmt:

1. Transformation des Rohdatensatzes,
2. Datenbereinigung,
3. Taxonomie-Harmonisierung,
4. Speicherung als Parquet,
5. automatisierte Datenqualitätsprüfung,
6. EDA und statistische Auswertung,
7. Segment- und Sensitivitätsanalyse,
8. Erzeugung analytischer Reports,
9. Erzeugung der Visualisierungen,
10. Erzeugung des interaktiven Dashboards,
11. Erzeugung einer Management Summary.

---

## 4. Nur die Analyse erneut ausführen

Wenn bereits ein aktueller verarbeiteter Parquet-Datensatz vorhanden ist:

```bash
python scripts/run_analysis.py
```

---

## 5. Qualitätsprüfungen

```bash
pytest -q
ruff check .
```

Zusätzlich werden Python-Warnungen als Fehler behandelt:

```bash
pytest -q -W error
```

Aktueller Projektstand:

```text
24 Tests
24 bestanden
24 bestanden mit -W error
Ruff: All checks passed
```

Alternativ:

```bash
make test
make lint
make all
```

---

# EDA-Prozess

## 1. Datenaufnahme und Provenienz

Die Pipeline dokumentiert:

- Datenquelle,
- lokalen Snapshot,
- Dateigröße,
- Downloadzeitpunkt,
- SHA-256-Prüfsumme.

---

## 2. Datenprofiling und strukturelle Prüfung

Vor der eigentlichen Interpretation wird geprüft:

- welche Spalten vorhanden sind,
- welche Datentypen vorliegen,
- ob erwartete Felder fehlen,
- ob Complaint IDs eindeutig sind,
- welcher Zeitraum tatsächlich enthalten ist,
- welche Werte fehlen,
- ob unerwartete Kategorien auftreten.

---

## 3. Datenbereinigung

Datenbereinigung ist ein expliziter Bestandteil der EDA.

Geprüft und behandelt werden unter anderem:

- fehlende Werte,
- leere Textfelder,
- Datumsformate,
- Datentypen,
- doppelte Complaint IDs,
- negative oder unplausible Zeitdifferenzen,
- unerwartete Response-Werte,
- fehlende analytische Kategorien.

Fehlende Informationen werden nicht erfunden oder stillschweigend entfernt.

Wenn der CFPB-Rohdatensatz keinen Issue-Wert enthält:

```text
issue = null
```

bleibt dieser Originalwert unverändert.

Für die analytische Ebene wird zusätzlich:

```text
harmonized_issue = "Issue not provided"
```

gesetzt.

Damit bleibt die Datenherkunft erhalten und die Beschwerde geht nicht aus Aggregationen verloren.

---

## 4. Taxonomie-Harmonisierung

Historische Änderungen der CFPB-Klassifikation können Längsschnittanalysen verfälschen.

Deshalb enthält die analytische Datenebene:

```text
product
issue
```

sowie:

```text
harmonized_product
harmonized_issue
taxonomy_version
```

Die Originalwerte werden nicht überschrieben.

Jede Zuordnung wird in:

```text
reports/taxonomy_harmonization_audit.csv
```

protokolliert.

Im realen Analysedatensatz sind:

```text
1.335.250 Beschwerden
```

von einer Produktharmonisierung betroffen.

Das entspricht rund:

```text
13,0 %
```

des vollständigen Analysebestands.

---

## 5. Automatisierte Datenqualitätsprüfung

Vor der Interpretation prüft die Pipeline unter anderem:

- erwartete Spalten,
- eindeutige Complaint IDs,
- fehlende Complaint IDs,
- Vollständigkeit harmonisierter Produktfelder,
- Vollständigkeit harmonisierter Issue-Felder,
- negative Zeitdifferenzen,
- unerwartete `Timely response?`-Werte,
- gültige Taxonomieversionen,
- Minimum und Maximum des Analysezeitraums.

Der maschinenlesbare Report wird gespeichert unter:

```text
reports/data_quality_report.json
```

Der reale Analysebestand besteht die definierten strukturellen Quality Gates:

```text
passed = true
```

---

# Explorative Analyse

Die EDA verwendet unter anderem:

- deskriptive Statistik,
- Häufigkeitsanalysen,
- Missing-Value-Analyse,
- Gruppierung und Aggregation,
- Ranking und Filterung,
- Zeit- und Datumsoperationen,
- monatliche Zeitreihen,
- rollierende Mittelwerte,
- Pivot-Tabellen,
- Pearson-Korrelation,
- Spearman-Rangkorrelation,
- einfache lineare Regression,
- Segmentkontrolle,
- Sensitivitätsanalyse,
- statische Visualisierung,
- interaktive Visualisierung.

---

# Zeitreihenmethodik

Die monatliche Analyse berechnet:

- monatliches Beschwerdevolumen,
- Timely-Response-Rate,
- Narrative-Anteil.

Zusätzlich wird ein:

```text
rollierender 12-Monats-Durchschnitt
```

berechnet.

Der gleitende Durchschnitt wird bewusst **erst nach zwölf vollständig vorhandenen Monatsbeobachtungen** ausgegeben.

Die ersten elf Monate erhalten deshalb keinen scheinbar vollständigen 12-Monats-Durchschnitt.

Damit entspricht die dargestellte Kennzahl tatsächlich der benannten Fensterlänge.

---

# Fachliche Fragestellungen

## Beschwerdekonzentration

Welche harmonisierten Finanzproduktgruppen machen den größten Anteil der veröffentlichten Beschwerden aus?

## Produkt-Issue-Hotspots

Welche Kombinationen aus Finanzprodukt und Beschwerdegrund treten besonders häufig auf?

## Zeitliche Entwicklung

Wie entwickelt sich das monatliche Beschwerdevolumen zwischen 2022 und 2025?

## Wachstum und Veränderung

Welche Produkt-Issue-Kombinationen zeigen zwischen dem ersten und letzten vollständigen Kalenderjahr auffällige Veränderungen?

## Response Operations

Bei welchen Unternehmen oder Produktgruppen zeigen sich auffällige Unterschiede in der veröffentlichten Timely-Response-Rate?

## Zusammenhangsanalyse

Wie hängen monatliches Beschwerdevolumen, Narrative-Anteil und Timely-Response-Rate statistisch miteinander zusammen?

## Segmentkontrolle

Bleiben aggregierte Zusammenhänge bestehen, wenn das dominante Credit-Reporting-Segment aus dem Portfolio entfernt wird?

---

# Banking- und Finance-Relevanz

Das Projekt ist auf Fragestellungen übertragbar, die in Banken und Finanzdienstleistungsunternehmen regelmäßig auftreten.

Beispiele:

- Welche Produkte erzeugen besonders viele Beschwerden?
- Welche Prozesse stehen hinter den größten Issue-Clustern?
- Welche Beschwerden nehmen im Zeitverlauf zu?
- Wo sollten Root-Cause-Analysen priorisiert werden?
- Welche extern sichtbaren Signale sollten mit internen Prozessdaten verbunden werden?
- Wo könnten Customer-Outcome- oder Conduct-Risk-Untersuchungen sinnvoll sein?
- Wie stark verzerrt ein dominantes Geschäftssegment aggregierte Portfolio-KPIs?
- Wie kann aus heterogenen Beschwerdedaten eine kontrollierte Management-Sicht erzeugt werden?

---

# Relevanz für Versicherungen

Die CFPB-Daten selbst betreffen primär Finanzprodukte und nicht klassische Versicherungsbeschwerden.

Die entwickelte Methodik ist jedoch direkt auf Versicherungsdaten übertragbar, beispielsweise auf:

- Kundenbeschwerden,
- Schadenbearbeitung,
- Leistungsfälle,
- Policenverwaltung,
- Vertragsänderungen,
- Kontaktgründe,
- Bearbeitungszeiten,
- Ombudsmann-Daten,
- Beschwerdestellen-Daten.

Insbesondere die Architektur für:

- Datenbereinigung,
- Taxonomie-Harmonisierung,
- Qualitätskontrollen,
- Issue-Hotspots,
- Zeitreihen,
- Segmentanalysen,
- Management-Reporting

ist branchenübergreifend einsetzbar.

---

# Conduct Risk, Operational Risk und Customer Outcomes

Beschwerden können als Eingangssignal für weiterführende Untersuchungen dienen.

Beispielsweise für:

- mögliche Prozessschwächen,
- wiederkehrende Kundenprobleme,
- auffällige Produkt-Issue-Kombinationen,
- Veränderungen von Beschwerdemustern,
- Priorisierung von Root-Cause-Analysen,
- Identifikation von Bereichen für vertiefende Kontrollen.

Ohne zusätzliche interne Daten werden daraus keine regulatorischen oder kausalen Schlussfolgerungen gezogen.

---

# Relevanz für Technical AI Consulting

Das Projekt demonstriert einen vollständigen analytischen Problemlösungsprozess:

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

Damit zeigt das Repository:

- Übersetzung einer fachlichen Fragestellung in einen Datenprozess,
- Umgang mit einem realen Multi-Millionen-Zeilen-Datensatz,
- reproduzierbare Datenaufnahme,
- transparente Datenbereinigung,
- Umgang mit Taxonomieänderungen,
- automatisierte Qualitätskontrollen,
- statistische Analyse,
- kritische Prüfung aggregierter Ergebnisse,
- Sensitivitätsanalyse,
- adressatengerechtes Reporting,
- technische Modularisierung,
- Ableitung sinnvoller nächster Arbeitsschritte.

---

# Generierte Analyseergebnisse

Nach einem erfolgreichen Analyse-Lauf entstehen unter anderem:

```text
data/processed/complaints_analytics.parquet
```

sowie:

```text
reports/
├── company_timeliness.csv
├── data_cleaning_summary.json
├── data_quality_report.json
├── executive_summary.md
├── interactive_dashboard.html
├── issue_hotspots.csv
├── kpi_summary.csv
├── linear_trend.json
├── monthly_correlations.csv
├── monthly_trends.csv
├── product_summary.csv
├── segment_sensitivity_summary.json
├── segment_sensitivity_yearly.csv
├── taxonomy_harmonization_audit.csv
├── taxonomy_harmonization_summary.json
├── yearly_summary.csv
└── figures/
    ├── 01_monthly_complaints.png
    ├── 02_product_mix.png
    ├── 03_timely_response_by_product.png
    ├── 04_issue_hotspots.png
    ├── 05_product_year_heatmap.png
    └── 06_credit_reporting_sensitivity.png
```

---

# Visualisierungen

## 1. Monatliche Beschwerdeentwicklung

```text
reports/figures/01_monthly_complaints.png
```

Zeigt:

- monatliches Beschwerdevolumen,
- vollständigen rollierenden 12-Monats-Durchschnitt.

---

## 2. Produktmix

```text
reports/figures/02_product_mix.png
```

Zeigt die zehn volumenstärksten harmonisierten Finanzprodukte.

Die dominante Stellung von Credit Reporting bleibt bewusst auf linearer Skala sichtbar.

---

## 3. Timely-Response-Rate nach Produkt

```text
reports/figures/03_timely_response_by_product.png
```

Vergleicht die zehn volumenstärksten Produktgruppen als Dot-Plot.

Zusätzlich wird der beschwerdegewichtete Portfolio-Durchschnitt als Referenz dargestellt.

---

## 4. Produkt-Issue-Hotspots

```text
reports/figures/04_issue_hotspots.png
```

Visualisiert die größten harmonisierten Produkt-Issue-Kombinationen.

Direkte Beschwerdewerte erleichtern die quantitative Einordnung.

---

## 5. Produktentwicklung nach Jahr

```text
reports/figures/05_product_year_heatmap.png
```

Visualisiert die jährliche Produktentwicklung.

Die **Farbintensität ist logarithmisch skaliert**, damit sowohl sehr große als auch kleinere Produktgruppen sichtbar bleiben.

Die dargestellten Zellwerte bleiben absolute Beschwerdezahlen.

---

## 6. Credit-Reporting-Sensitivitätsanalyse

```text
reports/figures/06_credit_reporting_sensitivity.png
```

Vergleicht:

- Gesamtportfolio,
- Credit Reporting,
- Portfolio ohne Credit Reporting.

Die Grafik zeigt zusätzlich den jährlichen Credit-Reporting-Anteil und macht den zunehmenden Kompositionseffekt unmittelbar sichtbar.

---

# Interaktives Dashboard

```text
reports/interactive_dashboard.html
```

Das Plotly-Dashboard ergänzt die statischen Reports um interaktive Explorationen.

Es enthält unter anderem:

- monatliche Beschwerdeentwicklung,
- Produktvergleich,
- Segment-Sensitivitätsanalyse.

---

# Management Reporting

Die Pipeline erzeugt automatisch:

```text
reports/executive_summary.md
```

Die Management Summary fasst zusammen:

- Analyseumfang,
- zentrale Ergebnisse,
- Datenaufbereitung,
- Datenbereinigung,
- Taxonomie-Harmonisierung,
- Sensitivitätsanalyse,
- Banking-/Finance-/Versicherungsrelevanz,
- Consulting-Folgeschritte,
- Datenqualitätsstatus,
- Grenzen der Interpretation.

Damit existiert neben den technischen Ergebnissen eine eigene fachliche Entscheidungsebene.

---

# Grenzen der Analyse

Das Projekt behauptet ausdrücklich **nicht**:

- dass hohes Beschwerdevolumen automatisch schlechte Unternehmensleistung bedeutet,
- dass veröffentlichte Beschwerden repräsentativ für alle Kunden sind,
- dass Unternehmen ohne Berücksichtigung ihrer Größe fair miteinander verglichen werden können,
- dass eine Korrelation einen kausalen Zusammenhang beweist,
- dass die lineare Regression eine belastbare Zukunftsprognose darstellt,
- dass ein beobachteter Segmenteffekt automatisch ein Simpson-Paradox darstellt,
- dass externe Beschwerdedaten allein regulatorische oder operative Entscheidungen rechtfertigen.

Für belastbare Unternehmensvergleiche wären zusätzliche Nenner erforderlich, beispielsweise:

- Kundenanzahl,
- Anzahl Konten,
- Anzahl Verträge,
- Transaktionsvolumen,
- Kreditportfolio,
- Marktanteil,
- Produktnutzung.

---

# Mögliche Weiterentwicklung

## NLP und Generative AI

Die vorhandenen Consumer Narratives könnten später für:

- Topic Modeling,
- Embeddings,
- semantisches Clustering,
- Root-Cause-Erkennung,
- Beschwerdeklassifikation,
- Zusammenfassungen

verwendet werden.

Dies ist bewusst nicht Bestandteil dieses Modul-1-Projekts.

---

## Machine Learning

Mögliche spätere Fragestellungen:

- Klassifikation von Beschwerdekategorien,
- operative Fallpriorisierung,
- Erkennung ungewöhnlicher Beschwerdemuster,
- Anomalieerkennung.

---

## AI Engineering

Mögliche Weiterentwicklungen:

- automatisierte regelmäßige Datenaufnahme,
- Data-Quality-Monitoring,
- Taxonomy-Drift-Erkennung,
- API-Service,
- produktives Dashboard,
- automatisiertes Reporting,
- Monitoring historischer Datenstände.

---

## Institutionelles Consulting

Für ein konkretes Finanzinstitut könnten öffentliche Beschwerden mit internen Daten kombiniert werden:

```text
öffentliche Beschwerden
+ Kundenbestand
+ Produktbestand
+ Konten / Verträge
+ Transaktionsvolumen
+ Marktanteil
+ Service-KPIs
+ Kontaktgründe
+ Incident-Daten
+ Prozessdaten
+ Remediation-Ergebnisse
+ Customer-Outcome-Kennzahlen
```

Dadurch könnten aus explorativen öffentlichen Signalen belastbarere operative, regulatorische und risikoorientierte Analysen entstehen.

---

# Repository-Qualität

Das Projekt ist bewusst **kein einzelnes Notebook**.

Es beinhaltet:

- modulare Python-Paketstruktur,
- reproduzierbare Konfiguration,
- automatisierten Downloader,
- SHA-256-Provenienz,
- speichereffiziente Verarbeitung großer Datenmengen,
- Parquet-Datenebene,
- Datenprofiling,
- Datenbereinigung,
- Taxonomie-Harmonisierung,
- automatisierte Data-Quality-Gates,
- deskriptive Statistik,
- Zeitreihenanalyse,
- Korrelationsanalyse,
- Sensitivitätsanalyse,
- Unit Tests,
- Regressionstests,
- Warning-as-error-Prüfungen,
- Ruff-Linting,
- CI-Workflow,
- statische Visualisierungen,
- interaktives Dashboard,
- Management Summary,
- dokumentierte Interpretationsgrenzen.

Der aktuelle Qualitätsstand umfasst:

```text
24 automatisierte Tests
24 bestanden
24 bestanden mit Python-Warnungen als Fehler
Ruff: All checks passed
```

Damit demonstriert das Repository sowohl **technische Umsetzung** als auch **strukturiertes analytisches und consultingorientiertes Denken**.

---

# Autor

**Maik Hübner**

AI Engineering · Data Analysis · Machine Learning · Financial Services

---

*Dieses Projekt ist eine unabhängige Portfolioanalyse auf Basis öffentlich verfügbarer CFPB-Daten. Es besteht keine Verbindung zum Consumer Financial Protection Bureau und das Projekt wird vom CFPB nicht unterstützt oder empfohlen.*
