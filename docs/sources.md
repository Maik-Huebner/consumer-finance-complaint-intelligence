# Quellen und Datenprovenienz

Stand der Quellenprüfung für dieses Portfolio-Projekt: **11.08.2026**

## Primäre Datenquelle

**U.S. Consumer Financial Protection Bureau (CFPB) – Consumer Complaint Database**

Offizielle Quellen:

- Consumer Complaint Database: https://www.consumerfinance.gov/data-research/consumer-complaints/
- Bulk-Datensatz als CSV-ZIP: https://files.consumerfinance.gov/ccdb/complaints.csv.zip
- API-Dokumentation: https://cfpb.github.io/api/ccdb/
- Feldreferenz: https://cfpb.github.io/api/ccdb/fields.html

Die Consumer Complaint Database enthält veröffentlichte Beschwerden zu Finanzprodukten und Finanzdienstleistungen, die an Unternehmen zur Bearbeitung weitergeleitet wurden.

Der CFPB stellt die veröffentlichten Beschwerdedaten öffentlich zur Verfügung und erlaubt deren Nutzung, Analyse und Weiterverarbeitung.

Die Datenbank wird nach Angaben des CFPB grundsätzlich täglich aktualisiert.

## Verwendeter Analysezeitraum

Für das Portfolio-Projekt werden ausschließlich vollständige Kalenderjahre verwendet:

```text
2022-01-01 bis 2025-12-31
```

Der veröffentlichte Analysebestand umfasst:

```text
10.269.540 Beschwerden
```

Der genaue lokale Quelldaten-Snapshot des veröffentlichten Projektstands ist dokumentiert unter:

```text
reports/source_snapshot.json
```

Dort werden unter anderem festgehalten:

- Datenquelle,
- Downloadzeitpunkt,
- Dateigrößen,
- SHA-256-Prüfsumme,
- Analysezeitraum,
- analysierte Zeilenzahl,
- Data-Quality-Status.

## Methodische Einschränkungen der Quelle

Die Interpretation im Projekt folgt ausdrücklich den Hinweisen des CFPB.

### Keine repräsentative Stichprobe

Die Consumer Complaint Database ist keine statistisch repräsentative Stichprobe sämtlicher Kundenerfahrungen.

Veröffentlichte Beschwerden dürfen deshalb nicht ohne weitere Kontextinformationen auf die Gesamtheit aller Kunden eines Unternehmens oder Produkts übertragen werden.

### Beschwerdevolumen benötigt Bezugsgrößen

Ein hohes Beschwerdevolumen bedeutet nicht automatisch eine schlechte Unternehmens- oder Produktqualität.

Bei Unternehmens- und Produktvergleichen sollten unter anderem berücksichtigt werden:

- Unternehmensgröße,
- Kundenanzahl,
- Marktanteil,
- Produktbestand,
- Konten oder Verträge,
- Nutzung beziehungsweise Exposure.

Diese Bezugsgrößen stehen im verwendeten CFPB-Datensatz nicht vollständig zur Verfügung.

Unternehmensbezogene Kennzahlen werden deshalb im Projekt ausschließlich als explorative Screening-Signale interpretiert und nicht als faire Performance-Rangliste.

### Geografische Vergleiche benötigen Kontext

Geografisches Beschwerdevolumen sollte mit geeigneten Bezugsgrößen wie der Bevölkerung oder anderen Exposure-Daten kombiniert werden.

Aus diesem Grund stehen geografische Rankings nicht im Mittelpunkt der aktuellen EDA.

### Aktuelle Daten können unvollständig sein

Neue Beschwerden werden nicht zwangsläufig unmittelbar vollständig veröffentlicht.

Unternehmen erhalten Zeit zur Reaktion, und bei freigegebenen Consumer Narratives müssen zusätzlich Maßnahmen zur Entfernung personenbezogener Informationen durchgeführt werden.

Das Projekt verwendet deshalb ausschließlich vollständige Kalenderjahre bis einschließlich 2025.

### Consumer Narratives

Consumer Narratives sind Beschreibungen der Verbraucher selbst.

Sie werden nur veröffentlicht, wenn der Verbraucher einer Veröffentlichung zugestimmt hat und nachdem der CFPB Maßnahmen zur Entfernung personenbezogener Informationen vorgenommen hat.

Der CFPB verifiziert die beschriebenen Erfahrungen nicht unabhängig.

Im aktuellen Modul-1-Projekt werden Narrative deshalb nicht inhaltlich analysiert.

Es wird lediglich die analytische Kennzahl:

```text
has_narrative
```

abgeleitet.

Eine semantische oder NLP-basierte Analyse ist ausdrücklich eine mögliche spätere Erweiterung.

## Historische Taxonomieänderungen

Der CFPB dokumentiert historische Änderungen an:

- Produkten,
- Sub-Produkten,
- Issues,
- Sub-Issues.

Die Quelldaten speichern die ursprüngliche Klassifikation, die zum Zeitpunkt der jeweiligen Beschwerde verfügbar war.

Dadurch können historische Taxonomieänderungen Längsschnittanalysen beeinflussen.

Das Projekt behandelt dieses Problem ausdrücklich durch zusätzliche analytische Felder:

```text
taxonomy_version
harmonized_product
harmonized_issue
```

Die ursprünglichen Felder:

```text
product
sub_product
issue
```

bleiben unverändert erhalten.

Alle angewendeten Harmonisierungsschritte werden auditierbar dokumentiert unter:

```text
reports/taxonomy_harmonization_audit.csv
reports/taxonomy_harmonization_summary.json
```

## Verantwortungsvolle Interpretation

Das Projekt verwendet die CFPB-Daten als explorative externe Signaldaten.

Es wird ausdrücklich nicht behauptet, dass:

- veröffentlichte Beschwerden alle Kundenerfahrungen repräsentieren,
- hohe Beschwerdezahlen automatisch schlechte Unternehmensleistung bedeuten,
- Korrelationen kausale Zusammenhänge beweisen,
- Unternehmensvergleiche ohne Exposure-Nenner fair sind,
- externe Beschwerdedaten allein regulatorische oder operative Entscheidungen rechtfertigen.

Für institutionelle Anwendungen sollten die öffentlichen CFPB-Daten mit internen und externen Bezugsdaten ergänzt werden, beispielsweise:

- Kundenbeständen,
- Konten und Verträgen,
- Transaktionsvolumen,
- Marktanteilen,
- Service-KPIs,
- Prozessdaten,
- Incident-Daten,
- Customer-Outcome-Kennzahlen.
