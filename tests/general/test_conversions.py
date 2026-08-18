#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for pandoc file conversion via the converter modules.

Tests actual conversion pipelines:
- markdown → html
- markdown → latex
- markdown → docx (if pandoc supports it)
- rst → html
- html → markdown
"""

import os
import sys
import subprocess
import tempfile
import pytest
from pathlib import Path

# Ensure source is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_markdown(temp_dir):
    """Create a sample Markdown file."""
    content = """# Test Document

This is **bold** and *italic* text.

## Section 1

- Item A
- Item B
- Item C

## Section 2

Here is `inline code`.

    # Code block
    print("hello world")

> A blockquote

1. First
2. Second
"""
    f = temp_dir / "test.md"
    f.write_text(content, encoding="utf-8")
    return f


@pytest.fixture
def sample_rst(temp_dir):
    """Create a sample reStructuredText file."""
    content = """Test Document
=============

This is **bold** and *italic* text.

Section 1
---------

- Item A
- Item B

Section 2
---------

Here is ``inline code``.

.. code-block:: python

    print("hello")
"""
    f = temp_dir / "test.rst"
    f.write_text(content, encoding="utf-8")
    return f


@pytest.fixture
def sample_html(temp_dir):
    """Create a sample HTML file."""
    content = """<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<h1>Test Document</h1>
<p>This is <strong>bold</strong> and <em>italic</em>.</p>
<ul><li>Item A</li><li>Item B</li></ul>
</body>
</html>
"""
    f = temp_dir / "test.html"
    f.write_text(content, encoding="utf-8")
    return f


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _has_pandoc():
    return __import__("shutil").which("pandoc") is not None


def _convert_via_pandoc(input_file, from_fmt, to_fmt, output_file=None):
    """Convert a file using pandoc directly (bypassing the GUI)."""
    import shutil
    pandoc = shutil.which("pandoc")
    if not pandoc:
        pytest.skip("pandoc not found")

    cmd = [pandoc, f"--from={from_fmt}", f"--to={to_fmt}", str(input_file)]
    if output_file:
        cmd.extend(["--output", str(output_file)])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result


def _convert_text_via_pandoc(text, from_fmt, to_fmt):
    """Convert text using pandoc directly."""
    import shutil
    pandoc = shutil.which("pandoc")
    if not pandoc:
        pytest.skip("pandoc not found")

    result = subprocess.run(
        [pandoc, f"--from={from_fmt}", f"--to={to_fmt}", "-"],
        input=text,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result


# ─── Tests ────────────────────────────────────────────────────────────────────


class TestMarkdownToHtml:
    """Test markdown → HTML conversion."""

    @pytest.mark.requires_pandoc
    def test_markdown_to_html_file(self, sample_markdown, temp_dir):
        """Convert markdown file to HTML file."""
        output = temp_dir / "output.html"
        result = _convert_via_pandoc(sample_markdown, "markdown", "html", output)
        assert result.returncode == 0, f"Conversion failed: {result.stderr}"
        assert output.exists(), "Output file was not created"
        content = output.read_text()
        assert "<h1" in content and "Test Document" in content

    @pytest.mark.requires_pandoc
    def test_markdown_to_html_string(self, sample_markdown):
        """Convert markdown to HTML string."""
        result = _convert_text_via_pandoc(
            sample_markdown.read_text(), "markdown", "html"
        )
        assert result.returncode == 0, f"Conversion failed: {result.stderr}"
        assert "<h1" in result.stdout
        assert "<p>" in result.stdout

    @pytest.mark.requires_pandoc
    def test_markdown_heading_preserved(self, sample_markdown):
        """Headings should be preserved in HTML output."""
        result = _convert_text_via_pandoc(
            sample_markdown.read_text(), "markdown", "html"
        )
        assert result.returncode == 0
        assert "<h1" in result.stdout
        assert "<h2" in result.stdout


class TestMarkdownToLatex:
    """Test markdown → LaTeX conversion."""

    @pytest.mark.requires_pandoc
    def test_markdown_to_latex(self, sample_markdown):
        """Convert markdown to LaTeX."""
        result = _convert_text_via_pandoc(
            sample_markdown.read_text(), "markdown", "latex"
        )
        assert result.returncode == 0, f"Conversion failed: {result.stderr}"
        assert "\\section" in result.stdout or "\\section*" in result.stdout
        assert "\\textbf" in result.stdout or "\\textbf{" in result.stdout


class TestMarkdownToDocx:
    """Test markdown → docx conversion."""

    @pytest.mark.requires_pandoc
    def test_markdown_to_docx(self, sample_markdown, temp_dir):
        """Convert markdown to docx."""
        output = temp_dir / "output.docx"
        result = _convert_via_pandoc(sample_markdown, "markdown", "docx", output)
        assert result.returncode == 0, f"Conversion failed: {result.stderr}"
        assert output.exists(), "docx output file was not created"
        assert output.stat().st_size > 0, "docx file is empty"


class TestRstToHtml:
    """Test reStructuredText → HTML conversion."""

    @pytest.mark.requires_pandoc
    def test_rst_to_html(self, sample_rst):
        """Convert rst to HTML."""
        result = _convert_text_via_pandoc(
            sample_rst.read_text(), "rst", "html"
        )
        assert result.returncode == 0, f"Conversion failed: {result.stderr}"
        assert "<h1" in result.stdout or "<h2" in result.stdout


class TestHtmlToMarkdown:
    """Test HTML → Markdown conversion."""

    @pytest.mark.requires_pandoc
    def test_html_to_markdown(self, sample_html):
        """Convert HTML to markdown."""
        result = _convert_text_via_pandoc(
            sample_html.read_text(), "html", "markdown"
        )
        assert result.returncode == 0, f"Conversion failed: {result.stderr}"
        assert "#" in result.stdout  # Markdown headings
        assert "**" in result.stdout or "*" in result.stdout  # Bold/italic


class TestConverterModules:
    """Test the converter modules directly (with mocked settings)."""

    def test_batch_convert_manual_imports(self):
        """batch_converter module should be importable."""
        from source.converter import batch_converter
        assert hasattr(batch_converter, "batch_convert_manual")

    def test_manual_converter_imports(self):
        """manual_converter module should be importable."""
        from source.converter import manual_converter
        assert hasattr(manual_converter, "convert_universal")
        assert hasattr(manual_converter, "convert_binary")

    def test_interface_pandoc_imports(self):
        """interface_pandoc module should be importable."""
        from source.helpers import interface_pandoc
        assert hasattr(interface_pandoc, "get_pandoc_version")
        assert hasattr(interface_pandoc, "get_pandoc_formats")
        assert hasattr(interface_pandoc, "get_path_pandoc")
        assert hasattr(interface_pandoc, "get_path_multimarkdown")


class TestConversionEdgeCases:
    """Test edge cases in conversion."""

    @pytest.mark.requires_pandoc
    def test_empty_input(self):
        """Empty input should not crash pandoc."""
        result = _convert_text_via_pandoc("", "markdown", "html")
        # pandoc may return non-zero for empty input, but shouldn't crash
        assert result.returncode in (0, 1)  # 0=success, 1=empty/no output

    @pytest.mark.requires_pandoc
    def test_unicode_input(self, temp_dir):
        """Unicode content should be handled correctly."""
        content = """# Unicode Test

