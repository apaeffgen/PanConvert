#!/bin/bash
# =============================================================================
# PanConvert - Cleanup Script for macOS
# =============================================================================
# This script removes all components installed by panconvert_source_install_macos.sh
#
# Usage: bash panconvert_source_cleanup_macos.sh
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

# ── Configuration ────────────────────────────────────────────────────────────
INSTALL_DIR="${HOME}/Panconvert"
BREW_PACKAGES=(
    "python@3.12"
    "qt6"
    "pandoc"
    "git"
    "pkg-config"
    "libffi"
    "openssl@3"
    "libjpeg"
    "libpng"
    "freetype"
    "fontconfig"
    "zlib"
)

# ── Pre-flight ───────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  PanConvert Cleanup for macOS"
echo "============================================================"
echo ""
info "This script will remove:"
echo "  1. PanConvert installation directory (${INSTALL_DIR})"
echo "  2. Homebrew packages (Qt6, Python, pandoc, etc.)"
echo "  3. Shell alias in ~/.zshrc (if present)"
echo ""
read -p "Continue? [y/N]: " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    error "Aborted by user"
    exit 1
fi

# ── Step 1: Remove PanConvert installation ───────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 1: Removing PanConvert installation"
echo "────────────────────────────────────────────────────────────"

if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf "$INSTALL_DIR"
    success "Removed installation directory: ${INSTALL_DIR}"
else
    info "Installation directory not found: ${INSTALL_DIR}"
fi

# ── Step 2: Remove alias from shell config ───────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 2: Removing shell alias"
echo "────────────────────────────────────────────────────────────"

ALIAS_PATTERN="alias panconvert="
for shell_rc in ~/.zshrc ~/.bash_profile ~/.bashrc; do
    if [[ -f "$shell_rc" ]] && grep -q "$ALIAS_PATTERN" "$shell_rc"; then
        sed -i '' "/${ALIAS_PATTERN}/d" "$shell_rc"
        success "Removed alias from ${shell_rc}"
    fi
done

# ── Step 3: Uninstall Homebrew packages ──────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 3: Uninstalling Homebrew packages"
echo "────────────────────────────────────────────────────────────"

if ! command -v brew &>/dev/null; then
    warn "Homebrew not found. Skipping package removal."
else
    for pkg in "${BREW_PACKAGES[@]}"; do
        if brew list --formula 2>/dev/null | grep -q "^${pkg}$"; then
            info "Uninstalling ${pkg}..."
            brew uninstall --ignore-dependencies "$pkg" 2>/dev/null || true
            success "Removed ${pkg}"
        else
            info "${pkg} not installed via Homebrew, skipping"
        fi
    done
fi

# ── Step 4: Remove Homebrew (optional) ───────────────────────────────────────
echo ""
echo "────────────────────────────────────────────────────────────"
echo "  Step 4: Homebrew removal (optional)"
echo "────────────────────────────────────────────────────────────"
info "Homebrew itself is NOT removed. To uninstall Homebrew manually:"
echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/uninstall.sh)\""
info "Note: Removing Homebrew will uninstall ALL Homebrew packages, not just PanConvert dependencies."

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  Cleanup Complete!"
echo "============================================================"
echo ""
info "PanConvert has been removed from your system."
echo ""
echo "To fully clean up:"
echo "  1. Homebrew packages have been uninstalled"
echo "  2. PanConvert installation directory has been removed"
echo "  3. Shell alias has been removed"
echo ""
info "Homebrew itself was intentionally NOT removed."
echo ""
echo "============================================================"
