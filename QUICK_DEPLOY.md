# Quick Deployment Guide

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional, for CLI deployment):
   ```bash
   npm install -g vercel
   ```

## Deployment Options

### Option 1: Deploy via Vercel Dashboard (Recommended)

#### Deploy Backend

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
5. Click **"Deploy"**
6. After deployment, go to **Settings → Environment Variables** and add:
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_znGThYpK6to5@ep-late-sound-a4fa169w-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   BETTER_AUTH_SECRET=WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   ```
7. **Redeploy** after adding environment variables

#### Deploy Frontend

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New Project"**
3. Import the same GitHub repository
4. Configure project:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)
5. Click **"Deploy"**
6. After deployment, go to **Settings → Environment Variables** and add:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
   BETTER_AUTH_SECRET=WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k
   BETTER_AUTH_URL=https://your-frontend-url.vercel.app
   ```
7. **Update Backend CORS**: Go to backend project → Settings → Environment Variables → Update `CORS_ORIGINS` with frontend URL
8. **Redeploy both** frontend and backend

### Option 2: Deploy via CLI

#### Install Vercel CLI
```bash
npm install -g vercel
```

#### Login
```bash
vercel login
```

#### Deploy Backend
```bash
cd backend
vercel --prod
```

When prompted:
- Set up and deploy? **Yes**
- Which scope? **Your account**
- Link to existing project? **No** (first time)
- Project name: **todo-backend**
- Directory: **./**

After deployment, add environment variables in Vercel Dashboard.

#### Deploy Frontend
```bash
cd frontend
vercel --prod
```

When prompted:
- Set up and deploy? **Yes**
- Which scope? **Your account**
- Link to existing project? **No** (first time)
- Project name: **todo-frontend**
- Directory: **./**

After deployment, add environment variables in Vercel Dashboard.

---

## Environment Variables

### Backend Environment Variables

Add in Vercel Dashboard → Backend Project → Settings → Environment Variables:

```
DATABASE_URL=postgresql://neondb_owner:npg_znGThYpK6to5@ep-late-sound-a4fa169w-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
BETTER_AUTH_SECRET=WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

### Frontend Environment Variables

Add in Vercel Dashboard → Frontend Project → Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
BETTER_AUTH_SECRET=WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k
BETTER_AUTH_URL=https://your-frontend-url.vercel.app
```

**Important**: Replace `your-backend-url` and `your-frontend-url` with actual Vercel URLs after deployment.

---

## Deployment Order

1. **Deploy Backend first** → Get backend URL
2. **Deploy Frontend** → Get frontend URL
3. **Update Backend CORS** with frontend URL
4. **Update Frontend API URL** with backend URL
5. **Redeploy both** projects

---

## Verification

After deployment, verify:

1. **Backend Health**: `https://your-backend.vercel.app/api/health`
2. **Backend Docs**: `https://your-backend.vercel.app/docs`
3. **Frontend**: `https://your-frontend.vercel.app`
4. **Test Registration**: Create an account
5. **Test Login**: Login with account
6. **Test Tasks**: Create, edit, delete tasks

---

## Troubleshooting

- **CORS Errors**: Ensure `CORS_ORIGINS` includes frontend URL
- **API Connection**: Verify `NEXT_PUBLIC_API_URL` points to backend
- **Database Errors**: Check `DATABASE_URL` is correct
- **Auth Errors**: Ensure `BETTER_AUTH_SECRET` matches in both projects

For detailed troubleshooting, see `DEPLOYMENT_CHECKLIST.md`.


