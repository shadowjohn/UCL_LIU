rd /S build
SET VS90COMNTOOLS=%VS140COMNTOOLS%
rem c:\python27\scripts\pyinstaller uclliu.pyw -F -w --version-file=metadata.txt --exclude-module socket
c:\python27\scripts\pyinstaller uclliu.pyw -F -w --version-file=metadata.txt --exclude-module=_ssl --exclude-module=_bz2 --exclude-module=_lzma --exclude-module=pyconfig