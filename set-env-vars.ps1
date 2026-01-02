# PowerShell script to set Vercel environment variables
# Run this script to set all required environment variables
#
# ⚠️ IMPORTANT: This script reads from environment variables to avoid exposing credentials
# Set these environment variables before running this script:
#   $env:DATABASE_URL = "postgresql://username:password@host:port/database?sslmode=require&channel_binding=require"
#   $env:BETTER_AUTH_SECRET = "your-secret-key-here"
#   $env:CORS_ORIGINS = "https://your-frontend-url.vercel.app"
#   $env:NEXT_PUBLIC_API_URL = "https://your-backend-url.vercel.app"
#   $env:BETTER_AUTH_URL = "https://your-frontend-url.vercel.app"

Write-Host "Setting Backend Environment Variables..." -ForegroundColor Green

# Check if required environment variables are set
if (-not $env:DATABASE_URL) {
    Write-Host "ERROR: DATABASE_URL environment variable is not set!" -ForegroundColor Red
    Write-Host "Set it with: `$env:DATABASE_URL = 'postgresql://...'" -ForegroundColor Yellow
    exit 1
}

if (-not $env:BETTER_AUTH_SECRET) {
    Write-Host "ERROR: BETTER_AUTH_SECRET environment variable is not set!" -ForegroundColor Red
    Write-Host "Set it with: `$env:BETTER_AUTH_SECRET = 'your-secret-key-here'" -ForegroundColor Yellow
    exit 1
}

if (-not $env:CORS_ORIGINS) {
    Write-Host "ERROR: CORS_ORIGINS environment variable is not set!" -ForegroundColor Red
    Write-Host "Set it with: `$env:CORS_ORIGINS = 'https://your-frontend-url.vercel.app'" -ForegroundColor Yellow
    exit 1
}

# Backend Environment Variables
cd backend

# DATABASE_URL
echo $env:DATABASE_URL | vercel env add DATABASE_URL production

# BETTER_AUTH_SECRET
echo $env:BETTER_AUTH_SECRET | vercel env add BETTER_AUTH_SECRET production

# CORS_ORIGINS
echo $env:CORS_ORIGINS | vercel env add CORS_ORIGINS production

Write-Host "`nSetting Frontend Environment Variables..." -ForegroundColor Green

# Frontend Environment Variables
cd ../frontend

# Check if frontend environment variables are set
if (-not $env:NEXT_PUBLIC_API_URL) {
    Write-Host "ERROR: NEXT_PUBLIC_API_URL environment variable is not set!" -ForegroundColor Red
    Write-Host "Set it with: `$env:NEXT_PUBLIC_API_URL = 'https://your-backend-url.vercel.app'" -ForegroundColor Yellow
    exit 1
}

if (-not $env:BETTER_AUTH_URL) {
    Write-Host "ERROR: BETTER_AUTH_URL environment variable is not set!" -ForegroundColor Red
    Write-Host "Set it with: `$env:BETTER_AUTH_URL = 'https://your-frontend-url.vercel.app'" -ForegroundColor Yellow
    exit 1
}

# NEXT_PUBLIC_API_URL
echo $env:NEXT_PUBLIC_API_URL | vercel env add NEXT_PUBLIC_API_URL production

# BETTER_AUTH_SECRET
echo $env:BETTER_AUTH_SECRET | vercel env add BETTER_AUTH_SECRET production

# BETTER_AUTH_URL
echo $env:BETTER_AUTH_URL | vercel env add BETTER_AUTH_URL production

Write-Host "`nEnvironment variables set! Now redeploy both projects:" -ForegroundColor Yellow
Write-Host "  cd backend && vercel --prod" -ForegroundColor Cyan
Write-Host "  cd frontend && vercel --prod" -ForegroundColor Cyan


