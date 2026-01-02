# Deployment Checklist

## Pre-Deployment Verification

### ✅ Backend Configuration
- [x] `backend/vercel.json` exists and configured
- [x] `backend/api/index.py` has Mangum handler
- [x] `backend/requirements.txt` includes all dependencies
- [x] Database tables initialized (users, tasks)

### ✅ Frontend Configuration
- [x] Next.js project structure correct
- [x] `package.json` configured
- [x] Environment variables documented

### ✅ Environment Variables Ready
- [x] Backend `.env` configured
- [x] Frontend `.env.local` configured
- [x] JWT secret generated and matching

---

## Deployment Steps

### Step 1: Install Vercel CLI (if not installed)

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Deploy Backend

```bash
cd backend
vercel --prod
```

**During deployment, you'll be prompted:**
- Set up and deploy? **Yes**
- Which scope? **Select your account**
- Link to existing project? **No** (first time) or **Yes** (updates)
- Project name: **todo-backend** (or your choice)
- Directory: **./** (current directory)
- Override settings? **No**

**After deployment:**
1. Note the backend URL (e.g., `https://todo-backend.vercel.app`)
2. Go to Vercel Dashboard → Project Settings → Environment Variables
3. Add these variables:
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_znGThYpK6to5@ep-late-sound-a4fa169w-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   BETTER_AUTH_SECRET=WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   ```
4. Redeploy after adding environment variables

### Step 4: Deploy Frontend

```bash
cd frontend
vercel --prod
```

**During deployment:**
- Set up and deploy? **Yes**
- Which scope? **Select your account**
- Link to existing project? **No** (first time)
- Project name: **todo-frontend** (or your choice)
- Directory: **./** (current directory)
- Override settings? **No**

**After deployment:**
1. Note the frontend URL (e.g., `https://todo-frontend.vercel.app`)
2. Go to Vercel Dashboard → Project Settings → Environment Variables
3. Add these variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
   BETTER_AUTH_SECRET=WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k
   BETTER_AUTH_URL=https://your-frontend-url.vercel.app
   ```
4. **Important**: Update `CORS_ORIGINS` in backend with frontend URL
5. Redeploy both frontend and backend after adding environment variables

### Step 5: Update CORS in Backend

After you have both URLs:
1. Go to Backend project in Vercel Dashboard
2. Settings → Environment Variables
3. Update `CORS_ORIGINS` to include your frontend URL:
   ```
   CORS_ORIGINS=https://your-frontend-url.vercel.app
   ```
4. Redeploy backend

### Step 6: Verify Deployment

1. **Backend Health Check:**
   ```
   https://your-backend-url.vercel.app/api/health
   ```
   Should return: `{"status": "healthy", ...}`

2. **Backend API Docs:**
   ```
   https://your-backend-url.vercel.app/docs
   ```
   Should show Swagger UI

3. **Frontend:**
   ```
   https://your-frontend-url.vercel.app
   ```
   Should load the landing page

4. **Test Registration:**
   - Go to frontend URL
   - Click Register
   - Create an account
   - Verify redirect to dashboard

5. **Test Login:**
   - Logout
   - Login with created account
   - Verify access to dashboard

6. **Test Task Operations:**
   - Create a task
   - Edit a task
   - Toggle completion
   - Delete a task

---

## Environment Variables Summary

### Backend (Vercel)
```
DATABASE_URL=postgresql://neondb_owner:npg_znGThYpK6to5@ep-late-sound-a4fa169w-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
BETTER_AUTH_SECRET=WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

### Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
BETTER_AUTH_SECRET=WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k
BETTER_AUTH_URL=https://your-frontend-url.vercel.app
```

---

## Troubleshooting

### Backend Issues

**Problem**: Backend returns 500 errors
- Check Vercel function logs
- Verify environment variables are set
- Check DATABASE_URL is correct
- Ensure tables exist in database

**Problem**: CORS errors
- Verify CORS_ORIGINS includes frontend URL
- Check for trailing slashes in URLs
- Ensure frontend URL matches exactly

### Frontend Issues

**Problem**: Cannot connect to backend
- Verify NEXT_PUBLIC_API_URL is correct
- Check backend is deployed and accessible
- Verify CORS is configured correctly

**Problem**: Authentication not working
- Verify BETTER_AUTH_SECRET matches in both frontend and backend
- Check JWT tokens are being generated
- Verify API requests include Authorization header

### Database Issues

**Problem**: Database connection errors
- Verify DATABASE_URL is correct
- Check Neon database is accessible
- Ensure SSL mode is included: `?sslmode=require`
- Verify tables exist (run `check_tables.py` locally with production URL)

---

## Post-Deployment Checklist

- [ ] Backend health check returns 200
- [ ] Backend API docs accessible
- [ ] Frontend loads successfully
- [ ] User registration works
- [ ] User login works
- [ ] Task creation works
- [ ] Task listing works
- [ ] Task update works
- [ ] Task deletion works
- [ ] Task completion toggle works
- [ ] User isolation verified (create account, create task, logout, create another account, verify tasks are isolated)

---

## Quick Deploy Commands

```bash
# Deploy backend
cd backend
vercel --prod

# Deploy frontend
cd frontend
vercel --prod

# Or deploy from root (if configured)
vercel --prod
```

---

## Notes

- Database is already initialized (tables created)
- JWT secret is already generated and configured
- Both projects should be deployed as separate Vercel projects
- Environment variables must be set in Vercel Dashboard
- After setting environment variables, redeploy is required


