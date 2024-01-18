'''A pyHook module fork from Peter P. with some updates.

Python wrapper for out-of-context input hooks in Windows.
The pyWinhook package provides callbacks for global mouse and keyboard events in Windows. Python
applications register event handlers for user input events such as left mouse down, left mouse up,
key down, etc. and set the keyboard and/or mouse hook. The underlying C library reports information
like the time of the event, the name of the window in which the event occurred, the value of the
event, any keyboard modifiers, etc.
pyHook, original project download url: http://www.sourceforge.net/projects/pyhook
'''

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Topic :: System :: Monitoring
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Microsoft :: Windows
"""
__version__='1.6.2'
from setuptools import setup, Extension

libs = ['user32']
doclines = __doc__.split('\n')

setup(name='pyWinhook',
      version=__version__,
      author='Tungsteno',
      author_email='contacts00-pywinhook@yahoo.it',
      url='https://github.com/Tungsteno74/pyWinhook',
      download_url=''.join(('https://codeload.github.com/Tungsteno74/pyWinhook/zip/',__version__)),
      license='http://www.opensource.org/licenses/mit-license.php',
      platforms=['Win32', 'Win-amd64', 'Win-ia64'],
      description = doclines[0],
      classifiers = list(filter(None, classifiers.split('\n'))),
      long_description = ' '.join(doclines[2:]),
      packages = ['pyWinhook'],
      install_requires = ['pywin32'],
      ext_modules = [Extension('pyWinhook._cpyHook', ['pyWinhook/cpyHook.i'], libraries=libs)],
      data_files = [('Lib/site-packages/pyWinhook', ['pyWinhook/cpyHook.py', 'LICENSE.txt', 'README.txt', 'CHANGELOG.txt'])],
      keywords = 'hook win32 win64 keyboard input user control'
      )
