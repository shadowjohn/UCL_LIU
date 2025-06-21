#-----------------------------------------------------------------------------
# Copyright (c) 2013-2018, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


"""
django.core.mail uses part of the email package.
Problem is: when using runserver with autoreload mode, the thread that
checks fore changed files unwillingly trigger further imports within
the email package because of the LazyImporter in email (used in 2.5 for
backward compatibility).
We then need to name those modules as hidden imports, otherwise at
runtime the autoreload thread will complain with a traceback.
"""


hiddenimports = [
    'email.mime.message',
    'email.mime.image',
    'email.mime.text',
    'email.mime.multipart',
    'email.mime.audio'
]
