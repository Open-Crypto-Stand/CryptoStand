from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Settings(BaseSettings):
    port: int = 8000

    postgres_user: str = os.getenv("POSTGRES_USER", "user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "password")
    postgres_db: str = os.getenv("POSTGRES_DB", "name")
    postgres_dbname: str = os.getenv("POSTGRES_DBNAME", "dbname")
    postgres_port: int = os.getenv("POSTGRES_PORT", 5432)
    postgres_url: str = f"postgresql://{postgres_user}:{postgres_password}@{postgres_db}:{postgres_port}/{postgres_dbname}"
    
    token: str = ""

settings = Settings()