#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for source.helpers.interface_pandoc.get_path_multimarkdown()"""

import os
import platform
import sys
import unittest
from unittest.mock import patch, MagicMock, call


class TestGetPathMultimarkdown(unittest.TestCase):
    """Test cases for get_path_multimarkdown()."""

    def setUp(self):
        self.qsettings_mock = MagicMock()
        self.qsettings_mock.value.return_value = ''
        self.qsettings_mock.setValue = MagicMock()
        self.qsettings_mock.sync = MagicMock()

        self.patches = [
            patch('source.helpers.interface_pandoc._get_settings', return_value=self.qsettings_mock),
            patch('source.helpers.interface_pandoc.platform'),
            patch('source.helpers.interface_pandoc.os'),
            patch('source.helpers.interface_pandoc.which'),
            patch('source.helpers.interface_pandoc.sys'),
            patch('source.helpers.interface_pandoc.subprocess'),
        ]
        for p in self.patches:
            p.start()

        from source.helpers import interface_pandoc
        self.interface_pandoc = interface_pandoc
        self.qsettings_mock.reset_mock()

    def tearDown(self):
        for p in self.patches:
            p.stop()

    def _mock_platform_darwin(self):
        """Configure mocks for macOS."""
        self.interface_pandoc.platform.system.return_value = 'Darwin'
        self.interface_pandoc.os.name = 'posix'

    def _mock_platform_windows(self):
        """Configure mocks for Windows."""
        self.interface_pandoc.platform.system.return_value = 'Windows'
        self.interface_pandoc.os.name = 'nt'

    def _mock_linux(self):
        """Configure mocks for Linux."""
        self.interface_pandoc.platform.system.return_value = 'Linux'
        self.interface_pandoc.os.name = 'posix'

    # --- Frozen mode: which() helper (macOS/POSIX) ---

    def test_frozen_macos_uses_which_helper(self):
        """In frozen mode on macOS, which("multimarkdown") helper is used."""
        self._mock_platform_darwin()
        self.interface_pandoc.sys.frozen = True
        self.interface_pandoc.which.return_value = '/opt/homebrew/bin/multimarkdown'

        result = self.interface_pandoc.get_path_multimarkdown()

        self.interface_pandoc.which.assert_called_once_with('multimarkdown')
        self.qsettings_mock.setValue.assert_called_with('path_multimarkdown', '/opt/homebrew/bin/multimarkdown')
        self.qsettings_mock.sync.assert_called()
        self.assertEqual(result, '/opt/homebrew/bin/multimarkdown')

    def test_frozen_linux_uses_which_helper(self):
        """In frozen mode on Linux, which("multimarkdown") helper is used."""
        self._mock_linux()
        self.interface_pandoc.sys.frozen = True
        self.interface_pandoc.which.return_value = '/usr/bin/multimarkdown'

        result = self.interface_pandoc.get_path_multimarkdown()

        self.interface_pandoc.which.assert_called_once_with('multimarkdown')
        self.qsettings_mock.setValue.assert_called_with('path_multimarkdown', '/usr/bin/multimarkdown')
        self.qsettings_mock.sync.assert_called()
        self.assertEqual(result, '/usr/bin/multimarkdown')

    # --- Frozen mode: subprocess where (Windows) ---

    def test_frozen_windows_uses_subprocess_where(self):
        """In frozen mode on Windows, subprocess.Popen with 'where' is used."""
        self._mock_platform_windows()
        self.interface_pandoc.sys.frozen = True
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'C:\\Pandoc\\multimarkdown.exe\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_path_multimarkdown()

        self.interface_pandoc.subprocess.Popen.assert_called_once_with(
            ['where', 'multimarkdown'],
            stdin=self.interface_pandoc.subprocess.PIPE,
            stdout=self.interface_pandoc.subprocess.PIPE
        )
        mock_proc.communicate.assert_called_once()
        self.qsettings_mock.setValue.assert_called_with(
            'path_multimarkdown',
            'C:\\Pandoc\\multimarkdown.exe'
        )
        self.assertEqual(result, 'C:\\Pandoc\\multimarkdown.exe')

    # --- Non-frozen mode: subprocess which (macOS/POSIX) ---

    def test_non_frozen_macos_uses_subprocess_which(self):
        """In non-frozen mode on macOS, subprocess.Popen with 'which' is used."""
        self._mock_platform_darwin()
        self.interface_pandoc.sys.frozen = False
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'/usr/local/bin/multimarkdown\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_path_multimarkdown()

        self.interface_pandoc.subprocess.Popen.assert_called_once_with(
            ['which', 'multimarkdown'],
            stdin=self.interface_pandoc.subprocess.PIPE,
            stdout=self.interface_pandoc.subprocess.PIPE
        )
        mock_proc.communicate.assert_called_once()
        self.qsettings_mock.setValue.assert_called_with('path_multimarkdown', '/usr/local/bin/multimarkdown')
        self.assertEqual(result, '/usr/local/bin/multimarkdown')

    def test_non_frozen_linux_uses_subprocess_which(self):
        """In non-frozen mode on Linux, subprocess.Popen with 'which' is used."""
        self._mock_linux()
        self.interface_pandoc.sys.frozen = False
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'/usr/bin/multimarkdown\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_path_multimarkdown()

        self.interface_pandoc.subprocess.Popen.assert_called_once_with(
            ['which', 'multimarkdown'],
            stdin=self.interface_pandoc.subprocess.PIPE,
            stdout=self.interface_pandoc.subprocess.PIPE
        )
        mock_proc.communicate.assert_called_once()
        self.qsettings_mock.setValue.assert_called_with('path_multimarkdown', '/usr/bin/multimarkdown')
        self.assertEqual(result, '/usr/bin/multimarkdown')

    # --- Non-frozen mode: subprocess where (Windows) ---

    def test_non_frozen_windows_uses_subprocess_where(self):
        """In non-frozen mode on Windows, subprocess.Popen with 'where' is used."""
        self._mock_platform_windows()
        self.interface_pandoc.sys.frozen = False
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'C:\\Program Files\\Multimarkdown\\multimarkdown.exe\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_path_multimarkdown()

        self.interface_pandoc.subprocess.Popen.assert_called_once_with(
            ['where', 'multimarkdown'],
            stdin=self.interface_pandoc.subprocess.PIPE,
            stdout=self.interface_pandoc.subprocess.PIPE
        )
        mock_proc.communicate.assert_called_once()
        self.qsettings_mock.setValue.assert_called_with(
            'path_multimarkdown',
            'C:\\Program Files\\Multimarkdown\\multimarkdown.exe'
        )
        self.assertEqual(result, 'C:\\Program Files\\Multimarkdown\\multimarkdown.exe')

    # --- Settings persistence ---

    def test_settings_value_used_for_path(self):
        """The settings value is passed as stdin to the subprocess."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/multimarkdown'
        self._mock_platform_darwin()
        self.interface_pandoc.sys.frozen = False
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'/usr/local/bin/multimarkdown\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        self.interface_pandoc.get_path_multimarkdown()

        # The settings value is passed as stdin data to communicate()
        call_args = mock_proc.communicate.call_args
        self.assertEqual(call_args[0][0], b'/usr/local/bin/multimarkdown')

    def test_empty_settings_value_triggers_search(self):
        """An empty string in settings should trigger a binary search."""
        self.qsettings_mock.value.return_value = ''
        self._mock_platform_darwin()
        self.interface_pandoc.sys.frozen = False
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'/usr/bin/multimarkdown\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        self.interface_pandoc.get_path_multimarkdown()

        self.interface_pandoc.subprocess.Popen.assert_called_once()

    # --- Edge cases ---

    def test_subprocess_error_on_macos_returns_empty_string(self):
        """If subprocess fails on macOS, the result is whatever communicate returns."""
        self._mock_platform_darwin()
        self.interface_pandoc.sys.frozen = False
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'', b'command not found')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_path_multimarkdown()

        self.assertEqual(result, '')

    def test_subprocess_error_on_windows_returns_empty_string(self):
        """If subprocess fails on Windows, the result is whatever communicate returns."""
        self._mock_platform_windows()
        self.interface_pandoc.sys.frozen = False
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'', b'File Not Found')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_path_multimarkdown()

        self.assertEqual(result, '')

    def test_multimarkdown_not_found_returns_empty_string(self):
        """If the binary is not found, an empty string is returned."""
        self._mock_platform_darwin()
        self.interface_pandoc.sys.frozen = False
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_path_multimarkdown()

        self.assertEqual(result, '')
        self.qsettings_mock.setValue.assert_called_with('path_multimarkdown', '')
        self.qsettings_mock.sync.assert_called()

    def test_which_helper_returns_none(self):
        """If which() returns None in frozen mode, settings are set to None."""
        self._mock_platform_darwin()
        self.interface_pandoc.sys.frozen = True
        self.interface_pandoc.which.return_value = None

        result = self.interface_pandoc.get_path_multimarkdown()

        self.assertEqual(result, None)
        self.qsettings_mock.setValue.assert_called_with('path_multimarkdown', None)
        self.qsettings_mock.sync.assert_called()


if __name__ == '__main__':
    unittest.main()
