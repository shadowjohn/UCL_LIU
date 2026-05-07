@echo off
setlocal

set "PROJECT=tsf_bridge\UclTsfBridge\UclTsfBridge.vcxproj"
set "OUT_DLL_X64=tsf_bridge\UclTsfBridge\x64\Release\UclTsfBridge.dll"
set "OUT_DLL_X86=tsf_bridge\UclTsfBridge\Win32\Release\UclTsfBridge.dll"
set "DIST_DIR=dist\tsf_bridge"
set "MSBUILD="
set "PLATFORM_TOOLSET=v143"
set "UNLOCK_SCRIPT=tsf_bridge\unlock_tsf_bridge.ps1"
set "PS_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if exist "%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe" set "PS_EXE=%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe"
if not exist "%PS_EXE%" set "PS_EXE=powershell.exe"

rem Keep this file ASCII-only because cmd.exe may break UTF-8 batch files on user machines.
if "%MSBUILD%"=="" if exist "%ProgramFiles%\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\amd64\MSBuild.exe" set "MSBUILD=%ProgramFiles%\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\amd64\MSBuild.exe"
if "%MSBUILD%"=="" if exist "%ProgramFiles%\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\amd64\MSBuild.exe" set "MSBUILD=%ProgramFiles%\Microsoft Visual Studio\2022\BuildTools\MSBuild\Current\Bin\amd64\MSBuild.exe"
if "%MSBUILD%"=="" if exist "%ProgramFiles%\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\amd64\MSBuild.exe" set "MSBUILD=%ProgramFiles%\Microsoft Visual Studio\2022\Professional\MSBuild\Current\Bin\amd64\MSBuild.exe"
if "%MSBUILD%"=="" if exist "%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\amd64\MSBuild.exe" set "MSBUILD=%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\amd64\MSBuild.exe"
if "%MSBUILD%"=="" if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin\amd64\MSBuild.exe" set "MSBUILD=%ProgramFiles(x86)%\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin\amd64\MSBuild.exe"
if "%MSBUILD%"=="" if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\amd64\MSBuild.exe" set "MSBUILD=%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\amd64\MSBuild.exe"

if "%MSBUILD%"=="" if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" (
  for /f "usebackq tokens=*" %%i in (`"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -version "[16.0,18.0)" -products * -requires Microsoft.Component.MSBuild -find MSBuild\**\Bin\amd64\MSBuild.exe`) do (
    set "MSBUILD=%%i"
  )
)

if "%MSBUILD%"=="" (
  echo [ERROR] MSBuild.exe not found. Please install Visual Studio C++ Build Tools.
  exit /b 1
)

if not exist "%PROJECT%" (
  echo [ERROR] TSF Bridge project not found: %PROJECT%
  exit /b 1
)

echo [INFO] MSBuild: %MSBUILD%
echo [INFO] PlatformToolset override: %PLATFORM_TOOLSET%

rem Avoid stale MSVC PDB server instances from another VS toolset causing LNK1101.
taskkill /IM mspdbsrv.exe /F >nul 2>nul

echo [INFO] Build TSF Bridge Release x64...
"%MSBUILD%" "%PROJECT%" /p:Configuration=Release /p:Platform=x64 /p:PlatformToolset=%PLATFORM_TOOLSET% /p:PreferredToolArchitecture=x64 /nr:false
if errorlevel 1 (
  echo [ERROR] TSF Bridge x64 build failed.
  exit /b 1
)

echo [INFO] Build TSF Bridge Release Win32...
"%MSBUILD%" "%PROJECT%" /p:Configuration=Release /p:Platform=Win32 /p:PlatformToolset=%PLATFORM_TOOLSET% /p:PreferredToolArchitecture=x64 /nr:false
if errorlevel 1 (
  echo [ERROR] TSF Bridge Win32 build failed.
  exit /b 1
)

if not exist "%OUT_DLL_X64%" (
  echo [ERROR] Output DLL x64 not found: %OUT_DLL_X64%
  exit /b 1
)
if not exist "%OUT_DLL_X86%" (
  echo [ERROR] Output DLL x86 not found: %OUT_DLL_X86%
  exit /b 1
)

if not exist "%DIST_DIR%\x64" mkdir "%DIST_DIR%\x64"
if not exist "%DIST_DIR%\x86" mkdir "%DIST_DIR%\x86"

call :CopyWithUnlock "%OUT_DLL_X64%" "%DIST_DIR%\x64\UclTsfBridge.dll" "x64 DLL"
if errorlevel 1 (
  exit /b 1
)
call :CopyWithUnlock "%OUT_DLL_X86%" "%DIST_DIR%\x86\UclTsfBridge.dll" "x86 DLL"
if errorlevel 1 (
  exit /b 1
)

copy /Y "tsf_bridge\register_tsf_bridge.bat" "%DIST_DIR%\register_tsf_bridge.bat"
if errorlevel 1 (
  echo [ERROR] Failed to copy register_tsf_bridge.bat.
  exit /b 1
)
copy /Y "tsf_bridge\unregister_tsf_bridge.bat" "%DIST_DIR%\unregister_tsf_bridge.bat"
if errorlevel 1 (
  echo [ERROR] Failed to copy unregister_tsf_bridge.bat.
  exit /b 1
)
copy /Y "tsf_bridge\unlock_tsf_bridge.ps1" "%DIST_DIR%\unlock_tsf_bridge.ps1"
if errorlevel 1 (
  echo [ERROR] Failed to copy unlock_tsf_bridge.ps1.
  exit /b 1
)

echo [OK] TSF Bridge (x64/x86) copied to %DIST_DIR%
endlocal
exit /b 0

:CopyWithUnlock
set "COPY_SRC=%~1"
set "COPY_DST=%~2"
set "COPY_NAME=%~3"

copy /Y "%COPY_SRC%" "%COPY_DST%"
if not errorlevel 1 (
  exit /b 0
)

echo [WARN] Failed to copy %COPY_NAME%. It may be loaded by Explorer or another process.
echo [INFO] Trying to close processes that lock UclTsfBridge.dll...
call :RunUnlockHelper

copy /Y "%COPY_SRC%" "%COPY_DST%"
if errorlevel 1 (
  echo [ERROR] Failed to copy %COPY_NAME% after unlock attempt.
  echo [ERROR] Close the remaining process shown above, then run build_tsf.bat again.
  exit /b 1
)
exit /b 0

:RunUnlockHelper
if not exist "%UNLOCK_SCRIPT%" (
  echo [WARN] %UNLOCK_SCRIPT% not found; skipped lock cleanup.
  exit /b 1
)

"%PS_EXE%" -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%UNLOCK_SCRIPT%" -DllPath "%DIST_DIR%\x64\UclTsfBridge.dll" "%DIST_DIR%\x86\UclTsfBridge.dll"
exit /b 0
