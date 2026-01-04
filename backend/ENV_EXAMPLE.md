# Backend Environment Variables for Vercel Deployment

## Local Development (.env file)

Create a `.env` file in the `backend` directory with:

```env
# Database Configuration (Required)
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# Authentication Secret (Required)
# Generate a secure random string (256 bits recommended)
BETTER_AUTH_SECRET=your-256-bit-secret-key-here-change-this-in-production

# CORS Origins (Optional)
# Comma-separated list of allowed origins
CORS_ORIGINS=http://localhost:3000
```

## Vercel Deployment

Add these environment variables in your Vercel project dashboard:

1. Go to your Vercel project → Settings → Environment Variables
2. Add the following variables:

### Required Variables:

- **DATABASE_URL**: Your PostgreSQL database connection string
  - Example: `postgresql://user:password@host:port/database`
  - Recommended providers: Neon, Supabase, Railway, or Vercel Postgres

- **BETTER_AUTH_SECRET**: A secure random string (256 bits)
  - Must match the frontend `BETTER_AUTH_SECRET`
  - Generate with: `openssl rand -hex 32` or use an online generator

### Optional Variables:

- **CORS_ORIGINS**: Comma-separated list of allowed origins
  - Example: `https://your-frontend.vercel.app,https://your-custom-domain.com`
  - If not set, defaults to allow all origins

## Important Notes

- Environment variables in Vercel take precedence over `.env` files
- Never commit `.env` files to version control
- Use different secrets for development and production
- The `DATABASE_URL` must be a PostgreSQL connection string (not SQLite)

