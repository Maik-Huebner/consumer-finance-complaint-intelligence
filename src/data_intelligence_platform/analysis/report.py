"""Generate a German consulting-style executive summary from EDA outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def _pct(
    value: float | None,
) -> str:
    """Format a decimal value as a German-style percentage."""
    if pd.isna(
        value
    ):
        return "k. A."

    return (
        f"{float(value):.1%}"
        .replace(
            ".",
            ",",
        )
    )


def _precise_pct(
    value: float | None,
) -> str:
    """Format very small proportions without hiding them through rounding."""
    if pd.isna(
        value
    ):
        return "k. A."

    return (
        f"{float(value):.5%}"
        .replace(
            ".",
            ",",
        )
    )


def _num(
    value: float | int | None,
) -> str:
    """Format integer-like values with German thousands separators."""
    if pd.isna(
        value
    ):
        return "k. A."

    return (
        f"{float(value):,.0f}"
        .replace(
            ",",
            ".",
        )
    )


def _decimal(
    value: float | None,
    digits: int = 3,
) -> str:
    """Format a decimal value using a German decimal separator."""
    if pd.isna(
        value
    ):
        return "k. A."

    return (
        f"{float(value):.{digits}f}"
        .replace(
            ".",
            ",",
        )
    )


def _build_sensitivity_section(
    sensitivity: dict[str, object] | None,
) -> str:
    """Build the German management section for segment sensitivity."""
    if not sensitivity:
        return ""

    correlations = sensitivity[
        "correlations"
    ]

    narrative = correlations[
        "complaints_vs_narrative_share"
    ]

    timeliness = correlations[
        "complaints_vs_timely_response_rate"
    ]

    narrative_all = narrative[
        "all"
    ]

    narrative_without = narrative[
        "without_focus_product"
    ]

    timeliness_all = timeliness[
        "all"
    ]

    timeliness_without = timeliness[
        "without_focus_product"
    ]

    return f"""
## Sensitivitätsanalyse: Einfluss des dominanten Credit-Reporting-Segments

Die Gesamtanalyse wird stark durch **{sensitivity['focus_product']}** geprägt. Deshalb wurde zusätzlich geprüft, wie sich zentrale Ergebnisse verändern, wenn dieses dominante Segment aus der Aggregation entfernt wird.

- Der Anteil des Credit-Reporting-Segments steigt von **{_pct(sensitivity['focus_share_first_year'])}** im Jahr {sensitivity['first_year']} auf **{_pct(sensitivity['focus_share_last_year'])}** im Jahr {sensitivity['last_year']}. Das entspricht einer Verschiebung um **{_decimal(sensitivity['focus_share_change_percentage_points'], 1)} Prozentpunkte**.
- Auch ohne Credit Reporting steigt das veröffentlichte Beschwerdevolumen deutlich: von **{_num(sensitivity['without_focus_complaints_first_year'])}** auf **{_num(sensitivity['without_focus_complaints_last_year'])}** Beschwerden beziehungsweise um **{_pct(sensitivity['without_focus_growth_first_to_last'])}**.
- Die Steigung des einfachen linearen Monatstrends sinkt jedoch von rund **{_num(sensitivity['total_monthly_slope'])}** Beschwerden pro Monat im Gesamtportfolio auf rund **{_num(sensitivity['without_focus_monthly_slope'])}** ohne Credit Reporting.
- Rechnerisch entfallen damit rund **{_pct(sensitivity['focus_share_of_total_linear_slope'])}** der Steigung des linearen Gesamttrends auf den Credit-Reporting-Anteil der monatlichen Beschwerdereihe.
- Die Pearson-Korrelation zwischen monatlichem Beschwerdevolumen und Narrative-Anteil verändert sich von **r={_decimal(narrative_all['pearson_r'])}** im Gesamtportfolio auf **r={_decimal(narrative_without['pearson_r'])}** ohne Credit Reporting.
- Die Pearson-Korrelation zwischen Beschwerdevolumen und Timely-Response-Rate verändert sich von **r={_decimal(timeliness_all['pearson_r'])}** auf **r={_decimal(timeliness_without['pearson_r'])}** und wechselt damit in dieser Sensitivitätsanalyse die Richtung.

