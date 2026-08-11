# Methodik

## 1. Zielsetzung

Das Projekt untersucht veröffentlichte Verbraucherbeschwerden des U.S. Consumer Financial Protection Bureau (CFPB) mit Methoden der Exploratory Data Analysis.

Ziel ist nicht nur die Erstellung einzelner Diagramme, sondern ein reproduzierbarer Prozess von der Rohdatenquelle bis zur Management-Interpretation.

Der Workflow untersucht insbesondere:

- Beschwerdekonzentrationen,
- Produkt-Issue-Hotspots,
- zeitliche Entwicklungen,
- Response-Timeliness,
- statistische Zusammenhänge,
- Datenqualitätsprobleme,
- historische Taxonomieänderungen,
- Segment- und Kompositionseffekte.

---

# 2. Analysezeitraum

Standardmäßig werden vollständige Kalenderjahre analysiert:

```text
2022-01-01
bis
2025-12-31
```

Der Zeitraum ist konfigurierbar unter:

```text
configs/project.yaml
```

Die Verwendung vollständiger Kalenderjahre verhindert, dass ein unvollständiges laufendes Jahr direkt mit abgeschlossenen Vorjahren verglichen wird.

---

# 3. Datenquelle

Verwendet wird die offizielle:

**CFPB Consumer Complaint Database**

Der vollständige Bulk-Datensatz wird über das Download-Skript bezogen.

Die Rohdaten werden lokal gespeichert, aber nicht in Git versioniert.

---

# 4. Datenprovenienz

Beim Download werden Metadaten gespeichert.

Dazu gehören:

- Quell-URL,
- Downloadzeitpunkt,
- ZIP-Dateiname,
- ZIP-Dateigröße,
- SHA-256-Prüfsumme,
- extrahierter CSV-Dateiname,
- CSV-Dateigröße.

Datei:

```text
data/raw/download_metadata.json
```

Dadurch lässt sich nachvollziehen, welcher Snapshot einer Analyse zugrunde liegt.

---

# 5. Spaltenauswahl

Der vollständige Rohdatensatz enthält mehr Felder, als für die aktuelle EDA notwendig sind.

Die Transformation liest deshalb nur die für die aktuellen Fragestellungen erforderlichen Quellspalten.

Dazu gehören:

```text
Date received
Product
Sub-product
Issue
Consumer complaint narrative
Company
State
Submitted via
Date sent to company
Company response to consumer
Timely response?
Complaint ID
```

Diese Projektion reduziert unnötige Datenverarbeitung.

---

# 6. Datentypen und Textbereinigung

Während der Transformation werden:

- Datumsfelder geparst,
- Complaint IDs als Strings behandelt,
- Textfelder kontrolliert verarbeitet,
- führende und nachfolgende Leerzeichen entfernt.

Ungültige Datumswerte werden nicht künstlich ersetzt.

Die spätere Datenqualitätsprüfung kontrolliert die daraus resultierende analytische Struktur.

---

# 7. Zeitraumfilterung

Nach der Datumsumwandlung wird ausschließlich der konfigurierte Analysezeitraum berücksichtigt.

Die Filterung erfolgt innerhalb des Polars-Lazy-Plans.

Dadurch kann die Verarbeitung des großen Rohdatensatzes effizient durchgeführt werden.

---

# 8. Abgeleitete Zeitfelder

Aus `date_received` werden erzeugt:

```text
year
month
year_month
quarter
```

Diese Variablen dienen:

- Jahresvergleichen,
- Monatsanalysen,
- rollierenden Kennzahlen,
- Pivot-Tabellen,
- Zeittrendanalysen.

---

# 9. Prozesskennzahlen

Aus:

```text
date_received
```

und:

```text
date_sent_to_company
```

wird:

```text
days_to_company
```

berechnet.

Definition:

```text
date_sent_to_company - date_received
```

Negative Werte gelten im aktuellen Datenmodell als unplausibel und werden vom Quality Gate gemeldet.

---

# 10. Timely-Response-Ableitung

Der ursprüngliche Wert:

```text
timely_response
```

bleibt erhalten.

Zusätzlich wird erzeugt:

```text
is_timely
```

mit:

```text
timely_response == "Yes"
```

Dadurch können Response-Raten direkt als Mittelwert einer booleschen Variable berechnet werden.

---

# 11. Narrative-Verfügbarkeit

Der Consumer Narrative kann sehr lang sein und ist nur für einen Teil der Beschwerden verfügbar.

Für Modul 1 wird lediglich abgeleitet:

