#!/bin/bash
# Build Panconvert Linux standalone binary with PyInstaller
# Run from project root directory

set -e

echo "=== Panconvert Linux Build ==="
echo ""

# Detect platform
PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m | sed 's/x86_64/x86-64/; s/aarch64/arm64/')

# Detect Linux distribution
DISTRO=""
if [ -f /etc/os-release ]; then
    # Read the ID from /etc/os-release
    DISTRO_ID=$(. /etc/os-release && echo "$ID")
    
    # Map known distros to their base family
    case "$DISTRO_ID" in
        ubuntu|linuxmint|pop|zorin|elementary|neon|mx|kali|parrot|deepin|uos|kylin|manjaro|artix|endeavouros|garuda)
            DISTRO="debian"
            ;;
        fedora|centos|rhel|rocky|almalinux|ol|oracle|scientific|clear)
            DISTRO="fedora"
            ;;
        arch|archarm|manjaro|garuda|endeavouros|artix|antergos|blackarch|cachyos|parabola)
            DISTRO="arch"
            ;;
        opensuse|opensuse-leap|opensuse-tumbleweed|sles|sles_sap)
            DISTRO="opensuse"
            ;;
        alpine)
            DISTRO="alpine"
            ;;
        gentoo|funtoo)
            DISTRO="gentoo"
            ;;
        void)
            DISTRO="void"
            ;;
        nixos)
            DISTRO="nixos"
            ;;
        debian)
            DISTRO="debian"
            ;;
        *)
            # Fallback: use the detected ID as-is
            DISTRO="$DISTRO_ID"
            ;;
    esac
elif [ -f /etc/debian_version ]; then
    DISTRO="debian"
elif [ -f /etc/redhat-release ]; then
    DISTRO="rhel"
elif [ -f /etc/arch-release ]; then
    DISTRO="arch"
elif [ -f /etc/fedora-release ]; then
    DISTRO="fedora"
elif [ -f /etc/SuSE-release ]; then
    DISTRO="opensuse"
elif [ -f /etc/alpine-release ]; then
    DISTRO="alpine"
else
    DISTRO="unknown"
fi

PLATFORM_NAME="${PLATFORM}_${DISTRO}_${ARCH}"

# Activate virtual environment (use absolute path for reliability)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

if [ -f "${PROJECT_ROOT}/.venv/bin/activate" ]; then
    source "${PROJECT_ROOT}/.venv/bin/activate"
    echo "[✓] Virtual environment activated"
else
    echo "[✗] .venv not found at ${PROJECT_ROOT}/.venv"
    echo "    Create one with: python3 -m venv .venv"
    exit 1
fi

# Install pyinstaller if missing
if ! pip show pyinstaller &>/dev/null; then
    echo "[→] Installing pyinstaller..."
    pip install pyinstaller
fi

# Extract version from messages.py
VERSION=$(grep -oP "versionnumber = '\K[^']+" "${PROJECT_ROOT}/source/language/messages.py")
if [ -z "$VERSION" ]; then
    echo "[✗] Could not extract version from messages.py"
    exit 1
fi
echo "[→] Building version: $VERSION"
echo "[→] Platform: $PLATFORM_NAME"

# Clean old build artifacts
echo "[→] Cleaning old build artifacts..."
rm -rf dist/ build/

# Export version for the spec file
export PANVERSION="$VERSION"

# Build
echo "[→] Building Panconvert Linux binary..."
pyinstaller --clean --distpath="${PROJECT_ROOT}/dist" --workpath="${PROJECT_ROOT}/build" "${PROJECT_ROOT}/packaging/Panconvert_pyinstaller.spec"

# Rename the binary to include version, platform, and architecture
BINARY_NAME="Panconvert-${VERSION}-${PLATFORM_NAME}"
if [ -f "${PROJECT_ROOT}/dist/Panconvert" ]; then
    mv "${PROJECT_ROOT}/dist/Panconvert" "${PROJECT_ROOT}/dist/${BINARY_NAME}"
    chmod +x "${PROJECT_ROOT}/dist/${BINARY_NAME}"
    echo "[✓] Renamed to ${BINARY_NAME}"
else
    echo "[✗] Expected binary not found at ${PROJECT_ROOT}/dist/Panconvert"
    exit 1
fi

echo ""
echo "=== Build Complete ==="
echo "Output: dist/${BINARY_NAME}"
echo "Size:   $(du -h dist/${BINARY_NAME} | cut -f1)"
echo ""
echo "To launch:"
echo "    ./dist/${BINARY_NAME}"
echo ""
