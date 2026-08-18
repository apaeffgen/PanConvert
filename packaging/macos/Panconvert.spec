# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Panconvert on macOS
Includes QtWebEngine support with proper framework handling
"""
import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.utils.hooks import collect_dynamic_libs

# Resolve paths relative to this spec file
_spec_path = os.path.abspath(__file__) if '__file__' in dir() else os.path.abspath(sys.argv[0])
_root = os.path.dirname(os.path.dirname(os.path.dirname(_spec_path)))
_main_script = os.path.join(_root, 'Panconvert.py')

# Collect all source data files (UI files, icons, translations)
datas = [
    (os.path.join(_root, 'source'), 'source'),
]

# Note: Qt/QtWebEngine files are collected automatically by PyInstaller's
# PyQt6 hooks (hook-PyQt6.py, hook-PyQt6.QtWebEngineCore.py). Do NOT manually
# add Qt datas here - it breaks the expected framework structure for QtWebEngine.

# Collect hidden imports for QtWebEngine
hiddenimports = collect_submodules('source.gui.icons')
hiddenimports.extend([
    # PyQt6 core modules
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    # QtWebEngine modules (critical for web view functionality)
    'PyQt6.QtWebEngineCore',
    'PyQt6.QtWebEngineWidgets',
    'PyQt6.QtWebChannel',
    # Common Qt submodules
    'PyQt6.sip',
    'sip',
])

a = Analysis(
    [_main_script],
    pathex=[_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[os.path.join(_root, 'packaging', 'macos')],  # Include custom hooks
    hooksconfig={},
    runtime_hooks=[
        os.path.join(os.path.dirname(_spec_path), 'pyinstaller_qtwebengine_fix.py'),
    ],
    excludes=[],
    noarchive=True,   # onedir mode - preserves directory structure for Qt frameworks
                      # One-file mode breaks QtWebEngine framework symlinks when extracting to temp dir
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Panconvert',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  # Keep symbols for debugging
    upx=False,    # Disable UPX - can break Qt framework loading
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,  # Handle Apple Events for file opening
    target_arch=None,     # Universal binary
    codesign_identity='-',  # Don't sign during build (sign after)
    entitlements_file=None,
    target_application=None,
)

app = BUNDLE(
    exe,
    name='Panconvert.app',
    icon=None,  # Add icon path if available
    bundle_identifier='com.panconvert.app',
    info_plist={
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '11.0',  # macOS Big Sur+
    },
)