```text
has_narrative
```

Das Feld ist `True`, wenn ein nicht leerer Narrative vorliegt.

Der eigentliche Beschwerdetext wird nicht in das aktuelle Analyse-Parquet übernommen.

Damit bleibt die analytische Datenebene bei mehr als zehn Millionen Datensätzen speichereffizient.

Der vollständige Narrative bleibt im Rohdatensatz verfügbar.

---

# 12. Missing-Value-Behandlung

Fehlende Quellwerte werden nicht automatisch gelöscht.

Für fehlende Issue-Werte gilt:

```text
issue = null
```

im Originalfeld.

Für die analytische Gruppierung wird zusätzlich:

```text
harmonized_issue = "Issue not provided"
```

verwendet.

Dadurch:

- bleibt der Source-Wert unverändert,
- bleibt die Beschwerde in Aggregationen enthalten,
- wird der Missing Value sichtbar repräsentiert.

Die Behandlung wird separat zusammengefasst:

```text
reports/data_cleaning_summary.json
```

Im aktuellen Analysebestand fehlen bei:

```text
6 Beschwerden
```

Source-Issue-Werte.

Alle sechs werden analytisch behandelt.

Unbehandelte Fälle:

```text
0
```

---

# 13. Taxonomie-Harmonisierung

Die CFPB-Produkt- und Issue-Taxonomie hat sich historisch verändert.

Eine reine Gruppierung nach Originalwerten würde dadurch bestimmte fachlich zusammengehörige Kategorien über die Jahre hinweg künstlich trennen.

Deshalb werden zusätzliche Felder erzeugt:

```text
harmonized_product
harmonized_issue
taxonomy_version
```

Die Originalfelder:

```text
product
issue
```

bleiben unverändert.

Die Harmonisierung verwendet dokumentierte historische Änderungen sowie gegebenenfalls Sub-Product-Informationen, wenn eine frühere Sammelkategorie später aufgeteilt wurde.

---

# 14. Taxonomie-Audit

Alle Source-to-Analytical-Zuordnungen werden aggregiert auditiert.

Datei:

```text
reports/taxonomy_harmonization_audit.csv
```

Der Audit unterscheidet:

```text
unchanged
taxonomy_harmonization
missing_value_handling
```

Damit wird transparent, welche analytischen Änderungen aus:

- historischer Taxonomie-Harmonisierung,
- Datenbereinigung

entstanden sind.

---

# 15. Speicherung der Analysebasis

Die transformierten Daten werden streamend als:

```text
data/processed/complaints_analytics.parquet
```

gespeichert.

Kompression:

```text
zstd
```

Parquet wird verwendet, weil es:

- spaltenorientiert,
- komprimierbar,
- für wiederholte analytische Abfragen effizient

ist.

---

# 16. Speicheroptimierte Analyse

`scripts/run_analysis.py` liest nur die für den Kernreport erforderlichen Parquet-Spalten ein.

PyArrow-basierte Pandas-Datentypen reduzieren den Python-Object-Overhead.

Wiederkehrende Textdimensionen werden anschließend als Kategorien repräsentiert.

Der reale Analysebestand umfasst:

```text
10.269.540 Beschwerden
```

und benötigt für die projizierte Pandas-Analyseschicht ungefähr:

```text
599 MiB
```

Arbeitsspeicher.

---

# 17. Datenqualitätsprüfung

Vor der Interpretation wird eine automatisierte Validierung durchgeführt.

Geprüft werden:

- erforderliche Spalten,
- doppelte Complaint IDs,
- fehlende Complaint IDs,
- fehlende harmonisierte Produkte,
- fehlende harmonisierte Issues,
- negative `days_to_company`,
- unerwartete Timely-Response-Werte,
- unerwartete Taxonomieversionen,
- minimaler und maximaler Analysezeitpunkt,
- Missing-Value-Anteile.

Der Report wird gespeichert unter:

```text
reports/data_quality_report.json
```

Der aktuelle reale Analysebestand besteht alle definierten strukturellen Quality Gates:

```text
passed = true
```

---

# 18. Executive KPIs

Für den gesamten Analysezeitraum werden unter anderem berechnet:

- Anzahl Beschwerden,
- Anzahl Unternehmen,
- Anzahl harmonisierter Produktgruppen,
- Timely-Response-Rate,
- Narrative-Anteil,
- Median von `days_to_company`.

Aktueller Analysebestand:

```text
10.269.540 Beschwerden
5.601 Unternehmen
11 harmonisierte Produktgruppen
```

---

# 19. Jahresanalyse

