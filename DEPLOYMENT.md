# Vercel Deployment Guide

This guide explains how to deploy the Evolution of Todo application to Vercel with Neon database connection.

## Prerequisites

- Vercel account
- Neon database account
- GitHub repository connected to Vercel

## Deployment Steps

### 1. Deploy Frontend (Next.js)

The frontend will be automatically detected by Vercel as a Next.js project.

**Option A: Deploy from Vercel Dashboard**
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import your GitHub repository
4. Set root directory to `frontend`
5. Configure environment variables (see below)
6. Deploy

**Option B: Deploy via CLI**
```bash
cd frontend
vercel --prod
```

### 2. Deploy Backend (FastAPI)

The backend needs to be deployed as a separate Vercel project.

**Option A: Deploy from Vercel Dashboard**
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import the same GitHub repository
4. Set root directory to `backend`
5. Configure environment variables (see below)
6. Deploy

**Option B: Deploy via CLI**
```bash
cd backend
vercel --prod
```

## Environment Variables

### Frontend Environment Variables (Vercel)

Add these in Vercel Dashboard → Project Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
BETTER_AUTH_SECRET=your-256-bit-secret-key-here
BETTER_AUTH_URL=https://your-frontend.vercel.app
```

**Important**: 
- `NEXT_PUBLIC_API_URL` should point to your deployed backend URL
- `BETTER_AUTH_SECRET` must match the backend secret
- `BETTER_AUTH_URL` should be your frontend URL

### Backend Environment Variables (Vercel)

Add these in Vercel Dashboard → Project Settings → Environment Variables:

```
DATABASE_URL=postgresql://user:pass@host:5432/dbname?sslmode=require
BETTER_AUTH_SECRET=your-256-bit-secret-key-here
CORS_ORIGINS=https://your-frontend.vercel.app
```

**Important**:
- `DATABASE_URL` is your Neon database connection string
- `BETTER_AUTH_SECRET` must match the frontend secret
- `CORS_ORIGINS` should include your frontend URL

### Getting Neon Database URL

1. Go to [Neon Console](https://console.neon.tech)
2. Select your project
3. Go to "Connection Details"
4. Copy the connection string
5. It should look like:
   ```
   postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

## Post-Deployment Steps

### 1. Update Frontend API URL

After backend deployment, update `NEXT_PUBLIC_API_URL` in frontend environment variables to point to the backend URL.

### 2. Update Backend CORS

Update `CORS_ORIGINS` in backend environment variables to include your frontend URL.

### 3. Verify Database Connection

The database tables should already exist (created during development). If not, you can run:

```bash
# Locally, with production DATABASE_URL
DATABASE_URL=your-production-url python backend/init_db.py
```

## Project Structure for Vercel

```
todo-nexjs/
├── frontend/          # Next.js app (auto-detected)
│   ├── package.json
│   └── ...
├── backend/           # FastAPI app (needs vercel.json)
│   ├── vercel.json
│   ├── api/
│   │   └── index.py   # Serverless entry point
│   └── ...
└── vercel.json        # Root config (optional)
```

## Troubleshooting

### Backend Not Working

1. Check that `vercel.json` exists in `backend/` directory
2. Verify environment variables are set correctly
3. Check Vercel function logs for errors

### CORS Errors

1. Ensure `CORS_ORIGINS` includes your frontend URL
2. Check that frontend `NEXT_PUBLIC_API_URL` points to backend
3. Verify URLs don't have trailing slashes

### Database Connection Errors

1. Verify `DATABASE_URL` is correct
2. Check Neon database is accessible
3. Ensure SSL mode is set: `?sslmode=require`

## URLs After Deployment

- **Frontend**: `https://your-frontend.vercel.app`
- **Backend**: `https://your-backend.vercel.app`
- **API Docs**: `https://your-backend.vercel.app/docs`
- **Health Check**: `https://your-backend.vercel.app/api/health`

## Quick Deploy Commands

```bash
# Deploy frontend
cd frontend
vercel --prod

# Deploy backend
cd backend
vercel --prod

# Or deploy both from root
vercel --prod
```


