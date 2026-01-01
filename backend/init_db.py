from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import SQLModel, create_engine
from app.models import User, Task

class Settings(BaseSettings):
    database_url: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # Ignore extra fields like better_auth_secret, cors_origins
    )

settings = Settings()
engine = create_engine(settings.database_url, echo=True)

def init_database():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()

