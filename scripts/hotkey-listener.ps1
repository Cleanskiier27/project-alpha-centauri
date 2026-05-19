# NetworkBuster Global Hotkey Listener
# Registers:
# - LWin: Automated Finance Update
# - Ctrl + Win + F: Growth Advice Terminal

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;

public class HotKeyManager {
    [DllImport("user32.dll")]
    public static extern bool RegisterHotKey(IntPtr hWnd, int id, int fsModifiers, int vlc);

    [DllImport("user32.dll")]
    public static extern bool UnregisterHotKey(IntPtr hWnd, int id);

    public const int MOD_CONTROL = 0x0002;
    public const int MOD_WIN = 0x0008;
}
"@

$form = New-Object Windows.Forms.Form
$form.ShowInTaskbar = $false
$form.WindowState = [Windows.Forms.FormWindowState]::Minimized

# IDs for hotkeys
$FINANCE_ID = 1
$ADVICE_ID = 2

# FS Modifiers: Win=8, Control=2
# VLC: F=0x46, LWin=0x5B

# Register Ctrl + Win + F (Modifiers: 2 + 8 = 10)
$null = [HotKeyManager]::RegisterHotKey($form.Handle, $ADVICE_ID, 10, 0x46)

# Register LWin (Solo)
# NOTE: Registering LWin solo is risky. We'll use a listener loop for specific key states instead 
# if we want to avoid breaking the Start menu, but the user asked for it.
# $null = [HotKeyManager]::RegisterHotKey($form.Handle, $FINANCE_ID, 0, 0x5B)

Write-Host "🛰️ Global Hotkey Listener Active..." -ForegroundColor Green
Write-Host "   • [Ctrl + Win + F] : Growth Advice" -ForegroundColor Cyan
Write-Host "   • [LWin]           : Automated Finance (via Polling)" -ForegroundColor Cyan
Write-Host "`nListening for commands, Captain Middleton..." -ForegroundColor Gray

# Define Action Functions
function Update-Finance {
    Write-Host "`n[HOTKEY] Triggering Finance Update..." -ForegroundColor Yellow
    npm run finance:mine
}

function Show-Advice {
    Write-Host "`n[HOTKEY] Opening Growth Advice..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "node scripts/growth-advice.js"
}

# Message loop for HotKey events + Polling for solo Win key to avoid blocking it
$winKeyState = 0
while ($true) {
    # Check for RegisterHotKey events (ADVICE_ID)
    if ([Windows.Forms.Application]::DoEvents()) { } # Process messages

    # Native RegisterHotKey is complex in pure PS loop without WNDPROC
    # Switching to a more robust polling method for both to ensure performance
    
    $ctrl = [Windows.Forms.Control]::ModifierKeys -band [Windows.Forms.Keys]::Control
    $win = [Windows.Forms.Control]::ModifierKeys -band [Windows.Forms.Keys]::Windows
    $fKey = [Windows.Forms.Control]::IsKeyLocked([Windows.Forms.Keys]::F) # Not quite right for status
    
    # Using User32 GetAsyncKeyState for raw polling
    $getAsyncKeyState = Add-Type -MemberDefinition '[DllImport("user32.dll")] public static extern short GetAsyncKeyState(int vKey);' -Name "User32Key" -Namespace "Win32" -PassThru
    
    $isWinDown = [Win32.User32Key]::GetAsyncKeyState(0x5B) -ne 0 -or [Win32.User32Key]::GetAsyncKeyState(0x5C) -ne 0
    $isCtrlDown = [Win32.User32Key]::GetAsyncKeyState(0x11) -ne 0
    $isFDown = [Win32.User32Key]::GetAsyncKeyState(0x46) -ne 0

    # Trigger Finance on Win Key Press (Once per press)
    if ($isWinDown -and -not $isCtrlDown) {
        if ($winKeyState -eq 0) {
            Update-Finance
            $winKeyState = 1
        }
    } elseif (-not $isWinDown) {
        $winKeyState = 0
    }

    # Trigger Advice on Ctrl + Win + F
    if ($isWinDown -and $isCtrlDown -and $isFDown) {
        Show-Advice
        while ([Win32.User32Key]::GetAsyncKeyState(0x46) -ne 0) { Start-Sleep -Milliseconds 100 } # Wait for release
    }

    Start-Sleep -Milliseconds 100
}
