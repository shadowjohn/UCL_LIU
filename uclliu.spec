# -*- mode: python -*-

block_cipher = None


a = Analysis(['uclliu.pyw'],
             pathex=['F:\\GD\\UCL_LIU'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['_ssl', '_bz2', '_lzma', 'pyconfig'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='uclliu',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , version='metadata.txt', icon='pic\\uclliu_logo.ico')
