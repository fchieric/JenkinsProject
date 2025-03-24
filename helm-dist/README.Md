# Documentazione helm-dist

## Overview
Questa Helm Chart permette il deployment di un'applicazione Flask su Kubernetes. L'applicazione viene scaricata da un repository Nexus e deployata come un binario eseguibile. È possibile specificare quale versione dell'applicazione si desidera utilizzare.

## Prerequisiti
- Kubernetes cluster (K3s, Minikube, o Docker Desktop Kubernetes)
- Helm v3.x installato
- Nexus repository configurato e accessibile
- Docker e docker-compose installati
- GitLab installato e configurato

## Struttura dell'Ambiente
L'ambiente è composto da:
- Jenkins (porta 8080)
- Nexus (porta 8081)
- GitLab (porta 80)
- Flask Application (porta 5000)

### Network Configuration
Tutti i servizi sono connessi attraverso una rete Docker chiamata "devops_network". Questo permette la comunicazione tra i container e il cluster Kubernetes minikube.

## Struttura della Chart

```
helm-dist/
│
├── Chart.yaml            # Metadati della chart
├── values.yaml           # Valori di default configurabili
│
└── templates/
    ├── deployment.yaml   # Definizione del deployment
    ├── service.yaml      # Definizione del service
    └── ingress.yaml      # Configurazione dell'ingress
```

## Versioning
La chart supporta il deployment di versioni specifiche dell'applicazione. La versione desiderata può essere specificata nel file `values.yaml` o tramite parametri durante l'installazione o l'aggiornamento con Helm.

## Flusso di Deployment

### 1. Configurazione dell'ambiente base:

```bash
# Avvio dei servizi base
docker-compose up -d

# Verifica che Nexus sia accessibile
curl http://nexus:8081

# A runtime nel container Jenkins installa python
apt update
apt install python3
```

### 2. Build (Jenkins)
```bash
# Creazione ambiente virtuale
python3 -m venv venv
pip install -r requirements.txt

# Compilazione applicazione
pyinstaller --onefile app.py

# Upload su Nexus (specificando la versione)
export APP_VERSION="1.0.0"  # Cambia a seconda della versione desiderata
curl -u $NEXUS_USER:$NEXUS_PASS --upload-file app http://nexus:8081/repository/raw_repo/app-flask/$APP_VERSION/app
```

### 3. Configurazione Minikube:
```bash
# Avvio di Minikube con driver docker
minikube start --driver=docker

# Connessione di minikube alla rete
docker network connect progetto_devops_network minikube

# Abilitazione dell'Ingress Controller
minikube addons enable ingress
```

### 4. Deploy (Helm)
```bash
# Installazione della chart con versione di default (1.0.0)
helm install my-flask-app ./helm-dist

# Installazione specificando una versione particolare dell'applicazione
helm install my-flask-app ./helm-dist --set appVersion=1.1.0

# Aggiornamento ad una nuova versione
helm upgrade my-flask-app ./helm-dist --set appVersion=1.2.0
```

Quando esegui questo comando:
- Helm legge values.yaml (e i parametri aggiuntivi)
- Processa i template
- Kubernetes crea:
  * Pod che scarica ed esegue il binario della versione specificata
  * Service per esporre l'app
  * Ingress per l'accesso esterno

### 5. Runtime
- Il pod scarica il binario della versione specificata da Nexus
- L'applicazione Flask viene eseguita
- L'app è accessibile attraverso l'ingress configurato
- Il health check monitora lo stato dell'applicazione

## Comandi Utili

### Helm
```bash
# Installazione
helm install my-flask-app ./helm-dist

# Aggiornamento configurazione e/o versione
helm upgrade my-flask-app ./helm-dist --set agentName="nome-da-inserire" --set appVersion=1.1.0

# Lista delle release
helm list

# Stato della release
helm status my-flask-app

# Rimozione applicazione
helm uninstall my-flask-app
```

### Kubernetes
```bash
# Verifica dei pod
kubectl get pods

# Log dei pod
kubectl logs "nome pod"

# Shell nel pod
kubectl exec -it "nome pod" -- /bin/bash

# Verifica dei servizi
kubectl get services

# Verifica dell'ingress
kubectl get ingress
```

## Test dell'Applicazione
```bash
# Port-forward per test locale
kubectl port-forward service/flask-app-service 5000:5000

# Test degli endpoint
curl http://localhost:5000/
curl http://localhost:5000/health-check
```

# Come Funziona Helm

### 1. Chart.yaml
Definisce i metadati del pacchetto:
```yaml
name: flask-app
version: 0.2.0
appVersion: "1.0.0"
```

### 2. values.yaml
Contiene le configurazioni personalizzabili:
```yaml
replicaCount: 1
image:
  repository: bitnami/minideb
  tag: latest
agentName: "Fabi"
appVersion: "1.0.0"  # Versione dell'applicazione da usare
service:
  type: NodePort
  port: 5000
```

### 3. Templates
I file nella cartella templates/ definiscono come l'applicazione viene eseguita su Kubernetes:

#### deployment.yaml
- Usa minideb come immagine base
- Scarica il binario della versione specificata da Nexus
- Esegue l'applicazione
- Configura i health checks

#### service.yaml
- Crea un servizio NodePort sulla porta 5000
- Gestisce la comunicazione interna al cluster

#### ingress.yaml
- Configura i path / e /health-check
- Gestisce l'accesso esterno all'applicazione
