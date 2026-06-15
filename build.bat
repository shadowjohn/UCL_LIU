@echo off
setlocal
chcp 950
if exist build rd /S /Q build
SET VS90COMNTOOLS=%VS140COMNTOOLS%

:: Build TSF Bridge first
call build_tsf.bat
if errorlevel 1 (
  echo [ERROR] TSF Bridge build failed.
  exit /b 1
)

:: Build Main EXE
if not exist c:\python27\scripts\pyinstaller.exe (
  echo [ERROR] PyInstaller not found: c:\python27\scripts\pyinstaller.exe
  exit /b 1
)
c:\python27\scripts\pyinstaller -F -w --onefile --clean --icon="pic\uclliu_logo.ico" --version-file=metadata.txt --exclude-module=_ssl --exclude-module=_bz2 --exclude-module=_lzma --exclude-module=pyconfig uclliu.pyw 
if errorlevel 1 (
  echo [ERROR] PyInstaller build failed.
  exit /b 1
)
if not exist dist\uclliu.exe (
  echo [ERROR] dist\uclliu.exe was not created.
  exit /b 1
)

echo [OK] All components built.
endlocal
exit /b 0
