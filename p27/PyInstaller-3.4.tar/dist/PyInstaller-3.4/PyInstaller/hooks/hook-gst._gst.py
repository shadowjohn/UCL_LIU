#-----------------------------------------------------------------------------
# Copyright (c) 2013-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


# GStreamer contains a lot of plugins. We need to collect them and bundle
# them wih the exe file.
# We also need to resolve binary dependencies of these GStreamer plugins.


import glob
import os
from PyInstaller.compat import is_win
from PyInstaller.utils.hooks import exec_statement


hiddenimports = ['gmodule', 'gobject']

statement = """
import os
import gst
reg = gst.registry_get_default()
plug = reg.find_plugin('coreelements')
path = plug.get_filename()
print(os.path.dirname(path))
"""

plugin_path = exec_statement(statement)

if is_win:
    # TODO Verify that on Windows gst plugins really end with .dll.
    pattern = os.path.join(plugin_path, '*.dll')
else:
    # Even on OSX plugins end with '.so'.
    pattern = os.path.join(plugin_path, '*.so')

binaries = [
    (os.path.join('gst_plugins', os.path.basename(f)), f)
    # 'f' contains the absolute path
    for f in glob.glob(pattern)]
