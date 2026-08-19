#!/usr/bin/env python3
"""Erstellt einen aktuellen Wetterbericht für Leipzig auf Basis der Open-Meteo-API."""

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=51.3397&longitude=12.3731"
    "&current=temperature_2m,apparent_temperature,wind_speed_10m,precipitation,weather_code"
    "&timezone=Europe%2FBerlin"
)

STANDARD_AUSGABEVERZEICHNIS = "reports"
VORLAGEN_PFAD = Path(__file__).resolve().parent.parent / "templates" / "wetterbericht.md.tpl"

# Zuordnung der WMO-Wettercodes (siehe Open-Meteo-Dokumentation) zu deutschen Kurztexten.
WMO_CODES = {
    0: "Klarer Himmel",
    1: "Überwiegend klar",
    2: "Teilweise bewölkt",
    3: "Bedeckt",
    45: "Nebel",
    48: "Reifnebel",
    51: "Leichter Nieselregen",
    53: "Mäßiger Nieselregen",
    55: "Starker Nieselregen",
    56: "Leichter gefrierender Nieselregen",
    57: "Starker gefrierender Nieselregen",
    61: "Leichter Regen",
    63: "Mäßiger Regen",
    65: "Starker Regen",
    66: "Leichter gefrierender Regen",
    67: "Starker gefrierender Regen",
    71: "Leichter Schneefall",
    73: "Mäßiger Schneefall",
    75: "Starker Schneefall",
    77: "Schneegriesel",
    80: "Leichte Regenschauer",
    81: "Mäßige Regenschauer",
    82: "Heftige Regenschauer",
    85: "Leichte Schneeschauer",
    86: "Starke Schneeschauer",
    95: "Gewitter",
    96: "Gewitter mit leichtem Hagel",
    99: "Gewitter mit starkem Hagel",
}


class WetterdatenFehler(Exception):
    """Wird ausgelöst, wenn die Wetterdaten nicht abgerufen oder nicht ausgewertet werden können."""


def wmo_code_zu_text(code):
    """Übersetzt einen WMO-Wettercode in einen deutschen Kurztext."""
    return WMO_CODES.get(code, f"Unbekannter Wettercode ({code})")


def de_zahl(wert):
    """Formatiert eine Zahl mit einer Nachkommastelle im deutschen Format (Komma statt Punkt)."""
    return f"{wert:.1f}".replace(".", ",")


def hole_wetterdaten():
    """Ruft die aktuellen Wetterdaten für Leipzig von Open-Meteo ab."""
    try:
        with urllib.request.urlopen(API_URL, timeout=10) as antwort:
            rohdaten = antwort.read()
    except urllib.error.HTTPError as fehler:
        raise WetterdatenFehler(
            f"Open-Meteo hat einen Fehler gemeldet (HTTP {fehler.code})."
        ) from fehler
    except (urllib.error.URLError, TimeoutError) as fehler:
        raise WetterdatenFehler(
            f"Wetterdaten konnten nicht abgerufen werden (Netzwerkfehler): {fehler}"
        ) from fehler

    try:
        return json.loads(rohdaten)
    except json.JSONDecodeError as fehler:
        raise WetterdatenFehler(
            "Antwort von Open-Meteo hat ein unerwartetes Format."
        ) from fehler


def baue_markdown_tabelle(kopfzeilen, zeilen):
    """Erzeugt eine Markdown-Tabelle mit auf gleiche Breite ausgerichteten Spalten (Beautify-Regel)."""
    spaltenbreiten = [
        max(len(kopfzeilen[i]), *(len(zeile[i]) for zeile in zeilen))
        for i in range(len(kopfzeilen))
    ]

    def formatiere_zeile(zellen):
        return "| " + " | ".join(
            zelle.ljust(breite) for zelle, breite in zip(zellen, spaltenbreiten)
        ) + " |"

    trennzeile = "|" + "|".join("-" * (breite + 2) for breite in spaltenbreiten) + "|"

    zeilen_formatiert = [formatiere_zeile(kopfzeilen), trennzeile]
    zeilen_formatiert += [formatiere_zeile(zeile) for zeile in zeilen]
    return "\n".join(zeilen_formatiert)


def formatiere_bericht(daten):
    """Befüllt die Markdown-Vorlage mit den abgerufenen Wetterdaten."""
    try:
        aktuell = daten["current"]
        tabelle = baue_markdown_tabelle(
            ["Kennzahl", "Wert"],
            [
                ["Temperatur", f"{de_zahl(aktuell['temperature_2m'])} °C"],
                ["Gefühlte Temperatur", f"{de_zahl(aktuell['apparent_temperature'])} °C"],
                ["Windgeschwindigkeit", f"{de_zahl(aktuell['wind_speed_10m'])} km/h"],
                ["Niederschlag", f"{de_zahl(aktuell['precipitation'])} mm"],
                ["Wetterlage", wmo_code_zu_text(aktuell["weather_code"])],
            ],
        )
        werte = {
            "datum": datetime.now().strftime("%d.%m.%Y"),
            "uhrzeit": datetime.now().strftime("%H:%M Uhr"),
            "tabelle": tabelle,
            "erzeugt_am": datetime.now().strftime("%d.%m.%Y %H:%M Uhr"),
        }
    except KeyError as fehler:
        raise WetterdatenFehler(
            "Antwort von Open-Meteo hat ein unerwartetes Format."
        ) from fehler

    vorlage = VORLAGEN_PFAD.read_text(encoding="utf-8")
    return vorlage.format(**werte)


def speichere_bericht(inhalt, ausgabeverzeichnis):
    """Speichert den Bericht als Markdown-Datei mit Zeitstempel im Dateinamen."""
    ausgabeverzeichnis.mkdir(parents=True, exist_ok=True)
    dateiname = f"wetterbericht-leipzig-{datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
    pfad = ausgabeverzeichnis / dateiname
    pfad.write_text(inhalt, encoding="utf-8")
    return pfad


def main():
    parser = argparse.ArgumentParser(
        description="Erstellt einen aktuellen Wetterbericht für Leipzig."
    )
    parser.add_argument(
        "--output-dir",
        default=STANDARD_AUSGABEVERZEICHNIS,
        help=f"Zielverzeichnis für den Report (Standard: {STANDARD_AUSGABEVERZEICHNIS})",
    )
    parser.add_argument(
        "--kein-speichern",
        action="store_true",
        help="Bericht nur ausgeben, keine Datei speichern.",
    )
    argumente = parser.parse_args()

    try:
        daten = hole_wetterdaten()
        bericht = formatiere_bericht(daten)
    except WetterdatenFehler as fehler:
        print(f"Fehler: {fehler}", file=sys.stderr)
        sys.exit(1)

    print(bericht)

    if not argumente.kein_speichern:
        pfad = speichere_bericht(bericht, Path(argumente.output_dir))
        print(f"Bericht gespeichert unter: {pfad}", file=sys.stderr)


if __name__ == "__main__":
    main()
