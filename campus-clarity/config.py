import os
from dotenv import load_dotenv

# .env file se saari secret values load karega (API key waghera)
load_dotenv()

class Config:
    # Gemini API key - .env file se aayegi, kabhi bhi seedha yahan mat likhna
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    # SQLite database ka path - project folder ke andar hi "database.db" naam se banegi
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask ke forms/sessions ke liye secret key (kuch bhi random string chalega)
    SECRET_KEY = os.environ.get("SECRET_KEY", "campus-clarity-dev-key")
