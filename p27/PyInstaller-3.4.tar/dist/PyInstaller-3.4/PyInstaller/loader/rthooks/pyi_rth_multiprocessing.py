import sys

# 'spawn' multiprocessing needs some adjustments on osx
if sys.version_info >= (3, 4):
    import os
    import re
    import multiprocessing
    import multiprocessing.spawn as spawn
    from subprocess import _args_from_interpreter_flags

    # prevent spawn from trying to read __main__ in from the main script
    multiprocessing.process.ORIGINAL_DIR = None

    def _freeze_support():
        # we want to catch the two processes that are spawned by the
        # multiprocessing code:
        # - the semaphore tracker, which cleans up named semaphores in 
        #   the spawn multiprocessing mode
        # - the fork server, which keeps track of worker processes in 
        #   forkserver mode.
        # both of these processes are started by spawning a new copy of the
        # running executable, passing it the flags from
        # _args_from_interpreter_flags and then "-c" and an import statement.
        # look for those flags and the import statement, then exec() the
        # code ourselves.

        if len(sys.argv) >= 2 and \
                set(sys.argv[1:-2]) == set(_args_from_interpreter_flags()) and \
                sys.argv[-2] == '-c' and \
                (sys.argv[-1].startswith('from multiprocessing.semaphore_tracker import main') or \
                 sys.argv[-1].startswith('from multiprocessing.forkserver import main')):
            exec(sys.argv[-1])
            sys.exit()

        if spawn.is_forking(sys.argv):
            kwds = {}
            for arg in sys.argv[2:]:
                name, value = arg.split('=')
                if value == 'None':
                    kwds[name] = None
                else:
                    kwds[name] = int(value)
            spawn.spawn_main(**kwds)
            sys.exit()

    multiprocessing.freeze_support = spawn.freeze_support = _freeze_support

# Bootloader unsets _MEIPASS2 for child processes to allow running
# PyInstaller binaries inside pyinstaller binaries.
# This is ok for mac or unix with fork() system call.
# But on Windows we need to overcome missing fork() function.

# Module multiprocessing is organized differently in Python 3.4+
try:
    # Python 3.4+
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

# Patch Popen to re-set _MEIPASS2 from sys._MEIPASS.
class _Popen(forking.Popen):
    def __init__(self, *args, **kw):
        if hasattr(sys, 'frozen'):
            # We have to set original _MEIPASS2 value from sys._MEIPASS
            # to get --onefile mode working.
            os.putenv('_MEIPASS2', sys._MEIPASS)  # @UndefinedVariable
        try:
            super(_Popen, self).__init__(*args, **kw)
        finally:
            if hasattr(sys, 'frozen'):
                # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                # available. In those cases we cannot delete the variable
                # but only set it to the empty string. The bootloader
                # can handle this case.
                if hasattr(os, 'unsetenv'):
                    os.unsetenv('_MEIPASS2')
                else:
                    os.putenv('_MEIPASS2', '')

forking.Popen = _Popen
