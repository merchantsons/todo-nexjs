"""View all data in the database"""
import os
import sys
# Fix encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from app.dependencies.database import get_engine
from app.models import User, Task
from sqlmodel import Session, text, select

def main():
    print("=" * 60)
    print("Database Data Viewer")
    print("=" * 60)
    print()
    
    try:
        engine = get_engine()
        with Session(engine) as session:
            # Validate PostgreSQL connection
            db_url = os.getenv("DATABASE_URL") or ""
            if not db_url:
                from app.config import settings
                db_url = settings.database_url
            
            if not db_url.startswith(("postgresql://", "postgres://")):
                print("❌ Error: Only PostgreSQL databases are supported")
                print(f"   Current DATABASE_URL starts with: {db_url[:30] if db_url else 'empty'}...")
                return
            
            print(f"Database: PostgreSQL")
            print()
            
            # View Users
            print("-" * 60)
            print("USERS")
            print("-" * 60)
            users = session.exec(select(User)).all()
            if users:
                print(f"Total users: {len(users)}")
                print()
                for user in users:
                    print(f"  ID: {user.id}")
                    print(f"  Email: {user.email}")
                    print(f"  Created: {user.created_at}")
                    print()
            else:
                print("  No users found")
            print()
            
            # View Tasks
            print("-" * 60)
            print("TASKS")
            print("-" * 60)
            tasks = session.exec(select(Task)).all()
            if tasks:
                print(f"Total tasks: {len(tasks)}")
                print()
                for task in tasks:
                    print(f"  ID: {task.id}")
                    print(f"  User ID: {task.user_id}")
                    print(f"  Title: {task.title}")
                    print(f"  Description: {task.description or '(none)'}")
                    print(f"  Completed: {'Yes' if task.completed else 'No'}")
                    print(f"  Created: {task.created_at}")
                    print(f"  Updated: {task.updated_at}")
                    print()
            else:
                print("  No tasks found")
            print()
            
            # Summary
            print("=" * 60)
            print("SUMMARY")
            print("=" * 60)
            print(f"Users: {len(users)}")
            print(f"Tasks: {len(tasks)}")
            print()
            
            print("To view data in Neon dashboard:")
            print("1. Go to https://console.neon.tech")
            print("2. Select your project")
            print("3. Open your database")
            print("4. Click on 'SQL Editor' to run queries")
            print("5. Or click on 'Tables' to view data")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

