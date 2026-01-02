"""
Minimal test handler to verify Vercel Python function works
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Test endpoint works", "status": "ok"}

@app.get("/test")
async def test():
    import os
    return {
        "message": "Test successful",
        "env_vars": {
            "DATABASE_URL": "set" if os.getenv("DATABASE_URL") else "missing",
            "BETTER_AUTH_SECRET": "set" if os.getenv("BETTER_AUTH_SECRET") else "missing",
            "CORS_ORIGINS": "set" if os.getenv("CORS_ORIGINS") else "missing"
        }
    }

from mangum import Mangum
handler = Mangum(app)


