# Architektur

## Ziel

Die Consumer Finance Complaint Intelligence Platform trennt Datenaufnahme, Transformation, Datenbereinigung, Taxonomie-Harmonisierung, Validierung, Analyse, Sensitivitätsanalyse, Visualisierung und Management-Reporting bewusst voneinander.

Dadurch können die einzelnen Verarbeitungsschritte unabhängig:

- getestet,
- nachvollzogen,
- erweitert,
- reproduziert

werden.

Die Architektur ist für einen realen Multi-Millionen-Zeilen-Datensatz ausgelegt und soll nicht nur eine einmalige Notebook-Analyse ermöglichen, sondern einen kontrollierten analytischen Workflow.

---

# Gesamtprozess

```text
Offizieller CFPB-Bulk-Download
        │
        ▼
src/data_intelligence_platform/ingestion/download.py
        │
        ├── ZIP-Snapshot
        ├── extrahierte CSV
        └── SHA-256 + Download-Metadaten
        │
        ▼
data/raw/complaints.csv
        │
        ▼
src/data_intelligence_platform/transformation/complaints.py
        │
        ├── Spaltenprojektion
        ├── Datentypen und Datumsfelder
        ├── Textbereinigung
        ├── Zeitraumfilter
        ├── Feature-Ableitung
        ├── Missing-Value-Behandlung
        └── Taxonomie-Harmonisierung
        │
        ▼
data/processed/complaints_analytics.parquet
        │
        ├──────────────────────────────┐
        │                              │
        ▼                              ▼
validation/quality.py           analysis/metrics.py
        │                              │
        ▼                              ├── Executive KPIs
data_quality_report.json               ├── Jahresanalyse
                                       ├── Monatsanalyse
                                       ├── Produktanalyse
                                       ├── Issue-Hotspots
                                       ├── Company Timeliness
                                       ├── Korrelationen
                                       ├── linearer Zeittrend
                                       ├── Data-Cleaning-Summary
                                       ├── Taxonomie-Audit
                                       ├── Segment-Jahresanalyse
                                       └── Sensitivitätsanalyse
                                                │
                      ┌─────────────────────────┴─────────────────────────┐
                      ▼                                                   ▼
           visualization/charts.py                            analysis/report.py
                      │                                                   │
                      ├── 6 PNG-Grafiken                                  ▼
                      └── Plotly-Dashboard                       executive_summary.md
```

---

# Datenaufnahme

Die Datenaufnahme befindet sich unter:

```text
src/data_intelligence_platform/ingestion/
```

Der Downloader bezieht den offiziellen CFPB-Bulk-Datensatz.

Dabei wird nicht direkt in die endgültige ZIP-Datei geschrieben. Stattdessen entsteht zunächst eine temporäre `.part`-Datei.

Erst nach erfolgreichem Download wird diese in die endgültige Datei umbenannt.

Dadurch soll verhindert werden, dass ein unterbrochener Download später fälschlicherweise als vollständiger Snapshot behandelt wird.

Zusätzlich wird ein SHA-256-Hash erzeugt.

Die Download-Metadaten werden gespeichert unter:

```text
data/raw/download_metadata.json
```

Damit ist nachvollziehbar, welcher Rohdatenstand einer Analyse zugrunde liegt.

---

# Trennung von Rohdaten und analytischer Datenebene

Die Rohdaten werden nicht überschrieben.

Der originale CFPB-Snapshot bleibt unter:

```text
data/raw/
```

erhalten.

Die aufbereitete analytische Datenebene wird separat gespeichert:

```text
data/processed/complaints_analytics.parquet
```

Diese Trennung ist zentral für die Nachvollziehbarkeit des Projekts.

Bereinigungen, harmonisierte Kategorien und analytische Ableitungen verändern nicht die ursprüngliche Quelle.

---

# Transformation mit Polars

Die Transformation befindet sich in:

```text
src/data_intelligence_platform/transformation/complaints.py
```

Der vollständige CFPB-Rohdatensatz umfasst mehrere Gigabyte und viele Millionen Zeilen.

Deshalb wird die CSV über Polars lazy eingelesen:

```python
pl.scan_csv(...)
```

