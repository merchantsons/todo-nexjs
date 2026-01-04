# Quick Vercel Deployment Guide

Your code is now on GitHub! Follow these steps to deploy both frontend and backend to Vercel.

## 🚀 Deployment Steps

### Step 1: Deploy Backend First

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com) and sign in
   - Click "Add New..." → "Project"

2. **Import from GitHub**
   - Select your GitHub repository
   - Click "Import"

3. **Configure Backend Project**
   - **Framework Preset**: Other
   - **Root Directory**: `backend` ⚠️ **IMPORTANT: Set this!**
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
   - **Install Command**: `pip install -r requirements.txt`

4. **Add Environment Variables**
   Click "Environment Variables" and add:

   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   BETTER_AUTH_SECRET=generate-a-random-256-bit-secret
   CORS_ORIGINS=https://your-frontend-will-be-here.vercel.app
   ```

   **Note**: 
   - Get `DATABASE_URL` from your PostgreSQL provider (Neon, Supabase, Railway, etc.)
   - Generate `BETTER_AUTH_SECRET` with: `openssl rand -hex 32` or use [this generator](https://generate-secret.vercel.app/32)
   - For `CORS_ORIGINS`, you'll update this after deploying the frontend

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment (2-3 minutes)
   - **Copy your backend URL** (e.g., `https://todo-nexjs-backend.vercel.app`)

---

### Step 2: Deploy Frontend

1. **Create New Project in Vercel**
   - Click "Add New..." → "Project" again
   - Select the **same GitHub repository**

2. **Configure Frontend Project**
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend` ⚠️ **IMPORTANT: Set this!**
   - Build settings will auto-detect (you can leave them)

3. **Add Environment Variables**
   Click "Environment Variables" and add:

   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url-from-step-1.vercel.app
   BETTER_AUTH_SECRET=same-secret-as-backend
   BETTER_AUTH_URL=https://your-frontend-will-be-here.vercel.app
   ```

   **Note**: 
   - `NEXT_PUBLIC_API_URL`: Use the backend URL from Step 1
   - `BETTER_AUTH_SECRET`: Must be **exactly the same** as backend
   - `BETTER_AUTH_URL`: You can update this after deployment

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment (2-3 minutes)
   - **Copy your frontend URL** (e.g., `https://todo-nexjs-frontend.vercel.app`)

---

### Step 3: Update CORS Configuration

1. **Go back to Backend Project**
   - Settings → Environment Variables
   - Edit `CORS_ORIGINS`
   - Update to: `https://your-frontend-url.vercel.app`
   - Save and redeploy (or wait for auto-redeploy)

---

## ✅ Quick Checklist

### Backend Deployment
- [ ] Root Directory set to `backend`
- [ ] `DATABASE_URL` environment variable added
- [ ] `BETTER_AUTH_SECRET` environment variable added
- [ ] `CORS_ORIGINS` environment variable added (can update later)
- [ ] Deployment successful
- [ ] Backend URL copied

### Frontend Deployment
- [ ] Root Directory set to `frontend`
- [ ] `NEXT_PUBLIC_API_URL` set to backend URL
- [ ] `BETTER_AUTH_SECRET` matches backend
- [ ] `BETTER_AUTH_URL` set (optional, can update later)
- [ ] Deployment successful
- [ ] Frontend URL copied

### Final Steps
- [ ] Updated backend `CORS_ORIGINS` with frontend URL
- [ ] Tested frontend → backend connection
- [ ] Tested user registration/login

---

## 🔧 Troubleshooting

### Backend Issues

**"Module not found" errors:**
- Check that `requirements.txt` includes all dependencies
- Verify `mangum` is in requirements.txt (it is ✅)

**"DATABASE_URL not set" errors:**
- Go to Settings → Environment Variables
- Verify `DATABASE_URL` is added
- Make sure it's a PostgreSQL connection string (starts with `postgresql://`)

**"CORS error" in browser:**
- Update `CORS_ORIGINS` in backend environment variables
- Include your exact frontend URL (with `https://`)
- Redeploy backend

### Frontend Issues

**"Cannot connect to backend" errors:**
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend is deployed and accessible
- Test backend health: `https://your-backend.vercel.app/api/health`

**"Authentication failed" errors:**
- Verify `BETTER_AUTH_SECRET` matches between frontend and backend
- Check backend `/api/auth/login` endpoint is working

---

## 📝 Environment Variables Reference

### Backend (Vercel)
```
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-here
CORS_ORIGINS=https://your-frontend.vercel.app
```

### Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
BETTER_AUTH_SECRET=your-secret-here (same as backend)
BETTER_AUTH_URL=https://your-frontend.vercel.app
```

---

## 🎉 After Deployment

1. Visit your frontend URL
2. Try registering a new user
3. Create a task
4. Everything should work! 🚀

---

## 📚 Need More Help?

- See `VERCEL_DEPLOYMENT.md` for detailed documentation
- See `backend/ENV_EXAMPLE.md` for backend env vars
- See `frontend/ENV_EXAMPLE.md` for frontend env vars
- Check Vercel deployment logs if something fails

