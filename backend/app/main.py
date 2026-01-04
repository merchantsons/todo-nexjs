from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import os
import sys
import traceback

app = FastAPI(title="Evolution of Todo API", version="1.0.0")

# TASK-013: CORS Configuration - MUST be configured FIRST
# Read directly from environment (Vercel provides these)
try:
    # First try to get from settings (reads from .env file)
    from app.config import settings
    cors_origins_str = os.getenv("CORS_ORIGINS") or settings.cors_origins or "http://localhost:3000"
    
    # Remove trailing slashes from origins
    if cors_origins_str:
        cors_origins_str = cors_origins_str.rstrip("/")
    
    # Split and clean origins
    origins = [origin.strip().rstrip("/") for origin in cors_origins_str.split(",") if origin.strip()]
    
    # For local development, be more permissive - allow all localhost ports
    # This helps when frontend runs on different ports (3000, 3001, etc.)
    is_local_dev = any("localhost" in origin or "127.0.0.1" in origin for origin in origins) or not origins
    
    if is_local_dev and "*" not in origins:
        # Add common localhost ports for development
        localhost_origins = [
            "http://localhost:3000",
            "http://localhost:3001", 
            "http://localhost:3002",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "http://127.0.0.1:3002",
        ]
        for origin in localhost_origins:
            if origin not in origins:
                origins.append(origin)
    
    # In production (Vercel), if CORS_ORIGINS is not set or empty, allow all origins
    # This provides a fallback if environment variable is not configured
    # Note: In production, it's better to explicitly set CORS_ORIGINS for security
    if not origins:
        # Check if we're in production (Vercel) by checking for vercel environment
        is_vercel = os.getenv("VERCEL") == "1" or os.getenv("VERCEL_ENV")
        if is_vercel:
            # In Vercel production, allow all origins as fallback
            # But log a warning that CORS_ORIGINS should be set
            print("⚠️ Warning: CORS_ORIGINS not set in production. Allowing all origins.", file=sys.stderr, flush=True)
            origins = ["*"]
        else:
            # In local development, default to localhost
            origins = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]
    
    print(f"✅ CORS origins configured: {origins}", file=sys.stderr, flush=True)
except Exception as e:
    print(f"Warning: CORS config error: {e}", file=sys.stderr, flush=True)
    # Default to allow localhost for local development
    origins = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]

try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods including OPTIONS
        allow_headers=["*"],  # Allow all headers for development
        expose_headers=["*"],
        max_age=3600,  # Cache preflight requests for 1 hour
    )
    print("✅ CORS middleware added", file=sys.stderr, flush=True)
except Exception as e:
    print(f"Warning: CORS middleware error: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)

# Add explicit OPTIONS handler for all routes (backup for CORS preflight)
@app.options("/{full_path:path}")
async def options_handler(full_path: str, request: Request):
    """Handle OPTIONS requests for CORS preflight"""
    origin = request.headers.get("origin", "*")
    allowed_origin = origin if origin in origins else (origins[0] if origins else "*")
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": allowed_origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "3600",
        }
    )

# Exception handler for HTTPException - Add CORS headers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTPException with CORS headers"""
    import sys
    origin = request.headers.get("origin", "*")
    allowed_origin = origin if origin in origins else (origins[0] if origins else "*")
    
    # Ensure detail is a string
    detail = str(exc.detail) if exc.detail else "An error occurred"
    
    print(f"⚠️ HTTPException: {exc.status_code} - {detail}", file=sys.stderr, flush=True)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": detail},
        headers={
            "Access-Control-Allow-Origin": allowed_origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with CORS headers"""
    origin = request.headers.get("origin", "*")
    allowed_origin = origin if origin in origins else (origins[0] if origins else "*")
    
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
        headers={
            "Access-Control-Allow-Origin": allowed_origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

# Global exception handler - AFTER CORS middleware
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all unhandled exceptions and return proper error response with CORS headers"""
    error_msg = str(exc)
    error_trace = traceback.format_exc()
    print(f"❌ Unhandled exception: {error_msg}", file=sys.stderr, flush=True)
    print(f"Traceback: {error_trace}", file=sys.stderr, flush=True)
    
    # Get origin from request for CORS
    origin = request.headers.get("origin", "*")
    allowed_origin = origin if origin in origins else (origins[0] if origins else "*")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": error_msg,
            "type": type(exc).__name__
        },
        headers={
            "Access-Control-Allow-Origin": allowed_origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

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
