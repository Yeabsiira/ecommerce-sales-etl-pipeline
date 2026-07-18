from sqlalchemy import create_engine
from src.config import Config

def get_db_engine():
    """Creates and returns a secure SQLAlchemy database engine using the centralized Config class."""
    connection_string = Config.get_connection_string()
    try:
        engine = create_engine(connection_string)
        # Test connection instantly
        with engine.connect() as conn:
            print("🔌 Database Connection Gateway Established Successfully via Config!")
        return engine
    except Exception as e:
        raise ConnectionError(f"❌ Failed to connect to the database: {str(e)}")