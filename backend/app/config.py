from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import sys

class Settings(BaseSettings):
    # Make database_url optional to avoid initialization errors
    # It will be checked at runtime when needed
    database_url: str = ""
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
    # First try to read from environment variables directly (Vercel provides these)
    database_url = os.getenv("DATABASE_URL", "")
    better_auth_secret = os.getenv("BETTER_AUTH_SECRET", "")
    cors_origins = os.getenv("CORS_ORIGINS", "")
    
    # Remove trailing slash from CORS_ORIGINS if present
    if cors_origins and cors_origins.endswith("/"):
        cors_origins = cors_origins.rstrip("/")
    
    # Initialize Settings with environment variables
    settings = Settings(
        database_url=database_url,
        better_auth_secret=better_auth_secret,
        cors_origins=cors_origins
    )
    
    print(f"✅ Settings initialized", file=sys.stderr, flush=True)
    print(f"   DATABASE_URL: {'set' if settings.database_url else 'missing'}", file=sys.stderr, flush=True)
    print(f"   BETTER_AUTH_SECRET: {'set' if settings.better_auth_secret else 'missing'}", file=sys.stderr, flush=True)
    print(f"   CORS_ORIGINS: {settings.cors_origins or 'not set'}", file=sys.stderr, flush=True)
    
except Exception as e:
    # Fallback to reading directly from environment variables if Settings fails
    print(f"⚠️ Warning: Settings initialization failed: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)
    
    # Create a minimal settings object
    settings = Settings(
        database_url=os.getenv("DATABASE_URL", ""),
        better_auth_secret=os.getenv("BETTER_AUTH_SECRET", ""),
        cors_origins=os.getenv("CORS_ORIGINS", "").rstrip("/")
    )

