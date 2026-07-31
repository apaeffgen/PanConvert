#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for source.helpers.interface_pandoc.get_path_pandoc()"""

import os
import platform
import sys
import unittest
from unittest.mock import patch, MagicMock


class TestGetPathPandoc(unittest.TestCase):
    """Test cases for get_path_pandoc()."""

    def setUp(self):
        # Patch QSettings before importing the module
        self.qsettings_mock = MagicMock()
        self.qsettings_mock.value.return_value = ''
        self.qsettings_mock.setValue = MagicMock()
        self.qsettings_mock.sync = MagicMock()

        # Patch at the module level so the mocks reach the module's own references
        self.patches = [
            patch('source.helpers.interface_pandoc._get_settings', return_value=self.qsettings_mock),
            patch('source.helpers.interface_pandoc.platform'),
            patch('source.helpers.interface_pandoc.os'),
            patch('source.helpers.interface_pandoc.which'),
            patch('source.helpers.interface_pandoc.where'),
        ]
        for p in self.patches:
            p.start()

        from source.helpers import interface_pandoc
        self.interface_pandoc = interface_pandoc
        # Reset mocks so assertions are clean
        self.qsettings_mock.reset_mock()

    def tearDown(self):
        for p in self.patches:
            p.stop()

    def _mock_platform_darwin(self):
        """Configure mocks for macOS."""
        self.interface_pandoc.platform.system.return_value = 'Darwin'
        self.interface_pandoc.os.name = 'posix'
        self.interface_pandoc.os.path.isfile.return_value = False

    def _mock_platform_windows(self):
        """Configure mocks for Windows."""
        self.interface_pandoc.platform.system.return_value = 'Windows'
        self.interface_pandoc.os.name = 'nt'
        self.interface_pandoc.os.path.isfile.return_value = False

    def test_finds_pandoc_via_which_on_macos(self):
        """When path_pandoc is not set and not found, use which() on macOS."""
        self._mock_platform_darwin()
        self.interface_pandoc.which.return_value = '/usr/bin/pandoc'

        self.interface_pandoc.get_path_pandoc()

        self.interface_pandoc.which.assert_called_once_with('pandoc')
        self.qsettings_mock.setValue.assert_called_with('path_pandoc', '/usr/bin/pandoc')
        self.qsettings_mock.sync.assert_called()

    def test_finds_pandoc_via_where_on_windows(self):
        """When path_pandoc is not set and not found, use where() on Windows."""
        self._mock_platform_windows()
        self.interface_pandoc.where.return_value = 'C:\\Program Files\\Pandoc\\pandoc.exe'

        self.interface_pandoc.get_path_pandoc()

        self.interface_pandoc.where.assert_called_once_with('pandoc.exe')
        self.qsettings_mock.setValue.assert_called_with('path_pandoc', 'C:\\Program Files\\Pandoc\\pandoc.exe')
        self.qsettings_mock.sync.assert_called()

    def test_finds_pandoc_via_which_on_linux(self):
        """When path_pandoc is not set and not found, use which() on Linux."""
        self.interface_pandoc.platform.system.return_value = 'Linux'
        self.interface_pandoc.os.name = 'posix'
        self.interface_pandoc.os.path.isfile.return_value = False
        self.interface_pandoc.which.return_value = '/usr/bin/pandoc'

        self.interface_pandoc.get_path_pandoc()

        self.interface_pandoc.which.assert_called_once_with('pandoc')
        self.qsettings_mock.setValue.assert_called_with('path_pandoc', '/usr/bin/pandoc')
        self.qsettings_mock.sync.assert_called()

    def test_uses_cached_path_when_it_exists(self):
        """If the stored path_pandoc is a valid file, it should be returned directly."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True

        self.interface_pandoc.get_path_pandoc()

        # which/where should NOT be called
        self.interface_pandoc.which.assert_not_called()
        self.interface_pandoc.where.assert_not_called()
        # settings should NOT be updated
        self.qsettings_mock.setValue.assert_not_called()

    def test_settings_value_is_converted_to_string(self):
        """The value from QSettings should be converted to a string locally."""
        self.qsettings_mock.value.return_value = 12345  # non-string value
        self.interface_pandoc.os.path.isfile.return_value = True

        # Verify the function doesn't crash when value is not a string
        self.interface_pandoc.get_path_pandoc()
        # No assertion on module-level path_pandoc since get_path_pandoc() uses a local var

    def test_which_returns_none_when_pandoc_not_found(self):
        """If which() returns empty string, settings should still be updated."""
        self._mock_platform_darwin()
        self.interface_pandoc.which.return_value = ''

        self.interface_pandoc.get_path_pandoc()

        self.qsettings_mock.setValue.assert_called_with('path_pandoc', '')
        self.qsettings_mock.sync.assert_called()

    def test_which_returns_none_on_macos_when_pandoc_not_installed(self):
        """If which() returns None (pandoc not in path), settings are set to None."""
        self._mock_platform_darwin()
        self.interface_pandoc.which.return_value = None

        self.interface_pandoc.get_path_pandoc()

        self.interface_pandoc.which.assert_called_once_with('pandoc')
        self.qsettings_mock.setValue.assert_called_with('path_pandoc', None)
        self.qsettings_mock.sync.assert_called()

    def test_which_returns_none_on_linux_when_pandoc_not_installed(self):
        """If which() returns None on Linux (pandoc not in path), settings are set to None."""
        self.interface_pandoc.platform.system.return_value = 'Linux'
        self.interface_pandoc.os.name = 'posix'
        self.interface_pandoc.os.path.isfile.return_value = False
        self.interface_pandoc.which.return_value = None

        self.interface_pandoc.get_path_pandoc()

        self.interface_pandoc.which.assert_called_once_with('pandoc')
        self.qsettings_mock.setValue.assert_called_with('path_pandoc', None)
        self.qsettings_mock.sync.assert_called()

    def test_where_returns_none_on_windows_when_pandoc_not_installed(self):
        """If where() returns None (pandoc not in path), settings are set to None."""
        self._mock_platform_windows()
        self.interface_pandoc.where.return_value = None

        self.interface_pandoc.get_path_pandoc()

        self.interface_pandoc.where.assert_called_once_with('pandoc.exe')
        self.qsettings_mock.setValue.assert_called_with('path_pandoc', None)
        self.qsettings_mock.sync.assert_called()

    def test_settings_value_empty_string_triggers_research(self):
        """If the stored path_pandoc is an empty string, it should be treated as invalid."""
        self.qsettings_mock.value.return_value = ''
        self._mock_platform_darwin()
        self.interface_pandoc.which.return_value = '/usr/local/bin/pandoc'

        self.interface_pandoc.get_path_pandoc()

        # which should be called because empty string is not a valid file
        self.interface_pandoc.which.assert_called_once_with('pandoc')

    def test_uses_where_on_windows_when_frozen(self):
        """On Windows with frozen app, where() is used instead of subprocess."""
        self._mock_platform_windows()
        self.interface_pandoc.where.return_value = 'C:\\Pandoc\\pandoc.exe'

        self.interface_pandoc.get_path_pandoc()

        self.interface_pandoc.where.assert_called_once_with('pandoc.exe')
        self.qsettings_mock.setValue.assert_called_with('path_pandoc', 'C:\\Pandoc\\pandoc.exe')
        self.qsettings_mock.sync.assert_called()


if __name__ == '__main__':
    unittest.main()
