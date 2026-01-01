from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import create_engine, text

class Settings(BaseSettings):
    database_url: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
engine = create_engine(settings.database_url, echo=False)

def verify_users_table():
    print("\n=== Users Table Structure ===")
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'users' 
                ORDER BY ordinal_position
            """)
        )
        print("Columns:")
        for row in result:
            print(f"  - {row[0]}: {row[1]} (nullable: {row[2]}, default: {row[3]})")

def verify_tasks_table():
    print("\n=== Tasks Table Structure ===")
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'tasks' 
                ORDER BY ordinal_position
            """)
        )
        print("Columns:")
        for row in result:
            print(f"  - {row[0]}: {row[1]} (nullable: {row[2]}, default: {row[3]})")

if __name__ == "__main__":
    verify_users_table()
    verify_tasks_table()

