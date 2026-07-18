import os
from pathlib import Path
from dotenv import load_dotenv

# Find the root project directory and load the .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    @classmethod
    def get_connection_string(cls):
        """Constructs the standard PostgreSQL connection URI."""
        if not cls.DB_USER or not cls.DB_NAME or not cls.DB_PASSWORD:
            raise ValueError("❌ Missing database credentials in the .env file.")
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"