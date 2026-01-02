from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint that doesn't require database connection"""
    try:
        # Check if environment variables are set (without accessing database)
        db_url_set = bool(os.getenv("DATABASE_URL"))
        secret_set = bool(os.getenv("BETTER_AUTH_SECRET"))
        cors_set = bool(os.getenv("CORS_ORIGINS"))
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "env_check": {
                "DATABASE_URL": "set" if db_url_set else "missing",
                "BETTER_AUTH_SECRET": "set" if secret_set else "missing",
                "CORS_ORIGINS": "set" if cors_set else "missing"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

