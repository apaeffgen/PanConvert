#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for source.helpers.interface_pandoc.get_pandoc_formats()"""

import unittest
from unittest.mock import patch, MagicMock


class TestGetPandocFormats(unittest.TestCase):
    """Test cases for get_pandoc_formats()."""

    def setUp(self):
        self.qsettings_mock = MagicMock()
        self.qsettings_mock.value.return_value = ''
        self.qsettings_mock.setValue = MagicMock()
        self.qsettings_mock.sync = MagicMock()

        self.patches = [
            patch('source.helpers.interface_pandoc._get_settings', return_value=self.qsettings_mock),
            patch('source.helpers.interface_pandoc.os'),
            patch('source.helpers.interface_pandoc.subprocess'),
            patch('source.helpers.interface_pandoc.get_path_pandoc'),
            patch('source.helpers.interface_pandoc.get_pandoc_version'),
            patch('source.helpers.interface_pandoc.error_converter_path'),
        ]
        for p in self.patches:
            p.start()

        from source.helpers import interface_pandoc
        self.interface_pandoc = interface_pandoc
        self.qsettings_mock.reset_mock()

    def tearDown(self):
        for p in self.patches:
            p.stop()

    # --- No valid pandoc path ---

    def test_returns_none_when_no_pandoc_path(self):
        """If path_pandoc is invalid and get_path_pandoc fails, return (None, None)."""
        self.qsettings_mock.value.return_value = '/nonexistent/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = False
        self.interface_pandoc.get_path_pandoc.return_value = None
        # Second settings.value call also returns invalid path
        self.qsettings_mock.value.side_effect = ['/nonexistent/pandoc', '/nonexistent/pandoc']

        result = self.interface_pandoc.get_pandoc_formats()

        self.assertEqual(result, (None, None))
        self.interface_pandoc.error_converter_path.assert_called()

    def test_calls_get_path_pandoc_when_settings_path_invalid(self):
        """Should call get_path_pandoc() when the settings path is not a valid file."""
        self.qsettings_mock.value.side_effect = ['/nonexistent/pandoc', '/usr/local/bin/pandoc']
        # os.path.isfile is called 3 times: initial check, after get_path_pandoc, and final check
        self.interface_pandoc.os.path.isfile.side_effect = [False, True, True]
        self.interface_pandoc.get_pandoc_version.return_value = 3

        self.interface_pandoc.get_pandoc_formats()

        self.interface_pandoc.get_path_pandoc.assert_called_once()

    # --- Pandoc >= 2: --list-input-formats / --list-output-formats ---

    def test_returns_formats_for_pandoc_3(self):
        """Pandoc 3+ uses --list-input-formats and --list-output-formats."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 3

        mock_proc1 = MagicMock()
        mock_proc1.communicate.return_value = (
            b'markdown\ncsv\ntex\nrst\nhtml\n',
            b''
        )
        mock_proc2 = MagicMock()
        mock_proc2.communicate.return_value = (
            b'latex\ndocx\nepub\nbeamer\nhtml5\n',
            b''
        )
        self.interface_pandoc.subprocess.Popen.side_effect = [mock_proc1, mock_proc2]

        in_fmts, out_fmts = self.interface_pandoc.get_pandoc_formats()

        self.assertEqual(in_fmts, ['markdown', 'csv', 'tex', 'rst', 'html'])
        self.assertEqual(out_fmts, ['latex', 'docx', 'epub', 'beamer', 'html5'])

    def test_returns_formats_for_pandoc_2(self):
        """Pandoc 2 also uses --list-input-formats and --list-output-formats."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 2

        mock_proc1 = MagicMock()
        mock_proc1.communicate.return_value = (b'markdown\ncsv\n', b'')
        mock_proc2 = MagicMock()
        mock_proc2.communicate.return_value = (b'latex\ndocx\n', b'')
        self.interface_pandoc.subprocess.Popen.side_effect = [mock_proc1, mock_proc2]

        in_fmts, out_fmts = self.interface_pandoc.get_pandoc_formats()

        self.assertEqual(in_fmts, ['markdown', 'csv'])
        self.assertEqual(out_fmts, ['latex', 'docx'])

    def test_pandoc_4_uses_list_commands(self):
        """Pandoc 4+ should also use --list-input-formats / --list-output-formats."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 4

        mock_proc1 = MagicMock()
        mock_proc1.communicate.return_value = (b'markdown\n', b'')
        mock_proc2 = MagicMock()
        mock_proc2.communicate.return_value = (b'latex\n', b'')
        self.interface_pandoc.subprocess.Popen.side_effect = [mock_proc1, mock_proc2]

        in_fmts, out_fmts = self.interface_pandoc.get_pandoc_formats()

        self.assertEqual(in_fmts, ['markdown'])
        self.assertEqual(out_fmts, ['latex'])

    def test_calls_list_input_formats_command(self):
        """Should invoke pandoc --list-input-formats."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 3

        mock_proc1 = MagicMock()
        mock_proc1.communicate.return_value = (b'markdown\n', b'')
        mock_proc2 = MagicMock()
        mock_proc2.communicate.return_value = (b'latex\n', b'')
        self.interface_pandoc.subprocess.Popen.side_effect = [mock_proc1, mock_proc2]

        self.interface_pandoc.get_pandoc_formats()

        self.interface_pandoc.subprocess.Popen.assert_any_call(
            ['/usr/local/bin/pandoc', '--list-input-formats'],
            stdin=self.interface_pandoc.subprocess.PIPE,
            stdout=self.interface_pandoc.subprocess.PIPE
        )

    def test_calls_list_output_formats_command(self):
        """Should invoke pandoc --list-output-formats."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 3

        mock_proc1 = MagicMock()
        mock_proc1.communicate.return_value = (b'markdown\n', b'')
        mock_proc2 = MagicMock()
        mock_proc2.communicate.return_value = (b'latex\n', b'')
        self.interface_pandoc.subprocess.Popen.side_effect = [mock_proc1, mock_proc2]

        self.interface_pandoc.get_pandoc_formats()

        self.interface_pandoc.subprocess.Popen.assert_any_call(
            ['/usr/local/bin/pandoc', '--list-output-formats'],
            stdin=self.interface_pandoc.subprocess.PIPE,
            stdout=self.interface_pandoc.subprocess.PIPE
        )

    def test_strips_whitespace_from_format_names(self):
        """Format names should have leading/trailing whitespace stripped."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 3

        mock_proc1 = MagicMock()
        mock_proc1.communicate.return_value = (b'  markdown  \n  csv  \n', b'')
        mock_proc2 = MagicMock()
        mock_proc2.communicate.return_value = (b'  latex  \n  docx  \n', b'')
        self.interface_pandoc.subprocess.Popen.side_effect = [mock_proc1, mock_proc2]

        in_fmts, out_fmts = self.interface_pandoc.get_pandoc_formats()

        self.assertEqual(in_fmts, ['markdown', 'csv'])
        self.assertEqual(out_fmts, ['latex', 'docx'])

    # --- Pandoc < 2: help text parsing ---

    def test_returns_formats_for_pandoc_1(self):
        """Pandoc 1 parses help text for input/output formats."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 1

        # Source uses: txt = ' '.join(help_text[1:help_text.index('Options:')])
        # So 'Options:' must appear as a line, with Input/Output formats before it
        help_text = (
            b'Pandoc 1.12.3\n'
            b'Usage: pandoc [OPTIONS] FILE...\n'
            b'\n'
            b'Input formats: markdown, rst, html, tex\n'
            b'Output formats: latex, docx, html, epub\n'
            b'\n'
            b'Options:\n'
            b'  -f FORMAT, --from=FORMAT\n'
            b'  -t FORMAT, --to=FORMAT\n'
            b'  -o FILE, --output=FILE\n'
            b'  -s, --standalone\n'
            b'  -V NAME=VALUE\n'
            b'  --data-dir=DIR\n'
            b'  --email-obfuscation=METHOD\n'
            b'  --file-scope\n'
            b'  --filter=PROGRAM\n'
            b'  --indented-code-classes=CLASS\n'
            b'  --metadata=KEY:VALUE\n'
            b'\n'
            b'General options:\n'
            b'  -h, --help\n'
        )
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (help_text, b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        in_fmts, out_fmts = self.interface_pandoc.get_pandoc_formats()

        self.assertEqual(in_fmts, ['markdown', 'rst', 'html', 'tex'])
        self.assertEqual(out_fmts, ['latex', 'docx', 'html', 'epub'])

    def test_pandoc_1_calls_help_command(self):
        """Pandoc 1 should invoke pandoc -h."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 1

        # Source uses: txt = ' '.join(help_text[1:help_text.index('Options:')])
        help_text = (
            b'Pandoc 1.12.3\n'
            b'Usage: pandoc [OPTIONS] FILE...\n'
            b'\n'
            b'Input formats: markdown, rst\n'
            b'Output formats: latex, docx\n'
            b'\n'
            b'Options:\n'
            b'  -f FORMAT, --from=FORMAT\n'
            b'  -t FORMAT, --to=FORMAT\n'
            b'  -o FILE, --output=FILE\n'
            b'  -s, --standalone\n'
            b'  -V NAME=VALUE\n'
            b'  --data-dir=DIR\n'
            b'  --email-obfuscation=METHOD\n'
            b'  --file-scope\n'
            b'  --filter=PROGRAM\n'
            b'  --indented-code-classes=CLASS\n'
            b'  --metadata=KEY:VALUE\n'
            b'\n'
            b'General options:\n'
            b'  -h, --help\n'
        )
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (help_text, b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        self.interface_pandoc.get_pandoc_formats()

        self.interface_pandoc.subprocess.Popen.assert_called_once_with(
            ['/usr/local/bin/pandoc', '-h'],
            stdin=self.interface_pandoc.subprocess.PIPE,
            stdout=self.interface_pandoc.subprocess.PIPE
        )

    # --- Version-dependent behavior ---

    def test_pandoc_0_uses_help_text_parsing(self):
        """Pandoc version 0 falls through to help text parsing (version < 2)."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 0

        # Source uses: txt = ' '.join(help_text[1:help_text.index('Options:')])
        # 'Options:' must appear as a line, with Input/Output formats before it
        help_text = (
            b'Pandoc 0.9.0\n'
            b'Usage: pandoc [OPTIONS] FILE...\n'
            b'\n'
            b'Input formats: markdown\n'
            b'Output formats: html\n'
            b'\n'
            b'Options:\n'
            b'  -f FORMAT, --from=FORMAT\n'
            b'  -t FORMAT, --to=FORMAT\n'
            b'  -o FILE, --output=FILE\n'
            b'  -s, --standalone\n'
            b'  -V NAME=VALUE\n'
            b'  --data-dir=DIR\n'
            b'  --email-obfuscation=METHOD\n'
            b'  --file-scope\n'
            b'  --filter=PROGRAM\n'
            b'  --indented-code-classes=CLASS\n'
            b'  --metadata=KEY:VALUE\n'
            b'\n'
            b'General options:\n'
            b'  -h, --help\n'
        )
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (help_text, b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        in_fmts, out_fmts = self.interface_pandoc.get_pandoc_formats()

        self.assertEqual(in_fmts, ['markdown'])
        self.assertEqual(out_fmts, ['html'])

    def test_pandoc_1_5_uses_help_text_parsing(self):
        """Pandoc version 1.x falls through to help text parsing (version < 2)."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 1

        # Source uses: txt = ' '.join(help_text[1:help_text.index('Options:')])
        help_text = (
            b'Pandoc 1.12.3\n'
            b'Usage: pandoc [OPTIONS] FILE...\n'
            b'\n'
            b'Input formats: markdown\n'
            b'Output formats: html\n'
            b'\n'
            b'Options:\n'
            b'  -f FORMAT, --from=FORMAT\n'
            b'  -t FORMAT, --to=FORMAT\n'
            b'  -o FILE, --output=FILE\n'
            b'  -s, --standalone\n'
            b'  -V NAME=VALUE\n'
            b'  --data-dir=DIR\n'
            b'  --email-obfuscation=METHOD\n'
            b'  --file-scope\n'
            b'  --filter=PROGRAM\n'
            b'  --indented-code-classes=CLASS\n'
            b'  --metadata=KEY:VALUE\n'
            b'\n'
            b'General options:\n'
            b'  -h, --help\n'
        )
        mock_proc = MagicMock()
        mock_proc.communicate.return_value = (help_text, b'')
        self.interface_pandoc.subprocess.Popen.return_value = mock_proc

        in_fmts, out_fmts = self.interface_pandoc.get_pandoc_formats()

        self.assertEqual(in_fmts, ['markdown'])
        self.assertEqual(out_fmts, ['html'])

    # --- Empty formats ---

    def test_empty_input_formats(self):
        """Should handle empty input formats list."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 3

        mock_proc1 = MagicMock()
        mock_proc1.communicate.return_value = (b'', b'')
        mock_proc2 = MagicMock()
        mock_proc2.communicate.return_value = (b'latex\n', b'')
        self.interface_pandoc.subprocess.Popen.side_effect = [mock_proc1, mock_proc2]

        in_fmts, out_fmts = self.interface_pandoc.get_pandoc_formats()

        self.assertEqual(in_fmts, [])
        self.assertEqual(out_fmts, ['latex'])

    def test_empty_output_formats(self):
        """Should handle empty output formats list."""
        self.qsettings_mock.value.return_value = '/usr/local/bin/pandoc'
        self.interface_pandoc.os.path.isfile.return_value = True
        self.interface_pandoc.get_pandoc_version.return_value = 3

        mock_proc1 = MagicMock()
        mock_proc1.communicate.return_value = (b'markdown\n', b'')
        mock_proc2 = MagicMock()
        mock_proc2.communicate.return_value = (b'', b'')
        self.interface_pandoc.subprocess.Popen.side_effect = [mock_proc1, mock_proc2]

        in_fmts, out_fmts = self.interface_pandoc.get_pandoc_formats()

        self.assertEqual(in_fmts, ['markdown'])
        self.assertEqual(out_fmts, [])


if __name__ == '__main__':
    unittest.main()
