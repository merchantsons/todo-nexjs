# 🚨 URGENT: Backend Environment Variables Need Manual Setup

## Problem
The backend is crashing because environment variables are not set correctly via CLI. **You MUST set them manually in the Vercel Dashboard.**

## ⚠️ Critical: Do This Now

### Step 1: Go to Backend Project Settings

1. Open: **https://vercel.com/merchantsons-projects/backend/settings/environment-variables**
2. **Remove ALL existing environment variables** (click the "..." menu → Remove for each one)

### Step 2: Add Environment Variables

Click **"Add New"** and add these **3 variables** one by one:

#### Variable 1: DATABASE_URL
- **Key**: `DATABASE_URL`
- **Value**: `postgresql://neondb_owner:npg_znGThYpK6to5@ep-late-sound-a4fa169w-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require`
- **Environment**: Select **Production** ✅
- Click **Save**

#### Variable 2: BETTER_AUTH_SECRET
- **Key**: `BETTER_AUTH_SECRET`
- **Value**: `WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k`
- **Environment**: Select **Production** ✅
- Click **Save**

#### Variable 3: CORS_ORIGINS
- **Key**: `CORS_ORIGINS`
- **Value**: `https://frontend-xi-henna.vercel.app`
- **Environment**: Select **Production** ✅
- Click **Save**

### Step 3: Redeploy Backend

1. Go to: **https://vercel.com/merchantsons-projects/backend/deployments**
2. Find the **latest deployment**
3. Click the **"..."** menu (three dots)
4. Click **"Redeploy"**
5. Wait 1-2 minutes for deployment to complete

### Step 4: Test

After redeployment:

1. **Health Check**: https://backend-nine-sigma-81.vercel.app/api/health
   - Should return: `{"status": "healthy", ...}`

2. **API Docs**: https://backend-nine-sigma-81.vercel.app/docs
   - Should show Swagger UI

3. **Frontend**: https://frontend-xi-henna.vercel.app
   - Should now work without errors

## Why Dashboard Method?

The Vercel CLI method for setting environment variables is unreliable when piping values. The Dashboard is the **only reliable way** to ensure values are set correctly.

## Quick Links

- **Backend Environment Variables**: https://vercel.com/merchantsons-projects/backend/settings/environment-variables
- **Backend Deployments**: https://vercel.com/merchantsons-projects/backend/deployments
- **Backend URL**: https://backend-nine-sigma-81.vercel.app

## Verification Checklist

After setting variables and redeploying:

- [ ] All 3 environment variables are set in Dashboard
- [ ] All variables are set for **Production** environment
- [ ] Backend has been redeployed
- [ ] Health check returns 200 OK
- [ ] Frontend can connect to backend

---

**⚠️ This MUST be done via the Dashboard - CLI method doesn't work reliably!**


