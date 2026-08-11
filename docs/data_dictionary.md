# Datenwörterbuch

Dieses Dokument beschreibt die für die Consumer Finance Complaint Intelligence Platform verwendeten CFPB-Quellfelder sowie die daraus erzeugten analytischen Felder.

Die offizielle CFPB-Dokumentation bleibt maßgeblich für die fachliche Bedeutung der ursprünglichen Source-Felder.

Das Projekt verändert die ursprünglichen Werte nicht, sondern erzeugt bei Bedarf zusätzliche analytische Felder.

---

# Verwendete Quellfelder

| Projektfeld | CFPB-Quellfeld | Analytischer Typ | Bedeutung |
|---|---|---|---|
| `complaint_id` | `Complaint ID` | String | Eindeutige Kennung einer veröffentlichten Beschwerde |
| `date_received` | `Date received` | Datum | Datum, an dem das CFPB die Beschwerde erhalten hat |
| `product` | `Product` | Kategorie | Ursprüngliche veröffentlichte Produktklassifikation |
| `sub_product` | `Sub-product` | Kategorie / nullable | Detailliertere Produktklassifikation, sofern vorhanden |
| `issue` | `Issue` | Kategorie / nullable | Ursprüngliche veröffentlichte Issue-Klassifikation |
| `consumer_narrative` | `Consumer complaint narrative` | Text / nullable | Veröffentlichter Beschwerdetext, sofern vorhanden; wird nur zur Ableitung von `has_narrative` benötigt |
| `company` | `Company` | Kategorie | Unternehmen, auf das sich die Beschwerde bezieht |
| `state` | `State` | Kategorie / nullable | Veröffentlichter US-Bundesstaat, sofern vorhanden |
| `submitted_via` | `Submitted via` | Kategorie | Kanal, über den die Beschwerde eingereicht wurde |
| `date_sent_to_company` | `Date sent to company` | Datum | Datum der Weiterleitung durch das CFPB an das Unternehmen |
| `company_response` | `Company response to consumer` | Kategorie | Veröffentlichte Response-Kategorie des Unternehmens |
| `timely_response` | `Timely response?` | Kategorie | Kennzeichnet, ob die Unternehmensantwort vom CFPB als rechtzeitig geführt wird |

---

# Felder der verarbeiteten Parquet-Datenebene

Die Datei:

```text
data/processed/complaints_analytics.parquet
```

enthält folgende Felder.

| Feld | Typ / Rolle | Beschreibung |
|---|---|---|
| `complaint_id` | String | Eindeutige Complaint ID |
| `date_received` | Datum | Eingang der Beschwerde beim CFPB |
| `year` | Integer | Kalenderjahr von `date_received` |
| `month` | Integer | Kalendermonat von `date_received` |
| `year_month` | Datum | Auf Monatsbeginn normalisierte Zeitvariable |
| `quarter` | String | Quartal im Format `YYYY-Qn` |
| `taxonomy_version` | Kategorie | Kennzeichnet die für das Projekt relevante Taxonomiephase |
| `product` | Kategorie | Ursprünglicher CFPB-Produktwert |
| `sub_product` | Kategorie / nullable | Ursprünglicher CFPB-Sub-Product-Wert |
| `issue` | Kategorie / nullable | Ursprünglicher CFPB-Issue-Wert |
| `harmonized_product` | Kategorie | Für Längsschnittanalysen harmonisierte Produktklassifikation |
| `harmonized_issue` | Kategorie | Bereinigte und für Längsschnittanalysen harmonisierte Issue-Klassifikation |
| `company` | Kategorie | Unternehmen der Beschwerde |
| `state` | Kategorie / nullable | Veröffentlichter US-Bundesstaat |
| `submitted_via` | Kategorie | Einreichungskanal |
| `date_sent_to_company` | Datum | Datum der Weiterleitung an das Unternehmen |
| `days_to_company` | Integer | Kalendertage zwischen Eingang und Weiterleitung |
| `company_response` | Kategorie | Response-Kategorie des Unternehmens |
| `timely_response` | Kategorie | Ursprünglicher Wert aus `Timely response?` |
| `is_timely` | Boolean | Boolesche Ableitung von `timely_response == "Yes"` |
| `has_narrative` | Boolean | Kennzeichnet, ob ein nicht leerer Consumer Narrative vorhanden war |

---

# Abgeleitete Zeitfelder

## `year`

Kalenderjahr des Beschwerdeeingangs.

Ableitung:

```text
year(date_received)
```

Beispiel:

```text
2025
```

---

## `month`

Kalendermonat des Beschwerdeeingangs.

Wertebereich:

```text
1 bis 12
```

---

## `year_month`

Auf den ersten Tag des jeweiligen Monats normalisierte Zeitvariable.

Sie wird für monatliche Zeitreihen und Gruppierungen verwendet.

Beispiel:

```text
2025-04-01
```

steht für April 2025.

---

## `quarter`

Kalenderquartal des Beschwerdeeingangs.

Beispiel:

```text
2025-Q3
```

---

# Prozessbezogene Felder

## `days_to_company`

Kalendertage zwischen:

```text
date_received
```

und:

```text
date_sent_to_company
```

Berechnung:

```text
date_sent_to_company - date_received
```

Negative Werte werden durch die automatisierte Datenqualitätsprüfung als Fehlerzustand behandelt.

---

## `timely_response`

Unveränderter veröffentlichter CFPB-Wert aus:

```text
Timely response?
```

Erwartete Werte:

```text
Yes
No
```

