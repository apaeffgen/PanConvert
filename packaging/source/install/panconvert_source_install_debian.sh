#!/bin/bash
# =============================================================================
# PanConvert - Source Installer for Debian/Ubuntu (x86_64)
# =============================================================================
# This script installs all dependencies (Qt6, Python, PyQt6, pandoc, etc.)
# and clones the PanConvert source code from GitHub.
#
# Usage: sudo bash panconvert_source_install_debian.sh
#
# Requirements: Root privileges (sudo) for system package installation
# Tested on: Ubuntu 20.04+, Debian 11+
# Architecture: x86_64 (amd64)
# =============================================================================

set -euo pipefail

# ── Color output helpers ─────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[✓]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[✗]${NC} $1"; }

# ── Check root privileges ────────────────────────────────────────────────────
if [[ $EUID -ne 0 ]]; then
    error "This script must be run as root (use sudo)"
    exit 1
fi

# ── Detect distribution ─────────────────────────────────────────────────────
if [[ -f /etc/os-release ]]; then
    DISTRO_ID=$(. /etc/os-release && echo "$ID")
    DISTRO_VERSION=$(. /etc/os-release && echo "$VERSION_ID")
else
    error "Cannot detect Linux distribution"
    exit 1
fi

info "Detected: ${DISTRO_ID} ${DISTRO_VERSION}"

# Check for Debian or Ubuntu
if [[ "$DISTRO_ID" != "debian" && "$DISTRO_ID" != "ubuntu" && "$DISTRO_ID" != "linuxmint" ]]; then
    warn "This script is designed for Debian/Ubuntu. You are running ${DISTRO_ID}."
    read -p "Continue anyway? [y/N]: " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        error "Aborted by user"
        exit 1
    fi
fi

# ── Configuration ────────────────────────────────────────────────────────────
GITHUB_REPO="https://github.com/apaeffgen/PanConvert.git"
INSTALL_DIR="/opt/panconvert"
VENV_DIR="${INSTALL_DIR}/.venv"
PYTHON_VERSION="python3"
PYTHON3_VERSION=""

# ── Pre-flight checks ───────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  PanConvert Source Installer for Debian/Ubuntu (x86_64)"
echo "============================================================"
echo ""
info "This script will:"
echo "  1. Install system dependencies (Qt6, Python, pandoc, etc.)"
echo "  2. Install Python dependencies (PyQt6, etc.)"
echo "  3. Clone PanConvert source from GitHub to ${INSTALL_DIR}"
echo "  4. Set up a Python virtual environment"
echo ""

read -p "Continue? [y/N]: " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    error "Aborted by user"
    exit 1
fi

# ── Step 1: Update package lists ────────────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 1: Updating package lists"
echo "────────────────────────────────────────────────────────────"
info "Running apt update..."
apt-get update -y
success "Package lists updated"

# ── Step 2: Install system dependencies ─────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 2: Installing system dependencies"
echo "────────────────────────────────────────────────────────────"

# Core build and Python dependencies
SYSTEM_PACKAGES=(
    # Python
    "python3"
    "python3-pip"
    "python3-venv"
    "python3-dev"

    # Qt6 framework
    "qt6-base-dev"
    "qt6-webengine-dev"
    "qt6-webengine-dev-tools"
    "libqt6core6t64"
    "libqt6gui6t64"
    "libqt6webenginecore6"
    "libqt6webenginewidgets6"
    "libqt6webengine6-data"

    # Qt6 dependencies (transitive but sometimes needed explicitly)
    "libxcb-xinerama0"
    "libxcb-xinerama0-dev"
    "libxcb1"
    "libxcb1-dev"
    "libxkbcommon-x11-0"
    "libxkbcommon0"
    "libfontconfig1"
    "libfreetype6"
    "libx11-6"
    "libxext6"
    "libxrender1"
    "libxcb1"
    "libxcb-glx0"
    "libxcb-icccm4"
    "libxcb-image0"
    "libxcb-keysyms1"
    "libxcb-randr0"
    "libxcb-render-util0"
    "libxcb-shape0"
    "libxcb-shm0"
    "libxcb-sync1"
    "libxcb-util1"
    "libxcb-xfixes0"
    "libxcb-cursor0"
    "libpango-1.0-0"
    "libharfbuzz0b"
    "libthai0"
    "libegl1"
    "libopengl0"
    "libgbm1"
    "libnss3"
    "libatk1.0-0"
    "libatk-bridge2.0-0"
    "libdrm2"
    "libxcomposite1"
    "libxdamage1"
    "libxrandr2"
    "libasound2t64"
    "libpulse0"
    "libxshmfence1"

    # Pandoc (document converter)
    "pandoc"

    # Git (for cloning source)
    "git"

    # Build tools (for compiling Python packages)
    "build-essential"
    "pkg-config"
    "qtbase5-dev"  # Some PyQt6 components may need Qt5 dev headers

    # SSL and crypto libraries (needed by PyQt6)
    "libssl-dev"

    # Additional Qt6 modules that may be required
    "qt6-translations-l10n"
)

# Install all system packages
info "Installing system packages..."
apt-get install -y "${SYSTEM_PACKAGES[@]}"
success "System dependencies installed"

# ── Step 3: Verify Python version ────────────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 3: Verifying Python installation"
echo "────────────────────────────────────────────────────────────"

if ! command -v python3 &>/dev/null; then
    error "python3 not found. Please install it manually."
    exit 1
fi

PYTHON3_VERSION=$(python3 --version | awk '{print $2}')
info "Python version: ${PYTHON3_VERSION}"

