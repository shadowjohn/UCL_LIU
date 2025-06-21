#-----------------------------------------------------------------------------
# Copyright (c) 2005-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


from PyInstaller.compat import modname_tkinter
from PyInstaller.utils.hooks import collect_submodules

# Module django.core.management.commands.shell imports IPython but it
# introduces many other dependencies that are not necessary for simple
# django project. Ignore then IPython module.
excludedimports = ['IPython', 'matplotlib', modname_tkinter]

# Django requres management modules for the script 'manage.py'.
hiddenimports = collect_submodules('django.core.management.commands')
