@echo off
setlocal

set "PROJECT=tsf_bridge\UclTsfBridge\UclTsfBridge.vcxproj"
set "OUT_DLL_X64=tsf_bridge\UclTsfBridge\x64\Release\UclTsfBridge.dll"
set "OUT_DLL_X86=tsf_bridge\UclTsfBridge\Win32\Release\UclTsfBridge.dll"
set "DIST_DIR=dist\tsf_bridge"
set "MSBUILD="

rem Keep this file ASCII-only because cmd.exe may break UTF-8 batch files on user machines.
if exist "%ProgramFiles%\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\amd64\MSBuild.exe" set "MSBUILD=%ProgramFiles%\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\amd64\MSBuild.exe"
if "%MSBUILD%"=="" if exist "%ProgramFiles%\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\amd64\MSBuild.exe" set "MSBUILD=%ProgramFiles%\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\amd64\MSBuild.exe"
if "%MSBUILD%"=="" if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\amd64\MSBuild.exe" set "MSBUILD=%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\amd64\MSBuild.exe"

if "%MSBUILD%"=="" if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" (
  for /f "usebackq tokens=*" %%i in (`"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.Component.MSBuild -find MSBuild\**\Bin\amd64\MSBuild.exe`) do (
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

echo [INFO] Build TSF Bridge Release x64...
"%MSBUILD%" "%PROJECT%" /p:Configuration=Release /p:Platform=x64
if errorlevel 1 (
  echo [ERROR] TSF Bridge x64 build failed.
  exit /b 1
)

echo [INFO] Build TSF Bridge Release Win32...
"%MSBUILD%" "%PROJECT%" /p:Configuration=Release /p:Platform=Win32
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

copy /Y "%OUT_DLL_X64%" "%DIST_DIR%\x64\UclTsfBridge.dll"
copy /Y "%OUT_DLL_X86%" "%DIST_DIR%\x86\UclTsfBridge.dll"

copy /Y "tsf_bridge\register_tsf_bridge.bat" "%DIST_DIR%\register_tsf_bridge.bat"
copy /Y "tsf_bridge\unregister_tsf_bridge.bat" "%DIST_DIR%\unregister_tsf_bridge.bat"

echo [OK] TSF Bridge (x64/x86) copied to %DIST_DIR%
endlocal
