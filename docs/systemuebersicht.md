# Systemübersicht – Acme GmbH

> Fiktives Beispiel im Rahmen des Operations-Template-Repositories. Alle Angaben (Firmen, Systeme, IPs, Domains) sind erfunden.

## Zweck

Dieses Dokument gibt einen Überblick über die von uns betreuten Systeme der Acme GmbH, deren Zweck, Kritikalität und die zugrunde liegende Cloud-Umgebung. Es dient als Einstiegspunkt für neue Teammitglieder und als Referenz für Incident-Response.

## Betreute Systeme

| System | Zweck | Kritikalität | Cloud-Provider | Region |
|---|---|---|---|---|
| `acme-shop` | Öffentlicher Online-Shop (B2C) | Hoch | AWS | eu-central-1 |
| `acme-payments` | Zahlungsabwicklung, PCI-relevanter Scope | Kritisch | AWS | eu-central-1 |
| `acme-crm` | Internes CRM-System | Mittel | Azure | germanywestcentral |
| `acme-data-platform` | Data Warehouse & Analytics | Mittel | AWS | eu-central-1 |
| `acme-internal-tools` | Interne Admin-Tools | Niedrig | AWS | eu-central-1 |

**Kritikalitätsstufen:**
- **Kritisch** – Ausfall hat direkten finanziellen/rechtlichen Impact (z. B. Zahlungsverkehr, Compliance).
- **Hoch** – Ausfall ist kundensichtbar und beeinträchtigt den Kernumsatz.
- **Mittel** – Ausfall beeinträchtigt interne Prozesse, kein direkter Kundenimpact.
- **Niedrig** – Ausfall ist tolerierbar, keine unmittelbaren Auswirkungen.

## Architekturprinzipien

Alle Systeme folgen den gemeinsamen Architekturprinzipien des Engagements:

- **Cloud-native, containerbasiert**: Workloads laufen als Microservices auf Kubernetes (Amazon EKS bzw. Azure AKS).
- **Infrastructure as Code**: Die gesamte Infrastruktur wird über Terraform verwaltet, keine manuellen Änderungen in der Konsole ("ClickOps") im Produktivbetrieb.
- **Automatisierte CI/CD-Pipelines**: Jede Änderung durchläuft automatisierte Tests, Security-Scans und ein kontrolliertes Deployment (siehe [Betriebshandbuch](betriebshandbuch.md)).
- **Least Privilege & Secrets Management**: Zugriffsrechte werden nach dem Prinzip der geringsten Berechtigung vergeben, Secrets liegen ausschließlich in AWS Secrets Manager / Azure Key Vault.
- **Kostenverantwortung (FinOps)**: Ressourcen werden getaggt und monatlich auf Kosten- und Auslastungsoptimierung geprüft (siehe [Kostenreport](../reports/)).

## Weiterführende Dokumente

- [Architektur: acme-shop](architektur-acme-shop.md)
- [Betriebshandbuch](betriebshandbuch.md)
- [Service Level Agreements](sla.md)
- [Ansprechpartner & Eskalation](ansprechpartner.md)
