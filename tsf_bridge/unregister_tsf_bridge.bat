@echo off
chcp 65001 >nul
setlocal
set "SCRIPT_DIR=%~dp0"

:: Check for Administrator rights
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Please run this batch file as ADMINISTRATOR.
    rem pause
    exit /b 1
)

set "DLL64=%SCRIPT_DIR%x64\UclTsfBridge.dll"
set "DLL86=%SCRIPT_DIR%x86\UclTsfBridge.dll"
set "UNLOCK_SCRIPT=%SCRIPT_DIR%unlock_tsf_bridge.ps1"
set "UNREGISTER_FAILED=0"
set "PS_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if exist "%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe" set "PS_EXE=%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe"
if not exist "%PS_EXE%" set "PS_EXE=powershell.exe"

:: Unregister 64-bit DLL
if exist "%DLL64%" (
    echo [INFO] Unregistering x64 TSF Bridge...
    "%SystemRoot%\System32\regsvr32.exe" /u /s "%DLL64%"
    if errorlevel 1 (
        echo [ERROR] Failed to unregister x64 TSF Bridge.
        set "UNREGISTER_FAILED=1"
    )
)

:: Unregister 32-bit DLL
if exist "%SystemRoot%\SysWOW64\regsvr32.exe" (
    if exist "%DLL86%" (
        echo [INFO] Unregistering x86 TSF Bridge...
        "%SystemRoot%\SysWOW64\regsvr32.exe" /u /s "%DLL86%"
        if errorlevel 1 (
            echo [ERROR] Failed to unregister x86 TSF Bridge.
            set "UNREGISTER_FAILED=1"
        )
    )
) else (
    if exist "%DLL86%" (
        "%SystemRoot%\System32\regsvr32.exe" /u /s "%DLL86%"
        if errorlevel 1 (
            echo [ERROR] Failed to unregister x86 TSF Bridge.
            set "UNREGISTER_FAILED=1"
        )
    )
)

if "%UNREGISTER_FAILED%"=="1" (
    echo [ERROR] Unregistration failed.
    exit /b 1
)

if exist "%UNLOCK_SCRIPT%" (
    echo [INFO] Checking for processes still locking UclTsfBridge.dll...
    "%PS_EXE%" -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%UNLOCK_SCRIPT%" -DllPath "%DLL64%" "%DLL86%"
    if errorlevel 2 (
        echo [WARN] Some processes still lock UclTsfBridge.dll.
    ) else (
        if errorlevel 1 (
            echo [WARN] Lock cleanup did not complete normally.
        )
    )
) else (
    echo [WARN] unlock_tsf_bridge.ps1 not found; skipped lock cleanup.
)

echo [OK] Unregistration finished.
rem pause
exit /b 0
