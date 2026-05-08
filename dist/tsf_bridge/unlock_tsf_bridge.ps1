param(
    [string[]]$DllPath = @(),
    [switch]$PauseOnExit
)

$ErrorActionPreference = "Continue"

function Finish($ExitCode) {
    if ($PauseOnExit) {
        Read-Host "Press Enter to close this window" | Out-Null
    }
    exit $ExitCode
}

function Normalize-PathText($PathText) {
    if ([string]::IsNullOrWhiteSpace($PathText)) {
        return ""
    }
    try {
        return [System.IO.Path]::GetFullPath($PathText).TrimEnd('\').ToLowerInvariant()
    }
    catch {
        return $PathText.TrimEnd('\').ToLowerInvariant()
    }
}

function Read-YesNo($Prompt) {
    $answer = Read-Host ($Prompt + " [y/N]")
    if ([string]::IsNullOrWhiteSpace($answer)) {
        return $false
    }
    return $answer -match '^(y|yes)$'
}

function Get-LockingProcesses {
    $results = @()
    foreach ($process in Get-Process) {
        if ($process.Id -eq $PID) {
            continue
        }

        try {
            foreach ($module in $process.Modules) {
                if ($module.ModuleName -ieq "UclTsfBridge.dll") {
                    $results += [PSCustomObject]@{
                        Id = $process.Id
                        ProcessName = $process.ProcessName
                        ModulePath = $module.FileName
                    }
                    break
                }
            }
        }
        catch {
            continue
        }
    }
    return $results | Sort-Object ProcessName, Id
}

function Is-ProtectedProcessName($ProcessName) {
    $protectedNames = @(
        "idle",
        "system",
        "registry",
        "smss",
        "csrss",
        "wininit",
        "winlogon",
        "services",
        "lsass",
        "lsaiso",
        "fontdrvhost",
        "dwm",
        "svchost"
    )
    return $protectedNames -contains $ProcessName.ToLowerInvariant()
}

function Should-SkipProcessName($ProcessName) {
    $skipNames = @(
        "powershell",
        "pwsh",
        "regsvr32",
        "uclliu",
        "uclliu_debug",
        "python",
        "pythonw"
    )
    return $skipNames -contains $ProcessName.ToLowerInvariant()
}

function Close-LockingProcess($LockInfo) {
    $name = $LockInfo.ProcessName
    $id = [int]$LockInfo.Id

    if (Is-ProtectedProcessName $name) {
        Write-Warning "Skipping protected process $name (PID $id)."
        return
    }

    if (Should-SkipProcessName $name) {
        Write-Warning "Skipping helper/current process candidate $name (PID $id)."
        return
    }

    if ($name -ieq "explorer") {
        if (Read-YesNo "Restart explorer.exe to release UclTsfBridge.dll from PID $id?") {
            try {
                Stop-Process -Id $id -Force -ErrorAction Stop
                Start-Sleep -Seconds 2
                if (-not $script:ExplorerRestarted) {
                    Start-Process explorer.exe
                    $script:ExplorerRestarted = $true
                }
                Write-Host "Restarted explorer.exe."
            }
            catch {
                Write-Warning "Failed to restart explorer.exe from PID ${id}: $($_.Exception.Message)"
            }
        }
        return
    }

    if (-not (Read-YesNo "Close $name (PID $id) to release UclTsfBridge.dll?")) {
        return
    }

    try {
        $process = Get-Process -Id $id -ErrorAction Stop
        $closed = $false
        if ($process.MainWindowHandle -ne 0) {
            $closed = $process.CloseMainWindow()
        }

        if ($closed) {
            if ($process.WaitForExit(5000)) {
                Write-Host "Closed $name (PID $id)."
                return
            }
        }

        $stillRunning = Get-Process -Id $id -ErrorAction SilentlyContinue
        if ($stillRunning -and (Read-YesNo "Force terminate $name (PID $id)? Unsaved work may be lost.")) {
            Stop-Process -Id $id -Force -ErrorAction Stop
            Write-Host "Terminated $name (PID $id)."
        }
    }
    catch {
        Write-Warning "Failed to close $name (PID ${id}): $($_.Exception.Message)"
    }
}

$targetPaths = @()
foreach ($path in $DllPath) {
    $normalized = Normalize-PathText $path
    if ($normalized -ne "") {
        $targetPaths += $normalized
    }
}

Write-Host "[INFO] Checking processes that have UclTsfBridge.dll loaded..."
if ($targetPaths.Count -gt 0) {
    foreach ($path in $targetPaths) {
        Write-Host "       target: $path"
    }
}

$script:ExplorerRestarted = $false
$locks = @(Get-LockingProcesses)
if ($locks.Count -eq 0) {
    Write-Host "[OK] No process is locking UclTsfBridge.dll."
    Finish 0
}

Write-Host "[INFO] Processes currently loading UclTsfBridge.dll:"
$locks | Format-Table -AutoSize

foreach ($lock in $locks) {
    Close-LockingProcess $lock
}

Start-Sleep -Milliseconds 500
$remaining = @(Get-LockingProcesses)
if ($remaining.Count -eq 0) {
    Write-Host "[OK] UclTsfBridge.dll is no longer loaded by any visible process."
    Finish 0
}

Write-Warning "UclTsfBridge.dll is still loaded by the following process(es):"
$remaining | Format-Table -AutoSize
Write-Warning "Close the remaining process(es), then rebuild/copy again. A sign out is only needed if these processes cannot be closed."
Finish 2
