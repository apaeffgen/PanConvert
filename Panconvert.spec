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
    a.binaries,
    a.datas,
    [],
    name='Panconvert',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='Panconvert.app',
    icon=None,
    bundle_identifier=None,
)
