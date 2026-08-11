# Grenzen der Analyse und verantwortungsvolle Interpretation

Eine belastbare Exploratory Data Analysis beschreibt nicht nur, was sich aus Daten erkennen lässt, sondern ebenso klar, **was die Daten nicht beweisen können**.

Die folgenden Einschränkungen sind deshalb Bestandteil des analytischen Designs.

---

# Keine repräsentative Stichprobe

Die CFPB Consumer Complaint Database ist keine statistisch repräsentative Stichprobe aller Kundenerfahrungen.

Nicht jeder Kunde reicht bei einem Problem eine CFPB-Beschwerde ein.

Die Wahrscheinlichkeit einer Beschwerde kann unter anderem beeinflusst werden durch:

- Bekanntheit des CFPB,
- individuelle Beschwerdebereitschaft,
- Art und Schwere eines Problems,
- Produktgruppe,
- Kommunikationskanäle,
- externe Dienstleister,
- technische Einreichungsmöglichkeiten.

Die Anzahl veröffentlichter Beschwerden darf deshalb nicht mit der tatsächlichen Anzahl unzufriedener Kunden gleichgesetzt werden.

---

# Fehlende Exposure-Nenner

Der öffentliche Datensatz enthält keine vollständigen Bezugsgrößen für faire Unternehmensvergleiche.

Es fehlen insbesondere institutionenübergreifend vergleichbare Informationen wie:

- Anzahl Kunden,
- Anzahl Konten,
- Anzahl Verträge,
- Kreditvolumen,
- Transaktionsanzahl,
- Marktanteil,
- Produktbestand.

Ein großes Institut kann allein aufgrund seiner größeren Kundenbasis mehr Beschwerden erhalten als ein kleines Institut.

Deshalb ist:

```text
Anzahl Beschwerden
```

keine direkte Performance-Kennzahl.

Unternehmensbezogene Auswertungen dieses Projekts sind ausschließlich explorative Screening-Indikatoren.

---

# Keine Bewertung regulatorischer Verstöße

Aus einer CFPB-Beschwerde kann nicht automatisch geschlossen werden, dass:

- ein Unternehmen gegen regulatorische Anforderungen verstoßen hat,
- ein tatsächlicher finanzieller Schaden entstanden ist,
- das Unternehmen für den beschriebenen Sachverhalt verantwortlich ist,
- ein Beschwerdevorwurf sachlich bestätigt wurde.

Die EDA identifiziert Muster und Untersuchungsschwerpunkte.

Sie ersetzt keine Einzelfallprüfung, Compliance-Bewertung oder regulatorische Untersuchung.

---

# Taxonomieänderungen

Produkt- und Issue-Bezeichnungen des CFPB wurden historisch verändert.

Ohne Harmonisierung könnten dadurch künstliche:

- Wachstumssprünge,
- Rückgänge,
- neue Kategorien,
- verschwundene Kategorien

entstehen.

Das Projekt verwendet deshalb zusätzliche harmonisierte Felder.

Diese Harmonisierung verbessert die Vergleichbarkeit, ist aber selbst eine analytische Modellierungsentscheidung.

Die Originalwerte bleiben erhalten und alle Zuordnungen werden auditiert.

---

# Grenzen der Taxonomie-Harmonisierung

Nicht jede historische Klassifikationsänderung lässt sich allein aus einem Produktnamen vollständig rekonstruieren.

Wo eine Zuordnung vom Sub-Product abhängt, wird diese zusätzliche Information verwendet.

Dennoch gilt:

Eine harmonisierte Taxonomie ist eine analytische Abbildung der dokumentierten Quelländerungen und keine neue offizielle CFPB-Klassifikation.

Deshalb werden Source- und Analysewerte parallel gespeichert.

---

# Fehlende Issue-Werte

Ein sehr kleiner Teil der Source-Daten kann keinen veröffentlichten Issue-Wert enthalten.

Diese Fälle werden nicht gelöscht.

Der ursprüngliche Wert bleibt:

```text
issue = null
```

Für Aggregationen wird zusätzlich verwendet:

```text
harmonized_issue = "Issue not provided"
```

