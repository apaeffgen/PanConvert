#!/usr/bin/env python3
"""release_crossplatform.py - Publish files from the dist folder to a GitHub release.

Usage:
    python release_crossplatform.py [version]

Prerequisites:
    1. Set GH_TOKEN environment variable with a GitHub Personal Access Token
       (scope: repo, public_repo)
    2. Or run `gh auth login` first
    3. Ensure dist/ contains the built artifacts

Example:
    export GH_TOKEN=ghp_your_token_here
    python release_crossplatform.py 0.4.0

    # Or authenticate first:
    gh auth login
    python release_crossplatform.py 0.4.0
"""

import os
import re
import sys
import subprocess
import shutil
import argparse
from pathlib import Path
from typing import Optional


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


def check_auth() -> bool:
    """Check if gh CLI is authenticated."""
    if shutil.which("gh") is None:
        print("❌ GitHub CLI (gh) not found in PATH.")
        print("   Install it: https://cli.github.com/")
        print("   Or add it to your PATH and try again.")
        return False
    result = run(["gh", "auth", "status"])
    return result.returncode == 0


def get_project_root() -> Path:
    """Get the project root (parent of this script's parent)."""
    return Path(__file__).resolve().parent.parent


def extract_version_from_source(project_root: Path) -> Optional[str]:
    """Extract version from source/language/messages.py."""
    messages_py = project_root / "source" / "language" / "messages.py"
    if not messages_py.exists():
        return None
    content = messages_py.read_text(encoding="utf-8")
    match = re.search(r"versionnumber\s*=\s*'([^']+)'", content)
    return match.group(1) if match else None


def detect_platform() -> str:
    """Detect the current platform."""
    import platform
    system = platform.system().lower()

    if system == "darwin":
        return "macos"
    elif system == "linux":
        # Try to detect distro via package managers
        for cmd in ("dnf", "pacman", "apt-get"):
            if shutil.which(cmd):
                if cmd == "dnf":
                    return "rhel"
                elif cmd == "pacman":
                    return "arch"
                else:
                    return "debian"
        return "linux"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"


def classify_file(filepath: Path) -> str:
    """Classify a file by its name into a platform category."""
    name_lower = filepath.name.lower()

    debian_patterns = ["deb", "debian", "ubuntu"]
    rhel_patterns = ["rpm", "rhel", "centos", "fedora", "rocky"]
    arch_patterns = ["arch", "pacman"]
    macos_patterns = ["macos", "darwin", "dmg", "pkg"]
    windows_patterns = ["windows", "msi", "exe", "zip"]
    linux_patterns = ["linux", "x86_64", "bin"]

    for pattern in debian_patterns:
        if pattern in name_lower:
            return "debian"
    for pattern in rhel_patterns:
        if pattern in name_lower:
            return "rhel"
    for pattern in arch_patterns:
        if pattern in name_lower:
            return "arch"
    for pattern in macos_patterns:
        if pattern in name_lower:
            return "macos"
    for pattern in windows_patterns:
        if pattern in name_lower:
            return "windows"
    for pattern in linux_patterns:
        if pattern in name_lower:
            return "linux"
    return "unknown"


def file_size_human(filepath: Path) -> str:
    """Return human-readable file size."""
    size = filepath.stat().st_size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


# ── Main logic ────────────────────────────────────────────────────────────────

