# PowerShell script to set Vercel environment variables
# Run this script to set all required environment variables

Write-Host "Setting Backend Environment Variables..." -ForegroundColor Green

# Backend Environment Variables
cd backend

# DATABASE_URL
$dbUrl = "postgresql://neondb_owner:npg_znGThYpK6to5@ep-late-sound-a4fa169w-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
echo $dbUrl | vercel env add DATABASE_URL production

# BETTER_AUTH_SECRET
$secret = "WtxT_SqMLumf85IExMVyDV3jKYgaJCWC-gHdcKECn-k"
echo $secret | vercel env add BETTER_AUTH_SECRET production

# CORS_ORIGINS
$cors = "https://frontend-xi-henna.vercel.app"
echo $cors | vercel env add CORS_ORIGINS production

Write-Host "`nSetting Frontend Environment Variables..." -ForegroundColor Green

# Frontend Environment Variables
cd ../frontend

# NEXT_PUBLIC_API_URL
$apiUrl = "https://backend-nine-sigma-81.vercel.app"
echo $apiUrl | vercel env add NEXT_PUBLIC_API_URL production

# BETTER_AUTH_SECRET
echo $secret | vercel env add BETTER_AUTH_SECRET production

# BETTER_AUTH_URL
$frontendUrl = "https://frontend-xi-henna.vercel.app"
echo $frontendUrl | vercel env add BETTER_AUTH_URL production

Write-Host "`nEnvironment variables set! Now redeploy both projects:" -ForegroundColor Yellow
Write-Host "  cd backend && vercel --prod" -ForegroundColor Cyan
Write-Host "  cd frontend && vercel --prod" -ForegroundColor Cyan


