# -*- mode: python ; coding: utf-8 -*-
"""
Runtime hook for QtWebEngine process path fix.
This is called by PyInstaller at runtime before the main script runs.
"""

import os
import sys

def _pyi_rthook():
    """
    Fix QtWebEngineProcess path for PyInstaller builds on macOS.
    
    The PyQt6 PyPI wheel has a non-standard framework structure where
    Helpers and Resources are at the top level of the framework, not
    inside Versions/A. PyInstaller's hook collects these to the correct
    versioned location, but QtWebEngine expects the standard structure.
    
    This hook finds the actual location and sets the environment variable.
    """
    if not getattr(sys, 'frozen', False):
        # Not a PyInstaller build - nothing to do
        return
    
    meipass = sys._MEIPASS
    
    # Set QtWebEngine Chromium flags BEFORE QtWebEngine initializes
    # Disable sandbox for PyInstaller builds (macOS sandboxing conflicts with extraction)
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--no-sandbox --disable-gpu --disable-dev-shm-usage'
    print(f"QtWebEngine: Set Chromium flags: {os.environ['QTWEBENGINE_CHROMIUM_FLAGS']}", file=sys.stderr)
    
    # Build the base Qt path (where PyQt6/Qt6 is located)
    qt_base = os.path.join(meipass, 'PyQt6', 'Qt6', 'lib')
    if not os.path.exists(qt_base):
        # Fallback for different Qt installation layouts
        qt_base = meipass
    
    framework_path = os.path.join(qt_base, 'QtWebEngineCore.framework')
    if not os.path.exists(framework_path):
        print(f"WARNING: QtWebEngineCore.framework not found at {framework_path}", file=sys.stderr)
        return
    
    # Try multiple strategies to find QtWebEngineProcess
    
    # Strategy 1: Standard framework structure (PyInstaller onedir preserves this)
    # QtWebEngineCore.framework/Helpers/QtWebEngineProcess.app/Contents/MacOS/QtWebEngineProcess
    path1 = os.path.join(
        framework_path, 'Helpers', 'QtWebEngineProcess.app',
        'Contents', 'MacOS', 'QtWebEngineProcess'
    )
    
    # Strategy 2: Versioned structure (what PyInstaller hook SHOULD collect to)
    # QtWebEngineCore.framework/Versions/A/Helpers/QtWebEngineProcess.app/Contents/MacOS/QtWebEngineProcess
    path2 = os.path.join(
        framework_path, 'Versions', 'A', 'Helpers', 'QtWebEngineProcess.app',
        'Contents', 'MacOS', 'QtWebEngineProcess'
    )
    
    # Strategy 3: PyInstaller PyQt6 wheel bug - Resources is misidentified as version!
    # QtWebEngineCore.framework/Versions/Resources/Helpers/QtWebEngineProcess.app/Contents/MacOS/QtWebEngineProcess
    path3 = os.path.join(
        framework_path, 'Versions', 'Resources', 'Helpers', 'QtWebEngineProcess.app',
        'Contents', 'MacOS', 'QtWebEngineProcess'
    )
    
    # Strategy 4: Search entire framework directory
    def find_qtwebengine_process(fw_path):
        """Recursively search for QtWebEngineProcess executable."""
        for root, dirs, files in os.walk(fw_path):
            if 'QtWebEngineProcess' in files:
                return os.path.join(root, 'QtWebEngineProcess')
        return None
    
    found_path = None
    
    # Check strategies in order of preference
    for candidate in [path1, path2]:
        if os.path.exists(candidate):
            found_path = candidate
            break
    
    # Fallback to search
    if not found_path:
        # Check PyInstaller bug path first (Versions/Resources/...)
        bug_path = os.path.join(framework_path, 'Versions', 'Resources')
        if os.path.exists(bug_path):
            found_path = find_qtwebengine_process(bug_path)
        # Then search entire framework
        if not found_path:
            found_path = find_qtwebengine_process(framework_path)
    
    if found_path:
        os.environ['QTWEBENGINEPROCESS_PATH'] = found_path
        print(f"QtWebEngine: Found QtWebEngineProcess at {found_path}", file=sys.stderr)
    else:
        print(f"WARNING: QtWebEngineProcess not found in {framework_path}", file=sys.stderr)
        print(f"Searched paths:", file=sys.stderr)
        print(f"  {path1}", file=sys.stderr)
        print(f"  {path2}", file=sys.stderr)
    
    # Additional: Set QtWebEngine resources path
    # QtWebEngine looks for Resources at top-level, but PyInstaller may have collected to wrong location
    # Check multiple possible locations:
    resources_paths = [
        os.path.join(framework_path, 'Versions', 'Resources', 'Resources'),  # PyInstaller bug path
        os.path.join(framework_path, 'Versions', 'A', 'Resources'),           # Standard versioned path  
        os.path.join(framework_path, 'Resources'),                           # Top-level path
    ]
    
    resources_path = None
    for candidate in resources_paths:
        if os.path.exists(candidate):
            resources_path = candidate
            break
    
    if resources_path:
        os.environ['QTWEBENGINE_RESOURCES_PATH'] = resources_path
        print(f"QtWebEngine: Set resources path to {resources_path}", file=sys.stderr)
    else:
        print(f"WARNING: QtWebEngine resources not found in any expected location", file=sys.stderr)
    
    # Set QtWebEngine locales path
    # Look for qtwebengine_locales directory in multiple locations
    locales_paths = [
        os.path.join(framework_path, 'Versions', 'Resources', 'Resources', 'qtwebengine_locales'),  # PyInstaller bug path
        os.path.join(framework_path, 'Versions', 'A', 'Resources', 'qtwebengine_locales'),          # Standard versioned path
        os.path.join(framework_path, 'Resources', 'qtwebengine_locales'),                          # Top-level path
    ]
    
    locales_path = None
    for candidate in locales_paths:
        if os.path.exists(candidate):
            locales_path = candidate
            break
    
    if locales_path:
        os.environ['QTWEBENGINE_LOCALES_PATH'] = locales_path
        print(f"QtWebEngine: Set locales path to {locales_path}", file=sys.stderr)
    else:
        print(f"WARNING: QtWebEngine locales not found in any expected location", file=sys.stderr)
    
    # Additional: Try to create symlinks to satisfy QtWebEngine's expectations
    # This helps with framework structure validation
    
    # Helpers symlink - check both standard and PyInstaller bug paths
    helpers_versioned = os.path.join(framework_path, 'Versions', 'A', 'Helpers')
    helpers_pyinstaller_bug = os.path.join(framework_path, 'Versions', 'Resources', 'Helpers')
    helpers_top = os.path.join(framework_path, 'Helpers')
    
    # Use the one that actually exists
    helpers_actual = helpers_versioned if os.path.exists(helpers_versioned) else helpers_pyinstaller_bug
    
    if os.path.exists(helpers_actual) and not os.path.exists(helpers_top):
        try:
            # Calculate relative symlink path
            rel_path = os.path.relpath(helpers_actual, framework_path)
            os.symlink(rel_path, helpers_top)
            print(f"QtWebEngine: Created symlink {helpers_top} -> {rel_path}", file=sys.stderr)
        except Exception as e:
            print(f"QtWebEngine: Could not create Helpers symlink: {e}", file=sys.stderr)
    
    # Resources symlink - also check PyInstaller bug path
    resources_versioned = os.path.join(framework_path, 'Versions', 'A', 'Resources')
    resources_pyinstaller_bug = os.path.join(framework_path, 'Versions', 'Resources', 'Resources')
    resources_top = os.path.join(framework_path, 'Resources')
    
    # Use the one that actually exists
    resources_actual = resources_versioned if os.path.exists(resources_versioned) else resources_pyinstaller_bug
    
    if os.path.exists(resources_actual) and not os.path.exists(resources_top):
        try:
            rel_path = os.path.relpath(resources_actual, framework_path)
            os.symlink(rel_path, resources_top)
            print(f"QtWebEngine: Created symlink {resources_top} -> {rel_path}", file=sys.stderr)
        except Exception as e:
            print(f"QtWebEngine: Could not create Resources symlink: {e}", file=sys.stderr)
    
    # Fix rpath in QtWebEngineProcess so it can find QtWebEngineCore library
    # This is critical for one-file builds where QtWebEngineProcess runs from temp directory
    _fix_qtwebengine_rpath(framework_path, helpers_actual if os.path.exists(helpers_actual) else helpers_versioned)


