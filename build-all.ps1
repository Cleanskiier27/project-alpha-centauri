# Build all applications comprehensively
Write-Host "[BUILD] Building all NetworkBuster applications..." -ForegroundColor Cyan

# Build main React app (src/)
Write-Host "[MAIN] Building main React app..." -ForegroundColor Yellow
if (Test-Path "src") {
    npm run build
    Write-Host "[SUCCESS] Main app built" -ForegroundColor Green
}

# Build dashboard
Write-Host "[DASHBOARD] Building dashboard..." -ForegroundColor Yellow
if (Test-Path "dashboard") {
    Push-Location "dashboard"
    npm install
    npm run build
    Pop-Location
    Write-Host "[SUCCESS] Dashboard built" -ForegroundColor Green
}

# Build overlay
Write-Host "[OVERLAY] Building real-time overlay..." -ForegroundColor Yellow
if (Test-Path "challengerepo\real-time-overlay") {
    Push-Location "challengerepo\real-time-overlay"
    npm install
    npm run build
    Pop-Location
    Write-Host "[SUCCESS] Overlay built" -ForegroundColor Green
}

Write-Host "[FINISH] All applications built successfully!" -ForegroundColor Green
Write-Host "[READY] Ready to start server with: npm start" -ForegroundColor Cyan
