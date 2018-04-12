from distutils.core import setup
import py2exe, sys, os
sys.argv.append('py2exe')
setup(
    data_files = [
      ('',['api-ms-win-core-errorhandling-l1-1-1.dll']),
      ('',['api-ms-win-core-libraryloader-l1-2-0.dll']),
      ('',['api-ms-win-core-processthreads-l1-1-2.dll']),
      ('',['api-ms-win-core-profile-l1-1-0.dll']),
      ('',['api-ms-win-core-sysinfo-l1-2-1.dll']),
      ('',['mfc90.dll']),
      ('',['msvcp90.dll'])      
    ],
    options = {
      'py2exe': {
        'bundle_files': 1,
    		'optimize':2,
    		'compressed':1
      }
    },
    windows = [{'script': "uclliu.py"}],
    zipfile = None,
)