Die Transformation wird zunächst als Ausführungsplan aufgebaut.

Dadurch kann Polars unter anderem:

- nicht benötigte Spalten früh verwerfen,
- Zeitraumfilter in den Ausführungsplan integrieren,
- Transformationen effizient ausführen.

Die verarbeitete Datenmenge wird direkt über:

```python
sink_parquet(...)
```

in die Parquet-Datei geschrieben.

Dadurch muss die vollständige transformierte Datenmenge nicht gleichzeitig im Arbeitsspeicher materialisiert werden.

---

# Spaltenprojektion

Für die aktuelle EDA wird bewusst nur ein Teil der CFPB-Quellfelder eingelesen.

Verwendet werden insbesondere:

- Complaint ID,
- Date received,
- Product,
- Sub-product,
- Issue,
- Consumer complaint narrative,
- Company,
- State,
- Submitted via,
- Date sent to company,
- Company response to consumer,
- Timely response?.

Die Consumer Narrative wird während der Transformation ausschließlich verwendet, um:

```text
has_narrative
```

abzuleiten.

Der teilweise sehr lange Narrative-Text selbst wird nicht im aktuellen Modul-1-Parquet gespeichert.

Dadurch wird der Speicherbedarf der analytischen Datenebene reduziert.

Die vollständigen Narrative-Texte bleiben im Rohdatensatz erhalten und können für spätere NLP-Projekte erneut eingelesen werden.

---

# Datenbereinigung

Die Transformation übernimmt unter anderem:

- kontrollierte String-Verarbeitung,
- Bereinigung führender und nachfolgender Leerzeichen,
- Datumsumwandlung,
- Standardisierung der Complaint ID als String,
- Zeitraumfilterung,
- Behandlung fehlender analytischer Issue-Werte.

Ein fehlendes Source-Issue bleibt im ursprünglichen Feld:

```text
issue
```

weiterhin:

```text
null
```

Für die analytische Ebene wird zusätzlich:

```text
harmonized_issue = "Issue not provided"
```

gesetzt.

Damit wird ein fehlender Quellwert nicht erfunden oder versteckt.

Gleichzeitig bleibt die Beschwerde bei Gruppierungen und Aggregationen erhalten.

Die Missing-Value-Behandlung wird separat ausgewiesen:

```text
reports/data_cleaning_summary.json
```

---

# Taxonomie-Harmonisierung

Die CFPB-Klassifikation wurde innerhalb des Analysezeitraums verändert.

Deshalb werden Originalfelder und analytische Felder getrennt geführt.

Original:

```text
product
issue
```

Analytisch:

```text
harmonized_product
harmonized_issue
taxonomy_version
```

Die Originalwerte bleiben unverändert.

Die harmonisierten Felder ermöglichen konsistentere Längsschnittanalysen.

Die Zuordnungen werden zusätzlich dokumentiert:

```text
reports/taxonomy_harmonization_audit.csv
```

Eine kompakte Übersicht wird erzeugt unter:

```text
reports/taxonomy_harmonization_summary.json
```

Missing-Value-Behandlung und Taxonomie-Harmonisierung werden getrennt klassifiziert.

Im aktuellen Analysebestand sind rund:

```text
13,0 %
```

der Beschwerden von mindestens einer Produktharmonisierung betroffen.

---

# Parquet als analytische Datenebene

Die transformierten Daten werden als Parquet gespeichert.

Parquet bietet für dieses Projekt mehrere Vorteile:

- spaltenorientiertes Format,
- Kompression,
- schnelle Spaltenprojektion,
- geringerer Speicherbedarf als die Roh-CSV,
- effizientes wiederholtes Laden der Analysefelder.

Dadurch muss die mehrere Gigabyte große CSV nicht für jede einzelne EDA-Auswertung erneut vollständig verarbeitet werden.

---

# Pandas in der Analyseschicht

Die Analyseschicht befindet sich unter:

```text
src/data_intelligence_platform/analysis/
```

Für den EDA-Lauf wird nur die Teilmenge der Parquet-Spalten geladen, die für die aktuellen Kennzahlen benötigt wird.

Das Laden erfolgt mit PyArrow-gestützten Pandas-Datentypen.

Wiederkehrende Textdimensionen wie:

