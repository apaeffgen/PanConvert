#!/bin/bash
# =============================================================================
# PanConvert - Source Installer for macOS (x86_64/Apple Silicon)
# =============================================================================
# This script installs all dependencies (Qt6, Python, PyQt6, pandoc, etc.)
# and clones the PanConvert source code from GitHub.
#
# Usage: bash panconvert_source_install_macos.sh
#
# Requirements: Xcode Command Line Tools (or internet connection to install)
# Tested on: macOS 12 (Monterey)+
# Architecture: x86_64 (Intel) / arm64 (Apple Silicon)
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

# ── Detect architecture ─────────────────────────────────────────────────────
ARCH=$(uname -m)
if [[ "$ARCH" == "x86_64" ]]; then
    ARCH_TYPE="x86_64 (Intel)"
elif [[ "$ARCH" == "arm64" ]]; then
    ARCH_TYPE="arm64 (Apple Silicon)"
else
    ARCH_TYPE="$ARCH"
fi

info "Detected architecture: ${ARCH_TYPE}"

# ── Install Homebrew if not present ─────────────────────────────────────────
if ! command -v brew &>/dev/null; then
    warn "Homebrew is not installed. Installing it now..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add Homebrew to PATH
    if [[ "$(uname -m)" == "arm64" ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    else
        eval "$(/usr/local/bin/brew shellenv)"
    fi
    success "Homebrew installed and configured"
else
    success "Homebrew found: $(brew --version | head -1)"
fi

# ── Check Xcode Command Line Tools ──────────────────────────────────────────
if ! xcode-select -p &>/dev/null; then
    warn "Xcode Command Line Tools not detected. Installing..."
    xcode-select --install
    success "Xcode Command Line Tools installed"
fi

# ── Configuration ────────────────────────────────────────────────────────────
GITHUB_REPO="https://github.com/apaeffgen/Panconvert.git"
INSTALL_DIR="${HOME}/Panconvert"
VENV_DIR="${INSTALL_DIR}/.venv"
PYTHON_VERSION="python3"

# ── Pre-flight checks ───────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  PanConvert Source Installer for macOS"
echo "============================================================"
echo ""
info "This script will:"
echo "  1. Install system dependencies (Qt6, Python, pandoc, etc.) via Homebrew"
echo "  2. Install Python dependencies (PyQt6, etc.)"
echo "  3. Clone PanConvert source from GitHub to ${INSTALL_DIR}"
echo "  4. Set up a Python virtual environment"
echo ""

read -p "Continue? [y/N]: " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    error "Aborted by user"
    exit 1
fi

# ── Step 1: Update Homebrew ─────────────────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 1: Updating Homebrew"
echo "────────────────────────────────────────────────────────────"
info "Running brew update..."
brew update
success "Homebrew updated"

# ── Step 2: Install system dependencies via Homebrew ────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 2: Installing system dependencies"
echo "────────────────────────────────────────────────────────────"

# Core dependencies for macOS
BREW_PACKAGES=(
    # Python
    "python@3.12"

    # Qt6 framework
    "qt6"

    # Pandoc (document converter)
    "pandoc"

    # Git (for cloning source)
    "git"

    # Build tools
    "pkg-config"
    "libffi"
    "openssl@3"

    # Additional libraries needed by PyQt6
    "libjpeg"
    "libpng"
    "freetype"
    "fontconfig"
    "zlib"
)

# Install Homebrew packages
info "Installing Homebrew packages..."
brew install "${BREW_PACKAGES[@]}"
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

# ── Step 4: Set up Homebrew Python environment ──────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 4: Configuring Python environment"
echo "────────────────────────────────────────────────────────────"

# Ensure Homebrew Python is in PATH
HOMEBREW_PYTHON=$(brew --prefix python@3.12)/bin/python3
if [[ "$HOMEBREW_PYTHON" != "$(which python3)" ]]; then
    info "Homebrew Python detected at: ${HOMEBREW_PYTHON}"
    # Add Homebrew Python to PATH for this session
    export PATH="$(brew --prefix python@3.12)/bin:${PATH}"
    success "Added Homebrew Python to PATH"
fi

# ── Step 5: Create installation directory ────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 5: Setting up installation directory"
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

# ── Step 6: Clone source code from GitHub ────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 6: Cloning PanConvert source from GitHub"
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

# ── Step 7: Create Python virtual environment ────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 7: Creating Python virtual environment"
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

# ── Step 8: Install Python dependencies ─────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 8: Installing Python dependencies"
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

# ── Step 9: Verify installations ────────────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 9: Verifying installation"
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
if qt6/bin/qmake --version 2>/dev/null || $(brew --prefix qt6)/bin/qmake --version 2>/dev/null; then
    success "Qt6 development tools found"
else
    warn "Qt6 qmake not found. PyQt6 may still work, but Qt6 dev tools are recommended."
fi

# ── Step 10: Set permissions ─────────────────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 10: Setting permissions"
echo "────────────────────────────────────────────────────────────"

# Make the main script executable
chmod +x "${INSTALL_DIR}/Panconvert.py"
success "Made Panconvert.py executable"

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
echo "  Option 2 (create an alias in ~/.zshrc):"
echo "    echo 'alias panconvert=\"cd ${INSTALL_DIR} && source .venv/bin/activate && python3 Panconvert.py\"' >> ~/.zshrc"
echo "    source ~/.zshrc"
echo ""
echo "To update to the latest version:"
echo "    cd ${INSTALL_DIR}"
echo "    git pull"
echo ""
echo "To deactivate the virtual environment:"
echo "    deactivate"
echo ""
echo "============================================================"
