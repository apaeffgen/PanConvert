#!/bin/bash
# Build Panconvert Linux standalone binary with PyInstaller
# Compatible with Ubuntu/Debian, Rocky Linux, Red Hat EL, and Arch Linux
# Run from project root directory

set -e

echo "=== Panconvert Linux Build ==="
echo ""

# Detect package manager and install system dependencies
detect_and_install_deps() {
    if command -v dnf &>/dev/null; then
        echo "[→] Detected DNF (Rocky Linux / Red Hat EL)"
        echo "[→] Installing system dependencies..."
        # Rocky Linux / RHEL 8/9 dependencies
        sudo dnf install -y python3 python3-pip python3-virtualenv gcc make
        sudo dnf install -y python3-devel
        # Qt6 dependencies (required for PyQt6)
        sudo dnf install -y qt6-qtbase qt6-qtbase-devel
        # Optional: GTK/Qt dependencies if needed for GUI
        # sudo dnf install -y gtk3-devel libffi-devel openssl-devel bzip2-devel
        # sudo dnf install -y libxml2-devel libxslt-devel
    elif command -v pacman &>/dev/null; then
        echo "[→] Detected Pacman (Arch Linux / Manjaro / EndeavourOS)"
        echo "[→] Installing system dependencies..."
        # Arch Linux dependencies
        sudo pacman -S --noconfirm --needed python python-pip python-virtualenv gcc make
        # Qt6 dependencies (required for PyQt6)
        sudo pacman -S --noconfirm --needed qt6-base
        # Optional: GTK dependencies if needed for GUI
        # sudo pacman -S --noconfirm --needed gtk3 libffi openssl bzip2
        # sudo pacman -S --noconfirm --needed libxml2 libxslt
    elif command -v apt-get &>/dev/null; then
        echo "[→] Detected APT (Debian/Ubuntu)"
        echo "[→] Installing system dependencies..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv gcc make
        sudo apt-get install -y python3-dev
        # Qt6 dependencies (required for PyQt6)
        sudo apt-get install -y qt6-base-dev
        # Optional: GTK dependencies if needed for GUI
        # sudo apt-get install -y libgtk-3-dev libffi-dev libssl-dev libbz2-dev
        # sudo apt-get install -y libxml2-dev libxslt1-dev
    else
        echo "[✗] No supported package manager found (dnf, pacman, or apt-get required)"
        exit 1
    fi
}

# Check for required system packages and install if missing
if ! command -v python3 &>/dev/null || ! command -v gcc &>/dev/null; then
    detect_and_install_deps
fi

# Clone the project from git if not already present
PANCONVERT_HOME="$HOME/panconvert"
if [ ! -d "$PANCONVERT_HOME/.git" ]; then
    echo "[→] Cloning Panconvert repository..."
    mkdir -p "$PANCONVERT_HOME"
    git clone https://github.com/apaeffgen/Panconvert.git "$PANCONVERT_HOME" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "[✗] Failed to clone repository. Please check your internet connection."
        exit 1
    fi
    echo "[✓] Repository cloned to $PANCONVERT_HOME"
else
    echo "[✓] Repository already cloned at $PANCONVERT_HOME"
fi

# Update to latest version
cd "$PANCONVERT_HOME"
git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || echo "[→] Could not pull latest changes, continuing with current code"

echo "[→] Working directory: $(pwd)"

# Project root is now the cloned repository
PACKAGING_DIR="$PANCONVERT_HOME"

# Verify project files exist
if [ ! -f "$PACKAGING_DIR/source/language/messages.py" ]; then
    echo "[✗] Project files not found in $PACKAGING_DIR"
    exit 1
fi
echo "[→] Project root: $PACKAGING_DIR"

# Find spec file location
SPEC_FILE=""
for candidate in "$PACKAGING_DIR/packaging/Panconvert_pyinstaller.spec" "$PACKAGING_DIR/packaging/linux/Panconvert.spec" "$PACKAGING_DIR/Panconvert.spec"; do
    if [ -f "$candidate" ]; then
        SPEC_FILE="$candidate"
        break
    fi
done

