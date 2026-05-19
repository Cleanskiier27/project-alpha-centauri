# NetworkBuster Simple PowerShell Functions
# Source this file: . .\nb.ps1

function nb-start {
    "Starting NetworkBuster..."
    & .\.venv\Scripts\python.exe tools\python\auto_start_service.py
}

function nb-stop {
    "Stopping NetworkBuster..."
    & .\.venv\Scripts\python.exe networkbuster_launcher.py --stop
}

function nb-status {
    "Checking status..."
    & .\.venv\Scripts\python.exe networkbuster_launcher.py --status
}

function nb-map {
    "Opening Network Map..."
    Start-Process http://localhost:6000
    & .\.venv\Scripts\python.exe tools\python\network_map_viewer.py
}

function nb-tracer {
    "Opening API Tracer..."
    Start-Process http://localhost:8000
    & .\.venv\Scripts\python.exe tools\python\api_tracer.py
}

function nb-backup {
    "Running git backup..."
    & .\.venv\Scripts\python.exe tools\python\flash_git_backup.py
}

function nb-thumbs {
    "Extracting thumbnails..."
    & .\.venv\Scripts\python.exe tools\python\extract_thumbnails.py
    Start-Process network_thumbnails\index.html
}

function nb-mission {
    "Opening Mission Control..."
    Start-Process http://localhost:5000
    & .\.venv\Scripts\python.exe tools\python\nasa_home_base.py
}

function nb-all {
    "Opening all dashboards..."
    Start-Process http://localhost:7000  # Universal Launcher
    Start-Process http://localhost:6000  # Network Map
    Start-Process http://localhost:8000  # API Tracer
    Start-Process http://localhost:5000  # Mission Control
}

function nb-autostart {
    "Installing auto-start..."
    Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File install_autostart.ps1" -Verb RunAs
}

function nb-finance {
    "Initializing Personal Miner (Depenabot)..."
    npm run finance:mine
}

function nb-ledger {
    "Opening Project Ledger..."
    if (Test-Path "PROJECT_LEDGER.json") {
        Get-Content "PROJECT_LEDGER.json" | ConvertFrom-Json | Format-Table -AutoSize
    } else {
        Write-Host "❌ Ledger not found!" -ForegroundColor Red
    }
}

function nb-control {
    "Opening Control Panel..."
    Start-Process http://localhost:3000/control-panel
}

function nb-health {
    "Checking System Health..."
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:3000/api/health" -Method Get
        $response | ConvertTo-Json -Depth 5
    } catch {
        Write-Host "❌ Failed to connect to API: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function nb-api-status {
    "Checking API Status..."
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:3000/api/status" -Method Get
        $response | ConvertTo-Json -Depth 5
    } catch {
        Write-Host "❌ Failed to connect to API: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function nb-logs {
    "Fetching System Logs..."
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:3000/api/logs" -Method Get
        $response.logs | ForEach-Object { Write-Host $_ }
    } catch {
        Write-Host "❌ Failed to connect to API: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function nb-help {
    Write-Host "`nNetworkBuster Quick Commands:" -ForegroundColor Cyan
    Write-Host "  nb-start       Start all services" -ForegroundColor White
    Write-Host "  nb-stop        Stop all services" -ForegroundColor White
    Write-Host "  nb-status      Show service status" -ForegroundColor White
    Write-Host "  nb-control     Open Control Panel (Port 3000)" -ForegroundColor Green
    Write-Host "  nb-finance     Run Personal Miner (Financing)" -ForegroundColor Yellow
    Write-Host "  nb-funding     Show SBIR Funding Status" -ForegroundColor Cyan
    Write-Host "  nb-payout      Process Milestone Payout" -ForegroundColor Green
    Write-Host "  nb-ledger      Show Project Ledger" -ForegroundColor Yellow
    Write-Host "  nb-health      Check API Health (REST)" -ForegroundColor Cyan
    Write-Host "  nb-api-status  Check API Status (REST)" -ForegroundColor Cyan
    Write-Host "  nb-logs        Fetch System Logs (REST)" -ForegroundColor Cyan
    Write-Host "  nb-map         Open network map" -ForegroundColor White
    Write-Host "  nb-tracer      Open API tracer" -ForegroundColor White
    Write-Host "  nb-mission     Open mission control" -ForegroundColor White
    Write-Host "  nb-backup      Run git backup" -ForegroundColor White
    Write-Host "  nb-thumbs      Extract thumbnails" -ForegroundColor White
    Write-Host "  nb-all         Open all dashboards" -ForegroundColor White
    Write-Host "  nb-autostart   Install auto-start on boot" -ForegroundColor Yellow
    Write-Host "  nb-help        Show this help" -ForegroundColor White
    Write-Host ""
}

Write-Host "NetworkBuster commands loaded. Type 'nb-help' for usage." -ForegroundColor Green
     Run git backup" -ForegroundColor White
    Write-Host "  nb-thumbs      Extract thumbnails" -ForegroundColor White
    Write-Host "  nb-all         Open all dashboards" -ForegroundColor White
    Write-Host "  nb-autostart   Install auto-start on boot" -ForegroundColor Yellow
    Write-Host "  nb-help        Show this help" -ForegroundColor White
    Write-Host ""
}

Write-Host "NetworkBuster commands loaded. Type 'nb-help' for usage." -ForegroundColor Green
