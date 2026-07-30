#!/bin/bash
# Build Panconvert Linux standalone binary with PyInstaller
# Run from project root directory

set -e

echo "=== Panconvert Linux Build ==="
echo ""

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "[✓] Virtual environment activated"
else
    echo "[✗] .venv not found. Please create one first:"
    echo "    python3 -m venv .venv"
    echo "    source .venv/bin/activate"
    echo "    pip install -r requirements.txt"
    exit 1
fi

# Install pyinstaller if missing
if ! pip show pyinstaller &>/dev/null; then
    echo "[→] Installing pyinstaller..."
    pip install pyinstaller
fi

# Build paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGING_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Extract version from messages.py
VERSION=$(grep -oP "versionnumber = '\K[^']+" "${PACKAGING_DIR}/source/language/messages.py")
if [ -z "$VERSION" ]; then
    echo "[✗] Could not extract version from messages.py"
    exit 1
fi
echo "[→] Building version: $VERSION"

# Clean old build artifacts
echo "[→] Cleaning old build artifacts..."
rm -rf dist/ build/

# Export version for the spec file
export PANVERSION="$VERSION"

# Build
echo "[→] Building Panconvert Linux binary..."
pyinstaller --clean --distpath="${PACKAGING_DIR}/dist" --workpath="${PACKAGING_DIR}/build" "${SCRIPT_DIR}/Panconvert.spec"

echo ""
echo "=== Build Complete ==="
echo "Output: dist/Panconvert-${VERSION}-linux_x86-64"
echo "Size:   $(du -h dist/Panconvert-${VERSION}-linux_x86-64 | cut -f1)"
echo ""
echo "To launch:"
echo "    ./dist/Panconvert-${VERSION}-linux_x86-64"
echo ""