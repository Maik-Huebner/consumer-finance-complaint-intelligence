# Generierte Analyseberichte

Dieses Verzeichnis enthält die automatisch erzeugten Ergebnisse der **Consumer Finance Complaint Intelligence Platform**.

Die Reports entstehen durch den vollständigen Pipeline-Lauf:

```bash
python scripts/run_pipeline.py
```

Wenn bereits eine aktuelle verarbeitete Parquet-Datei vorhanden ist, kann alternativ nur die Analyse- und Reporting-Schicht ausgeführt werden:

```bash
python scripts/run_analysis.py
```

---

## Zweck dieses Verzeichnisses

Die Dateien unter `reports/` bilden die sichtbare Ergebnis- und Reporting-Ebene des Projekts.

Sie dokumentieren:

- Datenqualität,
- Datenbereinigung,
- Taxonomie-Harmonisierung,
- zentrale KPIs,
- Produkt- und Issue-Analysen,
- zeitliche Entwicklungen,
- statistische Zusammenhänge,
- Segment- und Sensitivitätsanalysen,
- Visualisierungen,
- Management-Interpretation.

Damit trennt das Projekt bewusst die technische Datenverarbeitung von der fachlichen Ergebnisdarstellung.

---

# Management Summary

```text
executive_summary.md
```

Die automatisch erzeugte Management Summary fasst die wichtigsten Ergebnisse für eine fachliche beziehungsweise consultingorientierte Betrachtung zusammen.

Sie enthält:

- Analyseumfang,
- zentrale Befunde,
- Datenaufbereitung,
- Datenbereinigung,
- Taxonomie-Harmonisierung,
- Sensitivitätsanalyse,
- Banking-/Finance-/Versicherungsbezug,
- empfohlene Consulting-Folgeschritte,
- Datenqualitätsstatus,
- Grenzen der Interpretation.

Ein besonderer Schwerpunkt liegt auf der Frage, wie stark aggregierte Portfolio-Kennzahlen durch das dominante Credit-Reporting-Segment beeinflusst werden.

---

# Datenqualität

```text
data_quality_report.json
```

Dieser maschinenlesbare Quality-Gate-Report dokumentiert die automatisierten Datenqualitätsprüfungen.

Geprüft werden unter anderem:

- Anzahl analysierter Datensätze,
- Anzahl analysierter Spalten,
- doppelte Complaint IDs,
- fehlende Complaint IDs,
- fehlende harmonisierte Produktwerte,
- fehlende harmonisierte Issue-Werte,
- negative Zeitdifferenzen,
- unerwartete `Timely response?`-Werte,
- unerwartete Taxonomieversionen,
- minimaler Analysezeitpunkt,
- maximaler Analysezeitpunkt,
- Missing-Value-Anteile.

Der zentrale Status:

```text
passed
```

zeigt, ob die vorgesehenen strukturellen Quality Gates erfolgreich bestanden wurden.

Für den aktuellen Analysebestand gilt:

```text
passed = true
```

---

# Datenbereinigung

```text
data_cleaning_summary.json
```

Dieser Report dokumentiert explizit behandelte Missing-Value-Fälle.

Dabei wird zwischen folgenden Zuständen unterschieden:

- fehlender Wert in den ursprünglichen Quelldaten,
- analytisch behandelter Missing Value,
- unbehandelter Missing Value.

Die ursprünglichen CFPB-Felder werden dabei nicht überschrieben.

Beispiel:

```text
issue = null
```

bleibt als ursprünglicher Source-Wert erhalten.

Für die analytische Ebene wird zusätzlich:

```text
harmonized_issue = "Issue not provided"
```

verwendet.

Dadurch bleibt die Beschwerde:

- vollständig im Datensatz erhalten,
- in Aggregationen sichtbar,
- hinsichtlich ihrer Datenherkunft nachvollziehbar.

Im aktuellen Analysebestand betrifft dies:

```text
6 Beschwerden
```

Alle sechs Fälle werden analytisch behandelt.

Unbehandelte Fälle:

```text
0
```

---

# Taxonomie-Harmonisierung

## Zusammenfassung

```text
taxonomy_harmonization_summary.json
```

Dieser Report zeigt unter anderem:

- Anzahl analysierter Beschwerden,
- Anzahl harmonisierter Produktwerte,
- Anteil harmonisierter Produktwerte,
- Anzahl harmonisierter Issue-Werte,
- Anteil harmonisierter Issue-Werte,
- Anzahl Datensätze mit mindestens einer Taxonomieänderung.

Im aktuellen Analysebestand sind:

