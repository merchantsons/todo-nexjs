# Vercel serverless function entry point for FastAPI
import sys
import traceback
import json

# Initialize handler variable
handler = None

try:
    # Import Mangum first
    from mangum import Mangum
    print("✅ Mangum imported", file=sys.stderr, flush=True)
    
    # Import the FastAPI app
    from app.main import app
    print("✅ FastAPI app imported", file=sys.stderr, flush=True)
    
    # Create Mangum handler for Vercel
    # Mangum converts ASGI (FastAPI) to AWS Lambda format (which Vercel uses)
    handler = Mangum(app, lifespan="off")
    print("✅ Mangum handler created", file=sys.stderr, flush=True)
    
except Exception as e:
    # If there's an import or initialization error, create a handler that returns the error
    error_msg = str(e)
    error_trace = traceback.format_exc()
    print(f"❌ Error initializing FastAPI app: {error_msg}", file=sys.stderr, flush=True)
    print(f"Traceback: {error_trace}", file=sys.stderr, flush=True)
    
    def error_handler(event, context):
        """Fallback handler that returns error information"""
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "error": "Server initialization failed",
                "message": error_msg,
                "type": type(e).__name__
            })
        }
    
    handler = error_handler

# Ensure handler is defined
if handler is None:
    def default_handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Handler not initialized"})
        }
    handler = default_handler

