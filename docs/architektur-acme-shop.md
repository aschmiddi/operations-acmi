# Architektur – acme-shop

> Fiktives Beispiel im Rahmen des Operations-Template-Repositories.

## Überblick

`acme-shop` ist die öffentliche E-Commerce-Plattform der Acme GmbH. Die Architektur ist als Microservices-Landschaft auf Kubernetes (Amazon EKS) umgesetzt und für hohe Verfügbarkeit über zwei Availability Zones ausgelegt.

```
                        ┌─────────────────────┐
                        │   CloudFront (CDN)   │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  Application Load     │
                        │  Balancer (ALB)       │
                        └──────────┬───────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
        ┌────────▼──────┐ ┌────────▼──────┐ ┌────────▼──────┐
        │ Service:       │ │ Service:      │ │ Service:      │
        │ Catalog        │ │ Checkout      │ │ Customer      │
        │ (EKS, 3 Pods)  │ │ (EKS, 3 Pods) │ │ (EKS, 2 Pods) │
        └────────┬──────┘ └────────┬──────┘ └────────┬──────┘
                 │                 │                 │
        ┌────────▼─────────────────▼─────────────────▼──────┐
        │           Amazon RDS (PostgreSQL, Multi-AZ)         │
        └──────────────────────────────────────────────────┘

        ┌──────────────────────────────────────────────────┐
        │  Amazon SQS (Event-Queue: Bestellungen)            │
        │  → verbindet Checkout mit acme-payments (extern)   │
        └──────────────────────────────────────────────────┘
```

## Komponenten

| Komponente | Technologie | Zweck |
|---|---|---|
| CDN | Amazon CloudFront | Statische Assets, DDoS-Absorption, geringe Latenz |
| Ingress | Application Load Balancer | TLS-Terminierung, Routing zu Services |
| Compute | Amazon EKS (Kubernetes 1.29) | Betrieb der Microservices |
| Datenhaltung | Amazon RDS PostgreSQL (Multi-AZ) | Transaktionale Daten (Katalog, Kunden, Bestellungen) |
| Messaging | Amazon SQS | Asynchrone Kopplung an `acme-payments` |
| Secrets | AWS Secrets Manager | DB-Zugangsdaten, API-Keys |
| Observability | Amazon CloudWatch, Grafana | Metriken, Logs, Alerting |

## Skalierung & Verfügbarkeit

- Horizontal Pod Autoscaling (HPA) auf Basis von CPU- und Request-Latenz-Metriken.
- Multi-AZ-Deployment für RDS und EKS-Node-Groups zur Absicherung gegen AZ-Ausfälle.
- Health Checks auf ALB- und Kubernetes-Ebene (Liveness/Readiness Probes) für automatisiertes Self-Healing.

## Sicherheit

- Netzwerksegmentierung über private Subnetze für Compute und Datenhaltung; nur ALB und CDN sind öffentlich erreichbar.
- IAM-Rollen nach dem Least-Privilege-Prinzip, pro Service ein dediziertes IAM-Rollenprofil (IRSA).
- Verschlüsselung at-rest (RDS, S3) und in-transit (TLS 1.2+ auf allen öffentlichen Endpunkten).
- Regelmäßige Abhängigkeits- und Container-Image-Scans in der CI/CD-Pipeline.

## Trade-offs

- **Microservices vs. Monolith**: Die Aufteilung in Services erhöht die operative Komplexität (mehr Deployments, verteiltes Tracing nötig), erlaubt aber unabhängige Skalierung von Checkout (lastintensiv) gegenüber Customer-Service (weniger lastintensiv) und getrennte Deployment-Zyklen pro Team.
- **Managed Services (RDS, EKS) vs. Self-Hosted**: Höhere Grundkosten gegenüber Self-Hosting, dafür deutlich reduzierter Betriebsaufwand (Patching, Backups, HA) – im Kontext eines schlanken Operations-Teams bewusst gewählt.
- **SQS statt synchronem Aufruf an `acme-payments`**: Entkopplung erhöht die Resilienz bei Lastspitzen (z. B. Sale-Events), führt aber zu Eventual Consistency im Bestellstatus, die im Frontend abgefangen werden muss.
