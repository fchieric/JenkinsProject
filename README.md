# JenkinsProject

# Configurazione del Monitoraggio per il Progetto CI/CD

Questo documento descrive come configurare il sistema di monitoraggio per il progetto CI/CD utilizzando Prometheus e Grafana.

## Struttura del Progetto

```
monitoring/
├── docker-compose-monitoring.yml     # Configurazione Docker Compose per Prometheus e Grafana
├── prometheus.yml                    # Configurazione di Prometheus
└── grafana/
    └── provisioning/
        ├── dashboards/
        │   ├── dashboards.yml        # Config per caricare le dashboard
        │   ├── flask-dashboard.json  # Dashboard per Flask
        │   └── jenkins-dashboard.json # Dashboard per Jenkins
        └── datasources/
            └── datasource.yml        # Configurazione fonte dati Prometheus
```

## Prerequisiti

- Docker e Docker Compose installati
- La rete Docker `progetto_devops_network` già configurata
- L'applicazione Flask modificata con l'endpoint `/metrics`
- Jenkins in esecuzione

## Passaggi di Configurazione

### 1. Aggiornare l'Applicazione Flask

Aggiornare il file `app.py` per includere il nuovo endpoint `/metrics` che fornisce i dati di monitoraggio.

### 2. Configurare Prometheus e Grafana

1. Creare la struttura delle directory:

```bash
mkdir -p monitoring/grafana/provisioning/{dashboards,datasources}
```

2. Copiare i file di configurazione nelle posizioni corrette:

```bash
cp prometheus.yml monitoring/
cp grafana/provisioning/dashboards/dashboards.yml monitoring/grafana/provisioning/dashboards/
cp grafana/provisioning/dashboards/flask-dashboard.json monitoring/grafana/provisioning/dashboards/
cp grafana/provisioning/dashboards/jenkins-dashboard.json monitoring/grafana/provisioning/dashboards/
cp grafana/provisioning/datasources/datasource.yml monitoring/grafana/provisioning/datasources/
cp docker-compose-monitoring.yml monitoring/docker-compose.yml
```

3. Avviare i servizi:

```bash
cd monitoring
docker-compose up -d
```

### 3. Accedere alle Dashboard

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000
  - Username: admin
  - Password: admin

Una volta effettuato l'accesso a Grafana, troverai già configurate due dashboard:
1. **Flask Application Dashboard**: Visualizza le metriche dell'applicazione Flask
2. **Jenkins Dashboard**: Visualizza le metriche di Jenkins

## Note sull'implementazione

- L'endpoint `/metrics` dell'app Flask fornisce dati in formato JSON che Prometheus può raccogliere
- Grafana è configurato per utilizzare Prometheus come fonte dati
- Le dashboard sono preconfigurate e caricate automaticamente
- Il sistema monitora sia l'applicazione Flask che Jenkins

## Personalizzazione

Per aggiungere nuove metriche all'applicazione Flask:
1. Aggiornare l'endpoint `/metrics` in `app.py`
2. Modificare la dashboard in Grafana aggiungendo nuovi pannelli

Per personalizzare il monitoraggio di Jenkins:
1. Installare plugin aggiuntivi di Jenkins se necessario
2. Aggiornare la configurazione di Prometheus in `prometheus.yml`
3. Modificare la dashboard di Jenkins in Grafana
