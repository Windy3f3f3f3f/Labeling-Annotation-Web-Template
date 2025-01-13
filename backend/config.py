"""
Backend configuration settings
"""
import os

# Base directory of the backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database settings
DATABASE = {
    'path': os.path.join(BASE_DIR, 'database', 'database.db'),
}

# Server settings
SERVER = {
    'host': '0.0.0.0',  # Listen on all interfaces
    'port': 5000,
    'debug': True,  # Set to False in production
}

# CORS settings
CORS_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://YOUR_IP:port", # modify here!
] 