Für jedes Kalenderjahr werden berechnet:

- Beschwerdevolumen,
- Timely-Response-Rate,
- Narrative-Anteil,
- Anzahl Unternehmen,
- Year-over-Year-Veränderung.

Die veröffentlichten Beschwerden steigen von:

```text
800.245 im Jahr 2022
```

auf:

```text
5.442.977 im Jahr 2025
```

Dies entspricht einer Veränderung von rund:

```text
+580,2 %
```

---

# 20. Monatliche Zeitreihe

Auf Monatsebene werden berechnet:

- Anzahl Beschwerden,
- Timely-Response-Rate,
- Narrative-Anteil.

Zusätzlich wird ein rollierender Durchschnitt des Beschwerdevolumens berechnet.

Standardfenster:

```text
12 Monate
```

Der Wert wird nur berechnet, wenn tatsächlich zwölf Monatsbeobachtungen im Fenster vorhanden sind.

Technisch:

```text
min_periods = rolling_window
```

Die ersten elf Monate enthalten deshalb keinen scheinbar vollständigen 12-Monats-Durchschnitt.

---

# 21. Produktanalyse

Die Produktanalyse basiert auf:

```text
harmonized_product
```

und nicht ausschließlich auf dem historischen Source-Feld `product`.

Berechnet werden:

- Beschwerdevolumen,
- Anteil am Gesamtvolumen,
- Timely-Response-Rate,
- Narrative-Anteil,
- Anzahl Unternehmen.

Die dominante Kategorie ist:

```text
Credit reporting or other personal consumer reports
```

mit:

```text
8.824.129 Beschwerden
```

beziehungsweise:

```text
85,9 %
```

des Analysebestands.

---

# 22. Produkt-Issue-Hotspots

Hotspots werden über:

```text
harmonized_product
+
harmonized_issue
```

gebildet.

Für jede Kombination werden unter anderem berechnet:

- Beschwerdeanzahl,
- Timely-Response-Rate,
- Narrative-Anteil,
- Anzahl Beschwerden im ersten Analysejahr,
- Anzahl Beschwerden im letzten Analysejahr,
- Veränderung zwischen erstem und letztem Jahr.

Wenn im ersten Jahr kein Fall vorhanden ist, wird keine künstlich unendliche Wachstumsrate erzeugt.

Die entsprechende Wachstumskennzahl bleibt dann nicht interpretierbar.

Der größte aktuelle Hotspot ist:

```text
Credit reporting or other personal consumer reports
→ Incorrect information on your report
```

mit:

```text
4.653.591 Beschwerden
```

---

# 23. Unternehmensbezogenes Screening

Für Unternehmen wird eine explorative Timely-Response-Auswertung erzeugt.

Damit kleine Fallzahlen nicht die Tabelle dominieren, gilt ein konfigurierbares Mindestvolumen.

Die Ergebnisse werden nicht als Performance-Ranking interpretiert.

Ohne:

- Kundenanzahl,
- Marktanteil,
- Produkt-Exposure,
- Transaktionsvolumen

ist ein fairer Unternehmensvergleich nicht möglich.

---

# 24. Pearson-Korrelation

Pearson misst die lineare Beziehung zwischen zwei metrischen Größen.

Auf Monatsebene werden untersucht:

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

Zusätzlich wird der jeweilige p-Wert dokumentiert.

Die Korrelationen werden nicht kausal interpretiert.

---

# 25. Spearman-Rangkorrelation

Spearman untersucht monotone Zusammenhänge anhand der Rangordnung.

Sie ergänzt Pearson, weil ein Zusammenhang auch dann monoton sein kann, wenn er nicht linear ist.

Auch hier gilt:

```text
Korrelation ≠ Kausalität
```

---

# 26. Deskriptive lineare Regression

Das monatliche Beschwerdevolumen wird gegen einen fortlaufenden Monatsindex regressiert.

Die Regression liefert:

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

Die Regression dient ausschließlich als **deskriptiver Trendindikator**.

Sie ist kein Prognosemodell.

---

# 27. Motivation der Sensitivitätsanalyse

Die EDA zeigt eine sehr starke Konzentration des Portfolios auf Credit Reporting.

Der Segmentanteil steigt von:

```text
75,3 % im Jahr 2022
```

auf:

```text
88,4 % im Jahr 2025
```

Damit besteht das Risiko, dass aggregierte Portfolio-Kennzahlen überwiegend die Entwicklung dieses einen Segments widerspiegeln.

Deshalb wird eine zusätzliche Segment-Sensitivitätsanalyse durchgeführt.

