from flask import Flask
from datetime import datetime
import pytz
import os

app = Flask(__name__)

# Configurazione del fuso orario italiano
timezone = pytz.timezone('Europe/Rome')

@app.route('/')
def hello():
    # Ottiene il nome dell'agente dalla variabile d'ambiente o usa un default
    agent_name = os.getenv('AGENT_NAME', 'Flask')
    # Ottiene l'ora corrente nel fuso orario italiano
    current_time = datetime.now(timezone)
    formatted_time = current_time.strftime("%H:%M")
    return f"Ciao mi chiamo {agent_name}, sono le ore {formatted_time}"

@app.route('/health-check')
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone).isoformat()
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
