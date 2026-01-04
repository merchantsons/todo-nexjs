"""
Ultra-simple handler to test if Vercel Python works at all
"""
def handler(event, context):
    """Simple handler that returns JSON"""
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": '{"message": "Handler works!", "status": "ok"}'
    }