Die Ergebnisse zeigen, dass die aggregierten Portfolio-Kennzahlen erheblich durch den Produktmix beeinflusst werden. Das starke Gesamtwachstum verschwindet ohne Credit Reporting nicht, fällt aber wesentlich schwächer aus. Gleichzeitig verändern sich die aggregierten Korrelationsstrukturen deutlich.

Die Analyse wird bewusst **nicht vorschnell als Simpson-Paradox klassifiziert**. Sie zeigt jedoch einen klaren Segment- beziehungsweise Kompositionseffekt und unterstreicht, dass Portfolio-Aggregate ohne Segmentkontrolle nicht isoliert interpretiert werden sollten.

Für Management- und Consulting-Entscheidungen bedeutet dies: Gesamtportfolio-KPIs sollten durch segmentierte Analysen ergänzt werden, bevor Ursachen, operative Risiken oder Customer Outcomes abgeleitet werden.
"""


def write_executive_summary(
    *,
    output_path: Path,
    yearly: pd.DataFrame,
    product: pd.DataFrame,
    hotspots: pd.DataFrame,
    trend: dict[str, float],
    correlations: pd.DataFrame,
    cleaning: dict[str, int | float],
    taxonomy: dict[str, int | float],
    quality_passed: bool,
    sensitivity: dict[str, object] | None = None,
) -> None:
    """Create a German management summary from analytical outputs."""
    first = yearly.iloc[
        0
    ]

    last = yearly.iloc[
        -1
    ]

    growth = (
        last[
            "complaints"
        ]
        / first[
            "complaints"
        ]
        - 1
        if first[
            "complaints"
        ]
        else float(
            "nan"
        )
    )

    top_product = product.iloc[
        0
    ]

    top_hotspot = hotspots.iloc[
        0
    ]

    volume_timeliness = correlations[
        (
            correlations[
                "x"
            ]
            == "complaints"
        )
        & (
            correlations[
                "y"
            ]
            == "timely_response_rate"
        )
    ]

    volume_narrative = correlations[
        (
            correlations[
                "x"
            ]
            == "complaints"
        )
        & (
            correlations[
                "y"
            ]
            == "narrative_share"
        )
    ]

    timeliness_text = (
        "Für die Beziehung zwischen Beschwerdevolumen und "
        "Timely-Response-Rate waren keine belastbaren "
        "Korrelationskennzahlen verfügbar."
    )

    if not volume_timeliness.empty:
        row = volume_timeliness.iloc[
            0
        ]

        timeliness_text = (
            "Zwischen monatlichem Beschwerdevolumen und "
            "Timely-Response-Rate ergibt sich eine "
            "Pearson-Korrelation von "
            f"**r={_decimal(row['pearson_r'])}** und eine "
            "Spearman-Rangkorrelation von "
            f"**ρ={_decimal(row['spearman_rho'])}**. "
            "Der Zusammenhang ist rein deskriptiv und erlaubt "
            "keine kausale Interpretation."
        )

    narrative_text = (
        "Für die Beziehung zwischen Beschwerdevolumen und "
        "Narrative-Anteil waren keine belastbaren "
        "Korrelationskennzahlen verfügbar."
    )

    if not volume_narrative.empty:
        row = volume_narrative.iloc[
            0
        ]

        narrative_text = (
            "Zwischen monatlichem Beschwerdevolumen und Narrative-Anteil "
            "ergibt sich eine Pearson-Korrelation von "
            f"**r={_decimal(row['pearson_r'])}** und eine "
            "Spearman-Rangkorrelation von "
            f"**ρ={_decimal(row['spearman_rho'])}**. "
            "Der Zusammenhang ist deskriptiv und kann wesentlich durch "
            "Veränderungen des Produktmixes beeinflusst sein."
        )

    source_missing_issue_rows = int(
        cleaning[
            "source_missing_issue_rows"
        ]
    )

    handled_issue_rows = int(
        cleaning[
            "missing_issue_rows_handled"
        ]
    )

    unhandled_issue_rows = int(
        cleaning[
            "missing_issue_rows_unhandled"
        ]
    )

    quality_text = (
        "bestanden"
        if quality_passed
        else "Befunde gemeldet, die vor einer Freigabe geprüft werden müssen"
    )

    sensitivity_section = _build_sensitivity_section(
        sensitivity
    )

    text = f"""# Management Summary

