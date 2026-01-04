"""Check which database is actually being used and verify connection"""
import os
import sys
# Fix encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from app.config import settings
from app.dependencies.database import get_engine
from sqlmodel import text

def main():
    print("=" * 60)
    print("Database Connection Diagnostic")
    print("=" * 60)
    print()
    
    # Check environment variable
    env_db_url = os.getenv("DATABASE_URL")
    print(f"1. Environment Variable (DATABASE_URL):")
    if env_db_url:
        # Mask password in connection string
        masked = mask_connection_string(env_db_url)
        print(f"   [OK] SET: {masked}")
        print(f"   Database Type: {get_database_type(env_db_url)}")
        print(f"   Database Name: {get_database_name(env_db_url)}")
    else:
        print(f"   [X] NOT SET")
    print()
    
    # Check settings (from .env file)
    settings_db_url = settings.database_url
    print(f"2. Settings (.env file):")
    if settings_db_url:
        masked = mask_connection_string(settings_db_url)
        print(f"   [OK] SET: {masked}")
        print(f"   Database Type: {get_database_type(settings_db_url)}")
        print(f"   Database Name: {get_database_name(settings_db_url)}")
    else:
        print(f"   [X] NOT SET")
    print()
    
    # Check which one is actually being used (priority: env > settings)
    actual_db_url = env_db_url or settings_db_url
    print(f"3. Actual Database Being Used:")
    if actual_db_url:
        masked = mask_connection_string(actual_db_url)
        print(f"   {masked}")
        print(f"   Database Type: {get_database_type(actual_db_url)}")
        print(f"   Database Name: {get_database_name(actual_db_url)}")
    else:
        print(f"   [X] NO DATABASE CONFIGURED")
        return
    print()
    
            # Test connection
    print(f"4. Testing Connection:")
    try:
        # Validate PostgreSQL connection string
        if not actual_db_url.startswith(("postgresql://", "postgres://")):
            print(f"   [X] Invalid database type. Only PostgreSQL is supported.")
            print(f"   Current DATABASE_URL starts with: {actual_db_url[:30]}...")
            return
        
        engine = get_engine()
        with engine.connect() as conn:
            # Get database name from connection
            result = conn.execute(text("SELECT current_database();"))
            db_name = result.scalar()
            print(f"   [OK] Connected to PostgreSQL database: {db_name}")
            
            # Check tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            tables = [row[0] for row in result]
            print(f"   Tables found: {', '.join(tables) if tables else 'None'}")
            
            # Check data in users table
            if 'users' in tables:
                result = conn.execute(text("SELECT COUNT(*) FROM users;"))
                user_count = result.scalar()
                print(f"   Users in database: {user_count}")
            
            # Check data in tasks table
            if 'tasks' in tables:
                result = conn.execute(text("SELECT COUNT(*) FROM tasks;"))
                task_count = result.scalar()
                print(f"   Tasks in database: {task_count}")
    except Exception as e:
        print(f"   [X] Connection failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("Recommendations:")
    print("=" * 60)
    
    if not actual_db_url.startswith(("postgresql://", "postgres://")):
        print("[!] Only PostgreSQL databases are supported!")
        print("   Please set DATABASE_URL to a PostgreSQL connection string:")
        print("   postgresql://user:password@host:port/database?sslmode=require")
        return
    
    db_name = get_database_name(actual_db_url)
    print("[OK] You are connected to PostgreSQL")
    print(f"   Database name: {db_name}")
    print("   If data is not showing in Neon dashboard:")
    print("   1. Make sure you're viewing the correct database")
    print("   2. Check if transactions are being committed (they should be)")
    print("   3. Refresh the Neon dashboard")

def mask_connection_string(url: str) -> str:
    """Mask password in connection string"""
    if "@" in url:
        parts = url.split("@")
        if "://" in parts[0]:
            protocol_user = parts[0]
            if ":" in protocol_user:
                protocol, user_pass = protocol_user.split("://", 1)
                if ":" in user_pass:
                    user, _ = user_pass.split(":", 1)
                    return f"{protocol}://{user}:***@{parts[1]}"
    return url

def get_database_type(url: str) -> str:
    """Extract database type from connection string"""
    if url.startswith("postgresql://") or url.startswith("postgres://"):
        return "PostgreSQL"
    else:
        return "Unknown (Only PostgreSQL supported)"

def get_database_name(url: str) -> str:
    """Extract database name from connection string"""
    try:
        if url.startswith(("postgresql://", "postgres://")):
            # PostgreSQL: postgresql://user:pass@host:port/dbname
            if "/" in url:
                parts = url.split("/")
                if len(parts) > 1:
                    db_part = parts[-1]
                    # Remove query parameters
                    if "?" in db_part:
                        db_part = db_part.split("?")[0]
                    return db_part
    except:
        pass
    return "unknown"

if __name__ == "__main__":
    main()

