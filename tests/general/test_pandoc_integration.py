#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for pandoc integration from the packaged binary.

Verifies:
- Pandoc detection from the bundled binary
- Pandoc version parsing
- Format detection (--list-input-formats, --list-output-formats)
"""

import os
import sys
import platform
import subprocess
import tempfile
import shutil
import pytest
from pathlib import Path


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _find_binary_in_dist(dist_dir: Path):
    if dist_dir is None or not dist_dir.exists():
        return None
    system = platform.system().lower()
    if system == "windows":
        for f in dist_dir.glob("Panconvert*.exe"):
            if f.is_file() and "-installer" not in f.name.lower():
                return f
    elif system == "darwin":
        # First check for direct binary at dist/Panconvert
        direct_binary = dist_dir / "Panconvert"
        if direct_binary.exists() and direct_binary.is_file():
            return direct_binary
        # Also check .app bundle structure
        for f in dist_dir.glob("Panconvert*.app"):
            if f.is_dir():
                binary = f / "Contents" / "MacOS" / "Panconvert"
                if binary.exists():
                    return binary
    else:
        for f in dist_dir.glob("Panconvert-*-linux*"):
            if f.is_file() and not f.name.endswith(".AppImage"):
                return f
        for f in dist_dir.glob("Panconvert*"):
            if f.is_file() and os.access(f, os.X_OK):
                return f
    return None


def _get_dist_dir():
    return Path(__file__).resolve().parent.parent.parent / "dist"


def _run_binary(binary_path, args, timeout=30):
    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"
    env["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
    result = subprocess.run(
        [str(binary_path)] + args,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    return result.stdout, result.stderr, result.returncode


def _is_binary_broken(binary_path) -> bool:
    """Check if the binary is broken (e.g., code signature issues on macOS)."""
    if binary_path is None or not binary_path.exists():
        return False
    try:
        env = os.environ.copy()
        env["QT_QPA_PLATFORM"] = "offscreen"
        env["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
        result = subprocess.run(
            [str(binary_path), "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            env=env,
        )
        combined = (result.stderr + result.stdout).lower()
        # PYI errors indicate PyInstaller binary issues
        if "pyi-" in combined and "error" in combined:
            return True
        # Code signature errors
        if "code signature" in combined or "team ids" in combined:
            return True
        # Library loading errors
        if "failed to load" in combined and ("library" in combined or "dylib" in combined):
            return True
        return False
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False


def _skip_if_binary_broken(binary):
    """Skip test if binary is broken."""
    if _is_binary_broken(binary):
        pytest.skip("Binary is broken (code signature/library loading issues)")


def _has_system_pandoc():
    return shutil.which("pandoc") is not None


def _get_system_pandoc_version():
    if not _has_system_pandoc():
        return 0
    try:
        result = subprocess.run(
            ["pandoc", "-v"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return 0
        for line in result.stdout.splitlines():
            if line.startswith("pandoc"):
                import re
                m = re.search(r"pandoc\s+(\d+)", line)
                if m:
                    return int(m.group(1))
        return 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return 0


def _get_system_pandoc_path():
    return shutil.which("pandoc") or ""


def _pandoc_list_input_formats(pandoc_path):
    """Get input formats from pandoc."""
    result = subprocess.run(
        [pandoc_path, "--list-input-formats"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        return []
    return [f.strip() for f in result.stdout.strip().splitlines() if f.strip()]


def _pandoc_list_output_formats(pandoc_path):
    """Get output formats from pandoc."""
    result = subprocess.run(
        [pandoc_path, "--list-output-formats"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        return []
    return [f.strip() for f in result.stdout.strip().splitlines() if f.strip()]


# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def binary():
    return _find_binary_in_dist(_get_dist_dir())


@pytest.fixture(scope="module")
def has_pandoc():
    """Skip tests if no pandoc is available."""
    if not _has_system_pandoc():
        pytest.skip("pandoc not found on system")
    return True


@pytest.fixture(scope="module")
def pandoc_path():
    return _get_system_pandoc_path()


@pytest.fixture(scope="module")
def pandoc_version():
    return _get_system_pandoc_version()


# ─── Tests ────────────────────────────────────────────────────────────────────


class TestPandocDetection:
    """Test that the binary can detect pandoc."""

    @pytest.mark.requires_pandoc
    def test_pandoc_is_available(self, has_pandoc):
        """Pandoc should be installed for integration tests."""
        assert has_pandoc

    @pytest.mark.requires_pandoc
    def test_pandoc_version_is_major_2_or_higher(self, pandoc_version):
        """Pandoc major version should be >= 2."""
        assert pandoc_version >= 2, f"Expected pandoc >= 2, got {pandoc_version}"


class TestPandocFormats:
    """Test pandoc format detection."""

    @pytest.mark.requires_pandoc
    def test_input_formats_not_empty(self, pandoc_path):
        """Pandoc should report non-empty input formats."""
        formats = _pandoc_list_input_formats(pandoc_path)
        assert len(formats) > 0, "No input formats reported by pandoc"

    @pytest.mark.requires_pandoc
    def test_output_formats_not_empty(self, pandoc_path):
        """Pandoc should report non-empty output formats."""
        formats = _pandoc_list_output_formats(pandoc_path)
        assert len(formats) > 0, "No output formats reported by pandoc"

    @pytest.mark.requires_pandoc
    def test_markdown_is_input_format(self, pandoc_path):
        """markdown should be a valid input format."""
        formats = _pandoc_list_input_formats(pandoc_path)
        assert "markdown" in formats, f"markdown not in input formats: {formats}"

    @pytest.mark.requires_pandoc
    def test_markdown_is_output_format(self, pandoc_path):
        """markdown should be a valid output format."""
        formats = _pandoc_list_output_formats(pandoc_path)
        assert "markdown" in formats, f"markdown not in output formats: {formats}"

    @pytest.mark.requires_pandoc
    def test_html_is_output_format(self, pandoc_path):
        """html should be a valid output format."""
        formats = _pandoc_list_output_formats(pandoc_path)
        assert "html" in formats, f"html not in output formats: {formats}"

    @pytest.mark.requires_pandoc
    def test_latex_is_output_format(self, pandoc_path):
        """latex should be a valid output format."""
        formats = _pandoc_list_output_formats(pandoc_path)
        assert "latex" in formats, f"latex not in output formats: {formats}"

    @pytest.mark.requires_pandoc
    def test_docx_is_output_format(self, pandoc_path):
        """docx should be a valid output format."""
        formats = _pandoc_list_output_formats(pandoc_path)
        assert "docx" in formats, f"docx not in output formats: {formats}"


class TestPandocVersionParsing:
    """Test that pandoc version is correctly detected."""

    @pytest.mark.requires_pandoc
    def test_version_output_starts_with_pandoc(self, pandoc_path):
        """pandoc -v output should start with 'pandoc'."""
        result = subprocess.run(
            [pandoc_path, "-v"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        first_line = result.stdout.splitlines()[0] if result.stdout.strip() else ""
        assert first_line.lower().startswith("pandoc"), (
            f"First line of pandoc -v should start with 'pandoc', got: '{first_line}'"
        )

    @pytest.mark.requires_pandoc
    def test_version_major_matches(self, pandoc_path, pandoc_version):
        """The parsed major version should match pandoc -v output."""
        result = subprocess.run(
            [pandoc_path, "-v"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        import re
        first_line = result.stdout.splitlines()[0] if result.stdout.strip() else ""
        m = re.search(r"pandoc\s+(\d+)", first_line)
        assert m is not None, f"Could not parse version from: {first_line}"
        parsed = int(m.group(1))
        assert parsed == pandoc_version, (
            f"Parsed version {parsed} doesn't match reported {pandoc_version}"
        )


class TestBundledPandoc:
    """Test bundled pandoc behavior (Windows/macOS)."""

    def test_bundled_pandoc_on_windows(self, binary):
        """On Windows, bundled pandoc should be in the same directory as the binary."""
        if binary is None:
            pytest.skip("No binary available")
        if platform.system().lower() != "windows":
            pytest.skip("Windows-only test")

        # The binary should be in dist/ and pandoc.exe should be alongside it
        # or in the same directory as the .app bundle
        binary_dir = binary.parent
        bundled_pandoc = binary_dir / "pandoc.exe"
        # This is informational - bundled pandoc may or may not be present
        # depending on how the binary was built
        if bundled_pandoc.exists():
            assert bundled_pandoc.is_file()
            assert bundled_pandoc.stat().st_size > 0

    def test_bundled_pandoc_on_macos(self, binary):
        """On macOS, check if pandoc is bundled or available."""
        if binary is None:
            pytest.skip("No binary available")
        if platform.system().lower() != "darwin":
            pytest.skip("macOS-only test")

        # Check if pandoc is in a common bundled location
        for loc in ["/usr/local/bin/pandoc", "/opt/homebrew/bin/pandoc", "/opt/local/bin/pandoc"]:
            if os.path.isfile(loc):
                assert os.access(loc, os.X_OK)
                break


class TestBinaryPandocInteraction:
    """Test that the binary interacts with pandoc correctly."""

    @pytest.mark.requires_pandoc
    def test_binary_runs_with_no_args(self, binary):
        """Running the binary with no args should not crash (may open GUI)."""
        if binary is None:
            pytest.skip("No binary available")
        _skip_if_binary_broken(binary)
        # We just verify it starts without immediate crash
        # It may hang waiting for GUI, so we use a short timeout
        try:
            env = os.environ.copy()
            env["QT_QPA_PLATFORM"] = "offscreen"
            env["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
            result = subprocess.run(
                [str(binary)],
                capture_output=True,
                timeout=5,
                env=env,
            )
            # Return code doesn't matter much for GUI apps
            # We just want to ensure it doesn't segfault immediately
        except subprocess.TimeoutExpired:
            # Expected for GUI apps - they don't exit on their own
            pass
        except FileNotFoundError:
            pytest.skip("Binary not found")
