from mangum import Mangum
from app.main import app

# Vercel serverless function wrapper for FastAPI
# Mangum converts ASGI app to AWS Lambda format (which Vercel uses)
handler = Mangum(app, lifespan="off")
