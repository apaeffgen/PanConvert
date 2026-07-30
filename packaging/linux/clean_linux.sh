#!/bin/bash
# Clean all Linux build artifacts
# Run from project root directory

set -e

echo "=== Panconvert Linux Clean ==="
echo ""

# Clean PyInstaller artifacts
echo "[→] Cleaning build artifacts..."
rm -rf dist/ build/

# Clean PyInstaller cache
if [ -f ".pyinstaller" ]; then
    rm -rf .pyinstaller/
    echo "[✓] Removed .pyinstaller cache"
fi

# Clean pycache
echo "[→] Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Clean Python bytecode
echo "[→] Removing .pyc files..."
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Clean egg-info
echo "[→] Cleaning *.egg-info directories..."
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

echo ""
echo "=== Clean Complete ==="
echo "Removed: dist/, build/, .pyinstaller/, __pycache__/, *.pyc, *.egg-info"
echo ""
