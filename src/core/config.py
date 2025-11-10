"""
Core configuration management using Pydantic Settings.
Handles environment variables and application settings.
"""
import os
from functools import lru_cache
from typing import Literal, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "Agentic AI Platform"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    reload: bool = True
    
    # LLM API Keys
    groq_api_key: str = Field(default="", description="Groq API Key")
    openai_api_key: str = Field(default="", description="OpenAI API Key")
    
    # Search Tools
    tavily_api_key: str = Field(default="", description="Tavily API Key")
    
    # LangSmith Tracing
    langchain_tracing_v2: bool = False
    langchain_endpoint: str = "https://api.smith.langchain.com"
    langchain_api_key: str = ""
    langchain_project: str = "agentic-ai-platform"
    
    # Security
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        min_length=32
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"]
    )
    allowed_methods: List[str] = Field(default=["*"])
    allowed_headers: List[str] = Field(default=["*"])
    
    # Database
    database_url: str = "sqlite:///./data/app.db"
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # Model Configuration
    default_llm_provider: Literal["groq", "openai"] = "groq"
    default_model: str = "llama-3.3-70b-versatile"
    default_temperature: float = 0.7
    default_max_tokens: int = 4096
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @property
    def is_development(self) -> bool:
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


def setup_langsmith():
    """Setup LangSmith tracing environment variables."""
    settings = get_settings()
    
    if settings.langchain_tracing_v2 and settings.langchain_api_key:
        os.environ["LANGCHAIN_TRACING_V2"] = str(settings.langchain_tracing_v2)
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint
        os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
        return True
    return False


# Global settings instance
settings = get_settings()

# Setup LangSmith on import
langsmith_enabled = setup_langsmith()
