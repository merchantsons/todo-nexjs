# PowerShell script to start the backend server
# Usage: .\start-server.ps1

Write-Host "Starting backend server..." -ForegroundColor Green

# Check if .env file exists
if (-not (Test-Path .env)) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "Run .\setup-local-env.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Check if database connection is configured (PostgreSQL)
Write-Host "Checking database configuration..." -ForegroundColor Cyan
try {
    python -c "from app.config import settings; from app.dependencies.database import get_engine; engine = get_engine(); print('✅ Using PostgreSQL database')" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: Database configuration failed!" -ForegroundColor Red
        Write-Host "   Make sure DATABASE_URL in .env is a PostgreSQL connection string" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ ERROR: Could not verify database configuration" -ForegroundColor Red
    exit 1
}

# Stop any existing uvicorn processes
Write-Host "Checking for existing server processes..." -ForegroundColor Cyan
Get-Process | Where-Object {$_.ProcessName -eq "python"} | ForEach-Object {
    $cmd = (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
    if ($cmd -like "*uvicorn*") {
        Write-Host "Stopping existing uvicorn process (PID $($_.Id))..." -ForegroundColor Yellow
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
}

# Start the server
Write-Host ""
Write-Host "🚀 Starting backend server on http://localhost:8000" -ForegroundColor Green
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

# Start uvicorn
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000



