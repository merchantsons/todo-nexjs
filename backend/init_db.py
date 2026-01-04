from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import SQLModel, create_engine
from app.models import User, Task
import sys

class Settings(BaseSettings):
    database_url: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # Ignore extra fields like better_auth_secret, cors_origins
    )

settings = Settings()

# Enforce PostgreSQL only
if not settings.database_url.startswith(("postgresql://", "postgres://")):
    print(f"❌ ERROR: Only PostgreSQL databases are supported!", file=sys.stderr)
    print(f"   Current DATABASE_URL starts with: {settings.database_url[:30]}...", file=sys.stderr)
    print(f"   Please set DATABASE_URL to a PostgreSQL connection string", file=sys.stderr)
    sys.exit(1)

print(f"✅ Using PostgreSQL database: {settings.database_url.split('@')[1] if '@' in settings.database_url else 'configured'}", file=sys.stderr)
engine = create_engine(settings.database_url, echo=True)

def init_database():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()

