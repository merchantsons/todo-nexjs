from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import sys
from pathlib import Path

# Get the backend directory (parent of app directory)
# This ensures .env file is found regardless of where uvicorn is started from
BACKEND_DIR = Path(__file__).parent.parent
ENV_FILE = BACKEND_DIR / ".env"

class Settings(BaseSettings):
    # Make database_url optional to avoid initialization errors
    # It will be checked at runtime when needed
    database_url: str = ""
    better_auth_secret: str = ""
    cors_origins: str = ""
    
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True
    )

# Initialize settings
# Pydantic-settings will automatically:
# 1. Read from environment variables first (which Vercel provides in production)
# 2. Fall back to .env file (if it exists) for local development
# Environment variables take precedence over .env file values
try:
    # Initialize Settings - it will automatically read from:
    # 1. Environment variables (os.getenv) - highest priority
    # 2. .env file - fallback if env vars not set
    # The SettingsConfigDict with env_file=".env" handles this automatically
    settings = Settings()
    
    # Remove trailing slash from CORS_ORIGINS if present
    if settings.cors_origins and settings.cors_origins.endswith("/"):
        settings.cors_origins = settings.cors_origins.rstrip("/")
    
    print(f"✅ Settings initialized", file=sys.stderr, flush=True)
    print(f"   DATABASE_URL: {'set' if settings.database_url else 'missing'}", file=sys.stderr, flush=True)
    print(f"   BETTER_AUTH_SECRET: {'set' if settings.better_auth_secret else 'missing'}", file=sys.stderr, flush=True)
    print(f"   CORS_ORIGINS: {settings.cors_origins or 'not set'}", file=sys.stderr, flush=True)
    
except Exception as e:
    # Fallback to reading directly from environment variables if Settings fails
    print(f"⚠️ Warning: Settings initialization failed: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)
    
    # Create a minimal settings object with fallback
    cors_origins = os.getenv("CORS_ORIGINS", "").rstrip("/")
    settings = Settings(
        database_url=os.getenv("DATABASE_URL", ""),
        better_auth_secret=os.getenv("BETTER_AUTH_SECRET", ""),
        cors_origins=cors_origins
    )

