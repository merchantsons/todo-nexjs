"""
Ultra-simple handler to test if Vercel Python works at all
Vercel Python functions should export a 'handler' function
"""
import json

def handler(request):
    """
    Vercel Python handler
    request is a Request object from Vercel
    """
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Handler works!", "status": "ok"})
    }

