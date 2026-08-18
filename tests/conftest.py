#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Root conftest.py for PanConvert tests.

Provides:
- Responsive table report option (--table-report)
- Global fixtures for all tests
"""

import os
import platform
import shutil
import subprocess
import time

import pytest


# ─── Table Reporter Options ──────────────────────────────────────────────────


def pytest_addoption(parser):
    """Add command-line options for the table reporter."""
    group = parser.getgroup("terminal reporting")
    group.addoption(
        "--table-report",
        action="store_true",
        default=False,
        help="Enable responsive table output format",
    )
    group.addoption(
        "--max-name-width",
        type=int,
        default=60,
        help="Maximum width for test names (default: 60)",
    )
    group.addoption(
        "--min-width",
        type=int,
        default=40,
        help="Minimum terminal width before truncating (default: 40)",
    )


# ─── Responsive Table Reporter ───────────────────────────────────────────────

class MinimalProgressReporter:
    """Shows minimal progress during test execution."""

    def __init__(self, config):
        self.config = config
        self.total_tests = 0
        self.completed_tests = 0
        self.current_test = ""

    def pytest_collection_modifyitems(self, config, session, items):
        """Called when test collection is complete."""
        self.total_tests = len(items)
        self.completed_tests = 0
        print(f"\nRunning {self.total_tests} tests...\n", flush=True)

    def pytest_runtest_logstart(self, nodeid, location):
        """Called when a test starts - show test name."""
        self.current_test = nodeid.split("::")[-1] if "::" in nodeid else nodeid
        # Print progress with test name on same line
        print(f"\r  {self.completed_tests:3d}/{self.total_tests:3d} - {self.current_test:<50}", end="", flush=True)

    def pytest_runtest_logreport(self, report):
        """Called when a test result is reported."""
        if report.when != "call":
            return
            
        self.completed_tests += 1
        
        # Calculate progress percentage  
        percent = (self.completed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        # Clear and show progress percentage on same line
        print(f"\r{percent:7.1f}% done    ", end="", flush=True)


class ResponsiveTableReporter:
    """Responsive table reporter that adapts to terminal width."""

    def __init__(self, config):
        self.config = config
        self.tests = []
        self.start_time = None
        self.term_width = self._get_terminal_width()

    def _get_terminal_width(self):
        """Get current terminal width, with fallback."""
        try:
            return os.get_terminal_size().columns
        except (OSError, AttributeError):
            return 80

    def _truncate_name(self, name, max_width):
        """Truncate test name with ellipsis if too long."""
        if len(name) <= max_width:
            return name
        return name[: max_width - 3] + "..."

    def _get_status_symbol(self, report):
        """Get status symbol for test result."""
        if report.skipped:
            return "S"
        elif report.passed:
            return "✓"
        elif report.failed:
            return "✗"
        return "?"

    def _get_status_color(self, report):
        """Get color code for status."""
        if report.skipped:
            return "\033[93m"  # Yellow
        elif report.passed:
            return "\033[92m"  # Green
        elif report.failed:
            return "\033[91m"  # Red
        return "\033[0m"  # Reset

    def pytest_collection(self, session):
        """Called when test collection starts."""
        self.start_time = time.time()

    def pytest_runtest_logreport(self, report):
        """Collect test results."""
        if report.when == "call":
            self.tests.append(report)

    def pytest_sessionfinish(self):
        """Called when test session finishes - print the table."""
        if not self.tests or not self.config.getoption("--table-report", default=False):
            return

        # Recalculate terminal width
        self.term_width = self._get_terminal_width()
        max_opt = self.config.getoption("--max-name-width", default=60)
        
        max_name_width = min(max_opt, max(30, self.term_width - 25))

        # Collect statistics
        stats = {"passed": 0, "failed": 0, "skipped": 0}
        for test in self.tests:
            if test.skipped:
                stats["skipped"] += 1
            elif test.passed:
                stats["passed"] += 1
            elif test.failed:
                stats["failed"] += 1

        reset = self._reset_color()

        # Print table header
        print(f"\n{'='*self.term_width}")
        print(f"{'Status':<6} {'Test Name':<{max_name_width}} {'Duration':>10} {'Result':>10}")
        print(f"{'-'*self.term_width}")

        # Print each test result
        for test in self.tests:
            symbol = self._get_status_symbol(test)
            color = self._get_status_color(test)

            nodeid = test.nodeid
            if "::" in nodeid:
                display_name = nodeid.split("::")[-1]
            else:
                display_name = nodeid
            display_name = self._truncate_name(display_name, max_name_width)

            duration_ms = test.duration * 1000 if hasattr(test, "duration") else 0
            if duration_ms < 1000:
                duration_str = f"{duration_ms:.0f}ms"
            else:
                duration_str = f"{duration_ms / 1000:.2f}s"

            if test.skipped:
                result = "SKIPPED"
            elif test.failed:
                result = "FAILED"
            else:
                result = "PASSED"

            row = f"{color}{symbol:<6}{reset} {display_name:<{max_name_width}} {duration_str:>10} {result:>10}"
            print(row)

        # Print summary
        print(f"{'-'*self.term_width}")
        total = len(self.tests)
        elapsed = time.time() - self.start_time if self.start_time else 0

        summary = (
            f"Total: {total} | "
            f"Passed: {stats['passed']} | "
            f"Failed: {stats['failed']} | "
            f"Skipped: {stats['skipped']} | "
            f"Time: {elapsed:.2f}s"
        )
        print(f"{'='*self.term_width}")
        print(f"{summary}\n")

    def _reset_color(self):
        """Reset color codes."""
        return "\033[0m"


def pytest_report_teststatus(report, config):
    """Suppress default progress output when using table report."""
    if config.getoption("--table-report", default=False):
        # Return custom status to prevent default progress output
        if report.when == "call":
            return ("x", " ", "passed")  # Use space instead of dot
        # Suppress setup/teardown status
        return None


def pytest_configure(config):
    """Register custom markers and enable table reporter."""
    config.addinivalue_line("markers", "requires_pandoc: mark test as requiring pandoc")
    config.addinivalue_line("markers", "requires_display: mark test as requiring a display server")
    config.addinivalue_line("markers", "platform_windows: mark test as Windows-only")
    config.addinivalue_line("markers", "platform_macos: mark test as macOS-only")
    config.addinivalue_line("markers", "platform_linux: mark test as Linux-only")
    
    if config.getoption("--table-report", default=False):
        # Unregister the default terminal reporter to suppress its output
        tr = config.pluginmanager.get_plugin("terminalreporter")
        if tr:
            config.pluginmanager.unregister(tr)
        
        # Use minimal progress reporter for clean execution display
        config.pluginmanager.register(MinimalProgressReporter(config), "minimal_progress")
        # Register the table reporter for final output
        config.pluginmanager.register(ResponsiveTableReporter(config), "responsive_table")


# ─── Helper Functions ───────────────────────────────────────────────────────


def _is_binary_broken(binary_path) -> bool:
    """Check if the binary is broken (e.g., code signature issues on macOS).
    
    Returns True if the binary exists but cannot run due to internal errors.
    """
    if binary_path is None or not binary_path.exists():
        return False
    try:
        import subprocess
        env = {"QT_QPA_PLATFORM": "offscreen", "QTWEBENGINE_DISABLE_SANDBOX": "1"}
        result = subprocess.run(
            [str(binary_path), "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            env=env,
        )
        # Check for common broken binary error patterns
        stderr = result.stderr.lower()
        stdout = result.stdout.lower()
        combined = stderr + stdout
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


def _has_pandoc() -> bool:
    """Check if pandoc is available on the system."""
    return shutil.which("pandoc") is not None


def _pandoc_version() -> int:
    """Get the major version of pandoc, or 0 if not found."""
    if not _has_pandoc():
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


def _pandoc_path() -> str:
    """Get the path to pandoc, or empty string."""
    return shutil.which("pandoc") or ""


# ─── Pandoc Skip Marker ───────────────────────────────────────────────────────


def pytest_collection_modifyitems(config, items):
    """Skip pandoc-requiring tests if pandoc is not available."""
    for item in items:
        if "requires_pandoc" in item.keywords:
            if not _has_pandoc():
                item.add_marker(
                    pytest.mark.skip(reason="pandoc not found on this system")
                )
            else:
                item.add_marker(
                    pytest.mark.skipif(
                        _pandoc_version() < 2,
                        reason="Test requires pandoc >= 2",
                    )
                )
        # Platform-specific markers
        for plat in ("windows", "macos", "linux"):
            marker_name = f"platform_{plat}"
            if marker_name in item.keywords:
                current = platform.system().lower()
                if plat == "windows" and current != "windows":
                    item.add_marker(
                        pytest.mark.skip(reason=f"Windows-only test, running on {current}")
                    )
                elif plat == "macos" and current != "darwin":
                    item.add_marker(
                        pytest.mark.skip(reason=f"macOS-only test, running on {current}")
                    )
                elif plat == "linux" and current != "linux":
                    item.add_marker(
                        pytest.mark.skip(reason=f"Linux-only test, running on {current}")
                    )
