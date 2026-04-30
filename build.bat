rd /S build
SET VS90COMNTOOLS=%VS140COMNTOOLS%
rem c:\python27\scripts\pyinstaller uclliu.pyw -F -w --version-file=metadata.txt --exclude-module socket
rem --exclude-module=_ssl --exclude-module=_bz2 --exclude-module=_lzma --exclude-module=pyconfig
c:\python27\scripts\pyinstaller -F -w --onefile --clean --icon="pic\uclliu_logo.ico" --version-file=metadata.txt --exclude-module=_ssl --exclude-module=_bz2 --exclude-module=_lzma --exclude-module=pyconfig uclliu.pyw 
if exist "tsf_bridge\UclTsfBridge\x64\Release\UclTsfBridge.dll" (
  if not exist "dist\tsf_bridge" mkdir "dist\tsf_bridge"
  copy /Y "tsf_bridge\UclTsfBridge\x64\Release\UclTsfBridge.dll" "dist\tsf_bridge\UclTsfBridge.dll"
  copy /Y "tsf_bridge\register_tsf_bridge.bat" "dist\tsf_bridge\register_tsf_bridge.bat"
  copy /Y "tsf_bridge\unregister_tsf_bridge.bat" "dist\tsf_bridge\unregister_tsf_bridge.bat"
)
