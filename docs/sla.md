# Service Level Agreements (SLA)

> Fiktives Beispiel im Rahmen des Operations-Template-Repositories.

## Geltungsbereich

Diese SLAs gelten für die in der [Systemübersicht](systemuebersicht.md) gelisteten produktiven Systeme der Acme GmbH und definieren die vertraglich zugesicherten Verfügbarkeits- und Reaktionszeiten des Operations-Teams.

## Verfügbarkeit

| System | Kritikalität | Verfügbarkeitsziel | Max. Downtime/Monat |
|---|---|---|---|
| `acme-payments` | Kritisch | 99,95 % | ~ 22 Min. |
| `acme-shop` | Hoch | 99,9 % | ~ 43 Min. |
| `acme-data-platform` | Mittel | 99,5 % | ~ 3,6 Std. |
| `acme-crm` | Mittel | 99,5 % | ~ 3,6 Std. |
| `acme-internal-tools` | Niedrig | 99,0 % | ~ 7,3 Std. |

Geplante Wartungsfenster (angekündigt mit mind. 5 Werktagen Vorlauf) werden nicht auf die Downtime angerechnet.

## Schweregrade

| Schweregrad | Definition | Beispiel |
|---|---|---|
| **Sev1 – Kritisch** | Vollständiger Ausfall eines kritischen Systems, Kundenimpact | Checkout in `acme-shop` nicht erreichbar |
| **Sev2 – Hoch** | Erhebliche Beeinträchtigung, Workaround ggf. möglich | Erhöhte Latenz, einzelne Funktionen gestört |
| **Sev3 – Mittel** | Eingeschränkte Funktionalität ohne unmittelbaren Kundenimpact | Reporting-Verzögerung in `acme-data-platform` |
| **Sev4 – Niedrig** | Kleinere Störung, keine Dringlichkeit | Kosmetischer Fehler im internen Admin-Tool |

## Reaktions- und Wiederherstellungszeiten

| Schweregrad | Reaktionszeit | Ziel-Wiederherstellungszeit | Servicezeit |
|---|---|---|---|
| Sev1 | 15 Minuten | 2 Stunden | 24/7 |
| Sev2 | 30 Minuten | 4 Stunden | 24/7 |
| Sev3 | 4 Stunden | 1 Werktag | Mo–Fr, 8–18 Uhr |
| Sev4 | 1 Werktag | 5 Werktage | Mo–Fr, 8–18 Uhr |

## Eskalation

Wird die Reaktionszeit überschritten, erfolgt automatisch eine Eskalation an die nächste Stufe gemäß [Ansprechpartner & Eskalation](ansprechpartner.md).

## Reporting

Die Einhaltung der SLAs wird monatlich im Verfügbarkeits-Report unter [`reports/`](../reports/) dokumentiert und dem Kunden zur Verfügung gestellt.
