"""
Configuration module for the FastAPI application.
Uses environment variables for configuration management.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings using Pydantic v2 BaseSettings."""

    # Application Configuration
    app_name: str = Field(default="AdvRAG Backend", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    
    # API Configuration
    api_title: str = Field(default="AdvRAG API", description="API title")
    api_description: str = Field(default="Advanced RAG Backend API", description="API description")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    reload: bool = Field(default=True, description="Auto-reload on code changes")
    
    # Supabase Configuration
    supabase_url: str = Field(..., description="Supabase project URL")
    supabase_key: str = Field(..., description="Supabase anon key")
    supabase_service_role_key: str = Field(..., description="Supabase service role key")
    
    # Database Configuration (Supabase PostgreSQL)
    database_url: str = Field(..., description="PostgreSQL database URL")
    database_pool_size: int = Field(default=20, description="Database connection pool size")
    database_max_overflow: int = Field(default=10, description="Max connections beyond pool size")
    database_pool_timeout: int = Field(default=30, description="Pool connection timeout in seconds")
    database_pool_recycle: int = Field(default=3600, description="Recycle connections after seconds")
    database_echo: bool = Field(default=False, description="Echo SQL statements")
    
    # Database Connection Retry Configuration
    db_max_retries: int = Field(default=3, description="Maximum retry attempts for DB connection")
    db_retry_delay: int = Field(default=2, description="Initial delay between retries in seconds")
    db_retry_backoff: int = Field(default=2, description="Backoff multiplier for retries")
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field(default="gpt-4-turbo-preview", description="OpenAI model name")
    openai_embedding_model: str = Field(default="text-embedding-3-small", description="Embedding model")
    openai_temperature: float = Field(default=0.7, description="Temperature for generation")
    openai_max_tokens: int = Field(default=2000, description="Max tokens for generation")
    
    # LangChain Configuration
    langchain_tracing_v2: bool = Field(default=False, description="Enable LangChain tracing")
    langchain_api_key: str | None = Field(default=None, description="LangChain API key")
    langchain_project: str = Field(default="advrag", description="LangChain project name")
    
    # Vector Store Configuration
    vector_store_type: str = Field(default="supabase", description="Vector store type")
    vector_dimension: int = Field(default=1536, description="Vector dimension")
    vector_collection_name: str = Field(default="documents", description="Collection name")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis URL")
    celery_broker_url: str = Field(default="redis://localhost:6379/0", description="Celery broker URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/1", description="Celery result backend")
    
    # Document Processing Configuration
    max_file_size_mb: int = Field(default=50, description="Maximum file size in MB")
    allowed_file_types: str = Field(default="pdf,txt,docx,md", description="Allowed file types")
    chunk_size: int = Field(default=1000, description="Text chunk size for embeddings")
    chunk_overlap: int = Field(default=200, description="Chunk overlap size")
    
    # Session Configuration
    session_timeout_minutes: int = Field(default=60, description="Session timeout in minutes")
    max_sessions_per_user: int = Field(default=10, description="Maximum sessions per user")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
