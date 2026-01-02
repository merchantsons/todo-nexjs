# Vercel serverless function entry point for FastAPI
import sys
import traceback
import json
import os

# Initialize handler variable
_original_handler = None

try:
    # Import Mangum first
    from mangum import Mangum
    print("✅ Mangum imported", file=sys.stderr, flush=True)
    
    # Import the FastAPI app
    from app.main import app
    print("✅ FastAPI app imported", file=sys.stderr, flush=True)
    
    # Create Mangum handler for Vercel
    # Mangum converts ASGI (FastAPI) to AWS Lambda format (which Vercel uses)
    # Use lifespan="off" to avoid issues with startup/shutdown events
    _original_handler = Mangum(app, lifespan="off", log_level="info")
    print("✅ Mangum handler created", file=sys.stderr, flush=True)
    
except Exception as e:
    # If there's an import or initialization error, create a handler that returns the error
    error_msg = str(e)
    error_trace = traceback.format_exc()
    print(f"❌ Error initializing FastAPI app: {error_msg}", file=sys.stderr, flush=True)
    print(f"Traceback: {error_trace}", file=sys.stderr, flush=True)
    
    def error_handler(event, context):
        """Fallback handler that returns error information"""
        try:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "error": "Server initialization failed",
                    "message": error_msg,
                    "type": type(e).__name__
                })
            }
        except Exception as handler_error:
            print(f"❌ Error in error handler: {handler_error}", file=sys.stderr, flush=True)
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Critical server error"})
            }
    
    _original_handler = error_handler

# Ensure handler is defined
if _original_handler is None:
    def default_handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Handler not initialized"})
        }
    _original_handler = default_handler

# Wrap handler with additional error handling for runtime errors
def wrapped_handler(event, context):
    """Wrapper that catches runtime errors and returns proper error responses"""
    try:
        # Log request info for debugging
        if event:
            path = event.get("path", "unknown")
            method = event.get("httpMethod", "unknown")
            print(f"📥 Request: {method} {path}", file=sys.stderr, flush=True)
        
        # Call the original handler (Mangum handles async internally)
        result = _original_handler(event, context)
        
        # Handle if result is a coroutine (shouldn't happen with Mangum, but just in case)
        if hasattr(result, '__await__'):
            import asyncio
            try:
                # Try to get existing event loop
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # Create new event loop if none exists
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            result = loop.run_until_complete(result)
        
        # Ensure result is in correct format
        if isinstance(result, dict):
            return result
        else:
            print(f"⚠️ Handler returned unexpected type: {type(result)}", file=sys.stderr, flush=True)
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Invalid handler response"})
            }
            
    except Exception as runtime_error:
        # Catch any runtime errors
        error_msg = str(runtime_error)
        error_trace = traceback.format_exc()
        print(f"❌ Runtime error in handler: {error_msg}", file=sys.stderr, flush=True)
        print(f"Traceback: {error_trace}", file=sys.stderr, flush=True)
        
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Internal server error",
                "message": error_msg,
                "type": type(runtime_error).__name__
            })
        }

# Export the wrapped handler
handler = wrapped_handler

