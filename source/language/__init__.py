#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Panconvert language support.

Provides _translate() wrapper and load_language() to install Qt translations
at runtime. Works in both source (dev) and bundled (PyInstaller) modes.
"""

from PyQt6 import QtCore
from PyQt6.QtCore import QTranslator, QCoreApplication, QLocale
from PyQt6.QtWidgets import QApplication
from importlib_resources import files
import sys
import os


# The _translate function used throughout the codebase
_translate = QCoreApplication.translate

# Track installed translator so we can unload/swap on language change
_installed_translator = None


def _get_qm_path(lang_code: str):
    """Return the path to the .qm file for the given language code.

    Works in both source mode and PyInstaller bundled mode.
    """
    filename = f'Panconvert_{lang_code}.qm'
    
    # PyInstaller bundled mode: files are in sys._MEIPASS
    if getattr(sys, '_MEIPASS', None):
        meipass = sys._MEIPASS
        # Check common locations where PyInstaller may place bundled data
        for subdir in ['language', 'MacOS', '']:
            if subdir:
                qm_path = os.path.join(meipass, subdir, filename)
            else:
                qm_path = os.path.join(meipass, filename)
            if os.path.isfile(qm_path):
                return qm_path

    # Try importlib_resources (works in dev mode)
    try:
        res = files('source.language').joinpath(filename)
        return str(res)
    except Exception:
        pass

    # Fallback: look in the same directory as this module (dev mode)
    mod_dir = os.path.dirname(os.path.abspath(__file__))
    qm_path = os.path.join(mod_dir, filename)
    if os.path.isfile(qm_path):
        return qm_path
    return None


def load_language(_app=None, lang_code: str = 'en'):
    """Load and install a Qt translation for the given language code.

    Uses QApplication.instance() internally since installTranslator/removeTranslator
    are QApplication methods, not QMainWindow methods.

    Parameters
    ----------
    _app : ignored, kept for backward compatibility
    lang_code : str
        Language code: 'en', 'de', 'es', 'fr'. 'en' loads nothing
        (English is the default).
    """
    global _installed_translator

    # Use QApplication instance for translator operations
    # (installTranslator/removeTranslator are on QApplication, not QMainWindow)
    qapp = QApplication.instance()
    if qapp is None:
        print('[lang] No QApplication instance available')
        return

    # Unload previous translator
    if _installed_translator is not None:
        qapp.removeTranslator(_installed_translator)
        _installed_translator = None

    # English is the default — no .qm file needed
    if lang_code == 'en':
        return

    qm_path = _get_qm_path(lang_code)
    if qm_path is None:
        print(f'[lang] No translation file found for {lang_code}')
        return

    translator = QTranslator(qapp)
    if translator.load(qm_path):
        qapp.installTranslator(translator)
        _installed_translator = translator
        print(f'[lang] Loaded translation: {lang_code}')
    else:
        print(f'[lang] Failed to load translation: {qm_path}')


def get_available_languages():
    """Return a dict of {code: display_name} for available translations."""
    from source.dialogs.dialog_preferences import lang
    return lang


def get_system_language():
    """Detect the system locale and return the closest supported language code."""
    locale = QLocale.system()
    code = locale.name()  # e.g. 'de_DE', 'fr_FR', 'en_US'
    lang_code = code.split('_')[0]  # 'de', 'fr', 'en'

    supported = get_available_languages()
    if lang_code in supported:
        return lang_code
    return 'en'
