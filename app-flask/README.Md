# Flask Time Display Application

## Overview
Questa è un'applicazione Flask che mostra l'ora corrente nel fuso orario italiano e include un endpoint di health check. L'applicazione è parte di un ambiente DevOps completo con CI/CD pipeline.

## Struttura dell'Applicazione

```
app-flask/
├── app.py              # Applicazione Flask principale
├── version.py          # Modulo per la gestione della versione
├── requirements.txt    # Dipendenze Python
├── Jenkinsfile         # Pipeline di CI/CD
└── helm-dist/          # Configurazione Helm per il deployment
```

## Funzionalità

### Endpoint
1. Root (`/`)
   * Mostra un messaggio di saluto con l'ora corrente
   * Il nome dell'agente è configurabile tramite variabile d'ambiente
   * Esempio: "Ciao mi chiamo Flask versione 20250314093024 sono le ore 14:30"

2. Health Check (`/health-check`)
   * Restituisce lo stato dell'applicazione
   * Formato: JSON
   ```json
   {
       "status": "healthy",
       "timestamp": "2024-02-20T14:30:00+01:00",
       "version": "20250314093024"
   }
   ```

### Rate Limiting
L'applicazione implementa rate limiting per proteggere gli endpoint:
* Massimo 100 richieste al minuto per indirizzo IP

## Requisiti
* Python 3.11 o superiore
* Flask 3.0.0
* pytz 2024.1
* Flask-Limiter 3.5.0
* Ruff 0.3.0 (per linting)
* Bandit 1.7.5 (per analisi di sicurezza)
* PyInstaller (per packaging)

## Ambiente di Sviluppo
L'applicazione è parte di un ambiente DevOps che include:
* Jenkins per CI/CD
* Nexus come repository
* GitLab per il controllo versione
* Kubernetes (via Minikube) per il deployment

### Setup dell'Ambiente
```bash
# Avvio dell'ambiente DevOps
docker-compose up -d

# Verifica dei servizi
docker ps
```

I servizi saranno disponibili su:
* Jenkins: http://localhost:8080
* Nexus: http://localhost:8081
* GitLab: http://localhost:80

## Pipeline CI/CD

### Processo di Build
La pipeline Jenkins:
1. Crea un ambiente Python virtuale e installa le dipendenze
2. Esegue controlli di codice con Ruff
3. Esegue analisi di sicurezza con Bandit
4. Aggiorna il numero di versione con timestamp
5. Compila l'applicazione con PyInstaller
6. Carica il binario su Nexus con versione timestamp e latest
7. Aggiorna il repository Git con il nuovo numero di versione e crea un tag

### Versionamento
Il sistema di versionamento utilizza timestamp nel formato YYYYMMDDHHmmSS:
* Esempio: 20250314093024
* Il numero di versione viene aggiornato automaticamente dalla pipeline Jenkins
* Il numero di versione è visibile negli endpoint dell'applicazione

## Deployment
Il deployment viene gestito tramite Helm su Kubernetes. Per i dettagli sulla configurazione Helm, vedere il README nella cartella `helm-dist/`.

### Comandi Base
```bash
# Sviluppo locale
python app.py

# Build manuale
pyinstaller --onefile app.py

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/health-check
```

## Variabili d'Ambiente
* `AGENT_NAME`: Nome dell'agente nel messaggio di saluto (default: "Fabi")
