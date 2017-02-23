# -*- mode: python -*-

block_cipher = None

a = Analysis(['Panconvert.py'],
             pathex=['/Users/apaeffgen/Programmierung/PanConvert'],
             binaries=[],
             datas=[('source/language/Panconvert_de.qm', '.'),('source/language/Panconvert_es.qm', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Panconvert',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Panconvert')
app = BUNDLE(coll,
             name='Panconvert.app',
             icon=None,
             bundle_identifier=None)