# Check Python version >= 3.8
MAJOR=$(echo "$PYTHON3_VERSION" | cut -d. -f1)
MINOR=$(echo "$PYTHON3_VERSION" | cut -d. -f2)
if [[ "$MAJOR" -lt 3 ]] || { [[ "$MAJOR" -eq 3 ]] && [[ "$MINOR" -lt 8 ]]; }; then
    error "Python 3.8 or higher is required. Found: ${PYTHON3_VERSION}"
    exit 1
fi

success "Python version check passed"

# ── Step 4: Create installation directory ────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 4: Setting up installation directory"
echo "────────────────────────────────────────────────────────────"

if [[ -d "$INSTALL_DIR" ]]; then
    warn "${INSTALL_DIR} already exists"
    read -p "Remove existing installation and reinstall? [y/N]: " confirm
    if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
        rm -rf "${INSTALL_DIR}"
        success "Removed existing installation"
    else
        info "Keeping existing installation"
    fi
fi

mkdir -p "${INSTALL_DIR}"
success "Installation directory created: ${INSTALL_DIR}"

# ── Step 5: Clone source code from GitHub ────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 5: Cloning PanConvert source from GitHub"
echo "────────────────────────────────────────────────────────────"

if [[ -d "${INSTALL_DIR}/.git" ]]; then
    info "Repository already cloned, pulling latest changes..."
    cd "${INSTALL_DIR}"
    git pull
    success "Source code updated"
else
    info "Cloning from ${GITHUB_REPO}..."
    git clone "${GITHUB_REPO}" "${INSTALL_DIR}"
    success "Source code cloned to ${INSTALL_DIR}"
fi

# ── Step 6: Create Python virtual environment ────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 6: Creating Python virtual environment"
echo "────────────────────────────────────────────────────────────"

if [[ -d "$VENV_DIR" ]]; then
    info "Virtual environment already exists at ${VENV_DIR}"
else
    info "Creating virtual environment..."
    python3 -m venv "${VENV_DIR}"
    success "Virtual environment created"
fi

# Activate virtual environment
source "${VENV_DIR}/bin/activate"
info "Virtual environment activated"

# Upgrade pip
info "Upgrading pip..."
pip install --upgrade pip setuptools wheel
success "pip upgraded"

# ── Step 7: Install Python dependencies ─────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 7: Installing Python dependencies"
echo "────────────────────────────────────────────────────────────"

# Install requirements from requirements.txt
if [[ -f "${INSTALL_DIR}/requirements.txt" ]]; then
    info "Installing packages from requirements.txt..."
    pip install -r "${INSTALL_DIR}/requirements.txt"
    success "Python dependencies installed"
else
    error "requirements.txt not found in ${INSTALL_DIR}"
    exit 1
fi

# ── Step 8: Verify installations ────────────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 8: Verifying installation"
echo "────────────────────────────────────────────────────────────"

# Check PyQt6
if python3 -c "import PyQt6" 2>/dev/null; then
    PYQT_VERSION=$(python3 -c "import PyQt6; print(PyQt6.__version__)" 2>/dev/null || echo "unknown")
    success "PyQt6 installed (version: ${PYQT_VERSION})"
else
    error "PyQt6 installation failed"
    exit 1
fi

# Check pandoc
if command -v pandoc &>/dev/null; then
    PANDOC_VERSION=$(pandoc --version | head -1)
    success "Pandoc installed: ${PANDOC_VERSION}"
else
    error "Pandoc not found. Please install it manually."
    exit 1
fi

# Check Qt6
if qmake6 --version 2>/dev/null || qmake-qt6 --version 2>/dev/null; then
    success "Qt6 development tools found"
else
    warn "Qt6 qmake not found. PyQt6 may still work, but Qt6 dev tools are recommended."
fi

# ── Step 9: Set permissions ─────────────────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 9: Setting permissions"
echo "────────────────────────────────────────────────────────────"

# Make the main script executable
chmod +x "${INSTALL_DIR}/Panconvert.py"
success "Made Panconvert.py executable"

# ── Step 10: Create desktop entry (optional) ─────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 10: Creating desktop entry"
echo "────────────────────────────────────────────────────────────"

DESKTOP_FILE="/usr/share/applications/panconvert.desktop"

if [[ -f "$DESKTOP_FILE" ]]; then
    warn "Desktop entry already exists at ${DESKTOP_FILE}"
else
    info "Creating desktop entry..."
    cat > "$DESKTOP_FILE" << 'EOF'
[Desktop Entry]
Name=PanConvert
Comment=Pandoc GUI Converter
Exec=/opt/panconvert/.venv/bin/python3 /opt/panconvert/Panconvert.py
Icon=utilities-file-archiver
Terminal=false
Type=Application
Categories=Utility;TextEditor;
StartupNotify=false
EOF
    success "Desktop entry created at ${DESKTOP_FILE}"
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  Installation Complete!"
echo "============================================================"
echo ""
info "PanConvert has been installed to: ${INSTALL_DIR}"
echo ""
echo "To run PanConvert:"
echo "  Option 1 (from terminal):"
echo "    cd ${INSTALL_DIR}"
echo "    source .venv/bin/activate"
echo "    python3 Panconvert.py"
echo ""
echo "  Option 2 (from desktop menu):"
echo "    Search for 'PanConvert' in your application launcher"
echo ""
echo "To update to the latest version:"
echo "    cd ${INSTALL_DIR}"
echo "    git pull"
echo ""
echo "To deactivate the virtual environment:"
echo "    deactivate"
echo ""
echo "============================================================"
