# Frontend Environment Variables for Vercel Deployment

## Local Development (.env.local file)

Create a `.env.local` file in the `frontend` directory with:

```env
# Backend API URL (Required)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Authentication Secret (Required)
# Must match the backend BETTER_AUTH_SECRET
BETTER_AUTH_SECRET=your-256-bit-secret-key-here-change-this-in-production

# Frontend URL (Optional)
BETTER_AUTH_URL=http://localhost:3000
```

## Vercel Deployment

Add these environment variables in your Vercel project dashboard:

1. Go to your Vercel project → Settings → Environment Variables
2. Add the following variables:

### Required Variables:

- **NEXT_PUBLIC_API_URL**: Your backend Vercel URL
  - Example: `https://your-backend.vercel.app`
  - This is the URL where your backend API is deployed

- **BETTER_AUTH_SECRET**: A secure random string (256 bits)
  - Must match the backend `BETTER_AUTH_SECRET`
  - Generate with: `openssl rand -hex 32` or use an online generator

### Optional Variables:

- **BETTER_AUTH_URL**: Your frontend Vercel URL
  - Example: `https://your-frontend.vercel.app`
  - If not set, defaults to the current domain

## Important Notes

- Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser
- Environment variables in Vercel take precedence over `.env.local` files
- Never commit `.env.local` files to version control
- Use different values for development and production
- After adding environment variables in Vercel, redeploy your application

