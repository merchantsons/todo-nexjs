# 🔧 Fix: Environment Variables Issue

## Problem
- Frontend trying to connect to `localhost:8000` instead of production backend
- Backend returning errors (likely missing/incorrect environment variables)

## ✅ Frontend Fix Applied
- ✅ Removed and re-added `NEXT_PUBLIC_API_URL` 
- ✅ Set to: `https://backend-nine-sigma-81.vercel.app`
- ✅ Frontend redeployed

## ⚠️ Backend Needs Fix

The backend environment variables were set via CLI, but the values might be empty or incorrect. **You need to verify and set them in the Vercel Dashboard.**

## Quick Fix Steps

### 1. Fix Backend Environment Variables

Go to: **https://vercel.com/merchantsons-projects/backend/settings/environment-variables**

**Remove all existing variables**, then **add these 3 variables** for **Production**:

**Variable 1:**
- Key: `DATABASE_URL`
- Value: `postgresql://neondb_owner:npg_znGThYpK6to5@ep-late-sound-a4fa169w-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require`
- Environment: **Production**

**Variable 2:**
- Key: `BETTER_AUTH_SECRET`
- Value: `WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k`
- Environment: **Production**

**Variable 3:**
- Key: `CORS_ORIGINS`
- Value: `https://frontend-xi-henna.vercel.app`
- Environment: **Production**

### 2. Verify Frontend Environment Variables

Go to: **https://vercel.com/merchantsons-projects/frontend/settings/environment-variables**

Verify these 3 variables exist for **Production**:

- `NEXT_PUBLIC_API_URL` = `https://backend-nine-sigma-81.vercel.app`
- `BETTER_AUTH_SECRET` = `WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k`
- `BETTER_AUTH_URL` = `https://frontend-xi-henna.vercel.app`

If any are missing or wrong, remove and re-add them.

### 3. Redeploy Both Projects

**Backend:**
1. Go to: https://vercel.com/merchantsons-projects/backend/deployments
2. Click **...** on latest deployment
3. Click **Redeploy**

**Frontend:**
1. Go to: https://vercel.com/merchantsons-projects/frontend/deployments
2. Click **...** on latest deployment
3. Click **Redeploy**

### 4. Test

After redeployment completes (2-3 minutes):

1. **Backend Health**: https://backend-nine-sigma-81.vercel.app/api/health
   - Should return: `{"status": "healthy", ...}`

2. **Frontend**: https://frontend-xi-henna.vercel.app
   - Should load without connection errors

3. **Test Registration**: Create an account
4. **Test Login**: Login with the account
5. **Test Tasks**: Create, edit, delete tasks

## Why Dashboard Method?

Setting environment variables via CLI by piping values sometimes doesn't work correctly. The Vercel Dashboard is the most reliable method to ensure values are set properly.

## Summary

- ✅ Frontend API URL fixed and redeployed
- ⚠️ Backend environment variables need to be set via Dashboard
- ⚠️ Both projects need to be redeployed after setting variables

---

**Follow the steps above to complete the fix!** The dashboard method is the most reliable way to ensure everything works.


