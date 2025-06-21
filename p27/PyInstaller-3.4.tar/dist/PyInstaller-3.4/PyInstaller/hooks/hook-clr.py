#-----------------------------------------------------------------------------
# Copyright (c) 2013-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


"""
pythonnet requires both clr.pyd and Python.Runtime.dll, 
but the latter isn't found by PyInstaller.
"""


import ctypes.util
from PyInstaller.compat import is_win, getsitepackages
from os.path import join, exists

# pythonnet is available for all platforms using .NET and Mono,
# but tested only on Windows using .NET.

if is_win:
    pyruntime = 'Python.Runtime'
    library = ctypes.util.find_library(pyruntime)
    datas = []
    if library:
        datas = [(library, '.')]
    else:
    	# find Python.Runtime.dll in pip-installed pythonnet package
    	for sitepack in getsitepackages():
    		library = join(sitepack, pyruntime + '.dll')
    		if exists(library):
    			datas = [(library, '.')]
    	if not datas:
    		raise Exception(pyruntime + ' not found')