- Produkt,
- Issue,
- Unternehmen,
- Response-Kategorie,
- Taxonomieversion

werden anschließend als Pandas-Kategorien repräsentiert.

Dadurch wird der Speicherbedarf der mehr als zehn Millionen Analysezeilen reduziert.

Der aktuelle reale Analyse-Lauf benötigt für die projizierte Pandas-Datenebene ungefähr:

```text
599 MiB
```

bei:

```text
10.269.540 Beschwerden
```

Pandas wird anschließend für:

- Gruppierungen,
- Aggregationen,
- Pivot-Tabellen,
- Zeitreihenoperationen,
- statistische Tabellen,
- Segmentanalysen,
- Management-Reporting

eingesetzt.

---

# Validierung

Die automatisierte Validierung befindet sich unter:

```text
src/data_intelligence_platform/validation/
```

Vor der fachlichen Interpretation werden unter anderem geprüft:

- erforderliche Analysefelder,
- doppelte Complaint IDs,
- fehlende Complaint IDs,
- fehlende harmonisierte Produkte,
- fehlende harmonisierte Issues,
- negative Zeitdifferenzen,
- unerwartete Timely-Response-Werte,
- unerwartete Taxonomieversionen,
- tatsächlicher Analysezeitraum.

Das Ergebnis wird maschinenlesbar gespeichert:

```text
reports/data_quality_report.json
```

Der Status:

```text
passed
```

zeigt, ob die definierten strukturellen Quality Gates bestanden wurden.

Für den aktuellen realen Analysebestand gilt:

```text
passed = true
```

---

# Analytische Ebene

Die fachliche Analyse befindet sich hauptsächlich in:

```text
src/data_intelligence_platform/analysis/metrics.py
```

Erzeugt werden unter anderem:

- Executive KPIs,
- Jahreskennzahlen,
- monatliche Zeitreihen,
- Produktkennzahlen,
- Produkt-Issue-Hotspots,
- Unternehmens-Screening zur Timely-Response-Rate,
- Pearson-Korrelationen,
- Spearman-Korrelationen,
- deskriptiver linearer Zeittrend,
- Data-Cleaning-Zusammenfassung,
- Taxonomie-Harmonisierungsübersicht,
- vollständiger Taxonomie-Audit,
- Segment-Jahresanalyse,
- Segment-Sensitivitätsanalyse.

Die analytische Logik ist damit von Reporting und Visualisierung getrennt.

---

# Zeitreihenarchitektur

Die monatliche Analyseschicht erzeugt:

```text
complaints
timely_response_rate
narrative_share
rolling_complaints
```

Der rollierende Durchschnitt verwendet standardmäßig:

```text
12 Monate
```

und wird erst berechnet, wenn ein vollständiges Fenster vorhanden ist.

Technisch:

```text
min_periods = rolling_window
```

Damit erhalten die ersten elf Monate keinen fälschlicherweise als vollständigen 12-Monats-Durchschnitt bezeichneten Wert.

---

# Korrelationsanalyse

Auf den monatlichen Aggregaten werden Pearson- und Spearman-Korrelationen berechnet.

Untersucht werden:

```text
complaints
↔ timely_response_rate
```

```text
complaints
↔ narrative_share
```

```text
timely_response_rate
↔ narrative_share
```

Die Korrelationsfunktion prüft vor der Berechnung:

- ausreichende Anzahl Beobachtungen,
- ausreichende Variabilität beider Variablen.

Nicht berechenbare Beziehungen werden als fehlende Werte ausgewiesen und nicht künstlich ersetzt.

---

# Deskriptiver linearer Zeittrend

Die monatlichen Beschwerden werden gegen einen fortlaufenden Monatsindex regressiert.

Verwendet wird:

```text
LinearRegression
```

aus scikit-learn.

Ausgegeben werden:

```text
monthly_slope
intercept
r2
```

Der Trend dient ausschließlich der Beschreibung des beobachteten Zeitraums.

Er ist kein Forecasting-Modell.

---

# Segment-Sensitivitätsanalyse

Ein zentraler Bestandteil der finalen EDA ist die Prüfung aggregierter Portfolio-Kennzahlen auf Segmentabhängigkeit.

