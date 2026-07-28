"""
PyInstaller runtime hook for PyQt6 Qt platform plugin path.

When running as a single-file executable, PyInstaller extracts files to
a temp directory (_MEIPASS). This hook tells Qt where to find its
platform plugins (qwindows.dll on Windows).
"""

import os
import sys

# Check if running as a PyInstaller bundle
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # _MEIPASS is the temp extraction directory
    meipass = sys._MEIPASS
    
    # Find the PyQt6 Qt plugins directory
    # The plugins are bundled under PyInstaller's _MEIPASS
    plugin_path = os.path.join(meipass, 'PyQt6', 'Qt6', 'plugins')
    
    # Also check common locations where PyInstaller might place them
    if not os.path.isdir(plugin_path):
        # Try alternate locations
        for candidate in [
            os.path.join(meipass, 'PyQt6', 'Qt', 'plugins'),
            os.path.join(meipass, 'plugins'),
        ]:
            if os.path.isdir(candidate):
                plugin_path = candidate
                break
    
    # Set the environment variable so Qt knows where to find platform plugins
    if os.path.isdir(plugin_path):
        os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