def main() -> int:
    project_root = get_project_root()
    os.chdir(project_root)

    parser = argparse.ArgumentParser(description="Publish dist/ artifacts to a GitHub release")
    parser.add_argument("version", nargs="?", help="Release version (e.g. 0.4.0)")
    args = parser.parse_args()

    # ── Detect platform ───────────────────────────────────────────────────────
    current_platform = detect_platform()
    print(f"🖥️  Detected platform: {current_platform}")

    # ── Check authentication ──────────────────────────────────────────────────
    if not check_auth():
        print("❌ Not authenticated with GitHub.")
        print()
        print("Option 1: Set GH_TOKEN environment variable:")
        print("  export GH_TOKEN=ghp_your_token_here")
        print()
        print("Option 2: Login interactively:")
        print("  gh auth login")
        print()
        print("Option 3: Login with token directly:")
        print("  gh auth login --with-token")
        return 1

    # ── Get version ───────────────────────────────────────────────────────────
    version = args.version
    if not version:
        version = extract_version_from_source(project_root)
        if not version:
            print("❌ Could not determine version. Pass it as an argument:")
            print("   python release_crossplatform.py 0.4.0")
            return 1

    # Remove 'v' prefix if present
    version = version.lstrip("v")

    print(f"📦 Publishing release: v{version}")

    # ── Check dist folder ─────────────────────────────────────────────────────
    dist_dir = project_root / "dist"
    if not dist_dir.exists():
        print("❌ dist/ folder not found. Build your release first.")
        return 1

    dist_files = [f for f in dist_dir.iterdir() if f.is_file()]
    if not dist_files:
        print("❌ dist/ folder is empty. Nothing to publish.")
        return 1

    # ── Classify files ────────────────────────────────────────────────────────
    platform_files: dict[str, list[Path]] = {
        "debian": [],
        "rhel": [],
        "arch": [],
        "macos": [],
        "windows": [],
        "linux": [],
        "unknown": [],
    }

    print()
    print("📁 Classifying artifacts in dist/:")
    for f in sorted(dist_files):
        plat = classify_file(f)
        platform_files[plat].append(f)
        size = file_size_human(f)
        print(f"  {'[' + plat + ']':-<12s} {f.name} ({size})")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("📋 Summary:")
    for plat in ("debian", "rhel", "arch", "macos", "windows", "linux", "unknown"):
        files = platform_files[plat]
        if files:
            marker = " ← current platform" if plat == current_platform else ""
            print(f"  {'✅' if plat == current_platform else 'ℹ️'} {plat} ({len(files)} file(s)){marker}")

    # ── Check for current platform files ──────────────────────────────────────
    has_current = any(platform_files[p] for p in ("debian", "rhel", "arch", "macos", "windows", "linux"))
    if not has_current:
        print()
        print("⚠️  No artifacts found for the current platform.")
        print("   Make sure to build the correct binary before publishing.")
        return 1

    print()
    print("🚀 Will upload all artifacts from dist/")

    # ── Create git tag ────────────────────────────────────────────────────────
    tag = f"v{version}"
    result = run(["git", "rev-parse", tag])
    if result.returncode == 0:
        print(f"✅ Tag {tag} already exists.")
    else:
        run(["git", "tag", "-a", tag, "-m", f"Release {tag}"])
        print(f"✅ Created git tag {tag}")

    # ── Push tag ──────────────────────────────────────────────────────────────
    print("📤 Pushing tag to GitHub...")
    gh_token = os.environ.get("GH_TOKEN")
    if gh_token:
        remote_url = f"https://x-access-token:{gh_token}@github.com/apaeffgen/Panconvert.git"
        run(["git", "remote", "set-url", "origin", remote_url])
    run(["git", "push", "origin", tag])
    print("✅ Tag pushed")

    # ── Check if release already exists ───────────────────────────────────────
    result = run(["gh", "release", "view", tag])
    if result.returncode == 0:
        print()
        print(f"⚠️  Release {tag} already exists.")
        print()
        print("Existing assets:")
        assets_result = run(["gh", "release", "view", tag, "--json", "name,assets"])
        if assets_result.returncode == 0:
            try:
                import json
                data = json.loads(assets_result.stdout)
                for asset in data.get("assets", []):
                    print(f"  {asset['name']}")
            except (json.JSONDecodeError, KeyError):
                pass
        print()
        reply = input("Re-upload the files from dist/? (y/N) ").strip().lower()
        if reply != "y":
            print("📋 Skipping upload. Release already exists.")
            print(f"   View at: https://github.com/apaeffgen/PanConvert/releases/tag/{tag}")
            return 0

    # ── Generate release notes ────────────────────────────────────────────────
    lines = [
        "## Changes",
        "- See [changelog](docs/Developer/changelog.md) for full details",
        "",
        "## Downloads",
        "",
        "| Platform | File |",
        "|----------|------|",
    ]
    for plat in ("debian", "rhel", "arch", "macos", "windows", "linux"):
        for f in platform_files[plat]:
            lines.append(f"| {plat} | {f.name} |")
    lines.extend([
        "",
        "## Installation",
        "See [ReadTheDocs](https://panconvert.readthedocs.io/en/latest/) for installation instructions.",
    ])
    release_notes = "\n".join(lines)

    # ── Create or update release ──────────────────────────────────────────────
    print()
    print("🚀 Creating GitHub release...")

    dist_glob = str(dist_dir / "*")
    result = run(["gh", "release", "view", tag])
    if result.returncode == 0:
        # Update existing release
        run(["gh", "release", "upload", tag, dist_glob, "--clobber"])
        print(f"✅ Release v{version} updated!")
    else:
        # Create new release
        run([
            "gh", "release", "create", tag,
            "--title", f"Panconvert {tag}",
            "--notes", release_notes,
            dist_glob,
        ])
        print(f"✅ Release v{version} published!")

    print(f"   View at: https://github.com/apaeffgen/PanConvert/releases/tag/{tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
