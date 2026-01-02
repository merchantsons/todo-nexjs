# 🚀 Redeploy Frontend to Vercel from GitHub

## Quick Redeploy Options

### Option 1: Automatic Redeploy (Recommended)
If your Vercel project is connected to GitHub with auto-deploy enabled:

1. **Push any changes to GitHub** (even a small change will trigger redeploy):
   ```bash
   git add .
   git commit -m "Trigger redeploy"
   git push origin main
   ```

2. Vercel will automatically detect the push and start a new deployment
3. Check deployment status at: https://vercel.com/merchantsons-projects/frontend

### Option 2: Manual Redeploy from Vercel Dashboard

1. Go to: https://vercel.com/merchantsons-projects/frontend
2. Click on the **Deployments** tab
3. Find the latest deployment
4. Click the **⋯** (three dots) menu
5. Select **Redeploy**
6. Confirm the redeploy

### Option 3: Redeploy via Vercel CLI

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

4. **Link to existing project** (if not already linked):
   ```bash
   vercel link
   ```
   - Select your account
   - Select the existing frontend project

5. **Deploy to production**:
   ```bash
   vercel --prod
   ```

## Verify Environment Variables

Before redeploying, ensure these environment variables are set in Vercel Dashboard:

1. Go to: https://vercel.com/merchantsons-projects/frontend/settings/environment-variables

2. Verify these variables exist for **Production**:
   - `NEXT_PUBLIC_API_URL` = `https://backend-nine-sigma-81.vercel.app`
   - `BETTER_AUTH_SECRET` = `WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k`
   - `BETTER_AUTH_URL` = `https://frontend-xi-henna.vercel.app`

3. If any are missing or incorrect:
   - Click **⋯** → **Remove** (for incorrect ones)
   - Click **Add New**
   - Enter Key and Value
   - Select **Production** environment
   - Click **Save**

## Project Configuration

The frontend is configured with:
- **Root Directory**: `frontend` (set in Vercel project settings)
- **Framework**: Next.js (auto-detected)
- **Build Command**: `npm run build`
- **Output Directory**: `.next`

## After Redeployment

1. **Wait for deployment to complete** (usually 2-3 minutes)
2. **Check deployment logs** for any errors
3. **Test the application**:
   - Visit: https://frontend-xi-henna.vercel.app
   - Test login/register functionality
   - Verify API connection to backend

## Troubleshooting

### Build Fails
- Check deployment logs in Vercel dashboard
- Verify `package.json` has correct build script
- Ensure all dependencies are listed in `package.json`

### Environment Variables Not Working
- Make sure variables are set for **Production** environment
- Redeploy after adding/updating variables
- Variables starting with `NEXT_PUBLIC_` are available in the browser

### API Connection Issues
- Verify `NEXT_PUBLIC_API_URL` points to correct backend URL
- Check backend is deployed and accessible
- Verify CORS settings on backend

## Current Frontend URL
- **Production**: https://frontend-xi-henna.vercel.app

