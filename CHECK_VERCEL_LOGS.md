# 🔍 How to Check Vercel Function Logs

## The backend is still crashing. We need to see the actual error.

## Steps to View Logs

### Method 1: Vercel Dashboard (Easiest)

1. **Go to Backend Project**:
   - https://vercel.com/merchantsons-projects/backend

2. **View Latest Deployment**:
   - Click on the latest deployment (top of the list)

3. **View Function Logs**:
   - Click **"Logs"** tab or **"View Function Logs"** button
   - Look for Python errors, tracebacks, or import errors

4. **Look for**:
   - `Error importing app: ...`
   - `ModuleNotFoundError`
   - `ImportError`
   - `ValidationError`
   - Any Python traceback

### Method 2: Vercel CLI

```bash
cd backend
vercel logs https://backend-nine-sigma-81.vercel.app
```

## What to Look For

Common errors you might see:

1. **Import Errors**:
   - `ModuleNotFoundError: No module named '...'`
   - Solution: Check `requirements.txt` has all dependencies

2. **Environment Variable Errors**:
   - `ValidationError` from pydantic
   - Solution: Verify all 3 env vars are set in Dashboard

3. **Database Connection Errors**:
   - `OperationalError` or connection timeout
   - Solution: Check DATABASE_URL is correct

4. **Settings Initialization Errors**:
   - Errors when creating Settings object
   - Solution: Environment variables not accessible

## Share the Error

Once you see the logs, please share:
- The error message
- The full traceback (if any)
- Which line is failing

This will help identify the exact issue!

---

**The logs will tell us exactly what's wrong!** Please check them and share the error message.


