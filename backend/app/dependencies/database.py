from sqlmodel import Session, create_engine
from app.config import settings
import os
import sys

# Create engine lazily to avoid connection errors at import time
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        # Get DATABASE_URL from environment directly (Vercel provides this)
        db_url = os.getenv("DATABASE_URL", "") or settings.database_url
        if not db_url:
            error_msg = "DATABASE_URL environment variable is not set"
            print(f"❌ {error_msg}", file=sys.stderr, flush=True)
            raise ValueError(error_msg)
        
        try:
            # For serverless, use connection pooling with appropriate settings
            # pool_pre_ping=True ensures connections are validated before use
            # pool_size and max_overflow set to 1 for serverless (single connection)
            _engine = create_engine(
                db_url, 
                echo=False, 
                pool_pre_ping=True,
                pool_size=1,
                max_overflow=0,
                pool_recycle=300,  # Recycle connections after 5 minutes
                connect_args={
                    "connect_timeout": 10,  # 10 second connection timeout
                    "sslmode": "require" if "postgres" in db_url.lower() else None
                } if "postgres" in db_url.lower() else {}
            )
            print("✅ Database engine created", file=sys.stderr, flush=True)
        except Exception as e:
            error_msg = f"Failed to create database engine: {str(e)}"
            print(f"❌ {error_msg}", file=sys.stderr, flush=True)
            raise
    
    return _engine

def get_db_session():
    """Get database session with error handling"""
    try:
        engine = get_engine()
        with Session(engine) as session:
            yield session
    except Exception as e:
        error_msg = f"Database session error: {str(e)}"
        print(f"❌ {error_msg}", file=sys.stderr, flush=True)
        # Re-raise to let FastAPI handle it properly
        raise

