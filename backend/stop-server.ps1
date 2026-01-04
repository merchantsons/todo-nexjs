# PowerShell script to stop all running backend servers
Write-Host "🛑 Stopping Backend Servers" -ForegroundColor Yellow
Write-Host ""

$stopped = 0
Get-Process | Where-Object {$_.ProcessName -eq "python"} | ForEach-Object {
    $cmd = (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
    if ($cmd -like "*uvicorn*") {
        Write-Host "Stopping uvicorn process (PID $($_.Id))..." -ForegroundColor Yellow
        Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        $stopped++
        Start-Sleep -Milliseconds 500
    }
}

if ($stopped -gt 0) {
    Write-Host ""
    Write-Host "Stopped $stopped backend server process(es)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Now restart the server with:" -ForegroundColor Cyan
    Write-Host "  .\start-server.ps1" -ForegroundColor White
    Write-Host "  OR" -ForegroundColor Cyan
    Write-Host "  .\restart-server.ps1" -ForegroundColor White
} else {
    Write-Host "No backend servers found running" -ForegroundColor Cyan
}

Write-Host ""

