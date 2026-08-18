#!/usr/bin/env bash
# Run PanConvert tests with pytest.
#
# Usage:
#   ./run_tests.sh                  # Run all tests (table output)
#   ./run_tests.sh -p              # Run only binary/platform tests
#   ./run_tests.sh -g              # Run only GUI tests
#   ./run_tests.sh -c              # Run only conversion tests
#   ./run_tests.sh -s              # Run only settings tests
#   ./run_tests.sh -- -v           # Pass extra args to pytest (overrides defaults)
#
# Requires:
#   - Python 3.12+
#   - pytest
#   - PyQt6 (for GUI tests)
#   - pandoc (for integration tests)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

# ── Activate virtual environment ──
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "[✓] Virtual environment activated"
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "[✓] Virtual environment activated (venv/)"
fi

# ── Install pytest if missing ──
if ! pip show pytest &>/dev/null; then
    echo "[→] Installing pytest..."
    pip install pytest pytest-qt
fi

# ── Platform detection ──
PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')
echo "[→] Platform: $PLATFORM"

# ── Test selection ──
TEST_DIRS="tests/"
PYTEST_ARGS=()

while getopts "pgcs" opt; do
    case $opt in
        p)
            TEST_DIRS="tests/test_binary_basics.py tests/test_pandoc_integration.py tests/platform/"
            ;;
        g)
            TEST_DIRS="tests/gui/"
            ;;
        c)
            TEST_DIRS="tests/test_conversions.py"
            ;;
        s)
            TEST_DIRS="tests/test_settings.py"
            ;;
        *)
            ;;
    esac
done

# ── Common pytest options ──
# Default: table output with quiet mode
PYTEST_ARGS+=(
    --table-report
    -q
    --tb=no
)

# ── Skip GUI tests if no display ──
if [ -z "$DISPLAY" ] && [ "$PLATFORM" != "darwin" ]; then
    echo "[→] No display detected, skipping GUI tests"
    if [ "$TEST_DIRS" = "tests/" ]; then
        TEST_DIRS="tests/test_binary_basics.py tests/test_pandoc_integration.py tests/test_conversions.py tests/test_settings.py tests/platform/"
    fi
fi

# ── Check pandoc availability ──
if command -v pandoc &>/dev/null; then
    PANDOC_VERSION=$(pandoc --version | head -1)
    echo "[✓] pandoc available: $PANDOC_VERSION"
else
    echo "[!] pandoc not found - integration tests will be skipped"
fi

# ── Run tests ──
echo ""
echo "═══════════════════════════════════════════════════"
echo "  PanConvert Test Suite"
echo "═══════════════════════════════════════════════════"
echo ""
echo "  Testing: $TEST_DIRS"
echo "  Options: --table-report -q --tb=no"
echo ""

# Pass through any extra arguments after --
if [ $# -gt 0 ]; then
    shift $((OPTIND - 1))
    PYTEST_ARGS+=("$@")
fi

python -m pytest $TEST_DIRS "${PYTEST_ARGS[@]}"
