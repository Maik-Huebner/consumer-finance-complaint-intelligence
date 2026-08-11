# Management Summary

## Analyseumfang

Diese Analyse untersucht veröffentlichte Verbraucherbeschwerden des U.S. Consumer Financial Protection Bureau (CFPB) für die vollständigen Kalenderjahre **2022 bis 2025**.

Die Pipeline bewahrt die ursprünglichen CFPB-Klassifikationen und ergänzt separate bereinigte beziehungsweise harmonisierte Analysefelder. Dadurch bleiben historische Quelldaten nachvollziehbar, während gleichzeitig konsistentere Zeitvergleiche ermöglicht werden.

## Zentrale Ergebnisse

- Das veröffentlichte Beschwerdevolumen veränderte sich von **800.245** Beschwerden im Jahr 2022 auf **5.442.977** im Jahr 2025. Dies entspricht einer Veränderung von **580,2%** über den betrachteten Zeitraum.
- Die größte harmonisierte Produktkategorie ist **Credit reporting or other personal consumer reports** mit einem Anteil von **85,9%** an allen Beschwerden im Analysezeitraum.
- Der volumenstärkste harmonisierte Produkt-Issue-Hotspot ist **Credit reporting or other personal consumer reports — Incorrect information on your report** mit **4.653.591** Beschwerden.
- Der deskriptive lineare Zeittrend entspricht durchschnittlich rund **10.511 zusätzlichen Beschwerden pro Monat** bei **R²=0,877**. Dieser Wert beschreibt ausschließlich den beobachteten Zeitraum und stellt keine Prognose dar.
- Zwischen monatlichem Beschwerdevolumen und Timely-Response-Rate ergibt sich eine Pearson-Korrelation von **r=0,343** und eine Spearman-Rangkorrelation von **ρ=0,519**. Der Zusammenhang ist rein deskriptiv und erlaubt keine kausale Interpretation.
- Zwischen monatlichem Beschwerdevolumen und Narrative-Anteil ergibt sich eine Pearson-Korrelation von **r=-0,891** und eine Spearman-Rangkorrelation von **ρ=-0,914**. Der Zusammenhang ist deskriptiv und kann wesentlich durch Veränderungen des Produktmixes beeinflusst sein.

## Sensitivitätsanalyse: Einfluss des dominanten Credit-Reporting-Segments

Die Gesamtanalyse wird stark durch **Credit reporting or other personal consumer reports** geprägt. Deshalb wurde zusätzlich geprüft, wie sich zentrale Ergebnisse verändern, wenn dieses dominante Segment aus der Aggregation entfernt wird.

- Der Anteil des Credit-Reporting-Segments steigt von **75,3%** im Jahr 2022 auf **88,4%** im Jahr 2025. Das entspricht einer Verschiebung um **13,1 Prozentpunkte**.
- Auch ohne Credit Reporting steigt das veröffentlichte Beschwerdevolumen deutlich: von **197.553** auf **632.673** Beschwerden beziehungsweise um **220,3%**.
- Die Steigung des einfachen linearen Monatstrends sinkt jedoch von rund **10.511** Beschwerden pro Monat im Gesamtportfolio auf rund **925** ohne Credit Reporting.
- Rechnerisch entfallen damit rund **91,2%** der Steigung des linearen Gesamttrends auf den Credit-Reporting-Anteil der monatlichen Beschwerdereihe.
- Die Pearson-Korrelation zwischen monatlichem Beschwerdevolumen und Narrative-Anteil verändert sich von **r=-0,891** im Gesamtportfolio auf **r=-0,227** ohne Credit Reporting.
- Die Pearson-Korrelation zwischen Beschwerdevolumen und Timely-Response-Rate verändert sich von **r=0,343** auf **r=-0,297** und wechselt damit in dieser Sensitivitätsanalyse die Richtung.

Die Ergebnisse zeigen, dass die aggregierten Portfolio-Kennzahlen erheblich durch den Produktmix beeinflusst werden. Das starke Gesamtwachstum verschwindet ohne Credit Reporting nicht, fällt aber wesentlich schwächer aus. Gleichzeitig verändern sich die aggregierten Korrelationsstrukturen deutlich.

