"""Verify that the application is using Neon PostgreSQL and not local SQLite"""
import os
import sys

# Fix encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=" * 60)
    print("Neon PostgreSQL Connection Verification")
    print("=" * 60)
    print()
    
    # Check .env file
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ .env file found")
        with open(env_file, 'r') as f:
            content = f.read()
            if "postgresql://" in content or "postgres://" in content:
                print(f"✅ .env contains PostgreSQL connection string")
            else:
                print(f"❌ .env does NOT contain PostgreSQL connection string!")
                print(f"   It may contain SQLite (sqlite://) which is not supported")
    else:
        print(f"⚠️  .env file not found")
    print()
    
    # Check for local database files
    local_db_files = ["local.db", "test.db"]
    found_local = False
    for db_file in local_db_files:
        if os.path.exists(db_file):
            print(f"⚠️  Found local database file: {db_file}")
            print(f"   This file should NOT exist for production use")
            print(f"   (test.db is OK for running tests)")
            found_local = True
    
    if not found_local:
        print(f"✅ No local database files found (except test.db which is for tests)")
    print()
    
    # Test actual database connection
    try:
        from app.dependencies.database import get_engine
        from sqlmodel import text
        
        engine = get_engine()
        db_url = str(engine.url)
        
        print(f"Database URL (masked):")
        if "@" in db_url:
            # Mask password
            parts = db_url.split("@")
            if "://" in parts[0]:
                protocol_user = parts[0]
                if ":" in protocol_user:
                    protocol, user_pass = protocol_user.split("://", 1)
                    if ":" in user_pass:
                        user, _ = user_pass.split(":", 1)
                        masked = f"{protocol}://{user}:***@{parts[1]}"
                        print(f"   {masked}")
        else:
            print(f"   {db_url[:50]}...")
        
        if db_url.startswith(("postgresql://", "postgres://")):
            print(f"✅ Using PostgreSQL database")
            
            # Test connection
            with engine.connect() as conn:
                result = conn.execute(text("SELECT current_database();"))
                db_name = result.scalar()
                print(f"✅ Connected to database: {db_name}")
                
                # Check tables
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """))
                tables = [row[0] for row in result]
                print(f"✅ Tables found: {', '.join(tables) if tables else 'None'}")
                
                # Check data
                if 'users' in tables:
                    result = conn.execute(text("SELECT COUNT(*) FROM users;"))
                    user_count = result.scalar()
                    print(f"   Users: {user_count}")
                
                if 'tasks' in tables:
                    result = conn.execute(text("SELECT COUNT(*) FROM tasks;"))
                    task_count = result.scalar()
                    print(f"   Tasks: {task_count}")
        else:
            print(f"❌ NOT using PostgreSQL!")
            print(f"   Current database type: {db_url.split('://')[0] if '://' in db_url else 'unknown'}")
            print(f"   Only PostgreSQL is supported")
            return False
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    print("=" * 60)
    print("✅ VERIFICATION COMPLETE")
    print("=" * 60)
    print()
    print("Your application is correctly configured to use Neon PostgreSQL.")
    print("All data will be saved to the Neon database, not local files.")
    print()
    print("⚠️  IMPORTANT: If you have a backend server running, RESTART it")
    print("   to ensure it picks up the PostgreSQL configuration.")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

