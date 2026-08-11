# Datenverzeichnisse

Große Roh- und Analysedateien werden bewusst nicht über Git versioniert.

Die Verzeichnisstruktur trennt verschiedene Stufen der Datenverarbeitung:

- `raw/` – unveränderter lokaler Snapshot der offiziellen CFPB-Quelldaten
- `interim/` – optionale temporäre Artefakte während der Transformation
- `processed/` – analysebereite Parquet-Daten
- `external/` – optionale zukünftige externe Ergänzungsdaten, beispielsweise Bevölkerungs-, Marktanteils- oder Exposure-Daten

Die eigentlichen Datendateien werden über `.gitignore` ausgeschlossen.

Leere `.gitkeep`-Dateien sorgen dafür, dass die Verzeichnisstruktur trotzdem Bestandteil des Repositorys bleibt.

## Rohdaten herunterladen

Der offizielle CFPB-Datensatz wird mit folgendem Befehl heruntergeladen:

```bash
python scripts/download_data.py
```

Das Skript:

1. lädt den offiziellen CFPB-Bulk-Datensatz,
2. schreibt zunächst in eine temporäre `.part`-Datei,
3. verhindert dadurch scheinbar vollständige, aber abgebrochene Downloads,
4. extrahiert die CSV-Datei,
5. berechnet eine SHA-256-Prüfsumme,
6. speichert lokale Download-Metadaten.

Die Rohdaten liegen anschließend unter:

```text
data/raw/
```

## Analysebestand erzeugen

Die vollständige Transformations- und Analysepipeline kann ausgeführt werden mit:

```bash
python scripts/run_pipeline.py
```

Dabei wird unter anderem der analysebereite Parquet-Datensatz erzeugt:

```text
data/processed/complaints_analytics.parquet
```

Der aktuelle Portfolio-Analysebestand umfasst vollständige Kalenderjahre vom:

```text
2022-01-01
```

bis:

```text
2025-12-31
```

und enthält:

```text
10.269.540 Beschwerden
```

## Warum die Daten nicht im Repository liegen

Der öffentliche CFPB-Rohdatensatz ist mehrere Gigabyte groß.

Eine Versionierung über Git würde:

- das Repository unnötig vergrößern,
- Klonen und CI-Läufe erschweren,
- große generierte Dateien dauerhaft in der Git-Historie speichern,
- keinen zusätzlichen analytischen Mehrwert liefern.

Stattdessen werden Datenaufnahme und Transformation reproduzierbar über Skripte bereitgestellt.

Die auf dem veröffentlichten Portfolio-Stand basierende Datenprovenienz ist zusätzlich dokumentiert unter:

```text
reports/source_snapshot.json
```

Dadurch bleibt nachvollziehbar, auf welchem Quelldaten-Snapshot die veröffentlichten Analyseergebnisse basieren, ohne die Rohdaten selbst im Repository abzulegen.