Das Fokussegment ist:

```text
Credit reporting or other personal consumer reports
```

Dieses Segment wurde nicht zufällig gewählt, sondern aufgrund seiner beobachteten Dominanz im Analysebestand.

Die jährliche Segmenttabelle wird erzeugt durch:

```text
segment_yearly_summary()
```

Sie enthält:

```text
year
total_complaints
focus_product_complaints
without_focus_product
focus_product_share
```

Ausgabe:

```text
reports/segment_sensitivity_yearly.csv
```

---

# Sensitivitätskennzahlen

Die Funktion:

```text
segment_sensitivity_summary()
```

vergleicht das Gesamtportfolio mit dem Portfolio ohne das dominante Credit-Reporting-Segment.

Berechnet werden unter anderem:

- Segmentanteil im ersten Analysejahr,
- Segmentanteil im letzten Analysejahr,
- Veränderung in Prozentpunkten,
- Gesamtwachstum,
- Wachstum ohne Fokussegment,
- linearer Trend des Gesamtportfolios,
- linearer Trend ohne Fokussegment,
- rechnerischer Segmentanteil an der Gesamttrend-Steigung,
- R² mit und ohne Fokussegment,
- Pearson-Korrelationen mit und ohne Fokussegment,
- Spearman-Korrelationen mit und ohne Fokussegment.

Ausgabe:

```text
reports/segment_sensitivity_summary.json
```

Die Sensitivitätsanalyse ist bewusst eine **Robustheits- und Interpretationsprüfung**.

Sie ist kein kausales Modell.

---

# Zentrale Sensitivitätsbefunde

Der Credit-Reporting-Anteil steigt von:

```text
75,3 % im Jahr 2022
```

auf:

```text
88,4 % im Jahr 2025
```

Auch ohne dieses Segment wächst das Beschwerdevolumen:

```text
197.553
→
632.673
```

beziehungsweise um rund:

```text
220,3 %
```

Der lineare Monatstrend reduziert sich jedoch von ungefähr:

```text
10.511 Beschwerden pro Monat
```

auf:

```text
925 Beschwerden pro Monat
```

ohne Credit Reporting.

Rechnerisch entfallen rund:

```text
91,2 %
```

der Steigung des linearen Gesamttrends auf den Credit-Reporting-Anteil der monatlichen Beschwerdereihe.

Auch die aggregierten Korrelationsstrukturen verändern sich erheblich.

Diese Ergebnisse werden als Segment- beziehungsweise Kompositionseffekt interpretiert.

Das Projekt behauptet bewusst nicht automatisch das Vorliegen eines Simpson-Paradoxons.

---

# Visualisierung

Die Visualisierung befindet sich unter:

```text
src/data_intelligence_platform/visualization/
```

Die Pipeline erzeugt sechs statische PNG-Grafiken.

```text
reports/figures/
├── 01_monthly_complaints.png
├── 02_product_mix.png
├── 03_timely_response_by_product.png
├── 04_issue_hotspots.png
├── 05_product_year_heatmap.png
└── 06_credit_reporting_sensitivity.png
```

---

# Visualisierungsprinzipien

Die Grafiken sind auf folgende Anforderungen ausgelegt:

- GitHub-Lesbarkeit,
- Management-Kommunikation,
- fachliche Aussagekraft,
- korrekte Skalen,
- direkte Kennzahlenbeschriftung,
- keine unnötige wissenschaftliche Zahlenformatierung,
- kontrollierter Umgang mit sehr unterschiedlichen Größenordnungen.

---

# Top-N-Visualisierungen

Produktdiagramme verwenden eine eigene vorbereitende Top-N-Funktion.

Diese stellt sicher, dass:

- wirklich nur die angeforderte Anzahl Produkte dargestellt wird,
- unbenutzte Pandas-Categorical-Levels entfernt werden,
- keine leeren Kategorien in Seaborn-Diagrammen erscheinen.

Damit wird ein zuvor identifizierter Categorical-Darstellungsfehler automatisch verhindert.

---

# Timely-Response-Visualisierung

Die Timely-Response-Raten der volumenstärksten Produkte werden als Dot-Plot dargestellt.

