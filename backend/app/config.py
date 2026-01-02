from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    database_url: str = ""
    better_auth_secret: str = ""
    cors_origins: str = ""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
        env_ignore_empty=True
    )

# Initialize settings, reading directly from environment variables (Vercel provides these)
# Use defaults to prevent validation errors
try:
    settings = Settings(
        database_url=os.getenv("DATABASE_URL", ""),
        better_auth_secret=os.getenv("BETTER_AUTH_SECRET", ""),
        cors_origins=os.getenv("CORS_ORIGINS", "https://frontend-xi-henna.vercel.app")
    )
except Exception as e:
    # Fallback to empty settings if initialization fails
    import sys
    print(f"Warning: Settings initialization failed: {e}", file=sys.stderr, flush=True)
    settings = Settings(
        database_url=os.getenv("DATABASE_URL", ""),
        better_auth_secret=os.getenv("BETTER_AUTH_SECRET", ""),
        cors_origins=os.getenv("CORS_ORIGINS", "https://frontend-xi-henna.vercel.app")
    )

