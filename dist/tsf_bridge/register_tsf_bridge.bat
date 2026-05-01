@echo off
chcp 65001 >nul
setlocal
set "SCRIPT_DIR=%~dp0"

:: Check for Administrator rights
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Please run this batch file as ADMINISTRATOR.
    echo TSF registration requires HKLM registry access.
    rem pause
    exit /b 1
)

set "DLL64=%SCRIPT_DIR%x64\UclTsfBridge.dll"
set "DLL86=%SCRIPT_DIR%x86\UclTsfBridge.dll"

:: Register 64-bit DLL
if exist "%DLL64%" (
    echo [INFO] Registering x64 TSF Bridge...
    "%SystemRoot%\System32\regsvr32.exe" /s "%DLL64%"
) else (
    echo [WARN] x64 DLL not found at %DLL64%
)

:: Register 32-bit DLL (on 64-bit Windows)
if exist "%SystemRoot%\SysWOW64\regsvr32.exe" (
    if exist "%DLL86%" (
        echo [INFO] Registering x86 TSF Bridge...
        "%SystemRoot%\SysWOW64\regsvr32.exe" /s "%DLL86%"
    ) else (
        echo [WARN] x86 DLL not found at %DLL86%
    )
) else (
    :: 32-bit Windows
    if exist "%DLL86%" (
        echo [INFO] Registering x86 TSF Bridge...
        "%SystemRoot%\System32\regsvr32.exe" /s "%DLL86%"
    )
)

echo [OK] Registration finished.
echo Please add "UCLLIU TSF Bridge" to your keyboard list in Language Settings.
rem pause
exit /b 0
