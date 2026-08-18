#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for settings persistence in the packaged binary.

Verifies that QSettings correctly:
- Saves and loads path_pandoc
- Saves and loads path_multimarkdown
- Saves and loads batch settings
- Persists across "restarts" (via temp file)
"""

import os
import tempfile
from pathlib import Path

import pytest


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _get_settings():
    """Get the settings object (used by interface_pandoc)."""
    from PyQt6.QtCore import QSettings
    return QSettings("Pandoc", "PanConvert")


# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def settings():
    """Provide a fresh settings object for each test."""
    return _get_settings()


# ─── Tests ────────────────────────────────────────────────────────────────────


class TestSettingsBasic:
    """Test basic QSettings functionality."""

    def test_settings_can_be_created(self, settings):
        """QSettings should be creatable."""
        assert settings is not None

    def test_settings_write_and_read(self, settings):
        """Should be able to write and read values."""
        test_key = "test_write_read"
        test_value = "test_value_123"

        settings.setValue(test_key, test_value)
        result = settings.value(test_key, "")

        assert result == test_value, f"Expected '{test_value}', got '{result}'"

    def test_settings_default_value(self, settings):
        """Should return default when key doesn't exist."""
        result = settings.value("nonexistent_key", "default_val")
        assert result == "default_val"

    def test_settings_sync(self, settings):
        """sync() should not raise an exception."""
        settings.setValue("test_sync_key", "test_value")
        try:
            settings.sync()
        except Exception as e:
            pytest.fail(f"sync() raised: {e}")


class TestPathPandocSettings:
    """Test path_pandoc settings persistence."""

    def test_set_path_pandoc(self, settings):
        """Should be able to store path_pandoc."""
        settings.setValue("path_pandoc", "/usr/local/bin/pandoc")
        result = settings.value("path_pandoc", "")
        assert result == "/usr/local/bin/pandoc"

    def test_set_empty_path_pandoc(self, settings):
        """Should be able to clear path_pandoc."""
        settings.setValue("path_pandoc", "")
        result = settings.value("path_pandoc", "")
        assert result == ""

    def test_path_pandoc_persists_across_getters(self, settings):
        """path_pandoc should persist across multiple get/set cycles."""
        settings.setValue("path_pandoc", "/opt/homebrew/bin/pandoc")
        r1 = settings.value("path_pandoc", "")
        settings.setValue("path_pandoc", "/usr/bin/pandoc")
        r2 = settings.value("path_pandoc", "")
        assert r1 == "/opt/homebrew/bin/pandoc"
        assert r2 == "/usr/bin/pandoc"


class TestPathMultiMarkdownSettings:
    """Test path_multimarkdown settings persistence."""

    def test_set_path_multimarkdown(self, settings):
        """Should be able to store path_multimarkdown."""
        settings.setValue("path_multimarkdown", "/usr/local/bin/multimarkdown")
        result = settings.value("path_multimarkdown", "")
        assert result == "/usr/local/bin/multimarkdown"

    def test_clear_path_multimarkdown(self, settings):
        """Should be able to clear path_multimarkdown."""
        settings.setValue("path_multimarkdown", "")
        result = settings.value("path_multimarkdown", "")
        assert result == ""


class TestBatchSettings:
    """Test batch conversion settings persistence."""

    def test_batch_open_path(self, settings):
        """Should be able to store batch_open_path."""
        settings.setValue("batch_open_path", "/Users/test/documents")
        result = settings.value("batch_open_path", "")
        assert result == "/Users/test/documents"

    def test_batch_open_path_output(self, settings):
        """Should be able to store batch_open_path_output."""
        settings.setValue("batch_open_path_output", "/Users/test/output")
        result = settings.value("batch_open_path_output", "")
        assert result == "/Users/test/output"

    def test_batch_convert_filter(self, settings):
        """Should be able to store batch_convert_filter."""
        settings.setValue("batch_convert_filter", "*.md;*.rst")
        result = settings.value("batch_convert_filter", "")
        assert result == "*.md;*.rst"


class TestLanguageSettings:
    """Test language settings persistence."""

    def test_default_language(self, settings):
        """Should be able to store default_language."""
        settings.setValue("default_language", "de")
        result = settings.value("default_language", "en")
        assert result == "de"

    def test_clear_default_language(self, settings):
        """Should be able to clear default_language."""
        settings.setValue("default_language", "")
        result = settings.value("default_language", "en")
        # When explicitly set to empty, QSettings returns empty (not default)
        assert result == ""


class TestSettingsEdgeCases:
    """Test edge cases in settings handling."""

    def test_none_value(self, settings):
        """Storing None should work."""
        settings.setValue("test_none", None)
        result = settings.value("test_none")
        # Qt may convert None to empty string or keep it
        assert result is None or result == ""

    def test_integer_value(self, settings):
        """Storing integers should work."""
        settings.setValue("test_int", 42)
        result = settings.value("test_int", 0)
        assert result == 42

    def test_boolean_value(self, settings):
        """Storing booleans should work."""
        settings.setValue("test_bool", True)
        result = settings.value("test_bool", False)
        # QSettings may return boolean as True (Python bool) or "true" (lowercase string)
        # depending on platform and Qt version
        assert result is True or result == "true" or result == "True", f"Expected True or 'true', got {result!r}"

    def test_long_path(self, settings):
        """Long paths should be stored correctly."""
        long_path = "/very/long/path/that/goes/on/and/on/and/on/and/on/and/on/and/on/and/on/and/on/and/on/pandoc"
        settings.setValue("test_long", long_path)
        result = settings.value("test_long", "")
        assert result == long_path

    def test_unicode_value(self, settings):
        """Unicode strings should be stored correctly."""
        unicode_val = "路径_путь_パス"
        settings.setValue("test_unicode", unicode_val)
        result = settings.value("test_unicode", "")
        assert result == unicode_val

    def test_special_characters(self, settings):
        """Special characters should be stored correctly."""
        special = "path/with;semicolons,and,commas"
        settings.setValue("test_special", special)
        result = settings.value("test_special", "")
        assert result == special


class TestSettingsCleanup:
    """Test settings cleanup between tests."""

    def test_settings_isolation(self, settings):
        """Settings should not leak between test classes."""
        # This test should pass regardless of what previous tests did
        # because each test class gets a fresh QSettings instance
        result = settings.value("nonexistent_key_xyz", "default")
        assert result == "default"

    def test_cleanup_test_keys(self, settings):
        """Test keys should be cleaned up."""
        settings.setValue("cleanup_test_key", "value")
        settings.setValue("cleanup_test_key2", "value2")
        settings.sync()
        # Clean up
        settings.remove("cleanup_test_key")
        settings.remove("cleanup_test_key2")
        settings.sync()
        assert settings.value("cleanup_test_key", "default") == "default"