Dadurch bleiben Unterschiede im hohen Prozentbereich besser erkennbar als in einem klassischen 0-bis-100-Prozent-Balkendiagramm.

Zusätzlich wird der beschwerdegewichtete Portfolio-Durchschnitt als Referenzlinie dargestellt.

---

# Heatmap

Die Produkt-Jahres-Heatmap verwendet eine logarithmische Farbskala.

Grund:

Das Credit-Reporting-Volumen liegt um Größenordnungen über mehreren anderen Produktgruppen.

Eine lineare Farbskala würde kleinere Segmente nahezu vollständig visuell ausblenden.

Die Farbintensität ist deshalb logarithmisch.

Die Zellwerte bleiben dagegen absolute Beschwerdezahlen.

Damit wird die Skalierung transparent dargestellt und die tatsächliche Größenordnung bleibt direkt ablesbar.

---

# Display-Bezeichnungen

Für besonders lange CFPB-Kategorien verwendet die Visualisierungsschicht teilweise verkürzte Display-Bezeichnungen.

Beispiel:

```text
Credit reporting or other personal consumer reports
```

wird in bestimmten dicht belegten Grafiken dargestellt als:

```text
Credit Reporting
```

Diese Verkürzung betrifft ausschließlich die Darstellung.

Die:

- Rohdaten,
- harmonisierten Daten,
- analytischen Tabellen

bleiben unverändert.

---

# Interaktives Dashboard

Zusätzlich wird erzeugt:

```text
reports/interactive_dashboard.html
```

Das Dashboard enthält:

- monatliche Beschwerdeentwicklung,
- Produktvergleich,
- Segment-Sensitivitätsanalyse.

Es dient der interaktiven Exploration und ersetzt weder Quality Gates noch dokumentierte Interpretationsgrenzen.

---

# Management Reporting

Die Management Summary wird automatisch aus den berechneten Ergebnissen erzeugt.

Datei:

```text
reports/executive_summary.md
```

Sie verbindet:

- zentrale Kennzahlen,
- Datenbereinigung,
- Taxonomie-Harmonisierung,
- statistische Ergebnisse,
- Sensitivitätsanalyse,
- Banking-/Finance-/Versicherungsrelevanz,
- Technical-AI-Consulting-Perspektive,
- Handlungsempfehlungen,
- Interpretationsgrenzen.

Dadurch werden technische Ergebnisse in eine fachlich verständliche Entscheidungsebene übersetzt.

---

# Test- und Qualitätsarchitektur

Die Test-Suite befindet sich unter:

```text
tests/
```

Der aktuelle Stand umfasst:

```text
24 automatisierte Tests
```

Abgedeckt werden unter anderem:

- Download- und Hash-Funktionen,
- Transformation,
- Zeitraumfilterung,
- Taxonomie-Harmonisierung,
- Missing-Value-Behandlung,
- analytische Kennzahlen,
- Data-Cleaning-Audit,
- Datenqualitätsprüfung,
- Reporting,
- Segment-Sensitivität,
- vollständiges Rolling Window,
- Visualisierung,
- Categorical-Datentypen,
- PyArrow-basierte numerische Werte,
- Top-N-Auswahl ohne unbenutzte Kategorien.

Normales Gate:

```bash
pytest -q
```

Strenger Warning-Test:

```bash
pytest -q -W error
```

Codequalität:

```bash
ruff check .
```

Aktueller Status:

```text
24 passed
24 passed mit -W error
Ruff: All checks passed
```

---

# Erweiterbarkeit

Die Architektur ist bewusst so gestaltet, dass spätere Projekte darauf aufbauen können.

Mögliche Erweiterungen sind beispielsweise:

```text
aktueller EDA-Layer
        │
        ├── NLP auf Consumer Narratives
        ├── Topic Modeling
        ├── Embeddings
        ├── ML-basierte Klassifikation
        ├── Anomalieerkennung
        ├── automatisierte Datenaufnahme
        ├── Taxonomy-Drift-Monitoring
        ├── API
        └── produktives Dashboard
```

Der aktuelle Stand bleibt bewusst ein **Datenanalyse-/EDA-Projekt** und erweitert den Modul-1-Umfang nicht künstlich um Machine Learning.
