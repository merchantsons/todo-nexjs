# Vercel serverless function entry point for FastAPI
from mangum import Mangum

# Import the FastAPI app
from app.main import app

# Create Mangum handler for Vercel
# Mangum converts ASGI (FastAPI) to AWS Lambda format (which Vercel uses)
handler = Mangum(app, lifespan="off")
