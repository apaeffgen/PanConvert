# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Panconvert.

Build command:
    pyinstaller Panconvert.spec

This bundles Panconvert with PyQt6, all source files, and icon assets
into a standalone executable.
"""

import os
import sys
from PyInstaller.utils.hooks import collect_submodules

# ── Collect PyQt6 resource files (translations, platform plugins) ──
hiddenimports = []
for pkg in ['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets']:
    hiddenimports += collect_submodules(pkg)

# Collect Qt platform plugin (qxcb on Linux, qminimal on headless,
# and the default platform plugin for macOS/Windows)
hiddenimports += collect_submodules('PyQt6.QtCore')

# ── Collect all data files from the source package ──
datas = []
for root, dirs, files in os.walk('source'):
    for f in files:
        src = os.path.join(root, f)
        dst = os.path.relpath(root, os.getcwd())
        datas.append((src, dst))

# ── App name and output directory ──
a = Analysis(
    ['Panconvert.py'],
    pathex=[],
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

# ── macOS: bundle as .app ──
# ── Windows/Linux: bundle as single directory ──
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
    console=False,  # set to True to see console output / debug
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS .app bundle
coll = BUNDLE(
    exe,
    name='Panconvert.app',
    debug=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    icon='source/gui/icons/icon.icns',
    version=None,
    bundle_identifier='com.panconvert.app',
)
