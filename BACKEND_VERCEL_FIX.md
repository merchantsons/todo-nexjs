# 🔧 Backend Vercel Connection Fix Guide

## Problem
Frontend showing error: "Cannot connect to backend server at https://todo-nextjs-backend.vercel.app/"

## Root Cause
The backend is deployed at `https://todo-nextjs-backend.vercel.app/` but is not responding or returning errors. The frontend code has been updated to use the correct backend URL.

## Solution Steps

### Step 1: Fix Frontend Environment Variable

1. Go to Vercel Dashboard: https://vercel.com/dashboard
2. Select your **frontend** project
3. Go to **Settings** → **Environment Variables**
4. Find `NEXT_PUBLIC_API_URL`
5. **Remove** the existing variable if it's set to `https://todo-nextjs-backend.vercel.app/`
6. **Add** a new variable:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://todo-nextjs-backend.vercel.app` (NO trailing slash)
   - **Environment**: Select **Production**, **Preview**, and **Development**
7. Click **Save**

### Step 2: Verify Backend is Working

Test the backend health endpoint:
- Visit: https://todo-nextjs-backend.vercel.app/api/health
- Should return: `{"status": "healthy", ...}`

If the backend returns an error:

#### Check Backend Environment Variables

1. Go to Vercel Dashboard
2. Select your **backend** project
3. Go to **Settings** → **Environment Variables**
4. Verify these 3 variables are set for **Production**:

   **Variable 1:**
   - Key: `DATABASE_URL`
   - Value: Your Neon PostgreSQL connection string
   - Format: `postgresql://username:password@host:port/database?sslmode=require`
   - ⚠️ Get this from your Neon dashboard

   **Variable 2:**
   - Key: `BETTER_AUTH_SECRET`
   - Value: A secure random string (e.g., generate with `openssl rand -base64 32`)
   - ⚠️ Must match the frontend `BETTER_AUTH_SECRET`

   **Variable 3:**
   - Key: `CORS_ORIGINS`
   - Value: `https://frontend-xi-henna.vercel.app` (or your frontend URL)
   - ⚠️ Must include your frontend URL

#### Check Backend Logs

1. Go to your backend project in Vercel Dashboard
2. Click on the **latest deployment**
3. Click **"Logs"** tab
4. Look for errors like:
   - `ModuleNotFoundError`
   - `ImportError`
   - `ValidationError`
   - Database connection errors

### Step 3: Redeploy Both Projects

After fixing environment variables:

**Frontend:**
1. Go to frontend project → **Deployments**
2. Click **...** on latest deployment
3. Click **Redeploy**

**Backend:**
1. Go to backend project → **Deployments**
2. Click **...** on latest deployment
3. Click **Redeploy**

### Step 4: Clear Browser Cache

The old JavaScript bundle might be cached:
- **Chrome/Edge**: `Ctrl+Shift+Delete` → Clear cached images and files
- **Or**: Hard refresh with `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- **Or**: Open in Incognito/Private window

## Verification Checklist

After fixing:

- [ ] `NEXT_PUBLIC_API_URL` is set to `https://todo-nextjs-backend.vercel.app` (no trailing slash)
- [ ] Backend health check works: https://todo-nextjs-backend.vercel.app/api/health
- [ ] Backend environment variables are set correctly
- [ ] Both projects have been redeployed
- [ ] Browser cache has been cleared
- [ ] Frontend can connect to backend

## Common Issues

### Issue 1: Backend Returns 500 Error
**Solution**: Check Vercel function logs for the actual error message. Common causes:
- Missing environment variables
- Database connection issues
- Import errors

### Issue 2: CORS Errors
**Solution**: Make sure `CORS_ORIGINS` in backend includes your frontend URL

### Issue 3: Environment Variable Not Applied
**Solution**: 
- Make sure you selected the correct environment (Production/Preview/Development)
- Redeploy after setting variables
- Variables set via CLI might not persist - use Dashboard instead

### Issue 4: Backend URL Has Trailing Slash
**Solution**: Remove trailing slash from `NEXT_PUBLIC_API_URL`. Should be:
- ✅ `https://backend-nine-sigma-81.vercel.app`
- ❌ `https://backend-nine-sigma-81.vercel.app/`

## Quick Test URLs

- **Backend Health**: https://todo-nextjs-backend.vercel.app/api/health
- **Backend API Docs**: https://todo-nextjs-backend.vercel.app/docs
- **Frontend**: https://frontend-xi-henna.vercel.app

---

**After completing these steps, the connection error should be resolved!**

