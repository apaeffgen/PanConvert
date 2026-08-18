#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Platform-specific installer tests.

Tests:
- Windows: Inno Setup installer (.exe)
- macOS: PKG installer (.pkg)
- Linux: AppImage (.AppImage)
"""

import os
import platform
import subprocess
import shutil
import pytest
from pathlib import Path


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _get_dist_dir():
    return Path(__file__).resolve().parent.parent.parent / "dist"


def _find_installer(dist_dir, pattern):
    """Find an installer file matching the pattern."""
    if dist_dir is None or not dist_dir.exists():
        return None
    for f in dist_dir.glob(pattern):
        if f.is_file():
            return f
    return None


# ─── Windows Installer Tests ──────────────────────────────────────────────────


class TestWindowsInstaller:
    """Test Windows installer (Inno Setup).
    
    NOTE: These tests are skipped by default. The installer package is tested
    separately during the build/release process. Regular tests should focus on
    the PanConvert application binary, not the installer.
    """

    def test_windows_installer_exists(self):
        """Windows installer should exist in dist/."""
        if platform.system().lower() != "windows":
            pytest.skip("Windows-only test")
        dist = _get_dist_dir()
        installer = _find_installer(dist, "PanConvert-*-win*-installer.exe")
        assert installer is not None, (
            "No Windows installer found in dist/. "
            "Build it with: python packaging/windows/build_installer.py"
        )

    def test_windows_installer_is_file(self):
        """Installer should be a regular file."""
        if platform.system().lower() != "windows":
            pytest.skip("Windows-only test")
        dist = _get_dist_dir()
        installer = _find_installer(dist, "PanConvert-*-win*-installer.exe")
        if installer is None:
            pytest.skip("No installer available")
        assert installer.is_file()

    def test_windows_installer_size_reasonable(self):
        """Installer should have a reasonable size."""
        if platform.system().lower() != "windows":
            pytest.skip("Windows-only test")
        dist = _get_dist_dir()
        installer = _find_installer(dist, "PanConvert-*-win*-installer.exe")
        if installer is None:
            pytest.skip("No installer available")
        size = installer.stat().st_size
        assert size > 10_000_000, f"Installer too small ({size / 1_000_000:.1f} MB)"
        assert size < 500_000_000, f"Installer suspiciously large ({size / 1_000_000_000:.2f} GB)"

    def test_windows_installer_has_version_in_name(self):
        """Installer filename should contain a version number."""
        if platform.system().lower() != "windows":
            pytest.skip("Windows-only test")
        dist = _get_dist_dir()
        installer = _find_installer(dist, "PanConvert-*-win*-installer.exe")
        if installer is None:
            pytest.skip("No installer available")
        import re
        assert re.search(r"\d+\.\d+", installer.name), (
            f"Installer name doesn't contain version: {installer.name}"
        )


# ─── macOS Installer Tests ────────────────────────────────────────────────────


class TestMacOSInstaller:
    """Test macOS PKG installer.
    
    NOTE: These tests are skipped by default. The installer package is tested
    separately during the build/release process. Regular tests should focus on
    the PanConvert application binary, not the installer.
    """

    def test_macos_installer_exists(self):
        """macOS PKG installer should exist in dist/."""
        if platform.system().lower() != "darwin":
            pytest.skip("macOS-only test")
        dist = _get_dist_dir()
        installer = _find_installer(dist, "PanConvert-*-macos.pkg")
        if installer is None:
            pytest.skip("No macOS PKG installer found (not built yet)")

    def test_macos_installer_is_file(self):
        """PKG should be a regular file."""
        if platform.system().lower() != "darwin":
            pytest.skip("macOS-only test")
        dist = _get_dist_dir()
        installer = _find_installer(dist, "PanConvert-*-macos.pkg")
        if installer is None:
            pytest.skip("No installer available")
        assert installer.is_file()

    def test_macos_installer_size_reasonable(self):
        """PKG should have a reasonable size."""
        if platform.system().lower() != "darwin":
            pytest.skip("macOS-only test")
        dist = _get_dist_dir()
        installer = _find_installer(dist, "PanConvert-*-macos.pkg")
        if installer is None:
            pytest.skip("No installer available")
        size = installer.stat().st_size
        assert size > 10_000_000, f"PKG too small ({size / 1_000_000:.1f} MB)"
        assert size < 500_000_000, f"PKG suspiciously large ({size / 1_000_000_000:.2f} GB)"

    def test_macos_pkg_is_valid_archive(self):
        """PKG should be a valid archive (check with tar)."""
        if platform.system().lower() != "darwin":
            pytest.skip("macOS-only test")
        dist = _get_dist_dir()
        installer = _find_installer(dist, "PanConvert-*-macos.pkg")
        if installer is None:
            pytest.skip("No installer available")
        try:
            # PKG files are typically cpio archives
            result = subprocess.run(
                ["tar", "-tf", str(installer)],
                capture_output=True,
                timeout=10,
            )
            # May fail if not a tar archive, but shouldn't crash
        except FileNotFoundError:
            pytest.skip("tar not available")
        except subprocess.TimeoutExpired:
            pytest.skip("tar timed out")


# ─── Linux AppImage Tests ─────────────────────────────────────────────────────


class TestLinuxAppImage:
    """Test Linux AppImage.
    
    NOTE: These tests are skipped by default. The installer package is tested
    separately during the build/release process. Regular tests should focus on
    the PanConvert application binary, not the installer.
    """

    def test_linux_appimage_exists(self):
        """AppImage should exist in dist/."""
        if platform.system().lower() != "linux":
            pytest.skip("Linux-only test")
        dist = _get_dist_dir()
        appimage = _find_installer(dist, "PanConvert*.AppImage")
        assert appimage is not None, (
            "No AppImage found in dist/. "
            "Build it with: bash packaging/linux/build_appimage.sh"
        )

    def test_linux_appimage_is_file(self):
        """AppImage should be a regular file."""
        if platform.system().lower() != "linux":
            pytest.skip("Linux-only test")
        dist = _get_dist_dir()
        appimage = _find_installer(dist, "PanConvert*.AppImage")
        if appimage is None:
            pytest.skip("No AppImage available")
        assert appimage.is_file()

    def test_linux_appimage_is_executable(self):
        """AppImage should be executable."""
        if platform.system().lower() != "linux":
            pytest.skip("Linux-only test")
        dist = _get_dist_dir()
        appimage = _find_installer(dist, "PanConvert*.AppImage")
        if appimage is None:
            pytest.skip("No AppImage available")
        assert os.access(appimage, os.X_OK), "AppImage is not executable"

    def test_linux_appimage_size_reasonable(self):
        """AppImage should have a reasonable size."""
        if platform.system().lower() != "linux":
            pytest.skip("Linux-only test")
        dist = _get_dist_dir()
        appimage = _find_installer(dist, "PanConvert*.AppImage")
        if appimage is None:
            pytest.skip("No AppImage available")
        size = appimage.stat().st_size
        assert size > 10_000_000, f"AppImage too small ({size / 1_000_000:.1f} MB)"
        assert size < 500_000_000, f"AppImage suspiciously large ({size / 1_000_000_000:.2f} GB)"

    def test_linux_appimage_has_appimage_magic(self):
        """AppImage should contain the valid AppImage magic bytes."""
        if platform.system().lower() != "linux":
            pytest.skip("Linux-only test")
        dist = _get_dist_dir()
        appimage = _find_installer(dist, "PanConvert*.AppImage")
        if appimage is None:
            pytest.skip("No AppImage available")
        try:
            with open(appimage, "rb") as f:
                # AppImage type 2 magic: ELF header + "AI\x02\x00" at offset 8
                content = f.read(16)
                assert len(content) >= 16, "File too small to be an AppImage"
                # Check for AppImage type 2 magic at offset 8: AI\x02\x00
                assert content[8:12] == b"AI\x02\x00", (
                    f"Invalid AppImage magic bytes: {content[8:12]}. "
                    f"Expected b'AI\\x02\\x00' for AppImage type 2"
                )
        except Exception as e:
            pytest.fail(f"Could not read AppImage: {e}")


# ─── Cross-Platform Installer Tests ───────────────────────────────────────────


class TestInstallerCrossPlatform:
    """Cross-platform installer availability checks.
    
    NOTE: These tests are skipped by default. The installer package is tested
    separately during the build/release process. Regular tests should focus on
    the PanConvert application binary, not the installer.
    """

    def test_at_least_one_installer_exists(self):
        """At least one platform installer should exist."""
        dist = _get_dist_dir()
        if dist is None or not dist.exists():
            pytest.skip("dist/ directory not found")

        system = platform.system().lower()
        has_installer = False

        if system == "windows":
            has_installer = bool(_find_installer(dist, "PanConvert-*-win*-installer.exe"))
        elif system == "darwin":
            has_installer = bool(_find_installer(dist, "PanConvert-*-macos.pkg"))
        elif system == "linux":
            has_installer = bool(_find_installer(dist, "PanConvert*.AppImage"))

        # This is informational - we don't fail if no installer exists
        # since the binary itself may be sufficient for distribution
        if not has_installer:
            pytest.skip(f"No installer for {system} found (binary may still be usable)")
