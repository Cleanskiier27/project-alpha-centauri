# NetworkBuster Universal Save & Cleanup
# Targeting: K: Drive (networkbustersetup)

$ErrorActionPreference = "Continue"
$ProjectRoot = "C:\Users\ceans\OneDrive\Documents\GitHub\networkbuster.net"
$BackupRoot = "K:\NETWORKBUSTER_BACKUPS"

Write-Host "--- INITIALIZING SAVE SEQUENCE (K: DRIVE) ---" -ForegroundColor Cyan

if (!(Test-Path $ProjectRoot)) { 
    Write-Host "Project not found at $ProjectRoot" -ForegroundColor Red
    exit 
}

Set-Location $ProjectRoot

# 1. Cleanup
Write-Host "Cleaning temporary files..." -ForegroundColor Yellow
$clean = @("*.log", "__pycache__", "node_modules\.cache", ".pytest_cache")
foreach ($p in $clean) {
    if (Test-Path $p) { Remove-Item -Path $p -Recurse -Force -ErrorAction SilentlyContinue }
}

# 2. Git Save
Write-Host "Staging and Committing..." -ForegroundColor Yellow
if (Get-Command git -ErrorAction SilentlyContinue) {
    git add -A
    git commit -m "Auto Save to K: Drive - $(Get-Date)"
}

# 3. Backup to K: Drive
Write-Host "Backing up to K: Drive..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmm"
$dest = Join-Path $BackupRoot "NB_Setup_Archive_$timestamp"

if (!(Test-Path $BackupRoot)) { New-Item -ItemType Directory -Path $BackupRoot -Force }
New-Item -ItemType Directory -Path $dest -Force

# Exclude .git, node_modules, .venv AND .security (due to access errors)
robocopy $ProjectRoot $dest /E /NFL /NDL /NJH /NJS /nc /ns /np /XD .git node_modules .venv .security

Write-Host "--- SAVE COMPLETE ---" -ForegroundColor Green
Write-Host "Location: $dest"
