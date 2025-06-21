#-----------------------------------------------------------------------------
# Copyright (c) 2005-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


# The 'sysconfig' module requires Makefile and pyconfig.h files from
# Python installation. 'sysconfig' parses these files to get some
# information from them.
# TODO Verify that bundling Makefile and pyconfig.h is still required for Python 3.

import sysconfig
import os

from PyInstaller.utils.hooks import relpath_to_config_or_make
from PyInstaller.compat import is_win

_CONFIG_H = sysconfig.get_config_h_filename()
if hasattr(sysconfig, 'get_makefile_filename'):
    # sysconfig.get_makefile_filename is missing in Python < 2.7.9
    _MAKEFILE = sysconfig.get_makefile_filename()
else:
    _MAKEFILE = sysconfig._get_makefile_filename()


datas = [(_CONFIG_H, relpath_to_config_or_make(_CONFIG_H))]

# The Makefile does not exist on all platforms, eg. on Windows
if os.path.exists(_MAKEFILE):
    datas.append((_MAKEFILE, relpath_to_config_or_make(_MAKEFILE)))

if not is_win and hasattr(sysconfig, '_get_sysconfigdata_name'):
    # Python 3.6 uses additional modules like
    # `_sysconfigdata_m_linux_x86_64-linux-gnu`, see
    # https://github.com/python/cpython/blob/3.6/Lib/sysconfig.py#L417
    # Note: Some versions of Anaconda backport this feature to before 3.6.
    # See issue #3105
    hiddenimports = [sysconfig._get_sysconfigdata_name()]