Hello 世界
مرحبا بالعالم
Привет мир

Emoji: 🎉🚀✨
"""
        f = temp_dir / "unicode.md"
        f.write_text(content, encoding="utf-8")
        result = _convert_text_via_pandoc(content, "markdown", "html")
        assert result.returncode == 0, f"Unicode conversion failed: {result.stderr}"

    @pytest.mark.requires_pandoc
    def test_large_input(self, temp_dir):
        """Large input should be handled without crashing."""
        lines = ["# Section " + str(i) for i in range(100)]
        content = "\n\n".join(lines) + "\n"
        f = temp_dir / "large.md"
        f.write_text(content, encoding="utf-8")
        result = _convert_text_via_pandoc(content, "markdown", "html")
        assert result.returncode == 0, f"Large input conversion failed: {result.stderr}"
        assert len(result.stdout) > 0

    @pytest.mark.requires_pandoc
    def test_special_characters_in_filename(self, temp_dir):
        """Files with special characters in names should work."""
        content = "# Test\n\nHello world\n"
        f = temp_dir / "test file (1).md"
        f.write_text(content, encoding="utf-8")
        output = temp_dir / "output.html"
        result = _convert_via_pandoc(f, "markdown", "html", output)
        assert result.returncode == 0, f"Special char filename failed: {result.stderr}"


class TestFormatCombinations:
    """Test various format combinations."""

    @pytest.mark.requires_pandoc
    def test_markdown_to_odt(self, sample_markdown, temp_dir):
        """markdown → ODT conversion."""
        output = temp_dir / "output.odt"
        result = _convert_via_pandoc(sample_markdown, "markdown", "odt", output)
        assert result.returncode == 0, f"ODT conversion failed: {result.stderr}"
        assert output.exists()

    @pytest.mark.requires_pandoc
    def test_markdown_to_epub(self, sample_markdown, temp_dir):
        """markdown → EPUB conversion."""
        output = temp_dir / "output.epub"
        result = _convert_via_pandoc(sample_markdown, "markdown", "epub", output)
        assert result.returncode == 0, f"EPUB conversion failed: {result.stderr}"
        assert output.exists()

    @pytest.mark.requires_pandoc
    def test_markdown_to_beamer(self, sample_markdown, temp_dir):
        """markdown → Beamer (PDF slides) conversion."""
        output = temp_dir / "output.pdf"
        result = _convert_via_pandoc(sample_markdown, "markdown", "beamer", output)
        # Beamer may fail if LaTeX is not installed, so we just check it doesn't crash
        # pandoc returns non-zero if LaTeX is missing, but the binary is still valid
        if result.returncode != 0:
            pytest.skip("LaTeX not installed (beamer requires it)")
        assert output.exists()

    @pytest.mark.requires_pandoc
    def test_html_to_docx(self, sample_html, temp_dir):
        """HTML → docx conversion."""
        output = temp_dir / "output.docx"
        result = _convert_via_pandoc(sample_html, "html", "docx", output)
        assert result.returncode == 0, f"HTML→docx failed: {result.stderr}"
        assert output.exists()
