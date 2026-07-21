#!/bin/bash
# Build Panconvert with PyInstaller
# Run from project root directory

set -e

echo "=== Panconvert PyInstaller Build ==="
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

# Clean old build artifacts
echo "[→] Cleaning old build artifacts..."
rm -rf dist/ build/

# Build
echo "[→] Building Panconvert.app..."
pyinstaller --clean Panconvert.spec

echo ""
echo "=== Build Complete ==="
echo "Output: dist/Panconvert.app"
echo ""
echo "To launch:"
echo "    open dist/Panconvert.app"
echo ""
