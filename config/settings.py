# API credentials
import os
from pathlib import Path
import logging
import logging.config

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# Create necessary directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DATA_DIR / "filings", exist_ok=True)
os.makedirs(DATA_DIR / "processed", exist_ok=True)
os.makedirs(DATA_DIR / "vector_store", exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'app.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'agents': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Configure logging
logging.config.dictConfig(LOGGING)

# SEC API settings
SEC_USER_AGENT = os.environ.get("SEC_USER_AGENT", "YourCompanyName yourname@email.com")
SEC_RATE_LIMIT_SLEEP = 0.1  # Time to sleep between SEC API calls in seconds

# LLM settings
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "ollama")
LLM_MODEL = os.environ.get("LLM_MODEL", "mistral")

# Analysis settings
DEFAULT_YEARS_HISTORY = 5
MAX_DOCUMENTS_TO_PROCESS = 10
CACHE_ENABLED = True
