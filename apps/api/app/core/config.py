"""Application configuration settings."""

from typing import List, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "AgentOps Nexus"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = "change-me-in-production-32-chars-min"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "postgresql://agentops:password@localhost:5432/agentops_nexus"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-large"

    # Anthropic
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"

    # Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-pro"

    # LiteLLM
    LITELLM_MASTER_KEY: str = ""
    LITELLM_API_BASE: str = "http://localhost:4000"

    # Enkrypt AI
    ENKRYPT_API_KEY: str = ""
    ENKRYPT_API_URL: str = "https://api.enkrypt.ai"

    # AgentOps
    AGENTOPS_API_KEY: str = ""

    # OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@agentopsnexus.com"

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "agentops-nexus"

    # Slack
    SLACK_BOT_TOKEN: str = ""
    SLACK_SIGNING_SECRET: str = ""

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    # MFA
    MFA_ISSUER: str = "AgentOps Nexus"
    TOTP_SECRET_LENGTH: int = 32

    # OpenTelemetry
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    OTEL_SERVICE_NAME: str = "agentops-nexus"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v


settings = Settings()
