#!/usr/bin/env python3
"""
Build Panconvert installer (Windows).

This script:
1. Builds the standalone exe with PyInstaller
2. Builds the Inno Setup installer
3. Outputs to dist/

Usage:
    python packaging/windows/build_installer.py

Prerequisites:
    - Python 3.10+
    - PyInstaller: pip install pyinstaller
    - Inno Setup 6.x (https://jrsoftware.org/isdl.php)
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path


def color(text: str, code: int) -> str:
    """Simple ANSI color output."""
    return f"\033[{code}m{text}\033[0m"


def print_header(text: str):
    print(f"\n{color('===', 36)} {color(text, 37)} {color('===', 36)}")


def print_step(text: str):
    print(f"{color('[->]', 33)} {text}")


def print_ok(text: str):
    print(f"{color('[OK]', 32)} {text}")


def print_fail(text: str):
    print(f"{color('[FAIL]', 31)} {text}")


def print_warn(text: str):
    print(f"{color('[WARN]', 35)} {text}")


def get_version():
    """Get version from source/language/messages.py"""
    project_root = Path(__file__).resolve().parent.parent.parent
    messages_path = project_root / "source" / "language" / "messages.py"
    
    version = "0.0.0"
    if messages_path.exists():
        content = messages_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.startswith("versionnumber = "):
                version = line.split('"')[1] if '"' in line else line.split("'")[1]
                break
    return version


def check_inno_setup():
    """Check if Inno Setup is installed."""
    iscc_paths = [
        r"C:\Program Files\Inno Setup 7\iscc.exe",
        r"C:\Program Files (x86)\Inno Setup 6\iscc.exe",
        r"C:\Program Files\Inno Setup 6\iscc.exe",
        "iscc",  # Check PATH
    ]
    
    for path in iscc_paths:
        if shutil.which(path):
            return path
    
    # Check registry
    try:
        import winreg
        for reg_path in [
            r"SOFTWARE\Inno Setup",
            r"SOFTWARE\WOW6432Node\Inno Setup",
        ]:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                val, _ = winreg.QueryValueEx(key, "Path")
                winreg.CloseKey(key)
                iscc = os.path.join(val, "iscc.exe")
                if os.path.exists(iscc):
                    return iscc
            except (FileNotFoundError, OSError):
                continue
    except ImportError:
        pass
    
    return None


def build_exe():
    """Build the standalone executable with PyInstaller."""
    project_root = Path(__file__).resolve().parent.parent.parent
    spec_path = project_root / "packaging" / "Panconvert_pyinstaller.spec"
    
    print_step("Building standalone executable...")
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm", str(spec_path)],
        cwd=project_root,
        capture_output=False,
    )
    
    if result.returncode != 0:
        print_fail("PyInstaller build failed!")
        sys.exit(1)
    
    print_ok("Executable built successfully")
    return True


def build_inno_setup(version: str):
    """Build the Inno Setup installer."""
    project_root = Path(__file__).resolve().parent.parent.parent
    iscc_path = check_inno_setup()
    
    if not iscc_path:
        print_warn("Inno Setup not found!")
        print()
        print(color("To install Inno Setup:", 36))
        print("  1. Download from: https://jrsoftware.org/isdl.php")
        print("  2. Run the installer")
        print("  3. Re-run this script")
        print()
        return False
    
    print_step(f"Inno Setup compiler: {iscc_path}")
    
    iss_path = project_root / "packaging" / "windows" / "Panconvert.iss"
    if not iss_path.exists():
        print_fail(f"Inno Setup script not found: {iss_path}")
        return False
    
    print_step("Building installer...")
    result = subprocess.run(
        [iscc_path, str(iss_path)],
        cwd=iss_path.parent,
        capture_output=True,
        text=True,
    )
    
    if result.returncode != 0:
        print_fail("Inno Setup build failed!")
        print(result.stdout)
        print(result.stderr)
        return False
    
    # Check output
    dist_dir = project_root / "dist"
    installer_pattern = f"Panconvert-{version}-win64-installer.exe"
    installer_path = dist_dir / installer_pattern
    
    if installer_path.exists():
        size = installer_path.stat().st_size / (1024 * 1024)
        print_ok(f"Installer created: {installer_path}")
        print_ok(f"Size: ~{size:.0f} MB")
        return True
    else:
        # List what was created
        print_warn("Installer may have been created with a different name:")
        for f in dist_dir.glob("Panconvert*"):
            print(f"  - {f.name}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Build Panconvert installer for Windows.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--exe-only", action="store_true",
        help="Only build the standalone executable (skip installer)",
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Clean build artifacts before building",
    )
    args = parser.parse_args()
    
    version = get_version()
    print_header(f"Panconvert Installer Builder v{version}")
    
    project_root = Path(__file__).resolve().parent.parent.parent
    dist_dir = project_root / "dist"
    
    # Clean if requested
    if args.clean:
        print_step("Cleaning old artifacts...")
        for d in [project_root / "build", dist_dir]:
            if d.exists():
                shutil.rmtree(d)
                print_ok(f"Removed {d.name}/")
    
    # Step 1: Build exe
    if not build_exe():
        print_fail("Build failed!")
        sys.exit(1)
    
    if args.exe_only:
        print_header("Executable build complete!")
        return 0
    
    # Step 2: Build installer
    print_header("Building Installer")
    if build_inno_setup(version):
        print_header("Build Complete!")
        print(color("Installer location:", 36))
        print(f"  {dist_dir}/Panconvert-{version}-win64-installer.exe")
        print()
        print(color("Next steps:", 36))
        print("  1. Test the installer on a clean Windows VM")
        print("  2. Sign the installer with a code signing certificate (optional)")
        print("  3. Distribute to users")
        return 0
    else:
        print_warn("Installer build skipped or failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
