from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, tasks
from app.config import settings

app = FastAPI(title="Evolution of Todo API", version="1.0.0")

# TASK-013: CORS Configuration
origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include routers
app.include_router(health.router, prefix="/api")
from app.routes import auth
app.include_router(auth.router)
app.include_router(tasks.router)

