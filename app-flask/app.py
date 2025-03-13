from flask import Flask, request
from datetime import datetime
import pytz
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Rate limiting configuration - 100 requests per minute
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://"
)

# Italian timezone configuration
timezone = pytz.timezone('Europe/Rome')

# Get version from version.info file
def get_version():
    try:
        with open('version.info', 'r') as version_file:
            return version_file.read().strip()
    except FileNotFoundError:
        return "1.0.0"  # Default version if file not found

@app.route('/')
@limiter.limit("100 per minute")
def hello():
    # Get agent name from environment variable or use default
    agent_name = os.getenv('AGENT_NAME', 'Flask')
    # Get current time in Italian timezone
    current_time = datetime.now(timezone)
    formatted_time = current_time.strftime("%H:%M")
    # Get version from file
    version = get_version()
    return f"Ciao, mi chiamo {agent_name} versione {version} sono le ore {formatted_time}"

@app.route('/health-check')
@limiter.limit("100 per minute")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone).isoformat(),
        "version": get_version()
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