Damit bleibt der Missing Value sichtbar und die Beschwerde geht nicht aus gruppierten Analysen verloren.

Die Behandlung fehlender Werte wird getrennt von Taxonomieänderungen dokumentiert.

---

# Consumer Narratives sind optional

Consumer Narratives stehen nur für einen Teil der veröffentlichten Beschwerden zur Verfügung.

Die Verfügbarkeit ist nicht zufällig.

Sie hängt unter anderem davon ab, ob ein Verbraucher der Veröffentlichung zugestimmt hat und ob die Voraussetzungen für eine Veröffentlichung erfüllt sind.

Der Anteil vorhandener Narratives darf deshalb nicht als repräsentativer Querschnitt aller Beschwerden interpretiert werden.

---

# Produktmix kann statistische Beziehungen beeinflussen

Eine beobachtete Korrelation zwischen zwei aggregierten Kennzahlen muss nicht bedeuten, dass auf Einzelfallebene derselbe Zusammenhang besteht.

Beispielsweise kann ein stark wachsendes Produktsegment gleichzeitig:

- besonders viele Beschwerden,
- einen niedrigen Narrative-Anteil

aufweisen.

Dadurch kann auf Monatsebene eine starke negative Korrelation zwischen Beschwerdevolumen und Narrative-Anteil entstehen, obwohl nicht bewiesen ist, dass steigendes Beschwerdevolumen selbst die Narrative-Bereitschaft verändert.

Solche Kompositionseffekte müssen bei Aggregatanalysen berücksichtigt werden.

---

# Korrelation ist keine Kausalität

Das Projekt berechnet Pearson- und Spearman-Korrelationen.

Diese Kennzahlen beschreiben statistische Zusammenhänge.

Sie zeigen nicht:

- welche Variable eine andere verursacht,
- ob eine dritte Variable beide beeinflusst,
- ob der beobachtete Zusammenhang operativ relevant ist.

Korrelationen werden deshalb ausschließlich explorativ interpretiert.

---

# Linearer Trend ist keine Prognose

Der lineare Zeittrend beschreibt die durchschnittliche Entwicklung des beobachteten monatlichen Beschwerdevolumens.

Die Regression verwendet einen fortlaufenden Monatsindex als erklärende Variable.

Sie ist kein Forecasting-Modell.

Insbesondere werden keine:

- Saisonalität,
- strukturellen Brüche,
- regulatorischen Veränderungen,
- Marktveränderungen,
- Taxonomieänderungen außerhalb der Harmonisierung,
- externen Einflussfaktoren

als Prognosekomponenten modelliert.

Eine Extrapolation in die Zukunft wäre deshalb methodisch nicht gerechtfertigt.

---

# Starkes Wachstum ist nicht automatisch Marktwachstum

Ein Anstieg veröffentlichter Beschwerden kann verschiedene Ursachen haben.

Mögliche Einflussfaktoren sind beispielsweise:

- tatsächliche Zunahme bestimmter Kundenprobleme,
- verändertes Meldeverhalten,
- höhere Bekanntheit des Beschwerdekanals,
- technische Änderungen,
- Veränderungen der Einreichungspraxis,
- Änderungen des Produktmixes.

Die EDA beschreibt die Entwicklung der veröffentlichten Beschwerden.

Sie behauptet nicht, dass dieselbe Wachstumsrate für tatsächliche Probleme im Gesamtmarkt gilt.

---

# Geografische Analyse benötigt Bezugsgrößen

Absolute Beschwerdezahlen eines Bundesstaates wären ohne zusätzlichen Kontext nur eingeschränkt interpretierbar.

Für belastbarere geografische Vergleiche wären beispielsweise erforderlich:

- Bevölkerung,
- Anzahl Kunden,
- Anzahl Verträge,
- Produktnutzung,
- Marktpenetration.

Der aktuelle Kernreport verzichtet deshalb bewusst auf ein unnormalisiertes geografisches Ranking.

---

# Zeitliche Vollständigkeit

Aktuelle Kalenderjahre können unvollständig sein.

Außerdem können Veröffentlichungs- und Bearbeitungsprozesse zu zeitlichen Verzögerungen führen.

Das Projekt verwendet deshalb standardmäßig nur vollständige Kalenderjahre von:

```text
2022 bis 2025
```

Der Analysezeitraum ist konfigurierbar.

---

# Unternehmensnamen und Unternehmensstruktur

Unternehmensbezeichnungen in öffentlichen Beschwerdedaten müssen nicht zwangsläufig einer für alle Analysezwecke idealen Konzernstruktur entsprechen.

Mögliche Herausforderungen sind beispielsweise:

- Tochtergesellschaften,
- unterschiedliche juristische Einheiten,
- historische Namensänderungen,
- Servicer und externe Dienstleister.

Das aktuelle Projekt harmonisiert keine Unternehmenskonzerne.

Company-Level-Ergebnisse werden deshalb vorsichtig als Screening-Signale behandelt.

---

# US-Datensatz

Die zugrunde liegenden CFPB-Daten beziehen sich auf den US-amerikanischen Finanzmarkt.

Die konkreten:

- Produktbezeichnungen,
- regulatorischen Strukturen,
- Marktmechanismen,
- Complaint-Prozesse

lassen sich nicht direkt auf Deutschland oder Europa übertragen.

Übertragbar ist vor allem die **analytische Methodik**:

- große Complaint-Daten aufbereiten,
- Datenqualität prüfen,
- Taxonomien harmonisieren,
- Hotspots identifizieren,
- Zeitreihen analysieren,
- Ergebnisse für Management und Consulting strukturieren.

---

# Übertragbarkeit auf Versicherungen

Die CFPB-Daten sind kein Versicherungsdatensatz.

Deshalb beweist dieses Projekt keine konkreten Muster für Versicherungsunternehmen.

Übertragbar ist jedoch die Datenanalyse-Architektur auf Fragestellungen wie:

- Schadenbeschwerden,
- Leistungsbearbeitung,
- Vertragsservice,
- Policenverwaltung,
- Kontaktgründe,
- Bearbeitungszeiten,
- Ombudsmann-Fälle.

Der Versicherungsbezug des Projekts ist damit **methodischer Transfer**, keine direkte empirische Versicherungsanalyse.

---

# Consumer Narrative nicht im aktuellen Analyse-Parquet

Der vollständige Beschwerdetext wird im aktuellen Modul-1-Projekt nicht in die Parquet-Analyseschicht übernommen.

Es wird lediglich:

```text
has_narrative
```

abgeleitet.

Damit bleibt die aktuelle EDA speichereffizient.

Für spätere NLP-Analysen muss der Narrative-Text erneut aus dem unveränderten Rohdatensatz geladen werden.

---

# Datenstand und Reproduzierbarkeit

Die Consumer Complaint Database wird weiter aktualisiert.

Ein späterer Download kann deshalb andere Zeilenzahlen enthalten als der für dieses Projekt verwendete Snapshot.

Das Projekt speichert aus diesem Grund:

- Downloadzeitpunkt,
- Dateigröße,
- SHA-256-Hash.

Damit ist der verwendete Rohdatenstand nachvollziehbar.

---

# Operative Folgeschritte sind erforderlich

Die EDA identifiziert Bereiche, die eine vertiefende Untersuchung rechtfertigen können.

Vor operativen oder regulatorischen Entscheidungen sollten die Ergebnisse mit weiteren Daten verbunden werden, beispielsweise:

```text
CFPB-Beschwerden
+
interne Kundenbestände
+
Konten oder Verträge
+
Transaktionsvolumen
+
Service-Level-Kennzahlen
+
Kontaktgründe
+
Incident-Daten
+
Prozessdaten
+
Remediation-Ergebnisse
+
Customer-Outcome-Kennzahlen
```

Erst dadurch können externe explorative Signale in eine belastbarere institutionelle Bewertung überführt werden.

---

# Grundsatz

Die Ergebnisse dieses Projekts dienen der:

- explorativen Priorisierung,
- Hypothesengenerierung,
- Identifikation möglicher Untersuchungsschwerpunkte,
- datenbasierten Entscheidungsunterstützung.

Sie dienen nicht als ungeprüfte Grundlage für:

- kausale Aussagen,
- Unternehmensrankings,
- regulatorische Vorwürfe,
- Zukunftsprognosen.
