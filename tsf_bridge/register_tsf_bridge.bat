@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "DLL=%SCRIPT_DIR%UclTsfBridge\x64\Release\UclTsfBridge.dll"
if not exist "%DLL%" set "DLL=%SCRIPT_DIR%UclTsfBridge.dll"
if not exist "%DLL%" (
  echo UclTsfBridge.dll not found.
  exit /b 2
)
%SystemRoot%\System32\regsvr32.exe /s "%DLL%"
exit /b %ERRORLEVEL%
