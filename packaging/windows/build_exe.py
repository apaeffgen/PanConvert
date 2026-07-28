#!/usr/bin/env python3
"""
Build Panconvert as a standalone executable with PyInstaller.

Usage:
    python packaging/windows/build_exe.py              # Normal build
    python packaging/windows/build_exe.py --clean      # Clean before building
    python packaging/windows/build_exe.py --debug      # Build with debug symbols (slower)
    python packaging/windows/build_exe.py --help       # Show help

PyCharm Integration:
    1. Go to Run > Edit Configurations
    2. Click + > Python
    3. Set:
       - Name: Build Standalone EXE
       - Script path: packaging/windows/build_exe.py
       - Working directory: $ProjectFileDir$
       - Python interpreter: .venv/Scripts/python.exe
    4. Apply & OK
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path


def color(text: str, code: int) -> str:
    """Simple ANSI color output (works in PyCharm terminal)."""
    return f"\033[{code}m{text}\033[0m"


def print_header(text: str):
    print(f"\n{color('===', 36)} {color(text, 37)} {color('===', 36)}")


def print_step(text: str):
    print(f"{color('[->]', 33)} {text}")


def print_ok(text: str):
    print(f"{color('[OK]', 32)} {text}")


def print_fail(text: str):
    print(f"{color('[FAIL]', 31)} {text}")


def check_pyinstaller():
    """Check if pyinstaller is installed, install if not."""
    try:
        import PyInstaller
        version = PyInstaller.__version__
        print_ok(f"PyInstaller {version} found")
        return True
    except ImportError:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Build Panconvert as a standalone executable.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Remove old build artifacts before building",
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Build with debug symbols (slower but easier to debug)",
    )
    parser.add_argument(
        "--spec", default="packaging/Panconvert_pyinstaller.spec",
        help="Path to the PyInstaller spec file (default: packaging/Panconvert_pyinstaller.spec)",
    )
    args = parser.parse_args()

    # ── Project root (parent of packaging/) ──
    # The script lives in packaging/windows/, so go up two levels
    packaging_dir = Path(__file__).parent.resolve()
    project_root = packaging_dir.parent.parent
    os.chdir(project_root)
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"

    # ── Check PyInstaller ──
    if not check_pyinstaller():
        print_step("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print_ok("PyInstaller installed")

    # ── Clean ──
    if args.clean:
        print_step("Cleaning old build artifacts...")
        for d in [dist_dir, build_dir]:
            if d.exists():
                shutil.rmtree(d)
                print_ok(f"Removed {d.name}/")
        print_ok("Clean complete")

    # ── Build command ──
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",          # Clean temporary files
        "--noconfirm",      # Overwrite without asking
        args.spec,          # Spec file as positional argument
    ]

    if args.debug:
        cmd.extend(["--debug", "all"])
        print_step("Debug build enabled")

    print_step(f"Building with spec: {args.spec}")
    print(f"  Output: {color(str(dist_dir), 37)}")
    print()

    # ── Run PyInstaller ──
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print_header("Build Complete!")
        exe_path = dist_dir / "Panconvert.exe"
        print_ok(f"Executable: {exe_path}")
        size = exe_path.stat().st_size / (1024 * 1024)
        print_ok(f"Size: ~{size:.0f} MB")
        print()
        print(color("To run:", 36))
        print(f"  Double-click: {dist_dir}/Panconvert.exe")
        print()
        print(color("To distribute:", 36))
        print("  Upload Panconvert.exe to your users.")
        print("  No Qt6/PyQt6 installation required!")
    else:
        print_fail("Build failed!")
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
