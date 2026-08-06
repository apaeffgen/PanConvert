#!/usr/bin/env bash
# release.sh - Publish files from the dist folder to a GitHub release
# Usage: ./scripts/release.sh [version]
#
# Prerequisites:
#   1. Set GH_TOKEN environment variable with a GitHub Personal Access Token
#      (scope: repo, public_repo)
#   2. Or run gh auth login first
#   3. Ensure dist/ contains the built artifacts
#
# Example:
#   export GH_TOKEN=ghp_your_token_here
#   ./scripts/release.sh 0.4.0
#
#   # Or authenticate first:
#   gh auth login --with-token <<< "ghp_your_token_here"
#   ./scripts/release.sh 0.4.0

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

# ── Detect platform ───────────────────────────────────────────────────────────
detect_platform() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v dnf &>/dev/null; then
            echo "rhel"
        elif command -v pacman &>/dev/null; then
            echo "arch"
        elif command -v apt-get &>/dev/null; then
            echo "debian"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

CURRENT_PLATFORM=$(detect_platform)
echo "🖥️  Detected platform: $CURRENT_PLATFORM"

# ── Classify dist files by platform ───────────────────────────────────────────
classify_file() {
    local file="$1"
    local basename
    basename=$(basename "$file" | tr '[:upper:]' '[:lower:]')
    
    if [[ "$basename" == *"deb"* ]] || [[ "$basename" == *"debian"* ]] || [[ "$basename" == *"ubuntu"* ]]; then
        echo "debian"
    elif [[ "$basename" == *"rpm"* ]] || [[ "$basename" == *"rhel"* ]] || [[ "$basename" == *"centos"* ]] || [[ "$basename" == *"fedora"* ]] || [[ "$basename" == *"rocky"* ]]; then
        echo "rhel"
    elif [[ "$basename" == *"arch"* ]] || [[ "$basename" == *"pacman"* ]]; then
        echo "arch"
    elif [[ "$basename" == *"macos"* ]] || [[ "$basename" == *"darwin"* ]] || [[ "$basename" == *"dmg"* ]] || [[ "$basename" == *"pkg"* ]]; then
        echo "macos"
    elif [[ "$basename" == *"windows"* ]] || [[ "$basename" == *"msi"* ]] || [[ "$basename" == *"exe"* ]] || [[ "$basename" == *"zip"* ]]; then
        echo "windows"
    elif [[ "$basename" == *"linux"* ]] || [[ "$basename" == *"x86_64"* ]] || [[ "$basename" == *"bin"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

# ── Check authentication ──────────────────────────────────────────────────────
if ! gh auth status &>/dev/null; then
    echo "❌ Not authenticated with GitHub."
    echo ""
    echo "Option 1: Set GH_TOKEN environment variable:"
    echo "  export GH_TOKEN=ghp_your_token_here"
    echo ""
    echo "Option 2: Login interactively:"
    echo "  gh auth login"
    echo ""
    echo "Option 3: Login with token directly:"
    echo "  gh auth login --with-token <<< \"ghp_your_token_here\""
    exit 1
fi

# ── Get version ───────────────────────────────────────────────────────────────
if [ -n "${1:-}" ]; then
    VERSION="$1"
else
    # Extract version from messages.py
    VERSION=$(grep -oP "versionnumber = '\K[^']+" source/language/messages.py)
fi

# Remove 'v' prefix if present
VERSION="${VERSION#v}"

echo "📦 Publishing release: v$VERSION"

# ── Check dist folder exists and has files ────────────────────────────────────
if [ ! -d "dist" ]; then
    echo "❌ dist/ folder not found. Build your release first."
    exit 1
fi

DIST_FILES=$(ls -A dist/ 2>/dev/null)
if [ -z "$DIST_FILES" ]; then
    echo "❌ dist/ folder is empty. Nothing to publish."
    exit 1
fi

echo ""
echo "📁 Classifying artifacts in dist/:"

# Arrays to hold files by platform
declare -A PLATFORM_FILES
for file in dist/*; do
    [ -f "$file" ] || continue
    platform=$(classify_file "$file")
    PLATFORM_FILES[$platform]="${PLATFORM_FILES[$platform]:-} $file"
    printf "  %-12s %s\n" "[$platform]" "$(basename "$file") ($(du -h "$file" | cut -f1))"
done

# Show summary
echo ""
echo "📋 Summary:"
for platform in debian rhel arch macos windows linux unknown; do
    if [ -n "${PLATFORM_FILES[$platform]:-}" ]; then
        count=$(echo "${PLATFORM_FILES[$platform]}" | wc -w)
        if [ "$platform" = "$CURRENT_PLATFORM" ]; then
            echo "  ✅ $platform ($count file(s)) ← current platform"
        else
            echo "  ℹ️   $platform ($count file(s))"
        fi
    fi
done

# Check if we have the current platform's files
HAS_CURRENT=false
for platform in debian rhel arch macos windows linux unknown; do
    if [ -n "${PLATFORM_FILES[$platform]:-}" ]; then
        HAS_CURRENT=true
        break
    fi
done

if [ "$HAS_CURRENT" = false ]; then
    echo ""
    echo "⚠️  No artifacts found for the current platform ($CURRENT_PLATFORM)."
    echo "   Make sure to build the correct binary before publishing."
    echo ""
    echo "Build commands:"
    echo "  Debian/Ubuntu: ./packaging/linux/build_linux.sh"
    echo "  Red Hat/Rocky: ./packaging/linux/build_linux_rh.sh"
    echo "  macOS:         ./packaging/macos/build_macos.sh"
    echo "  Windows:       ./packaging/windows/build_windows.sh"
    exit 1
fi

echo ""
echo "🚀 Will upload all artifacts from dist/"

# ── Create git tag ────────────────────────────────────────────────────────────
TAG="v$VERSION"
if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "✅ Tag $TAG already exists."
else
    git tag -a "$TAG" -m "Release $TAG"
    echo "✅ Created git tag $TAG"
fi

# ── Push tag ──────────────────────────────────────────────────────────────────
echo "📤 Pushing tag to GitHub..."
git push origin "$TAG"
echo "✅ Tag pushed"

# ── Check if release already exists ───────────────────────────────────────────
if gh release view "$TAG" &>/dev/null; then
    echo ""
    echo "⚠️  Release $TAG already exists."
    echo ""
    echo "Existing assets:"
    gh release view "$TAG" --json name,assets --jq '.assets[].name' 2>/dev/null || true
    echo ""
    read -p "Re-upload the files from dist/? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "📋 Skipping upload. Release already exists."
        echo "   View at: https://github.com/apaeffgen/PanConvert/releases/tag/$TAG"
        exit 0
    fi
fi

# ── Create or update GitHub release ───────────────────────────────────────────
echo ""
echo "🚀 Creating GitHub release..."

# ── Generate release notes with available downloads ────────────────────────────
DOWNLOADS=""
for platform in debian rhel arch macos windows linux; do
    if [ -n "${PLATFORM_FILES[$platform]:-}" ]; then
        for file in ${PLATFORM_FILES[$platform]}; do
            filename=$(basename "$file")
            DOWNLOADS+="- **$platform:** $filename\n"
        done
    fi
done

RELEASE_NOTES=$(cat <<EOF
## Changes
- See [changelog](docs/Developer/changelog.md) for full details

## Downloads

| Platform | File |
|----------|------|
$(for platform in debian rhel arch macos windows linux; do
    if [ -n "${PLATFORM_FILES[$platform]:-}" ]; then
        for file in ${PLATFORM_FILES[$platform]}; do
            filename=$(basename "$file")
            printf "| %s | %s |\n" "$platform" "$filename"
        done
    fi
done)

## Installation
See [ReadTheDocs](https://panconvert.readthedocs.io/en/latest/) for installation instructions.
EOF
)

if gh release view "$TAG" &>/dev/null; then
    # Update existing release
    gh release upload "$TAG" dist/* --clobber
    echo "✅ Release v$VERSION updated!"
else
    # Create new release
    gh release create "$TAG" \
        --title "Panconvert $TAG" \
        --notes "$RELEASE_NOTES" \
        dist/*
    echo "✅ Release v$VERSION published!"
fi
echo "   View at: https://github.com/apaeffgen/PanConvert/releases/tag/$TAG"
