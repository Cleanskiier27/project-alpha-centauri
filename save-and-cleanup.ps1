# NetworkBuster Universal Save & Cleanup
# Targeting: Documents Folder

$ErrorActionPreference = "Continue"
$ProjectRoot = "C:\Users\ceans\OneDrive\Documents\GitHub\networkbuster.net"
$BackupRoot = "C:\Users\ceans\OneDrive\Documents\NetworkBuster_Backups"

Write-Host "--- INITIALIZING SAVE SEQUENCE ---" -ForegroundColor Cyan

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
    git commit -m "Manual Save: $(Get-Date)"
}

# 3. Backup to Documents
Write-Host "Backing up to Documents..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmm"
$dest = Join-Path $BackupRoot "NB_Archive_$timestamp"

if (!(Test-Path $BackupRoot)) { New-Item -ItemType Directory -Path $BackupRoot -Force }
New-Item -ItemType Directory -Path $dest -Force

robocopy $ProjectRoot $dest /E /NFL /NDL /NJH /NJS /nc /ns /np /XD .git node_modules .venv

Write-Host "--- SAVE COMPLETE ---" -ForegroundColor Green
Write-Host "Location: $dest"
