# 🔧 Vercel Environment Variables Setup Guide

## ⚠️ Important: Environment Variables Must Be Set Correctly

The backend is failing because environment variables need to be verified and set correctly in the Vercel Dashboard.

## How to Set Environment Variables in Vercel Dashboard

### Backend Environment Variables

1. Go to: https://vercel.com/merchantsons-projects/backend/settings/environment-variables
2. **Remove existing variables** if they're incorrect
3. **Add these variables** for **Production** environment:

```
DATABASE_URL=postgresql://neondb_owner:npg_znGThYpK6to5@ep-late-sound-a4fa169w-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

```
BETTER_AUTH_SECRET=WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k
```

```
CORS_ORIGINS=https://frontend-xi-henna.vercel.app
```

4. Click **Save** for each variable
5. **Redeploy** the backend project

### Frontend Environment Variables

1. Go to: https://vercel.com/merchantsons-projects/frontend/settings/environment-variables
2. **Verify these variables** are set for **Production**:

```
NEXT_PUBLIC_API_URL=https://backend-nine-sigma-81.vercel.app
```

```
BETTER_AUTH_SECRET=WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k
```

```
BETTER_AUTH_URL=https://frontend-xi-henna.vercel.app
```

3. If any are missing or incorrect, **remove and re-add** them
4. **Redeploy** the frontend project

## Step-by-Step Instructions

### For Backend:

1. Visit: https://vercel.com/merchantsons-projects/backend
2. Click **Settings** → **Environment Variables**
3. For each variable:
   - If it exists and is wrong: Click **...** → **Remove**
   - Click **Add New**
   - Enter the **Key** (variable name)
   - Enter the **Value** (from above)
   - Select **Production** environment
   - Click **Save**
4. Go to **Deployments** tab
5. Click **...** on the latest deployment → **Redeploy**

### For Frontend:

1. Visit: https://vercel.com/merchantsons-projects/frontend
2. Click **Settings** → **Environment Variables**
3. Verify all three variables are set correctly
4. If any need fixing, remove and re-add them
5. Go to **Deployments** tab
6. Click **...** on the latest deployment → **Redeploy**

## Why This Is Needed

When setting environment variables via CLI by piping values, sometimes the values don't get set correctly. The Vercel Dashboard is the most reliable way to ensure values are set properly.

## After Setting Variables

1. **Redeploy both projects** from the Vercel Dashboard
2. **Wait for deployment to complete** (2-3 minutes)
3. **Test the application**:
   - Frontend: https://frontend-xi-henna.vercel.app
   - Backend Health: https://backend-nine-sigma-81.vercel.app/api/health

## Verification

After redeploying, check:

- ✅ Backend health endpoint returns 200 OK
- ✅ Frontend can connect to backend
- ✅ Registration works
- ✅ Login works
- ✅ Tasks can be created

---

**This is the most reliable way to fix the environment variable issues!**


