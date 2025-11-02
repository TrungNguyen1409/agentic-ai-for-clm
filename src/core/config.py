"""Configuration management for the multi-agent CLM system."""

from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM Configuration
    openai_api_key: str = Field(default="", description="OpenAI API key")
    anthropic_api_key: str = Field(default="", description="Anthropic API key")
    llm_provider: Literal["openai", "anthropic"] = Field(
        default="openai",
        description="LLM provider to use"
    )
    llm_model: str = Field(
        default="gpt-4-turbo-preview",
        description="Model name"
    )

    # AWS Configuration
    aws_access_key_id: str = Field(default="", description="AWS access key")
    aws_secret_access_key: str = Field(default="", description="AWS secret key")
    aws_region: str = Field(default="us-east-1", description="AWS region")

    # Supabase Configuration
    supabase_url: str = Field(default="", description="Supabase project URL")
    supabase_key: str = Field(default="", description="Supabase anon key")
    supabase_service_key: str = Field(default="", description="Supabase service key")

    # LangFuse Configuration
    langfuse_public_key: str = Field(default="", description="LangFuse public key")
    langfuse_secret_key: str = Field(default="", description="LangFuse secret key")
    langfuse_host: str = Field(
        default="https://cloud.langfuse.com",
        description="LangFuse host URL"
    )

    # Application Settings
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    max_retries: int = Field(default=3, description="Max retry attempts")
    timeout: int = Field(default=30, description="Request timeout in seconds")

    # Agent Configuration
    enable_risk_agent: bool = Field(default=True, description="Enable Risk Analysis Agent")
    enable_clause_agent: bool = Field(default=True, description="Enable Clause Alignment Agent")
    enable_obligation_agent: bool = Field(default=True, description="Enable Obligation Tracking Agent")
    enable_dependency_agent: bool = Field(default=True, description="Enable Dependency Graph Agent")

    # Vector Database
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="Embedding model name"
    )
    vector_dimension: int = Field(default=1536, description="Vector embedding dimension")
    similarity_threshold: float = Field(
        default=0.7,
        description="Similarity threshold for retrieval"
    )

    # Document Processing
    ocr_enabled: bool = Field(default=True, description="Enable OCR processing")
    max_file_size_mb: int = Field(default=50, description="Maximum file size in MB")
    supported_formats: str = Field(
        default="pdf,docx,doc,txt",
        description="Supported file formats"
    )

    @property
    def supported_formats_list(self) -> list[str]:
        """Return supported formats as a list."""
        return [fmt.strip() for fmt in self.supported_formats.split(",")]


# Global settings instance
settings = Settings()
