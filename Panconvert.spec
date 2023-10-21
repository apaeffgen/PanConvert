# -*- mode: python ; coding: utf-8 -*-
# Pyinstaller - Spcification file

block_cipher = None


a = Analysis(['Panconvert.py'],
             pathex=['/Users/apaeffgen/Programmierung/PyCharm/PanConvert'],
             binaries=[],
             datas=[('source/language/Panconvert_de.qm', '.'),('source/language/Panconvert_es.qm', '.'),('source/language/Panconvert_fr.qm', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Panconvert',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Panconvert')
app = BUNDLE(coll,
             name='Panconvert.app',
             icon=None,
             bundle_identifier=None)
