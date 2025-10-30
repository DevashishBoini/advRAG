"""
Configuration module for the FastAPI application.
Uses environment variables for configuration management.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings using Pydantic v2 BaseSettings."""

    app_name: str = "AdvRAG Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API Configuration
    api_title: str = "AdvRAG API"
    api_description: str = "Advanced RAG Backend API"
    api_version: str = "0.1.0"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
