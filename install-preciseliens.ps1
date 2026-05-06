#Requires -RunAsAdministrator

<#
.SYNOPSIS
    Preciseliens PLLC & NetworkBuster Suite Installation Helper
.DESCRIPTION
    Unified installer for the Preciseliens Mission Control, Marketplace, and NetworkBuster core.
#>

$ErrorActionPreference = "Stop"

Clear-Host
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        PRECISELIENS PLLC // MISSION CONTROL INSTALLER      ║" -ForegroundColor Cyan
Write-Host "║        Version 2026.05 - Personalized Suite                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

$InstallDir = $PSScriptRoot
Set-Location $InstallDir

# 1. Environment Check
Write-Host "`n[1/6] 🔍 Checking environments..." -ForegroundColor Yellow
$PythonReady = Test-Path ".venv\Scripts\python.exe"
$NodeReady = Get-Command npm -ErrorAction SilentlyContinue

if ($PythonReady) { Write-Host "   ✅ Python Venv: OK" -ForegroundColor Green } else { Write-Host "   ❌ Python Venv: MISSING" -ForegroundColor Red }
if ($NodeReady) { Write-Host "   ✅ Node.js/NPM: OK" -ForegroundColor Green } else { Write-Host "   ❌ Node.js/NPM: MISSING" -ForegroundColor Red }

if (-not $PythonReady -or -not $NodeReady) {
    Write-Host "   ! Please ensure both Python and Node.js environments are initialized." -ForegroundColor Yellow
    exit 1
}

# 2. Build Vite Overlay
Write-Host "`n[2/6] 🏗️  Building NASA SBIR Vite Overlay (Marketplace)..." -ForegroundColor Yellow
Push-Location "challengerepo/real-time-overlay"
try {
    Write-Host "   > Running npm install..." -ForegroundColor DarkGray
    npm install --silent
    Write-Host "   > Running vite build..." -ForegroundColor DarkGray
    npm run build --silent
    Write-Host "   ✅ Build Success: Preciseliens Overlay Ready" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Build Failed!" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location

# 3. Icon Setup
Write-Host "`n[3/6] 🎨 Deploying Preciseliens Branding..." -ForegroundColor Yellow
$IconPath = Join-Path $InstallDir "preciseliens.ico"
# Re-using icon generation logic from standard installer but themed
Add-Type -AssemblyName System.Drawing
$bitmap = New-Object System.Drawing.Bitmap(64, 64)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.Clear([System.Drawing.Color]::FromArgb(2, 2, 5)) # Deep Space Blue
$graphics.FillEllipse([System.Drawing.Brushes]::Cyan, 12, 12, 40, 40)
$graphics.DrawString("PL", (New-Object System.Drawing.Font("Outfit", 14, [System.Drawing.FontStyle]::Bold)), [System.Drawing.Brushes]::Black, 18, 22)
$bitmap.Save($IconPath, [System.Drawing.Imaging.ImageFormat]::Icon)
$graphics.Dispose(); $bitmap.Dispose()
Write-Host "   ✅ Branding Assets Deployed" -ForegroundColor Green

# 4. Shortcuts
Write-Host "`n[4/6] 📌 Creating Mission Control Shortcuts..." -ForegroundColor Yellow
$WshShell = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath("Desktop")

# Mission Control (Vite Overlay)
$Shortcut = $WshShell.CreateShortcut("$Desktop\Preciseliens Mission Control.lnk")
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c start `"$InstallDir\challengerepo\real-time-overlay\dist\index.html`""
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.IconLocation = $IconPath
$Shortcut.Description = "Preciseliens PLLC Mission Control & Marketplace"
$Shortcut.Save()
Write-Host "   ✅ Desktop: Preciseliens Mission Control" -ForegroundColor Green

# Marketplace Example
$Shortcut = $WshShell.CreateShortcut("$Desktop\Preciseliens Marketplace Example.lnk")
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c start `"$InstallDir\MARKETPLACE_EXAMPLE.html`""
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.IconLocation = $IconPath
$Shortcut.Description = "Preciseliens Personalized Marketplace Example"
$Shortcut.Save()
Write-Host "   ✅ Desktop: Preciseliens Marketplace Example" -ForegroundColor Green

# Neural OS
$Shortcut = $WshShell.CreateShortcut("$Desktop\Preciseliens OS.lnk")
$Shortcut.TargetPath = "cmd.exe"
$Shortcut.Arguments = "/c start `"$InstallDir\os.html`""
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.IconLocation = $IconPath
$Shortcut.Description = "Preciseliens Neural Coder OS"
$Shortcut.Save()
Write-Host "   ✅ Desktop: Preciseliens OS" -ForegroundColor Green

# 5. Core Services
Write-Host "`n[5/6] ⚙️  Synchronizing NetworkBuster Core..." -ForegroundColor Yellow
& ".venv\Scripts\python.exe" -c "import json; config = json.load(open('networkbuster_config.json')); config['launch_count'] += 1; json.dump(config, open('networkbuster_config.json', 'w'), indent=2)"
Write-Host "   ✅ Core Configuration Updated" -ForegroundColor Green

# 6. Finalization
Write-Host "`n[6/6] 📝 Finalizing Installation..." -ForegroundColor Yellow
Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║              ✅ INSTALLATION SUCCESSFUL!                    ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`n🚀 Preciseliens Mission Control is now ready for use." -ForegroundColor White
Write-Host "   Access the Marketplace directly via the desktop shortcut." -ForegroundColor Gray

$Launch = Read-Host "`nWould you like to launch Mission Control now? (Y/N)"
if ($Launch -eq "Y") {
    Start-Process "cmd.exe" -ArgumentList "/c start `"$InstallDir\challengerepo\real-time-overlay\dist\index.html`""
}