```text
1.335.250 Beschwerden
```

beziehungsweise rund:

```text
13,0 %
```

von einer Produktharmonisierung betroffen.

---

## Vollständiger Mapping-Audit

```text
taxonomy_harmonization_audit.csv
```

Der Audit dokumentiert die Beziehung zwischen Quellklassifikation und analytischer Klassifikation.

Beispielhafte Struktur:

```text
Dimension
→ Kontext
→ Originalwert
→ harmonisierter Wert
→ Anzahl Beschwerden
→ geändert ja/nein
→ Änderungstyp
```

Der Audit unterscheidet ausdrücklich zwischen:

```text
taxonomy_harmonization
```

und:

```text
missing_value_handling
```

Damit werden echte Änderungen der Datenklassifikation nicht mit Datenbereinigung vermischt.

---

# KPI-Übersicht

```text
kpi_summary.csv
```

Enthält zentrale Kennzahlen des vollständigen Analysezeitraums.

Unter anderem:

- Anzahl Beschwerden,
- Anzahl Unternehmen,
- Anzahl harmonisierter Produkte,
- Timely-Response-Rate,
- Narrative-Anteil,
- Median der Weiterleitungsdauer.

Aktueller Gesamtbestand:

```text
10.269.540 Beschwerden
5.601 Unternehmen
11 harmonisierte Produktgruppen
```

---

# Jahresanalyse

```text
yearly_summary.csv
```

Enthält aggregierte Kennzahlen je Kalenderjahr.

Dazu gehören unter anderem:

- Beschwerdevolumen,
- Timely-Response-Rate,
- Narrative-Anteil,
- Anzahl Unternehmen,
- Year-over-Year-Veränderung.

Die Analyse verwendet vollständige Kalenderjahre von:

```text
2022 bis 2025
```

Dadurch werden unvollständige laufende Jahre nicht mit vollständigen Vorjahren verglichen.

---

# Monatliche Zeitreihe

```text
monthly_trends.csv
```

Enthält:

- monatliches Beschwerdevolumen,
- Timely-Response-Rate,
- Narrative-Anteil,
- rollierenden 12-Monats-Durchschnitt.

Der rollierende Durchschnitt wird bewusst erst ausgegeben, wenn ein vollständiges Fenster von zwölf Monatsbeobachtungen vorliegt.

Die ersten elf Monate enthalten daher keinen scheinbar vollständigen 12-Monats-Wert.

---

# Produktanalyse

```text
product_summary.csv
```

Enthält aggregierte Kennzahlen auf Ebene der **harmonisierten Produktklassifikation**.

Unter anderem:

- Beschwerdevolumen,
- Beschwerdeanteil,
- Timely-Response-Rate,
- Narrative-Anteil,
- Anzahl beteiligter Unternehmen.

Die größte harmonisierte Produktgruppe ist:

```text
Credit reporting or other personal consumer reports
```

mit:

```text
8.824.129 Beschwerden
```

beziehungsweise rund:

```text
85,9 %
```

des vollständigen Analysebestands.

---

# Produkt-Issue-Hotspots

```text
issue_hotspots.csv
```

Dieser Report priorisiert Kombinationen aus:

```text
harmonized_product
+
harmonized_issue
```

nach Beschwerdevolumen.

Zusätzlich werden Veränderungen zwischen erstem und letztem vollständigen Analysejahr berechnet.

Der volumenstärkste aktuelle Hotspot ist:

```text
Credit reporting or other personal consumer reports
→ Incorrect information on your report
```

mit:

```text
4.653.591 Beschwerden
```

Die Tabelle kann beispielsweise als Ausgangspunkt für:

- Root-Cause-Analysen,
- Prozessuntersuchungen,
- Conduct-Risk-Fragestellungen,
- Customer-Outcome-Analysen,
- weiterführende NLP-Untersuchungen

verwendet werden.

---

# Unternehmensbezogene Timely-Response-Analyse

```text
company_timeliness.csv
```

Diese Tabelle enthält explorative Kennzahlen zur veröffentlichten Timely-Response-Rate von Unternehmen.

Um besonders instabile Kleinstichproben zu reduzieren, werden nur Unternehmen oberhalb eines konfigurierten Mindestbeschwerdevolumens berücksichtigt.

Die Ergebnisse stellen ausdrücklich **keine Unternehmensrangliste** dar.

Ohne zusätzliche Bezugsgrößen wie:

- Kundenanzahl,
- Konten,
- Verträge,
- Marktanteil,
- Produkt-Exposure,
- Transaktionsvolumen

