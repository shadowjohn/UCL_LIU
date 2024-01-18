rd /S build
SET VS90COMNTOOLS=%VS140COMNTOOLS%
rem c:\python27\scripts\pyinstaller uclliu.pyw -F -c -d -n uclliu_debug
copy /y uclliu.pyw uclliu_debug.py
c:\python312\scripts\pyinstaller uclliu_debug.py --onefile --clean --icon="pic\uclliu_logo.ico" --version-file=metadata.txt --exclude-module=_ssl --exclude-module=_bz2 --exclude-module=_lzma --exclude-module=pyconfig -F -c
del uclliu_debug.py