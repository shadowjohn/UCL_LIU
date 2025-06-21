# ----------------------------------------------------------------------------
# Copyright (c) 2005-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------
from ..hooks import exec_statement

# NOTE: This function requires PyInstaller to be on the default "sys.path" for
# the called Python process. Running py.test changes the working dir to a temp
# dir, so PyInstaller should be installed via either "setup.py install" or
# "setup.py develop" before running py.test.


def get_pywin32_module_file_attribute(module_name):
    """
    Get the absolute path of the PyWin32 DLL specific to the PyWin32 module
    with the passed name.

    On import, each PyWin32 module:

    * Imports a DLL specific to that module.
    * Overwrites the values of all module attributes with values specific to
      that DLL. This includes that module's `__file__` attribute, which then
      provides the absolute path of that DLL.

    This function safely imports that module in a PyWin32-aware subprocess and
    returns the value of that module's `__file__` attribute.

    Parameters
    ----------
    module_name : str
        Fully-qualified name of that module.

    Returns
    ----------
    str
        Absolute path of that DLL.

    See Also
    ----------
    `PyInstaller.utils.win32.winutils.import_pywin32_module()`
        For further details.
    """
    statement = """
        from PyInstaller.utils.win32 import winutils
        module = winutils.import_pywin32_module('%s')
        print(module.__file__)
    """
    return exec_statement(statement % module_name)

__all__ = ('get_pywin32_module_file_attribute', )
