#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for source.helpers.interface_pandoc.get_pandoc_version()"""

import unittest
from unittest.mock import patch, MagicMock


class TestGetPandocVersion(unittest.TestCase):
    """Test cases for get_pandoc_version()."""

    def setUp(self):
        self.qsettings_mock = MagicMock()
        self.qsettings_mock.value.return_value = ''
        self.qsettings_mock.setValue = MagicMock()
        self.qsettings_mock.sync = MagicMock()

        self.patches = [
            patch('source.helpers.interface_pandoc._get_settings', return_value=self.qsettings_mock),
            patch('source.helpers.interface_pandoc.os'),
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

    # --- Valid pandoc path ---

    def test_parses_pandoc_3_version(self):
        """Should extract major version 3 from 'pandoc 3.10.1'."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'pandoc 3.10.1\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_pandoc_version()

        self.assertEqual(result, 3)

    def test_parses_pandoc_2_version(self):
        """Should extract major version 2 from 'pandoc 2.11.4'."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'pandoc 2.11.4\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_pandoc_version()

        self.assertEqual(result, 2)

    def test_parses_pandoc_1_version(self):
        """Should extract major version 1 from 'pandoc 1.12.3'."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'pandoc 1.12.3\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_pandoc_version()

        self.assertEqual(result, 1)

    def test_parses_version_with_extra_lines(self):
        """Should use only the first line of pandoc -v output."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (
            b'pandoc 3.1.2\n'
            b'Compiled with pandoc-types 1.23, texmath 0.12.3, ...\n',
            b''
        )
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_pandoc_version()

        self.assertEqual(result, 3)

    # --- Invalid / missing pandoc path ---

    def test_returns_zero_when_path_is_not_a_file(self):
        """If path_pandoc is not a valid file, return 0."""
        self.qsettings_mock.value.return_value = '/nonexistent/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = False

        result = self.interface_pandoc.get_pandoc_version()

        self.assertEqual(result, 0)
        self.interface_pandoc.subprocess.Popen.assert_not_called()

    def test_returns_zero_when_settings_value_empty(self):
        """If settings value is empty, return 0."""
        self.qsettings_mock.value.return_value = ''
        self.interface_pandoc.os.path.isfile.return_value = False

        result = self.interface_pandoc.get_pandoc_version()

        self.assertEqual(result, 0)

    # --- Pandoc -v output edge cases ---

    def test_returns_zero_when_version_regex_fails(self):
        """If pandoc -v output doesn't match the expected pattern, return 0."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'unknown output format\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_pandoc_version()

        self.assertEqual(result, 0)

    def test_returns_zero_when_pandoc_output_is_empty(self):
        """If pandoc -v produces no output, return 0."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_pandoc_version()

        self.assertEqual(result, 0)

    def test_calls_pandoc_with_correct_args(self):
        """Should invoke pandoc with ['-v'] argument."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'pandoc 3.0.0\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        self.interface_pandoc.get_pandoc_version()

        self.interface_pandoc.subprocess.Popen.assert_called_once_with(
            ['/usr/local/bin/pandoc', '-v'],
            stdin=self.interface_pandoc.subprocess.PIPE,
            stdout=self.interface_pandoc.subprocess.PIPE
        )

    def test_empty_first_line_returns_zero(self):
        """If the first line of pandoc -v output is empty, return 0."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (b'\n', b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        result = self.interface_pandoc.get_pandoc_version()

        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