if [ -z "$SPEC_FILE" ]; then
    echo "[✗] Panconvert spec file not found."
    echo "    Searched:"
    echo "      - $PACKAGING_DIR/packaging/Panconvert_pyinstaller.spec"
    echo "      - $PACKAGING_DIR/packaging/linux/Panconvert.spec"
    echo "      - $PACKAGING_DIR/Panconvert.spec"
    exit 1
fi
echo "[→] Using spec file: $SPEC_FILE"

# Create virtual environment (always, to ensure clean build)
echo "[→] Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
# Ensure venv bin is in PATH (some shells don't update PATH properly)
export PATH="$(pwd)/.venv/bin:$PATH"
echo "[✓] Virtual environment created and activated"

# Upgrade pip inside the venv
echo "[→] Upgrading pip..."
pip install --upgrade pip

# Install project requirements first (including PyQt6)
echo "[→] Installing project requirements..."
pip install -r requirements.txt

# Install pyinstaller only if not already present
echo "[→] Checking pyinstaller..."
if ! pip show pyinstaller &>/dev/null; then
    echo "[→] Installing pyinstaller..."
    pip install pyinstaller
else
    echo "[✓] pyinstaller already installed"
fi

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
pyinstaller --clean --distpath="${PACKAGING_DIR}/dist" --workpath="${PACKAGING_DIR}/build" "$SPEC_FILE"

echo ""
echo "=== Build Complete ==="
echo "Output: dist/Panconvert-${VERSION}-linux_x86-64"
echo "Size:   $(du -h dist/Panconvert-${VERSION}-linux_x86-64 | cut -f1)"
echo ""

# Copy binary to ~/panconvert
echo "[→] Copying binary to $PANCONVERT_HOME..."
cp dist/Panconvert-${VERSION}-linux_x86-64 "$PANCONVERT_HOME/Panconvert"
chmod +x "$PANCONVERT_HOME/Panconvert"
echo "[✓] Binary installed to $PANCONVERT_HOME/Panconvert"

# Create startup script
echo "[→] Creating startup script..."
cat > "$PANCONVERT_HOME/panconvert.sh" << 'EOF'
#!/bin/bash
# Startup script for Panconvert
# Launches Panconvert from the virtual environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

# Launch Panconvert
exec "$SCRIPT_DIR/Panconvert" "$@"
EOF
chmod +x "$PANCONVERT_HOME/panconvert.sh"
echo "[✓] Startup script created: $PANCONVERT_HOME/panconvert.sh"

# Create desktop icon
echo "[→] Creating desktop icon..."
DESKTOP_FILE="$HOME/.local/share/applications/panconvert.desktop"
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=Panconvert
Comment=Document converter with PyQt6 GUI
Exec=$PANCONVERT_HOME/panconvert.sh
Icon=$PANCONVERT_HOME/icon.png
Type=Application
Categories=Utility;
Terminal=false
EOF

chmod +x "$DESKTOP_FILE"
echo "[✓] Desktop icon created: $DESKTOP_FILE"

# Try to copy icon if it exists in the project
if [ -f "$PACKAGING_DIR/icon.png" ]; then
    cp "$PACKAGING_DIR/icon.png" "$PANCONVERT_HOME/icon.png"
    echo "[→] Icon copied to $PANCONVERT_HOME/icon.png"
elif [ -f "$PACKAGING_DIR/resources/icon.png" ]; then
    cp "$PACKAGING_DIR/resources/icon.png" "$PANCONVERT_HOME/icon.png"
    echo "[→] Icon copied to $PANCONVERT_HOME/icon.png"
else
    echo "[→] No icon found in project, desktop icon will use fallback theme icon"
fi

# Register desktop file with system (optional)
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null || true
fi

echo ""
echo "=== Build Complete ==="
echo "Output: dist/Panconvert-${VERSION}-linux_x86-64"
echo "Size:   $(du -h dist/Panconvert-${VERSION}-linux_x86-64 | cut -f1)"
echo ""
echo "To launch:"
echo "    ~/panconvert/panconvert.sh"
echo ""
echo "Or from the application menu (search for 'Panconvert')"
echo ""