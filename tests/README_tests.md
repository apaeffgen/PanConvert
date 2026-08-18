# PanConvert Test Suite

This directory contains the comprehensive test suite for PanConvert, covering unit tests, integration tests, GUI tests, and packaging verification.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Test Organization](#test-organization)
- [Running Tests](#running-tests)
- [Custom Markers](#custom-markers)
- [Output Formats](#output-formats)
- [Troubleshooting](#troubleshooting)

---

## Overview

The test suite verifies:
- **Conversion functionality** - Pandoc and MultiMarkdown conversion paths
- **Settings persistence** - QSettings save/load behavior
- **Packaged binaries** - Binary execution and help/version output
- **Installers** - Platform-specific installer packages
- **GUI** - Main window functionality (requires display)

---

## Prerequisites

### Required
- Python 3.12+
- pytest (`pip install pytest`)
- PyQt6 (`pip install pytest-qt` for GUI tests)

### Optional (tests will skip if missing)
- **Pandoc** - Required for integration tests (`requires_pandoc` marker)
- **Display server** - Required for GUI tests (Linux/X11 or macOS)

### Check Dependencies
```bash
# Check pandoc
pandoc --version

# Check pytest
pytest --version

# Check PyQt6
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 OK')"
```

---

## Quick Start

### Run All Tests (Standard)
```bash
# Using the test runner script (table output)
./tests/run_tests.sh

# Or directly with pytest (same as script default)
pytest tests/ --table-report -q --tb=no
```

### Run With Table Output
```bash
# Responsive table that adapts to terminal width
python tests/run_tests_table.py

# Compact table (narrower columns)
python tests/run_tests_table.py --compact

# Full table (no truncation)
python tests/run_tests_table.py --full
```

### Run Specific Test Categories

```bash
# Conversion tests only
pytest tests/general/test_conversions.py -v

# Settings tests only
pytest tests/general/test_settings.py -v

# Binary/packaging tests
pytest tests/packaging/ -v

# Installer tests
pytest tests/platform_tests/ -v

# GUI tests (requires display)
pytest tests/gui/ -v
```

---

## Test Organization

```
tests/
├── converter/           # Converter path tests
│   ├── test_pandoc_formats.py    # Pandoc format conversion
│   ├── test_path_multimarkdown.py # MultiMarkdown path tests
│   └── test_path_pandoc.py       # Pandoc path tests
│
├── general/             # General integration tests
│   ├── test_conversions.py        # Basic conversion functionality
│   ├── test_pandoc_integration.py # Pandoc integration
│   ├── test_pandoc_version.py     # Pandoc version detection
│   └── test_settings.py           # Settings persistence
│
├── packaging/           # Packaged binary tests
│   ├── test_binary_basics.py      # Binary existence/version/help
│   └── test_binary_dependencies.py # Binary dependencies
│
├── platform_tests/      # Platform-specific tests
│   └── test_installers.py         # Installer packages
│
├── gui/                 # GUI tests (requires display)
│   └── test_main_window.py        # Main window functionality
│
├── conftest.py          # Shared fixtures and configuration
├── pytest.ini           # pytest configuration
├── run_tests.sh         # Bash test runner
└── run_tests_table.py   # Table output test runner
```

---

## Running Tests

### Standard pytest Commands

```bash
# Run all tests with table output (default)
pytest tests/ --table-report -q --tb=no

# Run all tests with verbose output
pytest tests/ -v

# Run all tests with colored output and short tracebacks
pytest tests/ --tb=short

# Run only tests matching a pattern
pytest tests/ -v -k "pandoc"

# Run specific test file
pytest tests/general/test_settings.py -v

# Run specific test function
pytest tests/general/test_settings.py::TestSettings::test_save_load -v

# Run specific test class
pytest tests/platform_tests/test_installers.py::TestWindowsInstaller -v

# Generate HTML report
pytest tests/ --html=report.html

# Run with coverage
pytest tests/ --cov=panconvert --cov-report=html
```

### Using the Shell Script

```bash
# Run all tests (table output)
./tests/run_tests.sh

# Run only binary/platform tests
./tests/run_tests.sh -p

# Run only GUI tests
./tests/run_tests.sh -g

# Run only conversion tests
./tests/run_tests.sh -c

# Run only settings tests
./tests/run_tests.sh -s

# Pass extra args to pytest
./tests/run_tests.sh -- -v --tb=long
```

### Using the Table Output Runner

```bash
# Default: responsive table
python tests/run_tests_table.py

# Compact output (narrower columns)
python tests/run_tests_table.py --compact

# Full output (no name truncation)
python tests/run_tests_table.py --full

# Extra options
python tests/run_tests_table.py --compact -- -k "pandoc"
```

---

## Custom Markers

Tests use custom markers to control execution based on environment:

### Markers

| Marker | Description | Behavior |
|--------|-------------|----------|
| `requires_pandoc` | Test needs pandoc binary | Skipped if pandoc not found or < v2 |
| `requires_display` | Test needs GUI display | Skipped if no display (Linux) |
| `platform_windows` | Windows-only test | Skipped on non-Windows |
| `platform_macos` | macOS-only test | Skipped on non-macOS |
| `platform_linux` | Linux-only test | Skipped on non-Linux |

### Examples

```python
@pytest.mark.requires_pandoc
def test_pandoc_conversion():
    # Only runs if pandoc is available
    ...

@pytest.mark.platform_macos
def test_macos_installer():
    # Only runs on macOS
    ...

@pytest.mark.requires_display
def test_gui_functionality():
    # Only runs with display available
    ...
```

### Running with Markers

```bash
# Run only pandoc-requiring tests
pytest tests/ -v -m requires_pandoc

# Run only platform-specific tests
pytest tests/ -v -m "platform_macos or platform_windows"

# Exclude certain markers
pytest tests/ -v -m "not requires_display"

# Combine with -k
pytest tests/ -v -m requires_pandoc -k "format"
```

---

## Output Formats

### Default pytest Output
```python
pytest tests/ --table-report -q --tb=no

# Output: Progress bar with percentage
# 100% done
#
# Then table at end:
# Status  Test Name                                              Duration     Result
# S       test_binary_version                                    8ms          SKIPPED
# ✓       test_binary_help                                       12ms         PASSED
```

### Verbose Output (Alternative)
```bash
pytest tests/ -v
tests/general/test_settings.py::TestSettings::test_save_load PASSED  [ 50%]
tests/general/test_settings.py::TestSettings::test_batch_settings PASSED [100%]

========================= 2 passed in 0.05s =========================
```

### Table Output (`--table-report`)
```
================================================================================
 Status  Test Name                                              Duration     Result
--------------------------------------------------------------------------------
 ✓       test_save_load                                        12ms        PASSED
 ✓       test_batch_settings                                   8ms         PASSED
--------------------------------------------------------------------------------
Total: 2 | Passed: 2 | Failed: 0 | Skipped: 0 | Time: 0.05s
================================================================================
```

### Table Output Options

| Option | Default | Description |
|--------|---------|-------------|
| `--table-report` | True in run_tests.sh | Enable table output |
| `-q` | True in run_tests.sh | Quiet mode (minimal output) |
| `--tb=no` | True in run_tests.sh | No traceback output |
| `--max-name-width=N` | 60 | Max width for test names |
| `--min-width=N` | 40 | Min terminal width before truncating |

---

## Troubleshooting

### Tests Failing with "No module named pytest"
```bash
pip install pytest pytest-qt
```

### GUI Tests Failing with "Cannot open display"
```bash
# On Linux, install and run Xvfb
sudo apt install xvfb
Xvfb :99 &
export DISPLAY=:99
pytest tests/gui/ -v

# Or skip GUI tests
pytest tests/ -v -m "not requires_display"
```

### Pandoc Tests Being Skipped
```bash
# Install pandoc
# macOS: brew install pandoc
# Ubuntu: sudo apt install pandoc
# Windows: choco install pandoc

# Verify installation
pandoc --version
```

### Virtual Environment Issues
```bash
# Activate the project venv
source .venv/bin/activate

# Or use the run_tests.sh script which handles this automatically
./tests/run_tests.sh
```

### Permission Denied on Scripts
```bash
chmod +x tests/run_tests.sh
chmod +x tests/run_tests_table.py
```

---

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run Tests
  run: |
    python -m pytest tests/ -v -m "not requires_display"
```

### With Pandoc
```yaml
- name: Install Pandoc
  run: |
    # macOS
    brew install pandoc
    # Ubuntu
    sudo apt install pandoc

- name: Run Tests
  run: |
    python -m pytest tests/ -v
```

---

## Contact

For issues or questions about the test suite, please open an issue in the project repository.