---

# 28. Segment-Jahresanalyse

Die jährliche Sensitivitätstabelle enthält:

```text
total_complaints
focus_product_complaints
without_focus_product
focus_product_share
```

Fokussegment:

```text
Credit reporting or other personal consumer reports
```

Ausgabe:

```text
reports/segment_sensitivity_yearly.csv
```

---

# 29. Wachstum ohne Credit Reporting

Das Restportfolio entwickelt sich von:

```text
197.553 Beschwerden im Jahr 2022
```

auf:

```text
632.673 Beschwerden im Jahr 2025
```

Dies entspricht:

```text
+220,3 %
```

Damit besteht erhebliches Wachstum auch außerhalb von Credit Reporting.

Das Gesamtwachstum wird jedoch stark durch das dominante Segment verstärkt.

---

# 30. Trend-Sensitivität

Gesamtportfolio:

```text
monthly_slope ≈ 10.511
R² ≈ 0,877
```

Portfolio ohne Credit Reporting:

```text
monthly_slope ≈ 925
R² ≈ 0,583
```

Die Differenz der beiden linearen Steigungen beträgt rund:

```text
9.586 Beschwerden pro Monat
```

Rechnerisch entspricht dies etwa:

```text
91,2 %
```

der Steigung des linearen Gesamttrends.

Diese Kennzahl beschreibt die Zerlegung der beobachteten linearen Trendsteigung.

Sie ist keine kausale Attribution.

---

# 31. Korrelations-Sensitivität

Die monatlichen Korrelationen werden sowohl für:

```text
Gesamtportfolio
```

als auch für:

```text
Portfolio ohne Credit Reporting
```

berechnet.

Beispiel Beschwerdevolumen versus Narrative-Anteil:

```text
Gesamtportfolio:
Pearson r = -0,891

ohne Credit Reporting:
Pearson r = -0,227
```

Beispiel Beschwerdevolumen versus Timely-Response-Rate:

```text
Gesamtportfolio:
Pearson r = +0,343

ohne Credit Reporting:
Pearson r = -0,297
```

Die Richtung des linearen Zusammenhangs wechselt damit bei der zweiten Beziehung.

---

# 32. Interpretation des Kompositionseffekts

Die Sensitivitätsanalyse zeigt, dass aggregierte Portfolio-Kennzahlen erheblich vom Produktmix beeinflusst werden.

Dies wird als:

```text
Segment- beziehungsweise Kompositionseffekt
```

interpretiert.

Das Projekt klassifiziert den Befund bewusst nicht automatisch als:

```text
Simpson-Paradox
```

Für eine solche Einordnung wäre eine systematischere Stratifizierung und Prüfung der zugrunde liegenden Gruppenbeziehungen erforderlich.

Die praktische Schlussfolgerung lautet daher:

**Portfolio-Aggregate sollten durch segmentierte Analysen ergänzt werden, bevor operative, kausale oder risikobezogene Aussagen abgeleitet werden.**

---

# 33. Produktmix und Aggregation

Der Sensitivitätscheck dient zugleich als methodische Kontrolle der ursprünglichen Korrelationsanalyse.

Eine starke Korrelation im Gesamtportfolio kann entstehen oder verstärkt werden, wenn sich gleichzeitig:

- Segmentanteile,
- Segmentvolumina,
- segmentspezifische Kennzahlen

verändern.

Damit wird verhindert, dass ein mathematisch starkes Aggregatergebnis automatisch als ebenso starker fachlicher Zusammenhang interpretiert wird.

---

# 34. Visualisierung

Die statische Visualisierung verwendet:

- Matplotlib,
- Seaborn.

Erzeugt werden:

```text
01_monthly_complaints.png
02_product_mix.png
03_timely_response_by_product.png
04_issue_hotspots.png
05_product_year_heatmap.png
06_credit_reporting_sensitivity.png
```

---

# 35. Monatsentwicklung

Die Monatsgrafik zeigt:

- monatliche Beschwerden,
- vollständigen rollierenden 12-Monats-Durchschnitt.

Die Zeitachse wird auf den tatsächlichen Analysezeitraum begrenzt.

Dadurch werden keine Ticks außerhalb des Datenfensters angezeigt.

---

# 36. Produktmix

Die Produktmix-Grafik zeigt exakt die zehn volumenstärksten Produktgruppen.

Unbenutzte Categorical Levels werden vor der Visualisierung entfernt.

Dadurch können keine zusätzlichen leeren oder nicht ausgewählten Kategorien erscheinen.

