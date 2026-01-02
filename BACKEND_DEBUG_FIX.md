# 🔧 Backend Debugging & Fix Guide

## Current Situation
- ✅ Backend deployed at: `https://todo-nextjs-backend.vercel.app/`
- ❌ Backend not responding or returning errors
- ✅ Frontend code updated to use correct backend URL

## Step 1: Test Backend Health Endpoint

First, verify if the backend is accessible:

1. **Health Check**: Visit https://todo-nextjs-backend.vercel.app/api/health
   - Should return: `{"status": "healthy", ...}`
   - If it returns an error, note the error message

2. **API Docs**: Visit https://todo-nextjs-backend.vercel.app/docs
   - Should show Swagger UI
   - If it doesn't load, the backend has an initialization error

## Step 2: Check Vercel Function Logs

**This is the most important step to diagnose the issue:**

1. Go to: https://vercel.com/dashboard
2. Find your **backend** project (todo-nextjs-backend)
3. Click on the **latest deployment**
4. Click the **"Logs"** tab (NOT "Build Logs")
5. **Make a request** to the backend (visit the health endpoint)
6. **Watch the logs** - you'll see Python errors appear

### What to Look For:

The logs will show errors like:
- `ModuleNotFoundError: No module named 'xyz'`
- `ImportError: cannot import name 'xyz'`
- `ValidationError: ...`
- `OperationalError: ...` (database connection)
- `BETTER_AUTH_SECRET not configured`
- `DATABASE_URL environment variable is not set`

**Copy and share the error message** - it will tell us exactly what's wrong!

## Step 3: Verify Backend Environment Variables

Go to: **Vercel Dashboard → Backend Project → Settings → Environment Variables**

Verify these 3 variables are set for **Production**:

### Variable 1: DATABASE_URL
- **Key**: `DATABASE_URL`
- **Value**: Your Neon PostgreSQL connection string
- **Format**: `postgresql://username:password@host:port/database?sslmode=require`
- ⚠️ **Get this from your Neon dashboard**
- ⚠️ **Must be set for Production environment**

### Variable 2: BETTER_AUTH_SECRET
- **Key**: `BETTER_AUTH_SECRET`
- **Value**: A secure random string
- **Generate**: `openssl rand -base64 32` (or use any secure random generator)
- ⚠️ **Must match the frontend `BETTER_AUTH_SECRET`**
- ⚠️ **Must be set for Production environment**

### Variable 3: CORS_ORIGINS
- **Key**: `CORS_ORIGINS`
- **Value**: Your frontend URL (e.g., `https://your-frontend.vercel.app`)
- ⚠️ **Must include your frontend URL to allow CORS**
- ⚠️ **Must be set for Production environment**

## Step 4: Common Issues & Solutions

### Issue 1: ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'mangum'` (or other module)

**Solution**:
1. Check `backend/requirements.txt` includes all dependencies
2. Verify the file is in the root of the backend directory
3. Redeploy the backend

### Issue 2: Missing Environment Variables

**Error**: `DATABASE_URL environment variable is not set` or `BETTER_AUTH_SECRET not configured`

**Solution**:
1. Go to Vercel Dashboard → Backend → Settings → Environment Variables
2. Add the missing variables
3. Make sure to select **Production** environment
4. Redeploy the backend

### Issue 3: Database Connection Error

**Error**: `OperationalError` or database connection timeout

**Solution**:
1. Verify `DATABASE_URL` is correct
2. Check if your Neon database allows connections from Vercel
3. Ensure the connection string includes `?sslmode=require`
4. Test the connection string locally if possible

### Issue 4: Handler Not Found

**Error**: 404 or handler not working

**Solution**:
1. Verify `backend/vercel.json` exists and is correct
2. Verify `backend/api/index.py` exists
3. Check that the handler is exported correctly

### Issue 5: CORS Errors

**Error**: CORS policy blocking requests from frontend

**Solution**:
1. Set `CORS_ORIGINS` environment variable to your frontend URL
2. Include the exact frontend URL (e.g., `https://your-frontend.vercel.app`)
3. Redeploy backend

## Step 5: Test Minimal Handler

If the backend still doesn't work, test with a minimal handler:

1. **Backup current handler**:
   ```bash
   cd backend
   mv api/index.py api/index.py.backup
   ```

2. **Use simple test handler**:
   ```bash
   cp api/test.py api/index.py
   ```

3. **Redeploy**:
   ```bash
   vercel --prod
   ```

4. **Test**: https://todo-nextjs-backend.vercel.app/test

**If test handler works**: The issue is in the main app code
**If test handler fails**: The issue is with Vercel Python setup

## Step 6: Verify Frontend Environment Variable

Make sure the frontend has the correct backend URL:

1. Go to: **Vercel Dashboard → Frontend Project → Settings → Environment Variables**
2. Verify `NEXT_PUBLIC_API_URL` is set to: `https://todo-nextjs-backend.vercel.app`
   - ⚠️ **NO trailing slash**
   - ⚠️ **Must be set for Production environment**
3. Redeploy frontend if you changed it

## Step 7: Redeploy After Fixes

After fixing environment variables or code:

1. **Backend**: Go to Deployments → Click "..." → Redeploy
2. **Frontend**: Go to Deployments → Click "..." → Redeploy
3. Wait 1-2 minutes for deployment to complete
4. Test again

## Quick Diagnostic Checklist

- [ ] Backend health endpoint accessible: https://todo-nextjs-backend.vercel.app/api/health
- [ ] Backend API docs accessible: https://todo-nextjs-backend.vercel.app/docs
- [ ] `DATABASE_URL` environment variable set in Vercel
- [ ] `BETTER_AUTH_SECRET` environment variable set in Vercel
- [ ] `CORS_ORIGINS` environment variable set in Vercel
- [ ] All environment variables set for **Production** environment
- [ ] `NEXT_PUBLIC_API_URL` in frontend set to `https://todo-nextjs-backend.vercel.app`
- [ ] Both projects redeployed after changes
- [ ] Checked Vercel function logs for errors

## Next Steps

1. **Check the Vercel logs** (most important!)
2. **Share the error message** from the logs
3. **Verify environment variables** are set correctly
4. **Test the health endpoint** directly in browser
5. **Redeploy** after making changes

---

**The Vercel function logs will show the exact error. Please check them and share what you find!**

