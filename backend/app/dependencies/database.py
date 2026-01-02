from sqlmodel import Session, create_engine
from app.config import settings
import os

# Create engine lazily to avoid connection errors at import time
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        # Get DATABASE_URL from environment directly (Vercel provides this)
        db_url = os.getenv("DATABASE_URL", "") or settings.database_url
        if not db_url:
            raise ValueError("DATABASE_URL environment variable is not set")
        _engine = create_engine(db_url, echo=False, pool_pre_ping=True)
    return _engine

def get_db_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

