from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    database_url: str  # Required - must be PostgreSQL connection string
    better_auth_secret: str = ""
    cors_origins: str = ""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True
    )

# Initialize settings
# Pydantic-settings will automatically:
# 1. Read from .env file (if it exists) for local development
# 2. Read from environment variables (which Vercel provides in production)
# Environment variables take precedence over .env file values
try:
    settings = Settings()
except Exception as e:
    # Fallback to reading directly from environment variables if Settings fails
    import sys
    print(f"Warning: Settings initialization failed: {e}", file=sys.stderr, flush=True)
    settings = Settings(
        database_url=os.getenv("DATABASE_URL", ""),
        better_auth_secret=os.getenv("BETTER_AUTH_SECRET", ""),
        cors_origins=os.getenv("CORS_ORIGINS", "https://frontend-xi-henna.vercel.app")
    )

