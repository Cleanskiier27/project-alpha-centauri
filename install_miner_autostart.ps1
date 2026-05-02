#Requires -RunAsAdministrator

<#
.SYNOPSIS
    NetworkBuster Miner Auto-Start Installer
.DESCRIPTION
    Registers the NetworkBuster processing engine (Miner) to Windows system startup.
#>

$InstallDir = $PSScriptRoot
$ServiceName = "NetworkBuster_Miner_AutoStart"
$MinerScript = "tools\python\ai-training-pipeline.py"

Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║  NetworkBuster Miner Registration Service                 ║" -ForegroundColor Yellow
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow

Write-Host "`n[1/3] Preparing Miner Execution Environment..." -ForegroundColor Cyan

# Create the batch wrapper for the miner
$minerBat = @"
@echo off
title NetworkBuster Miner Engine
echo 🛰️ Initializing Miner (AI Training Pipeline)...
cd /d "$InstallDir"
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)
python "$MinerScript"
pause
"@

$minerBatPath = Join-Path $InstallDir "run_miner.bat"
Set-Content -Path $minerBatPath -Value $minerBat
Write-Host "   ✅ Miner execution script created: $minerBatPath" -ForegroundColor Green

Write-Host "`n[2/3] Registering to Windows Startup (User Context)..." -ForegroundColor Cyan

$startupFolder = [Environment]::GetFolderPath("Startup")
$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut("$startupFolder\NetworkBusterMiner.lnk")
$shortcut.TargetPath = $minerBatPath
$shortcut.WorkingDirectory = $InstallDir
$shortcut.Description = "NetworkBuster Miner Auto-Start"
$shortcut.Save()

Write-Host "   ✅ Startup shortcut pinned: $startupFolder\NetworkBusterMiner.lnk" -ForegroundColor Green

Write-Host "`n[3/3] Registering System-Level Scheduled Task..." -ForegroundColor Cyan

$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$minerBatPath`"" -WorkingDirectory $InstallDir
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType InteractiveToken -RunLevel Highest

try {
    Register-ScheduledTask -Action $action -Trigger $trigger -Principal $principal -TaskName "$ServiceName" -Force | Out-Null
    Write-Host "   ✅ System-level autostart task registered: $ServiceName" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Failed to register scheduled task. Ensure you are running as Admin." -ForegroundColor Red
}

Write-Host "`n📊 Registration Summary:" -ForegroundColor White
Write-Host "   • Service: $ServiceName" -ForegroundColor White
Write-Host "   • Target: $MinerScript" -ForegroundColor White
Write-Host "   • Context: Highest Privileges / At Logon" -ForegroundColor White

Write-Host "`n✅ MINER AUTOSTART REGISTRATION COMPLETE" -ForegroundColor Green
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
