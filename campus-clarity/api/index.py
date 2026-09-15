import sys
import os

# CRITICAL: Add the root directory to the system path 
# so this file can import app.py, config.py, models.py, etc.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Vercel runs code from the 'api' folder, so we must explicitly 
# tell Flask where the templates and static folders are located in the root.
app.template_folder = os.path.join(os.path.dirname(__file__), '..', 'templates')
app.static_folder = os.path.join(os.path.dirname(__file__), '..', 'static')

# If your app uses SQLite, ensure it looks in the root 'instance' folder
app.instance_path = os.path.join(os.path.dirname(__file__), '..', 'instance')

# Vercel's Python runtime automatically looks for a variable named 'app' 
# to serve as the WSGI application.