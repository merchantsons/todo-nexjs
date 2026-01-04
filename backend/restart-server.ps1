# PowerShell script to restart the backend server with Neon PostgreSQL
# This ensures the server uses the correct database configuration

Write-Host "🔄 Restarting Backend Server" -ForegroundColor Cyan
Write-Host ""

# Step 1: Stop any existing uvicorn processes
Write-Host "1. Stopping existing server processes..." -ForegroundColor Yellow
$stopped = $false
Get-Process | Where-Object {$_.ProcessName -eq "python"} | ForEach-Object {
    $cmd = (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
    if ($cmd -like "*uvicorn*") {
        Write-Host "   Stopping uvicorn process (PID $($_.Id))..." -ForegroundColor Yellow
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        $stopped = $true
        Start-Sleep -Seconds 1
    }
}

if ($stopped) {
    Write-Host "   ✅ Existing processes stopped" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  No existing processes found" -ForegroundColor Cyan
}

Write-Host ""

# Step 2: Verify database configuration
Write-Host "2. Verifying database configuration..." -ForegroundColor Yellow
try {
    python verify_neon_connection.py 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Database configuration verified" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Database configuration check failed" -ForegroundColor Yellow
        Write-Host "   Run: python verify_neon_connection.py" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ⚠️  Could not verify database configuration" -ForegroundColor Yellow
}

Write-Host ""

# Step 3: Remove local database files (if they exist)
Write-Host "3. Cleaning up local database files..." -ForegroundColor Yellow
if (Test-Path "local.db") {
    Remove-Item "local.db" -Force -ErrorAction SilentlyContinue
    Write-Host "   ✅ Removed local.db" -ForegroundColor Green
} else {
    Write-Host "   ℹ️  No local.db file found" -ForegroundColor Cyan
}

Write-Host ""

# Step 4: Check .env file
Write-Host "4. Checking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "postgresql://") {
        Write-Host "   ✅ .env contains PostgreSQL connection string" -ForegroundColor Green
    } else {
        Write-Host "   ❌ .env does NOT contain PostgreSQL connection string!" -ForegroundColor Red
        Write-Host "   Please update .env with your Neon PostgreSQL connection string" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   ❌ .env file not found!" -ForegroundColor Red
    Write-Host "   Please create .env file with DATABASE_URL" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 5: Start the server
Write-Host "5. Starting backend server..." -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Backend server starting on http://localhost:8000" -ForegroundColor Green
Write-Host "   Using: Neon PostgreSQL database" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start uvicorn
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

