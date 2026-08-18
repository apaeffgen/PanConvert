#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run tests with responsive table output that scales with window size.

Usage:
    python run_tests_table.py
    python run_tests_table.py --full      # Show full test names (no truncation)
    python run_tests_table.py --compact   # More compact output
"""

import sys
import os
import subprocess
import shutil


def get_terminal_width():
    """Get current terminal width."""
    try:
        return shutil.get_terminal_size().columns
    except (OSError, AttributeError):
        return 80


def build_pytest_command(full=False, compact=False):
    """Build pytest command with appropriate options."""
    cmd = [sys.executable, "-m", "pytest", "tests/", "--table-report"]
    
    term_width = get_terminal_width()
    
    if compact:
        max_width = min(40, term_width - 20)
    elif full:
        max_width = 100
    else:
        # Scale with terminal width
        max_width = min(60, term_width - 25)
    
    max_width = max(30, max_width)  # Minimum width
    
    cmd.extend([f"--max-name-width={max_width}", f"--min-width={term_width - 10}"])
    
    return cmd


def main():
    """Run tests with responsive table output."""
    # Get the project root directory (parent of tests/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Change to project root
    os.chdir(project_root)
    
    # Parse arguments
    full = "--full" in sys.argv
    compact = "--compact" in sys.argv
    
    cmd = build_pytest_command(full=full, compact=compact)
    
    # Run pytest
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
