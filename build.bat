chcp 950
rd /S build
SET VS90COMNTOOLS=%VS140COMNTOOLS%

:: Build TSF Bridge first
call build_tsf.bat

:: Build Main EXE
c:\python27\scripts\pyinstaller -F -w --onefile --clean --icon="pic\uclliu_logo.ico" --version-file=metadata.txt --exclude-module=_ssl --exclude-module=_bz2 --exclude-module=_lzma --exclude-module=pyconfig uclliu.pyw 

echo [OK] All components built.
