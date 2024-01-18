rd /S build
SET VS90COMNTOOLS=%VS140COMNTOOLS%
rem c:\python27\scripts\pyinstaller uclliu.pyw -F -w --version-file=metadata.txt --exclude-module socket
rem --exclude-module=_ssl --exclude-module=_bz2 --exclude-module=_lzma --exclude-module=pyconfig
c:\python312\scripts\pyinstaller -F -w --onefile --clean --icon="pic\uclliu_logo.ico" --version-file=metadata.txt --exclude-module=_ssl --exclude-module=_bz2 --exclude-module=_lzma --exclude-module=pyconfig uclliu.pyw 