sind keine fairen Performance-Vergleiche möglich.

---

# Korrelationsanalyse

```text
monthly_correlations.csv
```

Enthält Pearson- und Spearman-Korrelationen zwischen ausgewählten monatlichen Kennzahlen.

Untersucht werden unter anderem Beziehungen zwischen:

```text
Beschwerdevolumen
↔ Timely-Response-Rate
```

```text
Beschwerdevolumen
↔ Narrative-Anteil
```

```text
Timely-Response-Rate
↔ Narrative-Anteil
```

Die Ergebnisse beschreiben statistische Zusammenhänge.

Sie beweisen keine Kausalität.

---

# Linearer Zeittrend

```text
linear_trend.json
```

Enthält die Parameter einer einfachen linearen Regression über das monatliche Beschwerdevolumen.

Dokumentiert werden insbesondere:

- Steigung,
- Achsenabschnitt,
- R².

Der aktuelle Gesamttrend entspricht ungefähr:

```text
+10.511 Beschwerden pro Monat
```

bei:

```text
R² = 0,877
```

Dieser Wert dient ausschließlich zur **deskriptiven Beschreibung des beobachteten Zeitraums**.

Er wird nicht als Prognosemodell verwendet.

---

# Sensitivitätsanalyse

Die EDA enthält zusätzlich eine Segmentkontrolle für die dominante Produktgruppe:

```text
Credit reporting or other personal consumer reports
```

Ziel ist zu prüfen, wie stark aggregierte Portfolio-Kennzahlen durch dieses Segment beeinflusst werden.

---

## Jährliche Sensitivitätsdaten

```text
segment_sensitivity_yearly.csv
```

Enthält je Jahr:

- Gesamtportfolio,
- Credit-Reporting-Beschwerden,
- Portfolio ohne Credit Reporting,
- Credit-Reporting-Anteil.

Aktuelle Entwicklung:

```text
2022: 75,3 %
2023: 80,9 %
2024: 86,5 %
2025: 88,4 %
```

---

## Sensitivitäts-Zusammenfassung

```text
segment_sensitivity_summary.json
```

Dokumentiert unter anderem:

- Segmentanteil im ersten und letzten Analysejahr,
- Veränderung in Prozentpunkten,
- Beschwerdewachstum mit und ohne Credit Reporting,
- linearen Monatstrend mit und ohne Credit Reporting,
- Anteil des Segments an der linearen Gesamttrend-Steigung,
- Korrelationsstrukturen mit und ohne dominantes Segment.

Ohne Credit Reporting steigt das veröffentlichte Beschwerdevolumen von:

```text
197.553
```

auf:

```text
632.673
```

beziehungsweise um:

```text
220,3 %
```

Die Steigung des linearen Monatstrends reduziert sich von rund:

```text
10.511
```

auf:

```text
925
```

Beschwerden pro Monat.

Rechnerisch entfallen damit rund:

```text
91,2 %
```

der linearen Gesamttrend-Steigung auf den Credit-Reporting-Anteil der monatlichen Beschwerdereihe.

Auch Korrelationsstrukturen verändern sich deutlich.

Beispiel:

```text
Beschwerdevolumen ↔ Narrative-Anteil

Gesamtportfolio:
Pearson r = -0,891

ohne Credit Reporting:
Pearson r = -0,227
```

Diese Ergebnisse zeigen einen deutlichen Segment- beziehungsweise Kompositionseffekt.

Sie werden bewusst nicht automatisch als Simpson-Paradox klassifiziert.

---

# Visualisierungen

Die Pipeline erzeugt sechs statische Kernvisualisierungen:

```text
figures/
├── 01_monthly_complaints.png
├── 02_product_mix.png
├── 03_timely_response_by_product.png
├── 04_issue_hotspots.png
├── 05_product_year_heatmap.png
└── 06_credit_reporting_sensitivity.png
```

---

## 1. Monatliche Beschwerdeentwicklung

```text
figures/01_monthly_complaints.png
```

Zeigt:

- monatliches Beschwerdevolumen,
- vollständigen rollierenden 12-Monats-Durchschnitt.

---

## 2. Produktmix

```text
figures/02_product_mix.png
```

Zeigt die zehn volumenstärksten harmonisierten Finanzprodukte.

Die dominante Stellung von Credit Reporting wird bewusst nicht durch eine logarithmische Balkenskala relativiert.

Absolute Werte werden direkt an den Balken ausgewiesen.

---

## 3. Timely-Response-Rate nach Produkt

```text
figures/03_timely_response_by_product.png
```