Absolute Beschwerdezahlen werden direkt dargestellt.

---

# 37. Timely-Response-Dot-Plot

Die zehn volumenstärksten Produktgruppen werden anschließend nach ihrer Timely-Response-Rate sortiert.

Die Darstellung erfolgt als Dot-Plot.

Zusätzlich wird der beschwerdegewichtete Portfolio-Durchschnitt als Referenz dargestellt.

Damit bleiben Unterschiede in einem insgesamt sehr hohen Prozentbereich sichtbar.

---

# 38. Hotspot-Visualisierung

Die 15 volumenstärksten Produkt-Issue-Kombinationen werden dargestellt.

Lange Produktbezeichnungen können ausschließlich für die Darstellung verkürzt werden.

Lange Issue-Bezeichnungen werden umgebrochen.

Die zugrunde liegenden Datenwerte bleiben unverändert.

---

# 39. Produkt-Jahres-Heatmap

Die Produkt-Jahres-Matrix enthält absolute Beschwerdezahlen.

Aufgrund der großen Größenunterschiede zwischen Produktgruppen wird die Farbintensität logarithmisch skaliert.

Dabei gilt:

```text
Farbe = logarithmische Skala
Zellwert = absolute Beschwerdezahl
```

Dadurch bleiben sowohl große als auch kleinere Kategorien sichtbar.

---

# 40. Sensitivitätsgrafik

Die sechste Grafik vergleicht:

```text
Gesamtportfolio
Credit Reporting
Portfolio ohne Credit Reporting
```

für die Jahre 2022 bis 2025.

Zusätzlich wird der jährliche Credit-Reporting-Anteil annotiert.

Damit wird die zunehmende Portfolio-Konzentration direkt sichtbar.

---

# 41. Interaktives Dashboard

Zusätzlich wird erzeugt:

```text
reports/interactive_dashboard.html
```

Das Dashboard enthält:

- monatliche Zeitreihe,
- Produktvergleich,
- Segment-Sensitivitätsanalyse.

Es dient der Exploration und ersetzt keine dokumentierte methodische Interpretation.

---

# 42. Management Summary

Die wichtigsten Ergebnisse werden automatisch in:

```text
reports/executive_summary.md
```

zusammengeführt.

Die Summary verbindet:

- Datenqualität,
- Datenbereinigung,
- Taxonomie-Harmonisierung,
- zentrale analytische Ergebnisse,
- statistische Zusammenhänge,
- Sensitivitätsanalyse,
- Banking- und Finance-Relevanz,
- methodische Übertragbarkeit auf Versicherungen,
- Technical-AI-Consulting-Perspektive,
- Folgeschritte,
- Interpretationsgrenzen.

---

# 43. Reproduzierbarkeit und Tests

Die Implementierung wird mit pytest getestet.

Aktueller Umfang:

```text
24 Tests
```

Normales Quality Gate:

```bash
pytest -q
```

Zusätzlich:

```bash
pytest -q -W error
```

Damit führen auch Python-Warnungen zum Fehlschlag der Testsuite.

Ruff prüft Codequalität:

```bash
ruff check .
```

Aktueller Stand:

```text
24 passed
24 passed mit -W error
Ruff: All checks passed
```

---

# 44. Regressionstests

Neben grundlegenden Funktionstests enthält das Projekt gezielte Regressionstests für bereits identifizierte Fehlerklassen.

Dazu gehören:

- Categorical-Textverarbeitung in Issue-Hotspots,
- PyArrow-basierte numerische Werte in Heatmaps,
- vollständiges Rolling Window,
- Top-N-Auswahl ohne unbenutzte Categorical Levels,
- Timely-Response-Visualisierung mit kategorischen Produktdimensionen.

Dadurch werden konkrete Fehler nicht nur einmal behoben, sondern gegen zukünftige Regression abgesichert.

---

# 45. Interpretation

Die Methodik dient der:

- explorativen Analyse,
- Priorisierung,
- Hypothesengenerierung,
- Identifikation möglicher Root-Cause-Untersuchungen,
- Prüfung von Segment- und Kompositionseffekten,
- datenbasierten Entscheidungsunterstützung.

Sie dient nicht der ungeprüften:

- Kausalitätsbehauptung,
- regulatorischen Bewertung,
- Unternehmensrangliste,
- Zukunftsprognose,
- Klassifikation eines Aggregationseffekts als Simpson-Paradox.

Diese Grenzen sind Bestandteil der Methodik und nicht nur ein nachträglicher Disclaimer.
