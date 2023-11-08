# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/apaeffgen/PROG/Python/PanConvert/Panconvert.py'],
    pathex=[],
    binaries=[],
    datas=[('source/language/Panconvert_de.qm', 'MacOS')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Panconvert',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Panconvert',
)
app = BUNDLE(
    coll,
    name='Panconvert.app',
    icon=None,
    bundle_identifier=None,
)
