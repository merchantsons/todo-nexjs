# Vercel serverless function entry point for FastAPI
import sys
import traceback
from mangum import Mangum

try:
    # Import the FastAPI app
    from app.main import app
    
    # Create Mangum handler for Vercel
    # Mangum converts ASGI (FastAPI) to AWS Lambda format (which Vercel uses)
    handler = Mangum(app, lifespan="off")
    
except Exception as e:
    # If there's an import or initialization error, create a handler that returns the error
    print(f"❌ Error initializing FastAPI app: {e}", file=sys.stderr, flush=True)
    traceback.print_exc(file=sys.stderr)
    
    def handler(event, context):
        """Fallback handler that returns error information"""
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"error": "Server initialization failed", "message": "{str(e)}"}}'
        }

