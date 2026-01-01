from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import create_engine, text
from app.models import User, Task

class Settings(BaseSettings):
    database_url: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
engine = create_engine(settings.database_url, echo=False)

def check_tables():
    print("Connecting to Neon database...")
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            )
            tables = [row[0] for row in result]
            
            print(f"\nExisting tables: {tables if tables else 'None'}")
            print(f"Users table exists: {'users' in tables}")
            print(f"Tasks table exists: {'tasks' in tables}")
            
            if 'users' not in tables or 'tasks' not in tables:
                print("\n[WARNING] Missing tables detected!")
                return False
            else:
                print("\n[SUCCESS] All required tables exist!")
                return True
    except Exception as e:
        print(f"\n[ERROR] Error checking tables: {e}")
        return False

if __name__ == "__main__":
    check_tables()