Die Analyse wird bewusst **nicht vorschnell als Simpson-Paradox klassifiziert**. Sie zeigt jedoch einen klaren Segment- beziehungsweise Kompositionseffekt und unterstreicht, dass Portfolio-Aggregate ohne Segmentkontrolle nicht isoliert interpretiert werden sollten.

Für Management- und Consulting-Entscheidungen bedeutet dies: Gesamtportfolio-KPIs sollten durch segmentierte Analysen ergänzt werden, bevor Ursachen, operative Risiken oder Customer Outcomes abgeleitet werden.

## Datenaufbereitung und Datenbereinigung

Die analytische Datenbasis wird vor der Interpretation explizit validiert und bereinigt. Unvollständige Datensätze werden nicht stillschweigend entfernt.

- Im Rohdatensatz fehlen bei **6** Beschwerden veröffentlichte Issue-Werte. Dies entspricht **0,00006%** des analysierten Datenbestands.
- Für **6** dieser Datensätze wird in der analytischen Klassifikation der explizite Wert `Issue not provided` verwendet.
- Das ursprüngliche CFPB-Feld `issue` bleibt bei diesen Datensätzen unverändert leer. Dadurch bleibt die Datenherkunft nachvollziehbar.
- **0** Datensätze mit fehlendem Source-Issue sind analytisch unbehandelt.
- Complaint IDs, Datumslogik, Response-Werte, Taxonomieversionen und Vollständigkeit der analytischen Klassifikation werden automatisiert kontrolliert.

Keine Beschwerde wird ausschließlich aufgrund eines fehlenden Issue-Werts aus der Analyse entfernt.

## Taxonomie-Harmonisierung

Historische CFPB-Produkt- und Issue-Bezeichnungen bleiben vollständig erhalten. Für Längsschnittanalysen werden zusätzliche harmonisierte Felder verwendet.

- **1.335.250** Beschwerden beziehungsweise **13,0%** erhalten für die Analyse eine Produktklassifikation, die vom ursprünglichen veröffentlichten Produktwert abweicht.
- **333.083** Beschwerden beziehungsweise **3,2%** erhalten eine harmonisierte Issue-Klassifikation.
- Insgesamt sind **1.335.251** Datensätze beziehungsweise **13,0%** von mindestens einer Taxonomie-Harmonisierung betroffen.
- Missing-Value-Behandlung wird getrennt von Taxonomieänderungen ausgewiesen.
- Die vollständige Source-to-Analytical-Zuordnung ist in `taxonomy_harmonization_audit.csv` dokumentiert.

Diese Trennung reduziert das Risiko, reine Änderungen der Quellklassifikation fälschlicherweise als wirtschaftliche oder operative Veränderungen zu interpretieren.

## Relevanz für Banking und Finanzdienstleistungen

Die Analyse zeigt, wie große externe Beschwerdedatensätze für eine strukturierte Identifikation von Auffälligkeiten und Untersuchungsschwerpunkten genutzt werden können.

Mögliche fachliche Fragestellungen sind:

- Welche Produkte und Prozesse konzentrieren besonders viele Beschwerden?
- Welche Issue-Kombinationen sollten für Root-Cause-Analysen priorisiert werden?
- Welche zeitlichen Veränderungen sind analytisch relevant und welche entstehen möglicherweise nur durch Taxonomieänderungen?
- Welche extern sichtbaren Signale sollten mit internen Kunden-, Produkt-, Prozess- oder Risikoindikatoren verbunden werden?
- Wo könnten Conduct-Risk-, Customer-Outcome- oder Operational-Risk-Untersuchungen sinnvoll sein?

## Relevanz für Versicherungen

Die CFPB-Daten betreffen primär Finanzprodukte und nicht klassische Versicherungsbeschwerden.

Die entwickelte Methodik ist jedoch direkt auf Versicherungsdaten übertragbar, zum Beispiel auf:

- Kundenbeschwerden,
- Schadenbearbeitung,
- Leistungsfälle,
- Policenverwaltung,
- Vertragsänderungen,
- Kontaktgründe,
- Bearbeitungszeiten,
- Ombudsmann- und Beschwerdestellen-Daten.

Insbesondere Datenbereinigung, Taxonomie-Harmonisierung, Quality Gates, Hotspot-Analyse, Zeitreihenanalyse und Management-Reporting sind branchenübergreifend einsetzbar.

## Relevanz für Technical AI Consulting

Das Projekt demonstriert einen vollständigen analytischen Problemlösungsprozess von der fachlichen Fragestellung bis zur reproduzierbaren Management-Ausgabe.

Dabei werden insbesondere folgende Fähigkeiten sichtbar:

- Übersetzung eines Business-Problems in einen Datenprozess,
- Verarbeitung eines realen Multi-Millionen-Zeilen-Datensatzes,
- reproduzierbare Datenaufnahme,
- nachvollziehbare Datenprovenienz,
- transparente Datenbereinigung,
- kontrollierter Umgang mit Taxonomieänderungen,
- automatisierte Datenqualitätskontrollen,
- explorative und statistische Analyse,
- Segment- und Sensitivitätsanalysen,
- adressatengerechtes Reporting,
- Ableitung sinnvoller nächster Untersuchungsschritte.

## Empfohlene Consulting-Folgeschritte

1. Hochvolumige und stark wachsende Produkt-Issue-Hotspots mit internen Kunden-, Vertrags-, Konto-, Transaktions- oder Marktanteilsdaten normalisieren.
2. Auffällige Timely-Response-Werte als Ausgangspunkt für operative Prozessanalysen verwenden und nicht als isolierte Unternehmensbewertung.
3. Beschwerdekategorien mit Service-Incidents, Kontaktgründen, Prozessverantwortung, Remediation-Maßnahmen und Customer-Outcome-Kennzahlen verbinden.
4. Für priorisierte Hotspots qualitative Analysen oder NLP-Verfahren auf Consumer Narratives einsetzen, um wiederkehrende Ursachen und Themen zu identifizieren.
5. Wiederkehrendes Monitoring mit kontrollierten Datensnapshots, Data-Quality-Gates und Taxonomy-Drift-Prüfungen aufbauen.
6. In regulierten Finanzunternehmen Beschwerdeindikatoren in bestehende Conduct-Risk-, Operational-Risk-, Customer-Outcome- und Governance-Prozesse einbetten.

## Datenqualitätsstatus

Die automatisierte strukturelle Datenqualitätsprüfung wurde **bestanden**.

Detaillierte Ergebnisse befinden sich in:

- `data_quality_report.json`
- `data_cleaning_summary.json`
- `taxonomy_harmonization_summary.json`
- `taxonomy_harmonization_audit.csv`
- `segment_sensitivity_summary.json`
- `segment_sensitivity_yearly.csv`

## Grenzen der Interpretation

Die CFPB Consumer Complaint Database ist keine repräsentative Stichprobe aller Kundenerfahrungen.

Rohes Beschwerdevolumen ist insbesondere nicht bereinigt um:

- Unternehmensgröße,
- Kundenanzahl,
- Marktanteil,
- Anzahl Konten oder Verträge,
- Produktnutzung,
- Transaktionsvolumen,
- unterschiedliche Beschwerdewahrscheinlichkeiten.

Unternehmensbezogene Kennzahlen sind deshalb explorative Screening-Indikatoren und keine Performance-Rangliste.

Korrelationen und der lineare Zeittrend sind rein deskriptiv. Sie beweisen keine kausalen Zusammenhänge und stellen keine Prognosemodelle dar.

Die Sensitivitätsanalyse zeigt zusätzlich, dass aggregierte Beziehungen deutlich vom Produktmix abhängen können. Portfolio-Kennzahlen sollten deshalb nicht ohne Segmentkontrolle interpretiert werden.

Die Analyse dient der **explorativen Priorisierung, Hypothesengenerierung, risikoorientierten Untersuchung und datenbasierten Entscheidungsunterstützung**.
