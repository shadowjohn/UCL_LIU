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

:: Unregister 64-bit DLL
if exist "%DLL64%" (
    echo [INFO] Unregistering x64 TSF Bridge...
    "%SystemRoot%\System32\regsvr32.exe" /u /s "%DLL64%"
)

:: Unregister 32-bit DLL
if exist "%SystemRoot%\SysWOW64\regsvr32.exe" (
    if exist "%DLL86%" (
        echo [INFO] Unregistering x86 TSF Bridge...
        "%SystemRoot%\SysWOW64\regsvr32.exe" /u /s "%DLL86%"
    )
) else (
    if exist "%DLL86%" (
        "%SystemRoot%\System32\regsvr32.exe" /u /s "%DLL86%"
    )
)

echo [OK] Unregistration finished.
rem pause
exit /b 0
