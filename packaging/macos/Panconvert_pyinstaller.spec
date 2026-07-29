# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Panconvert.

Build command:
    pyinstaller --clean packaging/macos/Panconvert_pyinstaller.spec

This bundles Panconvert with PyQt6, all source files, and icon assets
into a standalone executable.
"""

import os
import sys
from PyInstaller.utils.hooks import collect_submodules

# Resolve paths relative to the project root (parent of packaging/)
try:
    spec_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # PyInstaller may not set __file__
    spec_dir = os.path.dirname(os.path.abspath(sys.argv[-1]))
# spec_dir is packaging/macos/; go up two levels to reach project root
project_root = os.path.abspath(os.path.join(spec_dir, '../..'))
sys.path.insert(0, project_root)

# ── Collect PyQt6 resource files (translations, platform plugins) ──
hiddenimports = []
for pkg in ['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets']:
    hiddenimports += collect_submodules(pkg)

# Collect Qt platform plugin (qxcb on Linux, qminimal on headless,
# and the default platform plugin for macOS/Windows)
hiddenimports += collect_submodules('PyQt6.QtCore')

# ── Collect all data files from the source package ──
datas = []
for root, dirs, files in os.walk(os.path.join(project_root, 'source')):
    for f in files:
        src = os.path.join(root, f)
        dst = os.path.relpath(root, project_root)
        datas.append((src, dst))

# ── App name and output directory ──
a = Analysis(
    [os.path.join(project_root, 'Panconvert.py')],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,  # -O1: basic bytecode optimization
)

pyz = PYZ(a.pure)

# ── One-folder mode for all platforms ──
# One-folder mode provides better startup performance than --onefile
# because it avoids extracting to a temp directory on launch.

# macOS: bundle as .app (which is a directory bundle)
if sys.platform == 'darwin':
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
    coll = BUNDLE(
        exe,
        name='Panconvert.app',
        debug=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        icon=os.path.join(project_root, 'source/gui/icons/icon.icns'),
        version=None,
        bundle_identifier='com.panconvert.app',
    )
# Windows: one-folder output
elif sys.platform == 'win32':
    EXE(
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
# Linux: one-folder output
else:
    EXE(
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
