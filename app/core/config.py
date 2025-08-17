from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    app_name: str = "Mangodesk Notes Summarizer"
    app_env: str = "production"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    groq_api_key: str

    smtp_host: str
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    email_from: str = "no-reply@example.com"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