Vergleicht die zehn volumenstärksten Produktgruppen als Dot-Plot.

Zusätzlich wird der beschwerdegewichtete Portfolio-Durchschnitt dargestellt.

Dadurch werden Abweichungen wie beispielsweise bei Student Loans besser sichtbar als in einem klassischen 0-bis-100-Prozent-Balkendiagramm.

---

## 4. Produkt-Issue-Hotspots

```text
figures/04_issue_hotspots.png
```

Visualisiert die größten harmonisierten Produkt-Issue-Kombinationen.

Für die Visualisierung werden teilweise verkürzte Display-Bezeichnungen verwendet.

Die zugrunde liegenden Source- und Harmonized-Werte bleiben davon unverändert.

---

## 5. Produktentwicklung nach Jahr

```text
figures/05_product_year_heatmap.png
```

Zeigt die jährliche Entwicklung der wichtigsten harmonisierten Produktgruppen.

Die Farbintensität verwendet eine:

```text
logarithmische Skala
```

damit sowohl die dominante Credit-Reporting-Gruppe als auch kleinere Produktgruppen visuell unterscheidbar bleiben.

Die Zellwerte bleiben absolute Beschwerdezahlen.

---

## 6. Sensitivitätsanalyse

```text
figures/06_credit_reporting_sensitivity.png
```

Vergleicht:

- Gesamtportfolio,
- Credit Reporting,
- Portfolio ohne Credit Reporting.

Zusätzlich wird der Credit-Reporting-Anteil je Jahr annotiert.

Die Grafik visualisiert damit unmittelbar, wie stark sich der Produktmix im Analysezeitraum verändert.

---

# Interaktives Dashboard

```text
interactive_dashboard.html
```

Das Plotly-Dashboard ergänzt die statischen Reports um eine interaktive Exploration.

Es enthält unter anderem:

- monatliche Beschwerdeentwicklung,
- Produktvergleich,
- Segment-Sensitivitätsanalyse.

Das Dashboard ist als ergänzende Analyseoberfläche gedacht und ersetzt nicht:

- Quality Gates,
- methodische Dokumentation,
- Management-Interpretation.

---

# Reproduzierbarkeit

Die generierten Reports hängen vom verwendeten lokalen CFPB-Snapshot ab.

Der vollständige Rohdatensatz wird deshalb nicht im Repository gespeichert.

Die Pipeline dokumentiert stattdessen:

- Datenquelle,
- Downloadzeitpunkt,
- SHA-256-Hash,
- Analysezeitraum,
- Datenbereinigung,
- Datenqualitätsstatus,
- Taxonomie-Harmonisierung,
- Segment-Sensitivität.

Dadurch können Analyseergebnisse auf kontrollierten Datenständen reproduziert und miteinander verglichen werden.

---

# Technischer Qualitätsstand

Die aktuelle Implementierung wird durch automatisierte Tests abgesichert.

Aktueller Stand:

```text
24 Tests gesammelt
24 bestanden
24 bestanden mit -W error
Ruff: All checks passed
```

Getestet werden unter anderem:

- Download- und Hash-Funktionen,
- Transformation,
- Taxonomie-Harmonisierung,
- Missing-Value-Behandlung,
- analytische Kennzahlen,
- vollständiges Rolling Window,
- Segment-Sensitivität,
- Datenqualitätsprüfung,
- Reporting,
- Visualisierung,
- Categorical-Datentypen,
- PyArrow-basierte numerische Werte,
- Top-N-Visualisierung ohne unbenutzte Categorical Levels.

---

# Interpretation

Die Reports dienen der:

- explorativen Priorisierung,
- Hypothesengenerierung,
- risikoorientierten Untersuchung,
- datenbasierten Entscheidungsunterstützung.

Sie sind keine Grundlage für ungeprüfte kausale oder regulatorische Schlussfolgerungen.

Insbesondere gilt:

- Beschwerdevolumen ist keine direkte Qualitätskennzahl,
- Korrelation ist keine Kausalität,
- externe Complaint-Daten ersetzen keine internen Exposure-Daten,
- Unternehmenskennzahlen ohne Nenner sind keine faire Performance-Rangliste,
- der lineare Trend ist keine Prognose,
- aggregierte Kennzahlen können erheblich vom Produktmix beeinflusst werden,
- ein beobachteter Kompositionseffekt ist nicht automatisch ein Simpson-Paradox.

Diese Interpretationsgrenzen sind Bestandteil des analytischen Designs und nicht nur ein nachträglicher Disclaimer.
