#!/usr/bin/env python3
"""
Build Panconvert installer (Windows).

This script:
1. Downloads the bundled pandoc binary (if not already present)
2. Updates the PyInstaller spec to include pandoc
3. Builds the standalone exe with PyInstaller
4. Builds the Inno Setup installer
5. Outputs to dist/

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
import urllib.request
import hashlib
from pathlib import Path


# Pandoc binary configuration
PANDOC_VERSION = "3.10.1"
PANDOC_FILENAME = f"pandoc-{PANDOC_VERSION}-win64.exe"
PANDOC_URL = f"https://github.com/jgm/pandoc/releases/download/{PANDOC_VERSION}/{PANDOC_FILENAME}"
# Expected size for integrity check (approximate, for informational purposes)
PANDOC_EXPECTED_SIZE = 75_000_000  # ~75 MB


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


def download_pandoc(target_dir: Path) -> Path:
    """
    Download the pandoc Windows binary if not already present.
    Returns the path to the pandoc executable.
    """
    # Check if pandoc is already downloaded
    pandoc_exe = target_dir / "pandoc.exe"
    if pandoc_exe.exists():
        size_mb = pandoc_exe.stat().st_size / (1024 * 1024)
        print_ok(f"Using existing pandoc binary: {pandoc_exe} ({size_mb:.1f} MB)")
        return pandoc_exe
    
    # Create temp directory for download
    temp_dir = target_dir / "pandoc_download"
    temp_dir.mkdir(exist_ok=True)
    
    temp_exe = temp_dir / PANDOC_FILENAME
    print_step(f"Downloading pandoc v{PANDOC_VERSION}...")
    print_step(f"URL: {PANDOC_URL}")
    
    try:
        urllib.request.urlretrieve(PANDOC_URL, str(temp_exe))
        
        # Verify file size (should be ~75 MB)
        size_mb = temp_exe.stat().st_size / (1024 * 1024)
        if size_mb < 10:  # Sanity check - something went wrong if too small
            print_warn(f"Downloaded file seems too small ({size_mb:.1f} MB). Removing.")
            temp_exe.unlink()
            raise RuntimeError("Downloaded pandoc binary is too small")
        
        print_ok(f"Download complete ({size_mb:.1f} MB)")
        
        # Rename to pandoc.exe for easier reference
        shutil.move(str(temp_exe), str(pandoc_exe))
        
        # Clean up temp directory
        shutil.rmtree(temp_dir)
        
        print_ok(f"Pandoc binary ready: {pandoc_exe}")
        return pandoc_exe
        
    except Exception as e:
        print_fail(f"Failed to download pandoc: {e}")
        # Clean up on failure
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        if pandoc_exe.exists():
            pandoc_exe.unlink()
        raise


def update_pyinstaller_spec(pandoc_exe: Path):
    """Update the PyInstaller spec to include the pandoc binary."""
    project_root = Path(__file__).resolve().parent.parent.parent
    spec_path = project_root / "packaging" / "Panconvert_pyinstaller.spec"
    
    print_step("Updating PyInstaller spec to include pandoc...")
    
    # Read the current spec
    spec_content = spec_path.read_text(encoding="utf-8")
    
    # Add pandoc to the datas list (for data files)
    # We need to add it to the datas list in the spec file
    pandoc_rel = str(pandoc_exe.relative_to(project_root))
    
    # Find the datas = [] line and add our binary
    if "pandoc" not in spec_content:
        # Add pandoc to the datas collection
        # Insert after the existing datas collection loop
        old_block = """# ── Collect all data files from the source package ──
datas = []
for root, dirs, files in os.walk(os.path.join(project_root, 'source')):
    for f in files:
        src = os.path.join(root, f)
        dst = os.path.relpath(root, project_root)
        datas.append((src, dst))"""
        
        new_block = f"""# ── Collect all data files from the source package ──
datas = []
for root, dirs, files in os.walk(os.path.join(project_root, 'source')):
    for f in files:
        src = os.path.join(root, f)
        dst = os.path.relpath(root, project_root)
        datas.append((src, dst))

# ── Include bundled pandoc binary ──
pandoc_src = os.path.join(project_root, 'packaging', 'windows', 'pandoc.exe')
if os.path.exists(pandoc_src):
    datas.append((pandoc_src, 'pandoc'))"""
        
        spec_content = spec_content.replace(old_block, new_block)
        spec_path.write_text(spec_content, encoding="utf-8")
        print_ok("PyInstaller spec updated with pandoc binary")
    else:
        print_ok("PyInstaller spec already contains pandoc")


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


def build_exe(pandoc_exe: Path):
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


def build_inno_setup(version: str, pandoc_exe: Path):
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
    
    # Update ISS file to include pandoc
    iss_content = iss_path.read_text(encoding="utf-8")
    
    # Add pandoc to the [Files] section if not already present
    if "pandoc.exe" not in iss_content:
        # Add pandoc file entry
        files_section = "[Files]"
        pandoc_entry = f'; Include bundled pandoc binary\nSource: "pandoc.exe"; DestDir: "{{app}}"; Flags: ignoreversion\n'
        new_files_section = files_section + "\n" + pandoc_entry
        iss_content = iss_content.replace(files_section, new_files_section, 1)
        iss_path.write_text(iss_content, encoding="utf-8")
        print_ok("Inno Setup script updated with pandoc binary")
    
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
    parser.add_argument(
        "--skip-pandoc", action="store_true",
        help="Skip downloading pandoc (use existing binary)",
    )
    args = parser.parse_args()
    
    version = get_version()
    print_header(f"Panconvert Installer Builder v{version}")
    
    project_root = Path(__file__).resolve().parent.parent.parent
    dist_dir = project_root / "dist"
    pandoc_dir = project_root / "packaging" / "windows"
    
    # Step 0: Download pandoc binary
    if not args.skip_pandoc:
        print_header("Preparing Pandoc Binary")
        try:
            pandoc_exe = download_pandoc(pandoc_dir)
        except Exception as e:
            print_fail(f"Failed to prepare pandoc: {e}")
            print()
            print(color("You can:", 36))
            print("  1. Download pandoc manually from: https://pandoc.org/installing.html")
            print("  2. Place it at: packaging/windows/pandoc.exe")
            print("  3. Re-run with --skip-pandoc flag")
            return 1
    else:
        pandoc_exe = pandoc_dir / "pandoc.exe"
        if not pandoc_exe.exists():
            print_fail("pandoc.exe not found in packaging/windows/. Use --skip-pandoc to continue anyway.")
            return 1
        print_ok(f"Using existing pandoc: {pandoc_exe}")
    
    # Clean if requested
    if args.clean:
        print_step("Cleaning old artifacts...")
        for d in [project_root / "build", dist_dir]:
            if d.exists():
                shutil.rmtree(d)
                print_ok(f"Removed {d.name}/")
    
    # Step 1: Update PyInstaller spec
    print_header("Updating Build Configuration")
    update_pyinstaller_spec(pandoc_exe)
    
    # Step 2: Build exe
    print_header("Building Executable")
    if not build_exe(pandoc_exe):
        print_fail("Build failed!")
        sys.exit(1)
    
    if args.exe_only:
        print_header("Executable build complete!")
        return 0
    
    # Step 3: Build installer
    print_header("Building Installer")
    if build_inno_setup(version, pandoc_exe):
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
