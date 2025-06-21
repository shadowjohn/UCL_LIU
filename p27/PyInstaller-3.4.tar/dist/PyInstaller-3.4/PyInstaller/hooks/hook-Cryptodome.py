#-----------------------------------------------------------------------------
# Copyright (c) 2005-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

"""
Hook for Cryptodome module: https://pypi.python.org/pypi/pycryptodomex

Tested with Cryptodomex 3.4.2, Python 2.7 & 3.5, Windows
"""

import os
import glob

from PyInstaller.compat import EXTENSION_SUFFIXES
from PyInstaller.utils.hooks import get_module_file_attribute

# Include the modules as binaries in a subfolder named like the package.
# Cryptodome's loader expects to find them inside the package directory for
# the main module. We cannot use hiddenimports because that would add the
# modules outside the package.

binaries = []
binary_module_names = [
    'Cryptodome.Cipher',
    'Cryptodome.Util',
    'Cryptodome.Hash',
    'Cryptodome.Protocol',
    'Cryptodome.Math',
]

for module_name in binary_module_names:
    m_dir = os.path.dirname(get_module_file_attribute(module_name))
    for ext in EXTENSION_SUFFIXES:
        module_bin = glob.glob(os.path.join(m_dir, '_*%s' % ext))
        for f in module_bin:
            binaries.append((f, module_name.replace('.', '/')))
