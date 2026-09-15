import sys
import os

# This adds your root project folder to the path so imports like 
# 'from app import app' and 'from config import Config' work correctly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Flask app instance from your main app.py file
from app import app

# Vercel requires the WSGI application variable to be named exactly 'app'