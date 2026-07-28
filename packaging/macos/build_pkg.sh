#!/bin/bash
# Build a macOS PKG installer for Panconvert.
# Usage: bash build_pkg.sh
# Output: dist/Panconvert-<version>-macos.pkg
#
# Prerequisites:
#   pip install macOS-Pkg-Builder
#   Run build.sh first so dist/Panconvert.app exists

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DIST_DIR="$PROJECT_DIR/dist"
PKG_VERSION="0.3.1"
OUTPUT_PKG="$DIST_DIR/Panconvert-${PKG_VERSION}-macos.pkg"

# Source .app built by PyInstaller
SOURCE_APP="$DIST_DIR/Panconvert.app"

# ── Pre-flight checks ──
if [ ! -d "$SOURCE_APP" ]; then
    echo "[✗] Source app not found: $SOURCE_APP"
    echo "    Run 'bash build.sh' first to produce dist/Panconvert.app."
    exit 1
fi

mkdir -p "$DIST_DIR"

# ── Activate virtual environment ──
if [ -f "$PROJECT_DIR/.venv/bin/activate" ]; then
    source "$PROJECT_DIR/.venv/bin/activate"
    echo "[✓] Virtual environment activated"
else
    echo "[✗] .venv not found."
    exit 1
fi

# Install macOS-Pkg-Builder if missing
if ! pip show macos-pkg-builder &>/dev/null; then
    echo "[→] Installing macOS-Pkg-Builder..."
    pip install macOS-Pkg-Builder
fi

# ── Build the PKG ──
echo "[→] Building $OUTPUT_PKG..."

python3 -c "
from pathlib import Path
from macos_pkg_builder import Packages

pkg = Packages(
    pkg_output='$OUTPUT_PKG',
    pkg_bundle_id='com.panconvert.installer',
    pkg_version='$PKG_VERSION',
    pkg_file_structure={
        '$SOURCE_APP': '/Applications/Panconvert.app',
    },
)
ok = pkg.build()
if not ok:
    exit(1)
"

SIZE_MB=$(du -mh "$OUTPUT_PKG" | cut -f1)
echo ""
echo "[✓] Created: $OUTPUT_PKG ($SIZE_MB)"
echo ""
echo "To install:"
echo "    sudo installer -pkg $OUTPUT_PKG -target /"
