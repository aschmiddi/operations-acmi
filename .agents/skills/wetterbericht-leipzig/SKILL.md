# Skill: Wetterbericht Leipzig

## Zweck

Dieser Skill erstellt einen aktuellen Wetterbericht für Leipzig aus einer öffentlichen, kostenlosen Schnittstelle (Open-Meteo) und formatiert ihn anhand einer festen Vorlage. Er dient als Referenz-/Demo-Skill für das Reporting-Pattern dieses Repositorys: Ein Skript holt Daten, ein Template sorgt dafür, dass jeder Report unabhängig vom Ersteller gleich aussieht.

## Datenquelle

[Open-Meteo](https://open-meteo.com) — kostenlos, kein API-Key, keine Registrierung erforderlich. Abgefragt werden die aktuellen Werte für die Koordinaten Leipzigs (51.3397, 12.3731): Temperatur, gefühlte Temperatur, Windgeschwindigkeit, Niederschlag und der WMO-Wettercode (wird im Skript in einen deutschen Kurztext übersetzt, z. B. "Teilweise bewölkt").

## Voraussetzungen

Python 3 (Standardbibliothek genügt, keine zusätzlichen Pakete nötig).

## Verwendung

Bericht erzeugen (wird in `reports/` gespeichert und zusätzlich im Terminal/Chat ausgegeben):

```bash
python3 .agents/skills/wetterbericht-leipzig/scripts/wetterbericht.py
```

Anderes Ausgabeverzeichnis verwenden:

```bash
python3 .agents/skills/wetterbericht-leipzig/scripts/wetterbericht.py --output-dir sonstiges/verzeichnis
```

Nur Ausgabe im Terminal, keine Datei speichern:

```bash
python3 .agents/skills/wetterbericht-leipzig/scripts/wetterbericht.py --kein-speichern
```

Der Dateiname wird automatisch nach dem Schema `wetterbericht-leipzig-JJJJ-MM-TT_HHMM.md` vergeben.

## Hinweis für Claude

Wenn im Chat nach dem aktuellen Wetter oder Wetterbericht für Leipzig gefragt wird, kann dieses Skript direkt ausgeführt werden, um eine aktuelle, einheitlich formatierte Antwort zu liefern.

## Fehlerfälle

Bei Netzwerkproblemen oder einer fehlerhaften Antwort der Open-Meteo-API bricht das Skript mit einer verständlichen deutschen Fehlermeldung auf `stderr` und Exit-Code 1 ab, statt einen rohen Python-Traceback auszugeben.
