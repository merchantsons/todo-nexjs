from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    better_auth_secret: str
    cors_origins: str
    
    class Config:
        env_file = ".env"

settings = Settings()

