@echo off
setlocal

set "PROJECT=tsf_bridge\UclTsfBridge\UclTsfBridge.vcxproj"
set "OUT_DLL=tsf_bridge\UclTsfBridge\x64\Release\UclTsfBridge.dll"
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
  echo [ERROR] TSF Bridge build failed.
  exit /b 1
)

if not exist "%OUT_DLL%" (
  echo [ERROR] Output DLL not found: %OUT_DLL%
  exit /b 1
)

if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"
copy /Y "%OUT_DLL%" "%DIST_DIR%\UclTsfBridge.dll"
if errorlevel 1 (
  echo [ERROR] Copy UclTsfBridge.dll failed. Close UCL_LIU or unregister/unload TSF Bridge, then retry.
  exit /b 1
)
copy /Y "tsf_bridge\register_tsf_bridge.bat" "%DIST_DIR%\register_tsf_bridge.bat"
if errorlevel 1 (
  echo [ERROR] Copy register_tsf_bridge.bat failed.
  exit /b 1
)
copy /Y "tsf_bridge\unregister_tsf_bridge.bat" "%DIST_DIR%\unregister_tsf_bridge.bat"
if errorlevel 1 (
  echo [ERROR] Copy unregister_tsf_bridge.bat failed.
  exit /b 1
)

echo [OK] TSF Bridge copied to %DIST_DIR%
endlocal
