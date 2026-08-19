# Betriebshandbuch

> Fiktives Beispiel im Rahmen des Operations-Template-Repositories.

## Zweck

Dieses Betriebshandbuch beschreibt die Standardabläufe, die im Rahmen des Operations-Engagements für die Systeme der Acme GmbH gelten: Deployments, Monitoring, Incident-Response und Backups.

## Deployment-Prozess

1. **Entwicklung**: Feature-Branches, Pull Request gegen `main`.
2. **CI-Pipeline** (GitHub Actions):
   - Linting & Unit-Tests
   - Security-Scan (SAST, Dependency-Check, Container-Image-Scan)
   - `terraform plan` für Infrastrukturänderungen (Review-Pflicht vor `apply`)
3. **CD-Pipeline**: Automatisiertes Deployment nach Merge in `main`
   - Erst in die Staging-Umgebung
   - Nach erfolgreichem Smoke-Test automatisiertes Canary-Deployment in Produktion (10 % Traffic, danach schrittweise Erhöhung)
4. **Rollback**: Bei fehlgeschlagenem Health-Check erfolgt automatisches Rollback auf die letzte stabile Version.

> **Hinweis:** Manuelle Änderungen an der Produktionsinfrastruktur ("ClickOps") sind nicht zulässig. Alle Änderungen laufen über Terraform und die CI/CD-Pipeline.

## Monitoring & Alerting

| Ebene | Tool | Beispiel-Metrik | Alert-Schwelle |
|---|---|---|---|
| Infrastruktur | Amazon CloudWatch | CPU-/Memory-Auslastung EKS-Nodes | > 85 % für 5 Min. |
| Anwendung | Grafana / Prometheus | Request-Latenz (p95) `acme-shop` | > 500 ms für 5 Min. |
| Verfügbarkeit | Synthetic Monitoring | HTTP-Statuscode Checkout-Endpunkt | ≠ 200 für 3 aufeinanderfolgende Checks |
| Kosten | AWS Cost Anomaly Detection | Tagesausgaben pro Account | Abweichung > 20 % vom gleitenden Durchschnitt |

Alerts werden über PagerDuty an den diensthabenden On-Call-Ingenieur eskaliert (siehe [Ansprechpartner](ansprechpartner.md)).

## Incident-Response

1. **Erkennung**: Alert via Monitoring oder Meldung durch Kunden.
2. **Triage**: Einstufung nach Schweregrad (siehe [SLA](sla.md#schweregrade)).
3. **Kommunikation**: Bei Sev1/Sev2 Information des Kunden gemäß SLA-Reaktionszeit über den definierten Kommunikationskanal.
4. **Behebung**: Sofortmaßnahme (Mitigation) hat Vorrang vor vollständiger Root-Cause-Analyse.
5. **Nachbereitung**: Postmortem ohne Schuldzuweisung ("blameless") innerhalb von 3 Werktagen, Ablage im entsprechenden Report unter [`reports/`](../reports/).

## Backup & Recovery

- **RDS**: Automatisierte tägliche Snapshots, Aufbewahrung 14 Tage; Point-in-Time-Recovery innerhalb der letzten 7 Tage möglich.
- **Konfigurationsdaten**: Vollständig in Terraform-State und Git versioniert – Wiederherstellung durch `terraform apply` gegen eine neue Umgebung.
- **Recovery-Ziele**:
  - RTO (Recovery Time Objective): 2 Stunden für kritische Systeme
  - RPO (Recovery Point Objective): 15 Minuten für `acme-payments`, 24 Stunden für `acme-crm`

Ein DR-Test (Wiederherstellung in eine isolierte Umgebung) wird halbjährlich durchgeführt und im entsprechenden Report dokumentiert.

## Zugriffsverwaltung

- Zugriff auf Produktionsressourcen ausschließlich über SSO mit MFA.
- Rechtevergabe nach Least-Privilege-Prinzip, Review der IAM-Rollen quartalsweise.
- Break-Glass-Zugang für Notfälle ist protokolliert und erfordert nachträgliche Freigabe durch den Kunden.
