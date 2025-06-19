# backend/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql://inventory:password123@db:5432/parts_db"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
