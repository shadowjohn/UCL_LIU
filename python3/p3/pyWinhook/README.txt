A pyHook fork with some updates for support latest Visual Studio compilers.
See the website, http://pyhook.sourceforge.net/, for the original pyHook project.

Known bugs
----------
- PyInstaller can't build single-file executables using pyWinhook. This may be
  fixed in 1.5.1, but hasn't been tested.
- pyWinhook is reported to break dead keys on non-US-english keyboards.
- WM_CHAR messages are not intercepted by pyWinhook, even if SubscribeKeyChar() or
  SubscribeKeyAll() are used to set the callback function.

Limitations
-----------
- pyWinhook will not work on Win9x (no messages show up) as it uses hooks which
  are not present in Windows systems prior to NT 4.0 SP3.
