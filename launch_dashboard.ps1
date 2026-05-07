# Preciseliens Dashboard Launcher
# This script ensures the production server is running and opens the unified dashboard.

$port = 3000
$url = "http://localhost:3000/dashboard/"

Write-Host "🚀 Initializing Preciseliens Unified Dashboard..." -ForegroundColor Cyan

# Check if port 3000 is occupied
$process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -First 1
if ($process) {
    Write-Host "⚠️ Port $port is already in use. Restarting server..." -ForegroundColor Yellow
    Stop-Process -Id $process.OwningProcess -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

# Start the server in the background
Write-Host "⚡ Starting Production Server..." -ForegroundColor Green
Start-Process -FilePath "node" -ArgumentList "server.js" -WindowStyle Hidden -WorkingDirectory $PSScriptRoot

# Wait for server to initialize
Start-Sleep -Seconds 2

# Open the dashboard
Write-Host "🌐 Opening Dashboard at $url" -ForegroundColor White
Start-Process $url

Write-Host "✅ Launch sequence complete." -ForegroundColor Cyan