def _fix_qtwebengine_rpath(framework_path, helpers_path):
    """Fix rpath in QtWebEngineProcess executable using install_name_tool."""
    if not helpers_path or not os.path.exists(helpers_path):
        return
    
    # Find QtWebEngineProcess executable
    qwe_process = os.path.join(helpers_path, 'QtWebEngineProcess.app', 'Contents', 'MacOS', 'QtWebEngineProcess')
    if not os.path.exists(qwe_process):
        return
    
    # Find QtWebEngineCore library
    qwe_core_versions_a = os.path.join(framework_path, 'Versions', 'A', 'QtWebEngineCore')
    qwe_core_versions_resources = os.path.join(framework_path, 'Versions', 'Resources', 'QtWebEngineCore')
    
    if os.path.exists(qwe_core_versions_a):
        qwe_core = qwe_core_versions_a
    elif os.path.exists(qwe_core_versions_resources):
        qwe_core = qwe_core_versions_resources
    else:
        print(f"QtWebEngine: QtWebEngineCore library not found, skipping rpath fix", file=sys.stderr)
        return
    
    # Get the lib directory for rpath
    # framework_path = .../PyQt6/Qt6/lib/QtWebEngineCore.framework
    # We want lib_dir = .../PyQt6/Qt6/lib
    lib_dir = os.path.dirname(framework_path)
    
    if not os.path.exists(lib_dir):
        print(f"QtWebEngine: lib directory not found: {lib_dir}", file=sys.stderr)
        return
    
    print(f"QtWebEngine: Fixing rpath in QtWebEngineProcess", file=sys.stderr)
    print(f"  Executable: {qwe_process}", file=sys.stderr)
    print(f"  QtWebEngineCore: {qwe_core}", file=sys.stderr)
    print(f"  Setting rpath: {lib_dir}", file=sys.stderr)
    
    try:
        import subprocess
        # Remove codesignature to allow modification
        subprocess.run(['codesign', '--remove-signature', qwe_process],
                      capture_output=True, timeout=5)
        # Add the new rpath
        result = subprocess.run(['install_name_tool', '-add_rpath', lib_dir, qwe_process],
                               capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"  [✓] rpath added", file=sys.stderr)
        else:
            print(f"  [!] install_name_tool: {result.stderr}", file=sys.stderr)
        # Re-sign with ad-hoc signature
        subprocess.run(['codesign', '--force', '--sign', '-', qwe_process],
                      capture_output=True, timeout=5)
    except Exception as e:
        print(f"  [!] Error fixing rpath: {e}", file=sys.stderr)
    
    # Also set DYLD_LIBRARY_PATH as a fallback
    current_dyld = os.environ.get('DYLD_LIBRARY_PATH', '')
    if lib_dir not in current_dyld:
        if current_dyld:
            os.environ['DYLD_LIBRARY_PATH'] = f"{lib_dir}:{current_dyld}"
        else:
            os.environ['DYLD_LIBRARY_PATH'] = lib_dir
        print(f"  [✓] Set DYLD_LIBRARY_PATH: {lib_dir}", file=sys.stderr)

_pyi_rthook()
del _pyi_rthook