## Analyseumfang

Diese Analyse untersucht veröffentlichte Verbraucherbeschwerden des U.S. Consumer Financial Protection Bureau (CFPB) für die vollständigen Kalenderjahre **{int(first['year'])} bis {int(last['year'])}**.

Die Pipeline bewahrt die ursprünglichen CFPB-Klassifikationen und ergänzt separate bereinigte beziehungsweise harmonisierte Analysefelder. Dadurch bleiben historische Quelldaten nachvollziehbar, während gleichzeitig konsistentere Zeitvergleiche ermöglicht werden.

## Zentrale Ergebnisse

- Das veröffentlichte Beschwerdevolumen veränderte sich von **{_num(first['complaints'])}** Beschwerden im Jahr {int(first['year'])} auf **{_num(last['complaints'])}** im Jahr {int(last['year'])}. Dies entspricht einer Veränderung von **{_pct(growth)}** über den betrachteten Zeitraum.
- Die größte harmonisierte Produktkategorie ist **{top_product['product']}** mit einem Anteil von **{_pct(top_product['complaint_share'])}** an allen Beschwerden im Analysezeitraum.
- Der volumenstärkste harmonisierte Produkt-Issue-Hotspot ist **{top_hotspot['product']} — {top_hotspot['issue']}** mit **{_num(top_hotspot['complaints'])}** Beschwerden.
- Der deskriptive lineare Zeittrend entspricht durchschnittlich rund **{_num(trend['monthly_slope'])} zusätzlichen Beschwerden pro Monat** bei **R²={_decimal(trend['r2'])}**. Dieser Wert beschreibt ausschließlich den beobachteten Zeitraum und stellt keine Prognose dar.
- {timeliness_text}
- {narrative_text}
{sensitivity_section}
## Datenaufbereitung und Datenbereinigung

Die analytische Datenbasis wird vor der Interpretation explizit validiert und bereinigt. Unvollständige Datensätze werden nicht stillschweigend entfernt.

- Im Rohdatensatz fehlen bei **{_num(source_missing_issue_rows)}** Beschwerden veröffentlichte Issue-Werte. Dies entspricht **{_precise_pct(float(cleaning['source_missing_issue_share']))}** des analysierten Datenbestands.
- Für **{_num(handled_issue_rows)}** dieser Datensätze wird in der analytischen Klassifikation der explizite Wert `Issue not provided` verwendet.
- Das ursprüngliche CFPB-Feld `issue` bleibt bei diesen Datensätzen unverändert leer. Dadurch bleibt die Datenherkunft nachvollziehbar.
- **{_num(unhandled_issue_rows)}** Datensätze mit fehlendem Source-Issue sind analytisch unbehandelt.
- Complaint IDs, Datumslogik, Response-Werte, Taxonomieversionen und Vollständigkeit der analytischen Klassifikation werden automatisiert kontrolliert.

Keine Beschwerde wird ausschließlich aufgrund eines fehlenden Issue-Werts aus der Analyse entfernt.

## Taxonomie-Harmonisierung

Historische CFPB-Produkt- und Issue-Bezeichnungen bleiben vollständig erhalten. Für Längsschnittanalysen werden zusätzliche harmonisierte Felder verwendet.

- **{_num(taxonomy['product_rows_changed'])}** Beschwerden beziehungsweise **{_pct(float(taxonomy['product_change_share']))}** erhalten für die Analyse eine Produktklassifikation, die vom ursprünglichen veröffentlichten Produktwert abweicht.
- **{_num(taxonomy['issue_rows_changed'])}** Beschwerden beziehungsweise **{_pct(float(taxonomy['issue_change_share']))}** erhalten eine harmonisierte Issue-Klassifikation.
- Insgesamt sind **{_num(taxonomy['any_rows_changed'])}** Datensätze beziehungsweise **{_pct(float(taxonomy['any_change_share']))}** von mindestens einer Taxonomie-Harmonisierung betroffen.
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

Die automatisierte strukturelle Datenqualitätsprüfung wurde **{quality_text}**.

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
"""

    output_path.write_text(
        text,
        encoding="utf-8",
    )
