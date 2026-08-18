#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI tests for Panconvert.

These tests run the PyQt6 GUI in headless mode (QT_QPA_PLATFORM=offscreen).
They verify:
- Main window can be created without crashing
- Basic UI elements exist
- Preferences dialog can be opened
"""

import os
import sys
import platform
import pytest
from pathlib import Path

# Ensure source is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def headless_display(monkeypatch):
    """Force headless Qt platform for all GUI tests."""
    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
    monkeypatch.setenv("QTWEBENGINE_DISABLE_SANDBOX", "1")
    monkeypatch.setenv("QT_DEBUG_PLUGINS", "0")


@pytest.fixture
def qapp(monkeypatch):
    """Create a QApplication instance for testing."""
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt

    # Check if QApplication already exists
    if QApplication.instance() is None:
        app = QApplication(sys.argv)
        app.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
        yield app
        app.quit()
    else:
        yield QApplication.instance()


# ─── Tests ────────────────────────────────────────────────────────────────────


class TestMainWindow:
    """Test main window creation."""

    def test_main_gui_module_imports(self):
        """main_gui module should be importable."""
        from source import main_gui
        assert hasattr(main_gui, "StartQT5")

    def test_main_window_can_be_created(self, qapp):
        """Main window should be creatable without crashing."""
        from source.main_gui import StartQT5

        try:
            window = StartQT5()
            assert window is not None
            # Verify it's a QWidget
            from PyQt6.QtWidgets import QWidget
            assert isinstance(window, QWidget)
        except Exception as e:
            pytest.fail(f"Failed to create main window: {e}")

    def test_main_window_has_title(self, qapp):
        """Main window should have a title."""
        from source.main_gui import StartQT5

        window = StartQT5()
        title = window.windowTitle()
        assert "Pan" in title and "Convert" in title or "Pandoc" in title, (
            f"Window title should mention PanConvert/Pandoc, got: '{title}'"
        )

    def test_main_window_is_visible(self, qapp):
        """Main window should be shown (in headless mode)."""
        from source.main_gui import StartQT5

        window = StartQT5()
        window.show()
        assert window.isVisible()


class TestDialogs:
    """Test dialog creation."""

    def test_preferences_dialog_imports(self):
        """Preferences dialog module should be importable."""
        from source.dialogs import dialog_preferences
        assert hasattr(dialog_preferences, "PreferenceDialog")

    def test_preferences_dialog_can_be_created(self, qapp):
        """Preferences dialog should be creatable."""
        from source.dialogs.dialog_preferences import PreferenceDialog

        try:
            dialog = PreferenceDialog()
            assert dialog is not None
        except Exception as e:
            pytest.fail(f"Failed to create preferences dialog: {e}")

    def test_help_dialog_can_be_created(self, qapp):
        """Help dialog should be creatable."""
        from source.dialogs.dialog_help import HelpDialog

        try:
            dialog = HelpDialog()
            assert dialog is not None
        except Exception as e:
            pytest.fail(f"Failed to create help dialog: {e}")

    def test_about_dialog_can_be_created(self, qapp):
        """About dialog should be creatable (if it exists)."""
        try:
            from source.dialogs.dialog_info import DialogInfo
            dialog = DialogInfo()
            assert dialog is not None
        except (ImportError, ModuleNotFoundError):
            pytest.skip("dialog_info module not found")


class TestLanguage:
    """Test language loading."""

    def test_language_module_imports(self):
        """Language module should be importable."""
        from source.language import load_language, get_available_languages
        assert callable(load_language)
        assert callable(get_available_languages)

    def test_get_available_languages_returns_dict(self):
        """get_available_languages should return a dict of lang_code -> name."""
        from source.language import get_available_languages
        langs = get_available_languages()
        assert isinstance(langs, dict), f"Expected dict, got {type(langs)}"
        assert len(langs) > 0, "Should have at least one language"

    def test_default_language_is_available(self):
        """Default language 'en' should be available."""
        from source.language import get_available_languages
        langs = get_available_languages()
        assert "en" in langs, f"'en' should be in available languages: {langs}"


class TestMessages:
    """Test message functions."""

    def test_messages_module_imports(self):
        """Messages module should be importable."""
        from source.language import messages
        assert hasattr(messages, "error_converter_path")
        assert hasattr(messages, "error_file_selection")
        assert hasattr(messages, "message_file_converted")

    def test_error_converter_path_returns_string(self):
        """error_converter_path should return a string."""
        from source.language.messages import error_converter_path
        result = error_converter_path()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_version_function(self):
        """version() should return a version string."""
        from source.language.messages import version
        result = version()
        assert isinstance(result, str)
        assert "0.3" in result or "PanConvert" in result

    def test_version_number(self):
        """versionnumber should be a valid version string."""
        from source.language.messages import versionnumber
        assert isinstance(versionnumber, str)
        import re
        assert re.match(r"\d+\.\d+\.\d+", versionnumber), (
            f"versionnumber should match X.Y.Z: {versionnumber}"
        )


class TestHeadlessMode:
    """Test that headless mode works correctly."""

    def test_qt_platform_is_offscreen(self):
        """QT_QPA_PLATFORM should be set to offscreen."""
        assert os.environ.get("QT_QPA_PLATFORM") == "offscreen"

    def test_qt_webengine_sandbox_disabled(self):
        """QTWEBENGINE_DISABLE_SANDBOX should be set."""
        assert os.environ.get("QTWEBENGINE_DISABLE_SANDBOX") == "1"
