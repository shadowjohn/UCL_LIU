#-----------------------------------------------------------------------------
# Copyright (c) 2005-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

"""
PyWin32 package 'win32com' extends it's __path__ attribute with win32comext
directory and thus PyInstaller is not able to find modules in it. For example
module 'win32com.shell' is in reality 'win32comext.shell'.

>>> win32com.__path__
['win32com', 'C:\\Python27\\Lib\\site-packages\\win32comext']

"""


import os

from PyInstaller.utils.hooks import logger, get_module_file_attribute
from PyInstaller.compat import is_win, is_cygwin


def pre_safe_import_module(api):
    if not (is_win or is_cygwin):
        return
    win32com_dir = os.path.dirname(get_module_file_attribute('win32com'))
    comext_dir = os.path.join(os.path.dirname(win32com_dir), 'win32comext')
    logger.debug('win32com: extending __path__ with dir %r' % comext_dir)
    # Append the __path__ where PyInstaller will look for 'win32com' modules.'
    api.append_package_path(comext_dir)
