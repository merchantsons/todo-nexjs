# Vercel Deployment Guide

This guide will help you deploy both the frontend and backend of this Todo application to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. A PostgreSQL database (recommended: [Neon](https://neon.tech), [Supabase](https://supabase.com), or [Railway](https://railway.app))
3. Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### Step 1: Deploy Backend

1. **Connect Repository to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New Project"
   - Import your Git repository
   - Select the `backend` folder as the root directory

2. **Configure Build Settings**
   - Framework Preset: Other
   - Root Directory: `backend`
   - Build Command: (leave empty - Vercel will auto-detect Python)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`

3. **Add Environment Variables**
   Go to Settings → Environment Variables and add:

   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   BETTER_AUTH_SECRET=your-256-bit-secret-here
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

   **Important:**
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Generate with `openssl rand -hex 32`
   - `CORS_ORIGINS`: Will be set after frontend deployment (use your frontend URL)

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Note your backend URL (e.g., `https://your-backend.vercel.app`)

### Step 2: Deploy Frontend

1. **Connect Repository to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New Project"
   - Import the same Git repository
   - Select the `frontend` folder as the root directory

2. **Configure Build Settings**
   - Framework Preset: Next.js (auto-detected)
   - Root Directory: `frontend`
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `.next` (auto-detected)
   - Install Command: `npm install` (auto-detected)

3. **Add Environment Variables**
   Go to Settings → Environment Variables and add:

   ```
   NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
   BETTER_AUTH_SECRET=your-256-bit-secret-here
   BETTER_AUTH_URL=https://your-frontend.vercel.app
   ```

   **Important:**
   - `NEXT_PUBLIC_API_URL`: Your backend Vercel URL from Step 1
   - `BETTER_AUTH_SECRET`: Must match the backend secret
   - `BETTER_AUTH_URL`: Your frontend Vercel URL (can be set after deployment)

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Note your frontend URL (e.g., `https://your-frontend.vercel.app`)

### Step 3: Update CORS Configuration

1. **Update Backend CORS_ORIGINS**
   - Go to your backend Vercel project → Settings → Environment Variables
   - Update `CORS_ORIGINS` to include your frontend URL:
     ```
     CORS_ORIGINS=https://your-frontend.vercel.app
     ```
   - Redeploy the backend (Vercel will auto-redeploy on next push, or trigger manually)

### Step 4: Initialize Database

1. **Run Database Migrations**
   - You can use a local script or connect to your database directly
   - The backend will automatically create tables on first request if using SQLModel
   - Or run the `init_db.py` script locally with your production `DATABASE_URL`

## Project Structure for Vercel

```
todo-nexjs/
├── backend/
│   ├── api/
│   │   └── index.py          # Vercel serverless function entry point
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── config.py         # Configuration (reads from env vars)
│   │   └── ...
│   ├── vercel.json           # Vercel configuration
│   └── requirements.txt      # Python dependencies
│
└── frontend/
    ├── app/                  # Next.js App Router
    ├── lib/                  # API clients
    ├── vercel.json           # Vercel configuration
    └── package.json          # Node dependencies
```

## Environment Variables Summary

### Backend (Vercel Environment Variables)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Yes | JWT signing secret (256 bits) |
| `CORS_ORIGINS` | No | Comma-separated allowed origins |

### Frontend (Vercel Environment Variables)

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL |
| `BETTER_AUTH_SECRET` | Yes | Must match backend secret |
| `BETTER_AUTH_URL` | No | Frontend URL |

## Troubleshooting

### Backend Issues

1. **Import Errors**
   - Ensure `requirements.txt` includes all dependencies
   - Check that `mangum` is installed (required for Vercel)

2. **Database Connection Errors**
   - Verify `DATABASE_URL` is correct
   - Ensure database allows connections from Vercel IPs
   - Check SSL mode in connection string

3. **CORS Errors**
   - Verify `CORS_ORIGINS` includes your frontend URL
   - Check that frontend URL matches exactly (including https://)

### Frontend Issues

1. **API Connection Errors**
   - Verify `NEXT_PUBLIC_API_URL` is set correctly
   - Check backend is deployed and accessible
   - Verify CORS configuration in backend

2. **Authentication Errors**
   - Ensure `BETTER_AUTH_SECRET` matches between frontend and backend
   - Check that backend `/api/auth/*` routes are working

## Continuous Deployment

Both projects will automatically redeploy when you push to your Git repository:
- Backend: Deploys when changes are made in `backend/` directory
- Frontend: Deploys when changes are made in `frontend/` directory

## Custom Domains

You can add custom domains in Vercel project settings:
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Update `CORS_ORIGINS` and `NEXT_PUBLIC_API_URL` accordingly

## Monitoring

- Check deployment logs in Vercel Dashboard
- Monitor function logs for backend API calls
- Use Vercel Analytics for frontend performance

## Support

For issues specific to:
- **Vercel**: Check [Vercel Documentation](https://vercel.com/docs)
- **FastAPI on Vercel**: Check [Mangum Documentation](https://mangum.io)
- **Next.js**: Check [Next.js Documentation](https://nextjs.org/docs)