Weitere Werte werden durch die Datenqualitätsprüfung gemeldet.

---

## `is_timely`

Boolesches Analysefeld.

Definition:

```text
timely_response == "Yes"
```

Damit lassen sich Timely-Response-Raten direkt über Mittelwerte berechnen.

---

# Narrative-Feld

## `has_narrative`

Boolesches Feld, das angibt, ob ein nicht leerer veröffentlichter Consumer Narrative vorliegt.

Definition:

```text
Consumer complaint narrative != null
und
Textlänge > 0
```

Der vollständige Narrative-Text wird **nicht** in die aktuelle Parquet-Analyseschicht übernommen.

Grund:

Die Narrative-Texte können sehr lang sein und würden die Multi-Millionen-Zeilen-Analyseschicht erheblich vergrößern.

Für Modul 1 wird lediglich untersucht, ob ein Narrative vorhanden ist.

Der vollständige Text bleibt im unveränderten Rohdatensatz verfügbar und kann in einem späteren NLP-Projekt erneut eingelesen werden.

---

# Originalklassifikation und harmonisierte Klassifikation

## `product`

Enthält die ursprünglich veröffentlichte CFPB-Produktbezeichnung.

Dieser Wert wird nicht überschrieben.

---

## `harmonized_product`

Zusätzliche analytische Produktklassifikation.

Sie wird verwendet, wenn dokumentierte historische CFPB-Taxonomieänderungen ansonsten dazu führen würden, dass fachlich zusammengehörige Kategorien in Zeitvergleichen getrennt erscheinen.

Die Originalklassifikation bleibt parallel erhalten.

---

## `issue`

Enthält den ursprünglichen CFPB-Issue-Wert.

Dieses Feld kann in wenigen Source-Datensätzen fehlen.

Ein fehlender Originalwert bleibt:

```text
null
```

---

## `harmonized_issue`

Analytisches Issue-Feld.

Es erfüllt zwei Funktionen:

1. dokumentierte historische Issue-Bezeichnungen für Längsschnittanalysen zu harmonisieren,
2. fehlende Source-Issue-Werte analytisch sichtbar zu repräsentieren.

Wenn kein Source-Issue vorhanden ist:

```text
issue = null
```

wird analytisch:

```text
harmonized_issue = "Issue not provided"
```

verwendet.

Der ursprüngliche Missing Value bleibt trotzdem im Feld `issue` erhalten.

---

# `taxonomy_version`

Dieses Feld kennzeichnet die für die Projektlogik relevante historische Taxonomiephase.

Aktuelle Werte:

```text
pre_aug_2023
aug_2023_or_later
```

Der verwendete Trennzeitpunkt ist:

```text
2023-08-24
```

Das Feld dient der Nachvollziehbarkeit der historischen Klassifikationsänderung.

---

# Taxonomie-Audit

Die Zuordnung zwischen ursprünglichen und harmonisierten Werten wird zusätzlich gespeichert:

```text
reports/taxonomy_harmonization_audit.csv
```

Der Audit enthält:

| Feld | Bedeutung |
|---|---|
| `dimension` | Gibt an, ob Produkt oder Issue auditiert wird |
| `context_product` | Harmonisiertes Produkt als Kontext für Issue-Mappings |
| `source_value` | Ursprünglicher Source-Wert |
| `harmonized_value` | Verwendeter analytischer Wert |
| `complaints` | Anzahl betroffener Beschwerden |
| `changed` | Kennzeichnet eine Abweichung zwischen Source und analytischem Wert |
| `change_type` | Unterscheidet Taxonomie-Harmonisierung und Missing-Value-Behandlung |

Mögliche `change_type`-Werte:

```text
unchanged
taxonomy_harmonization
missing_value_handling
```

---

# Felder der Analyseebene

`scripts/run_analysis.py` lädt bewusst nicht sämtliche Parquet-Spalten.

Für die aktuelle EDA werden nur die für die Berechnungen benötigten Felder projiziert.

Dies reduziert den Arbeitsspeicherbedarf bei mehr als zehn Millionen Zeilen.

Die Analyse verwendet insbesondere:

```text
complaint_id
date_received
product
issue
harmonized_product
harmonized_issue
taxonomy_version
company
date_sent_to_company
company_response
timely_response
year
year_month
days_to_company
has_narrative
is_timely
```

Felder wie `state`, `submitted_via`, `sub_product`, `month` und `quarter` bleiben dennoch in der verarbeiteten Parquet-Datenebene für mögliche weiterführende Explorationen verfügbar.

---

# Umgang mit Datentypen

Die Transformation verwendet Polars-Datentypen.

Die Analyseebene lädt Parquet über PyArrow-gestützte Pandas-Datentypen.

Wiederkehrende Textdimensionen werden anschließend als Pandas-Kategorien gespeichert, unter anderem:

```text
product
issue
harmonized_product
harmonized_issue
taxonomy_version
company
company_response
timely_response
```

Diese Entscheidung reduziert den Speicherbedarf gegenüber einer reinen Python-Object-Repräsentation.

---

# Grundprinzip

Das Datenmodell unterscheidet konsequent zwischen:

```text
Source Truth
```

und:

```text
Analytical Representation
```

Das bedeutet:

- Source-Werte werden nicht stillschweigend überschrieben,
- Cleaning-Schritte werden sichtbar gemacht,
- Taxonomieänderungen werden separat dokumentiert,
- analytische Ableitungen bleiben reproduzierbar.

Diese Trennung ist zentral für Auditierbarkeit und verantwortungsvolle Interpretation.
