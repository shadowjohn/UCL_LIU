#-----------------------------------------------------------------------------
# Copyright (c) 2013-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


from PyInstaller.utils.hooks import qt_plugins_binaries

binaries = qt_plugins_binaries('sqldrivers', namespace='PyQt4')
hiddenimports = ['sip', 'PyQt4.QtCore', 'PyQt4.QtGui']
