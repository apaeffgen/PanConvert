# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# Resolve paths relative to the spec file location
spec_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
project_root = os.path.normpath(os.path.join(spec_dir, '..', '..'))

# Get version from environment variable (set by build_linux.sh)
version = os.environ.get('PANVERSION', '0.0.0')
binary_name = f'Panconvert-{version}-linux_x86-64'

a = Analysis(
    [os.path.join(project_root, 'Panconvert.py')],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join(project_root, 'source/language/Panconvert_de.qm'), 'language'),
        (os.path.join(project_root, 'source/language/Panconvert_es.qm'), 'language'),
        (os.path.join(project_root, 'source/language/Panconvert_fr.qm'), 'language'),
        (os.path.join(project_root, 'source/gui/icons'), 'source/gui/icons'),
    ],
    hiddenimports=['source.gui.icons'],
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
    a.zipfiles,
    a.datas,
    [],
    name=binary_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
