#!/usr/bin/env bash
# build_appimage.sh — Build an AppImage for PanConvert
#
# Usage:
#   ./build_appimage.sh          # Build from current dist/Panconvert
#   ./build_appimage.sh clean    # Remove build artifacts
#   ./build_appimage.sh rebuild  # Force rebuild (skip cache)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DIST_DIR="$PROJECT_DIR/dist"
BUILD_DIR="$PROJECT_DIR/build/Panconvert_AppImage"
APPDIR="$BUILD_DIR/AppDir"
ICON_DIR="$PROJECT_DIR/source/gui/icons"
APPIMAGE_TOOL="$HOME/.local/share/linuxdeploy/linuxdeploy-plugin-appimage-x86_64.AppImage"

# ── Colors ──
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ── Cleanup ──
do_clean() {
    info "Cleaning build artifacts..."
    rm -rf "$BUILD_DIR"
    info "Done."
}

# ── Download linuxdeploy + appimage plugin ──
LINUXDEPLOY_DIR="$HOME/.local/share/linuxdeploy"
LINUXDEPLOY_BIN="$LINUXDEPLOY_DIR/linuxdeploy-x86_64.AppImage"

ensure_tools() {
    mkdir -p "$LINUXDEPLOY_DIR"

    if [[ ! -x "$LINUXDEPLOY_BIN" ]]; then
        info "Downloading linuxdeploy..."
        curl -sL "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage" \
            -o "$LINUXDEPLOY_BIN"
        chmod +x "$LINUXDEPLOY_BIN"
    fi

    if [[ ! -x "$APPIMAGE_TOOL" ]]; then
        info "Downloading linuxdeploy-plugin-appimage..."
        curl -sL "https://github.com/linuxdeploy/linuxdeploy-plugin-appimage/releases/download/continuous/linuxdeploy-plugin-appimage-x86_64.AppImage" \
            -o "$APPIMAGE_TOOL"
        chmod +x "$APPIMAGE_TOOL"
    fi

    if [[ ! -x "$LINUXDEPLOY_BIN" ]]; then
        error "Failed to download linuxdeploy. Check your internet connection."
        exit 1
    fi
}

# ── Main build ──
do_build() {
    ensure_tools

    info "Building AppImage for Panconvert..."

    # Clean previous build
    rm -rf "$APPDIR"

    # Create AppDir structure
    mkdir -p "$APPDIR/usr/bin" \
             "$APPDIR/usr/lib" \
             "$APPDIR/usr/share/icons/hicolor/128x128/apps" \
             "$APPDIR/usr/share/applications"

    # Copy the binary (find the Panconvert binary in dist/)
    local binary
    binary=$(find "$DIST_DIR" -maxdepth 1 -type f -name 'Panconvert*' -executable 2>/dev/null | head -1)
    if [[ -z "$binary" || ! -f "$binary" ]]; then
        error "Binary not found in $DIST_DIR. Run 'pyinstaller packaging/Panconvert_pyinstaller.spec' first."
        exit 1
    fi

    cp "$binary" "$APPDIR/Panconvert"
    cp "$binary" "$APPDIR/usr/bin/Panconvert"
    info "Binary copied to AppDir."

    # Install icon
    if [[ -f "$ICON_DIR/icon.png" ]]; then
        cp "$ICON_DIR/icon.png" "$APPDIR/usr/share/icons/hicolor/128x128/apps/panconvert.png"
        info "Icon installed."
    else
        warn "No icon found at $ICON_DIR/icon.png. AppImage will use a generic icon."
    fi

    # Install desktop file (rename to match AppDir name for appimagetool)
    if [[ -f "$SCRIPT_DIR/Panconvert.desktop" ]]; then
        cp "$SCRIPT_DIR/Panconvert.desktop" "$APPDIR/AppDir.desktop"
        info "Desktop file installed."
    else
        warn "No .desktop file found at $SCRIPT_DIR/Panconvert.desktop"
    fi

    # Copy icon with name matching Icon= field in desktop file
    if [[ -f "$ICON_DIR/icon.png" ]]; then
        cp "$ICON_DIR/icon.png" "$APPDIR/panconvert.png"
        info "Root icon installed."
    fi

    # ── Bundle libxcb-cursor (required by Qt 6.5+ on RHEL/Rocky) ──
    # Qt 6.5+ requires libxcb-cursor.so.0 for the xcb platform plugin.
    # appimagetool doesn't bundle this, so we copy it manually.
    info "Bundling libxcb-cursor for Qt 6.5+ compatibility..."

    # Find libxcb-cursor.so.0 on the system
    LIBCURSOR=$(find /usr/lib64 /usr/lib /lib64 /lib -name 'libxcb-cursor.so.0' 2>/dev/null | head -1)

    if [[ -n "$LIBCURSOR" ]]; then
        cp "$LIBCURSOR" "$APPDIR/usr/lib64/" 2>/dev/null || cp "$LIBCURSOR" "$APPDIR/usr/lib/" 2>/dev/null || true
        info "  libxcb-cursor.so.0 bundled."
    else
        warn "  libxcb-cursor.so.0 not found on system."
        warn "  Install it with: sudo dnf install xcb-util-cursor"
        warn "  The AppImage may fail with 'xcb-cursor0 needed' error."
    fi

    # Create AppRun
    cat > "$APPDIR/AppRun" << 'APPRUN'
#!/bin/sh
# AppRun script for Panconvert AppImage
HERE="$(dirname "$0")"
export QT_QPA_PLATFORM=xcb
export QTWEBENGINE_DISABLE_SANDBOX=1

# Ensure bundled libraries are found (e.g., libxcb-cursor)
if [ -d "$HERE/usr/lib64" ]; then
    export LD_LIBRARY_PATH="$HERE/usr/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
elif [ -d "$HERE/usr/lib" ]; then
    export LD_LIBRARY_PATH="$HERE/usr/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fi

if [ -f "$HERE/Panconvert" ]; then
    exec "$HERE/Panconvert" "$@"
else
    echo "Error: Panconvert binary not found in AppDir" >&2
    exit 1
fi
APPRUN
    chmod +x "$APPDIR/AppRun"
    info "AppRun created."

    # Build the AppImage using the appimage plugin
    info "Building AppImage with appimagetool..."
    
    # Run appimagetool and capture output to find the generated filename
    local output_name
    output_name=$(cd "$APPDIR" && "$APPIMAGE_TOOL" --appdir "$APPDIR" 2>&1 | grep -oP '(?<=should be packaged as )[^ ]+' | head -1)
    
    if [[ -z "$output_name" ]]; then
        # Fallback: appimagetool may output to current dir
        output_name="Panconvert-x86_64.AppImage"
    fi

    local output_path="$APPDIR/$output_name"
    
    if [[ -f "$output_path" ]]; then
        mv "$output_path" "$DIST_DIR/$output_name"
        chmod +x "$DIST_DIR/$output_name"
        local size=$(du -h "$DIST_DIR/$output_name" | cut -f1)
        info "✅ AppImage built successfully!"
        info "   File: $DIST_DIR/$output_name"
        info "   Size: $size"
        info "   Run with: $DIST_DIR/$output_name"
    else
        error "AppImage build failed. Output file not found: $output_path"
        error "Check the output above for errors."
        exit 1
    fi
}

# ── Dispatch ──
case "${1:-build}" in
    clean)
        do_clean
        ;;
    rebuild)
        do_clean
        do_build
        ;;
    build|*)
        do_build
        ;;
esac
