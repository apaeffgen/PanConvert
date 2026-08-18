#!/usr/bin/env python3
"""
Build script for Panconvert macOS application using PyInstaller.

Run from project root: python packaging/macos/build.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).resolve().parent.parent.parent


def run_command(cmd, cwd=None, check=True):
    """Run a shell command."""
    print(f"$ {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(
        cmd if isinstance(cmd, list) else cmd.split(),
        cwd=cwd,
        check=check,
        capture_output=False
    )
    return result


def check_prerequisites():
    """Check that required tools are available."""
    print("Checking prerequisites...")
    
    # Check Python
    if not shutil.which("python3"):
        print("[✗] python3 not found")
        sys.exit(1)
    
    # Check virtual environment
    project_root = get_project_root()
    venv_path = project_root / ".venv"
    
    if not venv_path.exists():
        print(f"[✗] Virtual environment not found at {venv_path}")
        print("    Create it with: python3 -m venv .venv")
        sys.exit(1)
    
    # Activate venv
    activate_script = venv_path / "bin" / "activate"
    os.environ.setdefault("VIRTUAL_ENV", str(venv_path))
    os.environ.setdefault("PATH", f"{venv_path / 'bin'}:{os.environ.get('PATH', '')}")
    
    print("[✓] Virtual environment ready")
    return venv_path


def install_dependencies():
    """Install PyInstaller and dependencies."""
    print("\nInstalling PyInstaller...")
    run_command([
        "pip", "install", "-q",
        "pyinstaller",
        "pyinstaller-hooks-contrib"
    ])
    
    # Verify PyQt6
    print("Verifying PyQt6...")
    result = subprocess.run(
        ["python3", "-c", "import PyQt6.QtWebEngineWidgets"],
        capture_output=True
    )
    if result.returncode != 0:
        print("[✗] PyQt6.QtWebEngineWidgets not found")
        print("    Install with: pip install PyQt6 PyQt6-WebEngine")
        sys.exit(1)
    
    print("[✓] Dependencies ready")


def clean_build_artifacts(project_root):
    """Remove old build artifacts."""
    print("\nCleaning old build artifacts...")
    
    dirs_to_clean = [
        project_root / "dist",
        project_root / "build",
    ]
    
    for d in dirs_to_clean:
        if d.exists():
            shutil.rmtree(d)
            print(f"    Removed {d}")
    
    # Also clean PyInstaller cache
    import platform
    if platform.system() == "Darwin":
        pyinstaller_cache = Path.home() / "Library" / "Application Support" / "pyinstaller"
        if pyinstaller_cache.exists():
            shutil.rmtree(pyinstaller_cache)
            print(f"    Removed {pyinstaller_cache}")
    
    print("[✓] Clean")


def code_sign_app(app_path):
    """Code sign the application."""
    print("\nCode signing application...")
    
    codesign_identity = os.environ.get("CODE_SIGN_IDENTITY", "-")
    
    if codesign_identity == "-":
        print("[!] Using ad-hoc signing (CODE_SIGN_IDENTITY not set)")
        print("    Note: rpath fixes are handled at runtime by pyinstaller_qtwebengine_fix.py")
    
    # Sign main executable
    exec_name = app_path.name.replace(".app", "")
    main_exec = app_path / "Contents" / "MacOS" / exec_name
    
    if main_exec.exists():
        print(f"    Signing {exec_name}...")
        run_command(["codesign", "--force", "--sign", codesign_identity, str(main_exec)])
    
    # Sign all dylibs in the bundle
    internal_dir = app_path / "Contents" / "Resources" / "_internal"
    if internal_dir.exists():
        print("    Signing dynamic libraries...")
        for lib in internal_dir.rglob("*.dylib"):
            run_command(["codesign", "--force", "--sign", codesign_identity, str(lib)], check=False)
    
    # Sign the frameworks
    frameworks_dir = app_path / "Contents" / "Resources" / "_internal" / "PyQt6" / "Qt6" / "lib"
    if frameworks_dir.exists():
        print("    Signing frameworks...")
        for fw in frameworks_dir.glob("*.framework"):
            if fw.is_dir():
                for lib in fw.rglob("*.dylib"):
                    run_command(["codesign", "--force", "--sign", codesign_identity, str(lib)], check=False)
    
    # Sign the app bundle
    print("    Signing app bundle...")
    run_command(["codesign", "--force", "--deep", "--sign", codesign_identity, str(app_path)])
    
    print("[✓] Code signing complete")


def build_app():
    """Run PyInstaller build."""
    project_root = get_project_root()
    spec_path = project_root / "packaging" / "macos" / "Panconvert.spec"
    
    if not spec_path.exists():
        print(f"[✗] Spec file not found: {spec_path}")
        sys.exit(1)
    
    print(f"\nBuilding with PyInstaller...")
    print(f"    Spec: {spec_path}")
    
    run_command(["pyinstaller", "--clean", str(spec_path)], cwd=project_root)
    
    app_path = project_root / "dist" / "Panconvert.app"
    if not app_path.exists():
        print("[✗] Build failed - Panconvert.app not found")
        sys.exit(1)
    
    return app_path


def main():
    """Main build function."""
    print("=" * 60)
    print("  Panconvert macOS Build")
    print("=" * 60)
    
    # Step 1: Check prerequisites
    venv_path = check_prerequisites()
    
    # Step 2: Install dependencies
    install_dependencies()
    
    # Step 3: Clean old artifacts
    project_root = get_project_root()
    clean_build_artifacts(project_root)
    
    # Step 4: Build with PyInstaller
    app_path = build_app()
    
    # Step 5: Code sign
    code_sign_app(app_path)
    
    # Summary
    print("\n" + "=" * 60)
    print("  Build Complete!")
    print("=" * 60)
    print(f"\nOutput: {app_path}")
    
    if app_path.exists():
        size = shutil.get_terminal_size((80, 24)).columns
        try:
            size_mb = sum(f.stat().st_size for f in app_path.rglob('*') if f.is_file()) // (1024 * 1024)
            print(f"Size: ~{size_mb} MB")
        except Exception:
            pass
    
    print(f"\nTo test:")
    print(f"    open {app_path}")
    print()


if __name__ == "__main__":
    main()
