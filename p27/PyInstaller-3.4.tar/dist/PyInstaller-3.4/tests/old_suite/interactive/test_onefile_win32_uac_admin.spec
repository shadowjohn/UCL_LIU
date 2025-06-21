# -*- mode: python -*-
#-----------------------------------------------------------------------------
# Copyright (c) 2014-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


__testname__ = 'test_onefile_win32_uac_admin'

a = Analysis([__testname__ + '.py'],
             pathex=[])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          a.zipfiles,
          name=__testname__ + '.exe',
          debug=False,
          strip=False,
          upx=False,
          console=True,
          uac_admin=True)
