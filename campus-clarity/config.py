import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Use environment variable or fallback to a default
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-default-secret-key'
    
    # Database URI: Use external DB if provided, otherwise fallback to local SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Gemini API Key
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')