#-----------------------------------------------------------------------------
# Copyright (c) 2005-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


__all__ = ('HOMEPATH', 'PLATFORM', '__version__')

import os
import sys

from . import compat
from .compat import is_win, is_py2
from .utils.git import get_repo_revision


# Note: Keep this variable as plain string so it could be updated automatically
#       when doing a release.
__version__ = '3.4'


# Absolute path of this package's directory. Save this early so all
# submodules can use the absolute path. This is required e.g. if the
# current directorey changes prior to loading the hooks.
PACKAGEPATH = os.path.abspath(os.path.dirname(__file__))

HOMEPATH = os.path.dirname(PACKAGEPATH)
if is_win and is_py2:
    # This ensures for Python 2 that PyInstaller will work on Windows
    # with paths containing foreign characters.
    try:
        unicode(HOMEPATH)
    except UnicodeDecodeError:
        # Do conversion to ShortPathName really only in case HOMEPATH is not
        # ascii only - conversion to unicode type cause this unicode error.
        try:
            HOMEPATH = compat.win32api.GetShortPathName(HOMEPATH)
        except ImportError:
            pass


# Update __version__ as necessary.
if os.path.exists(os.path.join(HOMEPATH, 'setup.py')):
    # PyInstaller is run directly from source without installation or
    # __version__ is called from 'setup.py' ...
    if compat.getenv('PYINSTALLER_DO_RELEASE') == '1':
        # Suppress the git revision when doing a release.
        pass
    elif 'sdist' not in sys.argv:
        # and 'setup.py' was not called with 'sdist' argument.
        # For creating source tarball we do not want git revision
        # in the filename.
        try:
            __version__ += get_repo_revision()
        except Exception:
            # Write to stderr because stdout is used for eval() statement
            # in some subprocesses.
            sys.stderr.write('WARN: failed to parse git revision')
else:
    # PyInstaller was installed by `python setup.py install'.
    import pkg_resources
    __version__ = pkg_resources.get_distribution('PyInstaller').version


## Default values of paths where to put files created by PyInstaller.
## Mind option-help in build_main when changes these
# Folder where to put created .spec file.
DEFAULT_SPECPATH = compat.getcwd()
# Folder where to put created .spec file.
# Where to put the final app.
DEFAULT_DISTPATH = os.path.join(compat.getcwd(), 'dist')
# Where to put all the temporary work files, .log, .pyz and etc.
DEFAULT_WORKPATH = os.path.join(compat.getcwd(), 'build')


PLATFORM = compat.system() + '-' + compat.architecture()
# Include machine name in path to bootloader for some machines.
# e.g. 'arm'
if compat.machine():
    PLATFORM += '-' + compat.machine()
