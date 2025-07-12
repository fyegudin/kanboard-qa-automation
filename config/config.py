import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_URL = os.getenv("APP_URL", "http://localhost:8080")
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "database": os.getenv("DB_NAME", "kanboard"),
        "user": os.getenv("DB_USER", "kanboard"),
        "password": os.getenv("DB_PASSWORD", "kanboard123")
    }

    HEADLESS = os.getenv("HEADFUL", "False").strip().lower() != "true"
    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

DB_CONFIG = Config.DB_CONFIG