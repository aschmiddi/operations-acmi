# Ansprechpartner & Eskalation

> Fiktives Beispiel im Rahmen des Operations-Template-Repositories. Namen, Kontaktdaten und Firmen sind frei erfunden.

## Kontakte Kundenseite (Acme GmbH)

| Rolle | Verantwortungsbereich | Kontaktweg |
|---|---|---|
| IT-Leitung | Vertragliche Eskalation, strategische Entscheidungen | it-leitung@acme.example |
| Product Owner `acme-shop` | Fachliche Freigaben, Priorisierung | po-shop@acme.example |
| Security-Verantwortlicher | Freigabe bei sicherheitsrelevanten Incidents | security@acme.example |

## Kontakte Operations-Team (Dienstleister)

| Rolle | Verantwortungsbereich | Erreichbarkeit |
|---|---|---|
| On-Call Engineer (Stufe 1) | Erstreaktion auf Alerts, Sev1–Sev4 | 24/7 über PagerDuty |
| Team Lead Operations | Eskalationsstufe 2, Ressourcenkoordination | Mo–Fr, 8–20 Uhr |
| Engagement Manager | Vertragliche/kommerzielle Eskalation | Mo–Fr, 9–17 Uhr |

## Eskalationspfad

```
Alert / Meldung
      │
      ▼
On-Call Engineer (Stufe 1)
      │  Reaktionszeit überschritten oder Sev1 ungelöst > 1 Std.
      ▼
Team Lead Operations (Stufe 2)
      │  weiterhin ungelöst oder vertraglich relevant
      ▼
Engagement Manager (Stufe 3)
      │  strategische/kommerzielle Fragen
      ▼
IT-Leitung Acme GmbH
```

## Kommunikationskanäle

- **Sev1/Sev2**: Gemeinsamer Incident-Slack-Channel `#acme-incidents` (Bridge zwischen Kunde und Dienstleister), zusätzlich Statusupdates per E-Mail alle 30 Minuten.
- **Sev3/Sev4**: Ticket im gemeinsamen Ticketsystem (Jira Service Management), Bearbeitung gemäß [SLA](sla.md).
- **Reguläre Abstimmung**: Wöchentlicher Operations-Jour-fixe, monatlicher Report-Review (siehe [`reports/`](../reports/)).

> **Hinweis:** Kontaktdaten sind hier bewusst als Platzhalter (`@acme.example`) hinterlegt. In einem realen Projekt sind personenbezogene Kontaktdaten vertraulich zu behandeln und nicht im Klartext in einem Repository zu pflegen, sofern der Zugriff nicht entsprechend eingeschränkt ist.
