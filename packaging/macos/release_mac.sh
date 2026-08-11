#!/usr/bin/env bash
# release_mac.sh - Publish the macOS PKG installer to a GitHub release
# Usage: ./packaging/macos/release_mac.sh [version]
#
# Prerequisites:
#   1. Set GH_TOKEN environment variable with a GitHub Personal Access Token
#      (scope: repo, public_repo)
#   2. Or run gh auth login first
#   3. Ensure dist/ contains Panconvert-<version>-macos.pkg
#
# Example:
#   export GH_TOKEN=ghp_your_token_here
#   ./packaging/macos/release_mac.sh 0.3.1
#
#   # Or authenticate first:
#   gh auth login --with-token <<< "ghp_your_token_here"
#   ./packaging/macos/release_mac.sh 0.3.1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

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

# ── Confirm GitHub login ──────────────────────────────────────────────────────
echo "✅ GitHub login confirmed:"
gh auth status 2>&1 | head -3
echo ""
GH_USER=$(gh api user --jq '.login' 2>/dev/null)
echo "👤 Authenticated as: $GH_USER"
REPO=$(basename "$(git remote get-url origin 2>/dev/null | sed 's|.*\/||;s|\.git$||')")
echo "📦 Repository: $GH_USER/$REPO"
echo ""
if [ -z "$GH_USER" ] || [ -z "$REPO" ]; then
    echo "❌ Could not verify GitHub identity. Aborting."
    exit 1
fi

# ── Get version ───────────────────────────────────────────────────────────────
if [ -n "${1:-}" ]; then
    VERSION="$1"
else
    # Extract version from messages.py (macOS grep doesn't support -P)
    VERSION=$(sed -n "s/^versionnumber = '\([^']*\)'/\1/p" source/language/messages.py)
fi

# Remove 'v' prefix if present
VERSION="${VERSION#v}"

echo "📦 Publishing macOS release: v$VERSION"

# ── Locate the PKG file ───────────────────────────────────────────────────────
PKG_FILE=""
if [ -n "${1:-}" ]; then
    # Use provided version to find the pkg
    PKG_FILE="dist/Panconvert-${VERSION}-macos.pkg"
else
    # Find the latest pkg in dist/
    PKG_FILE=$(ls -t dist/Panconvert-*-macos.pkg 2>/dev/null | head -n 1)
fi

if [ -z "$PKG_FILE" ] || [ ! -f "$PKG_FILE" ]; then
    echo "❌ macOS PKG installer not found in dist/."
    echo "   Run 'bash packaging/macos/build.sh && bash packaging/macos/build_pkg.sh' first."
    exit 1
fi

echo "📁 PKG file: $(basename "$PKG_FILE") ($(du -mh "$PKG_FILE" | cut -f1))"

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
if git push origin "$TAG" 2>&1; then
    echo "✅ Tag pushed"
else
    echo "❌ Git push failed."
    echo ""
    echo "Your network may be blocking github.com:443."
    echo ""
    echo "Fix: switch to SSH and add an SSH key to GitHub:"
    echo "  git remote set-url origin git@github.com:apaeffgen/PanConvert.git"
    echo "  ssh-add ~/.ssh/id_ed25519   # or your key file"
    echo ""
    echo "Or push manually from a working network:"
    echo "  git push origin $TAG"
    exit 1
fi

# ── Check if release already exists ───────────────────────────────────────────
if gh release view "$TAG" &>/dev/null; then
    echo "⚠️  Release $TAG already exists."
    echo ""
    echo -n "Re-upload the PKG file? (y/N) "
    read -r UPLOAD
    echo
    if [[ ! "$UPLOAD" =~ ^[Yy]$ ]]; then
        echo "📋 Skipping upload. Release already exists."
        echo "   View at: https://github.com/apaeffgen/PanConvert/releases/tag/$TAG"
        exit 0
    fi
    echo ""
fi

# ── Generate release notes ────────────────────────────────────────────────────
RELEASE_NOTES=$(cat <<EOF
## Changes
- See [changelog](docs/Developer/changelog.md) for full details

## macOS Download

| File | Size |
|------|------|
| $(basename "$PKG_FILE") | $(du -mh "$PKG_FILE" | cut -f1) |

## Installation
    sudo installer -pkg Panconvert-${VERSION}-macos.pkg -target /

See [ReadTheDocs](https://panconvert.readthedocs.io/en/latest/) for more installation instructions.
EOF
)

# ── Create or update GitHub release ───────────────────────────────────────────
echo ""
echo "🚀 Creating GitHub release..."

if gh release view "$TAG" &>/dev/null; then
    # Update existing release, upload only the PKG
    # Remove existing asset first (avoids --clobber hang on large files)
    EXISTING=$(gh release view "$TAG" --json assets --jq -r '.assets[] | select(.name == "'"$(basename "$PKG_FILE")"'") | .id' 2>/dev/null || true)
    if [ -n "$EXISTING" ]; then
        echo "🗑️  Removing existing asset $(basename "$PKG_FILE")..."
        gh release delete-asset "$TAG" "$EXISTING" --yes
    fi
    FILE_SIZE_MB=$(du -m "$PKG_FILE" | cut -f1)
    RELEASE_ID=$(gh release view "$TAG" --json id --jq '.id')
    GH_TOKEN=$(gh auth status --show-token 2>&1 | grep '✓ Token:' | sed 's/.*✓ Token: //')
    echo "📤 Uploading $(basename "$PKG_FILE") (${FILE_SIZE_MB}MB)..."

    if gh release upload "$TAG" "$PKG_FILE" --clobber 2>&1; then
        echo "✅ Release v$VERSION updated!"
    else
        echo "❌ Upload failed."
        echo ""
        echo "Upload manually: https://github.com/apaeffgen/PanConvert/releases/edit/$TAG"
        exit 1
    fi
else
    # Create new release
    gh release create "$TAG" \
        --title "Panconvert $TAG" \
        --notes "$RELEASE_NOTES" \
        "$PKG_FILE"
    echo "✅ Release v$VERSION published!"
fi

echo "   View at: https://github.com/apaeffgen/PanConvert/releases/tag/$TAG"
