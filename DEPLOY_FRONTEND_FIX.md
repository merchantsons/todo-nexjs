# Fix Vercel 404 Error - Frontend Deployment

## Quick Fix: Deploy from Frontend Directory

Since you can't find the Root Directory setting, deploy directly from the frontend folder:

### Step 1: Install Vercel CLI (if not installed)
```bash
npm install -g vercel
```

### Step 2: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 3: Link to Your Existing Project
```bash
vercel link
```
- Select your account
- Select your existing frontend project
- When asked about settings, choose to keep existing settings

### Step 4: Deploy
```bash
vercel --prod
```

This will deploy from the frontend directory, which Vercel will treat as the root.

## Alternative: Update Root Directory via Vercel Dashboard

1. Go to your project: https://vercel.com/dashboard
2. Click on your **frontend project**
3. Go to **Settings** tab
4. Look for **Build & Development Settings** section
5. Find **Root Directory** field
6. Set it to: `frontend`
7. Click **Save**
8. Trigger a new deployment

## Alternative: Re-import Project with Correct Root

If the setting is still not visible:

1. Go to Vercel Dashboard
2. Click **Add New Project**
3. Import your GitHub repository again
4. During import, you should see a **Root Directory** option
5. Set it to: `frontend`
6. Use a different project name (or delete the old one first)

## Verify Configuration

After deploying, check:
- Build logs show it's building from `frontend` directory
- No 404 errors on the homepage
- Routes like `/login` and `/register` work

