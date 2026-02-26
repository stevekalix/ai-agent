"""
Configuration settings for the AI Agent System
Supports environment variables and .env files
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings"""

    # App Configuration
    APP_NAME: str = "AI Agent System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # CORS Configuration
    CORS_ORIGINS: List[str] = ["*"]

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./ai_agent.db"

    # Agent Configuration
    MAX_CONVERSATION_HISTORY: int = 50
    AGENT_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create global settings instance
settings = Settings()

