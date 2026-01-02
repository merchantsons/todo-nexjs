from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
import traceback

app = FastAPI(title="Evolution of Todo API", version="1.0.0")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all unhandled exceptions and return proper error response"""
    error_msg = str(exc)
    error_trace = traceback.format_exc()
    print(f"❌ Unhandled exception: {error_msg}", file=sys.stderr, flush=True)
    print(f"Traceback: {error_trace}", file=sys.stderr, flush=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": error_msg,
            "type": type(exc).__name__
        }
    )

# TASK-013: CORS Configuration
# Read directly from environment (Vercel provides these)
try:
    cors_origins_str = os.getenv("CORS_ORIGINS", "https://frontend-xi-henna.vercel.app")
    origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]
    if not origins:
        origins = ["*"]  # Fallback to allow all if not set
    print(f"✅ CORS origins configured: {origins}", file=sys.stderr, flush=True)
except Exception as e:
    print(f"Warning: CORS config error: {e}", file=sys.stderr, flush=True)
    origins = ["*"]

try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    print("✅ CORS middleware added", file=sys.stderr, flush=True)
except Exception as e:
    print(f"Warning: CORS middleware error: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)

# Include routers - health check first (doesn't need database)
try:
    from app.routes import health
    app.include_router(health.router, prefix="/api")
    print("✅ Health router loaded", file=sys.stderr, flush=True)
except Exception as e:
    print(f"❌ Error loading health router: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)

# Other routers (may need database)
try:
    from app.routes import auth
    app.include_router(auth.router)
    print("✅ Auth router loaded", file=sys.stderr, flush=True)
except Exception as e:
    print(f"❌ Error loading auth router: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)

try:
    from app.routes import tasks
    app.include_router(tasks.router)
    print("✅ Tasks router loaded", file=sys.stderr, flush=True)
except Exception as e:
    print(f"❌ Error loading tasks router: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)

print("✅ App initialization complete", file=sys.stderr, flush=True)

