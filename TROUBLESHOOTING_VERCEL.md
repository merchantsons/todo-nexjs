# Troubleshooting Vercel 500 Error

## Common Causes and Fixes

### 1. Missing DATABASE_URL Environment Variable

**Error**: `FUNCTION_INVOCATION_FAILED` or `DATABASE_URL environment variable is not set`

**Fix**:
1. Go to your Vercel project → Settings → Environment Variables
2. Add `DATABASE_URL` with your PostgreSQL connection string:
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   ```
3. Make sure it starts with `postgresql://` or `postgres://`
4. Redeploy your project

### 2. CORS_ORIGINS with Trailing Slash

**Error**: CORS errors or initialization issues

**Fix**:
- Remove trailing slash from `CORS_ORIGINS` in Vercel environment variables
- Should be: `https://your-frontend.vercel.app` (not `https://your-frontend.vercel.app/`)

### 3. Missing BETTER_AUTH_SECRET

**Error**: Authentication failures

**Fix**:
1. Generate a secret: `openssl rand -hex 32` or use [this generator](https://generate-secret.vercel.app/32)
2. Add `BETTER_AUTH_SECRET` in Vercel environment variables
3. Use the same secret in both frontend and backend projects

### 4. Check Vercel Function Logs

**How to Debug**:
1. Go to Vercel Dashboard → Your Project → Functions
2. Click on the function that's failing
3. Check the "Logs" tab
4. Look for error messages starting with `❌` or `⚠️`

### 5. Verify Environment Variables

**Check in Vercel**:
1. Go to Settings → Environment Variables
2. Verify these are set:
   - ✅ `DATABASE_URL`
   - ✅ `BETTER_AUTH_SECRET`
   - ✅ `CORS_ORIGINS` (optional but recommended)

### 6. Test Health Endpoint

After fixing environment variables, test:
```
https://your-backend.vercel.app/api/health
```

Should return:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "version": "1.0.0",
  "env_check": {
    "DATABASE_URL": "set",
    "BETTER_AUTH_SECRET": "set",
    "CORS_ORIGINS": "set"
  }
}
```

## Quick Fix Checklist

- [ ] `DATABASE_URL` is set in Vercel environment variables
- [ ] `DATABASE_URL` is a valid PostgreSQL connection string
- [ ] `BETTER_AUTH_SECRET` is set in Vercel environment variables
- [ ] `CORS_ORIGINS` has no trailing slash
- [ ] All environment variables are saved
- [ ] Project has been redeployed after adding variables
- [ ] Checked function logs for specific error messages

## After Fixing

1. **Redeploy**: Vercel will auto-redeploy on next push, or trigger manually
2. **Test Health**: Visit `/api/health` endpoint
3. **Test Frontend**: Try to connect from your frontend

## Still Having Issues?

1. Check Vercel function logs (most important!)
2. Verify database is accessible from Vercel's IPs
3. Ensure database connection string includes SSL parameters if required
4. Check that all Python dependencies are in `requirements.txt`

