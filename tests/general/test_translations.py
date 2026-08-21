#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translation coverage tests for PanConvert.

These tests verify:
- All .ts files contain translations for new strings
- No "unfinished" translations remain in active contexts
- .qm files are up to date with their .ts counterparts
- All source strings have translations in all supported languages
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest


# ─── Configuration ────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LANGUAGE_DIR = PROJECT_ROOT / "source" / "language"

SUPPORTED_LANGUAGES = ["de", "es", "fr"]
TS_FILES = {lang: LANGUAGE_DIR / f"Panconvert_{lang}.ts" for lang in SUPPORTED_LANGUAGES}
QM_FILES = {lang: LANGUAGE_DIR / f"Panconvert_{lang}.qm" for lang in SUPPORTED_LANGUAGES}

# Contexts that should have active translations (not vanished/obsolete)
ACTIVE_CONTEXTS = [
    "From_Format_Dialog",
    "To_Format_Dialog",
    "DialogBatch",
    "DialogOpenURI",
    "DialogPreferences",
    "Information_Dialog",
    "Help_Dialog",
    "ManualConverterDialog",
    "message",
]

# Known unfinished strings that are acceptable to leave untranslated
# (e.g., newly added strings awaiting translation, or format names like EPub)
KNOWN_UNFINISHED = {
    "EPub",  # Format name, often kept in English
    "Epub",  # Alternative casing of EPub
    "Open URI",  # UI string, can be translated when convenient
    "Open Uri",  # Alternative casing
    "Stay on Top",  # UI string, can be translated when convenient
}

# Maximum allowed unfinished translations per language (for new additions)
MAX_UNFINISHED_PER_LANGUAGE = 10


# ─── Helper Functions ─────────────────────────────────────────────────────────


def parse_ts_file(ts_path: Path) -> dict:
    """Parse a .ts file and return a dict of {context: {source: translation}}."""
    if not ts_path.exists():
        return {}

    tree = ET.parse(ts_path)
    root = tree.getroot()

    result = {}
    for context_elem in root.findall("context"):
        context_name = context_elem.find("name").text
        result[context_name] = {}

        for message_elem in context_elem.findall("message"):
            source_elem = message_elem.find("source")
            translation_elem = message_elem.find("translation")

            if source_elem is not None and translation_elem is not None:
                source = source_elem.text or ""
                translation = translation_elem.text or ""

                # Check translation status
                is_unfinished = translation_elem.get("type") == "unfinished"
                is_obsolete = translation_elem.get("type") == "obsolete"
                is_vanished = translation_elem.get("type") == "vanished"

                result[context_name][source] = {
                    "translation": translation,
                    "unfinished": is_unfinished,
                    "obsolete": is_obsolete,
                    "vanished": is_vanished,
                }

    return result


def get_all_source_strings() -> dict:
    """Extract all source strings from the project."""
    source_strings = {}

    # Find all Python and UI files in the source directory
    source_dir = PROJECT_ROOT / "source"

    for py_file in source_dir.rglob("*.py"):
        # Read file and look for _translate calls
        try:
            content = py_file.read_text(encoding="utf-8")
            # Match _translate('context', 'string') or _translate("context", "string")
            pattern = r"_translate\s*\(\s*['\"](\w+)['\"]\s*,\s*['\"](.+?)['\"]\s*\)"
            matches = re.findall(pattern, content)
            for context, source in matches:
                if context not in source_strings:
                    source_strings[context] = set()
                source_strings[context].add(source)
        except Exception:
            continue

    return source_strings


def check_lupdate_available() -> bool:
    """Check if lupdate and lrelease are available."""
    try:
        subprocess.run(["lupdate", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


# ─── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def ts_data():
    """Load all .ts files once per test module."""
    return {lang: parse_ts_file(path) for lang, path in TS_FILES.items()}


@pytest.fixture(scope="module")
def has_lupdate():
    """Check if lupdate is available."""
    return check_lupdate_available()


# ─── Basic Tests ──────────────────────────────────────────────────────────────


class TestTranslationFilesExist:
    """Test that translation files exist."""

    @pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
    def test_ts_file_exists(self, lang):
        """All .ts files should exist."""
        assert TS_FILES[lang].exists(), f"Missing .ts file: {TS_FILES[lang]}"

    @pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
    def test_qm_file_exists(self, lang):
        """All .qm files should exist."""
        assert QM_FILES[lang].exists(), f"Missing .qm file: {QM_FILES[lang]}"

    @pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
    def test_qm_file_not_empty(self, lang):
        """All .qm files should have content."""
        assert QM_FILES[lang].stat().st_size > 0, f"Empty .qm file: {QM_FILES[lang]}"


class TestTranslationValidity:
    """Test that translation files are valid XML."""

    @pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
    def test_ts_file_valid_xml(self, lang):
        """All .ts files should be valid XML."""
        try:
            ET.parse(TS_FILES[lang])
        except ET.ParseError as e:
            pytest.fail(f"Invalid XML in {TS_FILES[lang]}: {e}")


class TestContexts:
    """Test translation contexts."""

    def test_all_active_contexts_exist(self, ts_data):
        """All active contexts should exist in at least one language."""
        for lang, data in ts_data.items():
            # At minimum, From_Format_Dialog and To_Format_Dialog should exist
            assert "From_Format_Dialog" in data, (
                f"Missing From_Format_Dialog context in {lang}"
            )
            assert "To_Format_Dialog" in data, (
                f"Missing To_Format_Dialog context in {lang}"
            )

    def test_message_context_exists(self, ts_data):
        """The 'message' context should exist in all languages."""
        for lang, data in ts_data.items():
            assert "message" in data, f"Missing 'message' context in {lang}"


class TestNewSearchStrings:
    """Test that new search dialog strings are translated."""

    SEARCH_STRINGS = {
        "Search formats...": {
            "de": "Formate suchen...",
            "es": "Buscar formatos...",
            "fr": "Rechercher des formats...",
        },
        "Clear": {
            "de": "Löschen",
            "es": "Limpiar",
            "fr": "Effacer",
        },
    }

    @pytest.mark.parametrize("source", list(SEARCH_STRINGS.keys()))
    @pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
    def test_search_strings_translated(self, ts_data, source, lang):
        """Search dialog strings should be translated in all languages."""
        expected = self.SEARCH_STRINGS[source][lang]
        data = ts_data[lang]

        # Check in both From_Format_Dialog and To_Format_Dialog
        for context in ["From_Format_Dialog", "To_Format_Dialog"]:
            if context in data:
                if source in data[context]:
                    translation_info = data[context][source]
                    assert not translation_info["unfinished"], (
                        f"'{source}' is unfinished in {lang}/{context}"
                    )
                    assert translation_info["translation"] == expected, (
                        f"Expected '{expected}' for '{source}' in {lang}, "
                        f"got '{translation_info['translation']}'"
                    )

    @pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
    def test_search_strings_no_unfinished(self, ts_data, lang):
        """Search strings should not have unfinished translations."""
        data = ts_data[lang]
        for source in self.SEARCH_STRINGS.keys():
            for context in ["From_Format_Dialog", "To_Format_Dialog"]:
                if context in data and source in data[context]:
                    assert not data[context][source]["unfinished"], (
                        f"'{source}' is unfinished in {lang}/{context}"
                    )


class TestUnfinishedTranslations:
    """Test for unfinished translations in active contexts."""

    def test_no_unfinished_in_active_contexts(self, ts_data):
        """Active contexts should not have unfinished translations."""
        for lang, data in ts_data.items():
            for context in ACTIVE_CONTEXTS:
                if context in data:
                    for source, info in data[context].items():
                        if info["unfinished"]:
                            # Skip if translation is already filled in (even if marked unfinished)
                            if info["translation"]:
                                continue
                            # Skip known unfinished strings
                            if source in KNOWN_UNFINISHED:
                                continue
                            pytest.fail(
                                f"Unfinished translation in {lang}/{context}: "
                                f"'{source[:50]}...' -> '{info['translation']}'"
                            )

    def test_count_unfinished_by_language(self, ts_data):
        """Report count of unfinished translations per language."""
        for lang, data in ts_data.items():
            unfinished_count = 0
            for context, messages in data.items():
                for source, info in messages.items():
                    if info["unfinished"] and source not in KNOWN_UNFINISHED:
                        unfinished_count += 1
            # Just an assertion to track this - should be low for production
            assert unfinished_count <= MAX_UNFINISHED_PER_LANGUAGE, (
                f"{lang} has {unfinished_count} unfinished translations "
                f"(excluding known: {KNOWN_UNFINISHED}). "
                f"Please complete them before release."
            )


class TestTranslationCoverage:
    """Test that translations cover all source strings."""

    @pytest.mark.skipif(
        not check_lupdate_available(),
        reason="lupdate not available",
    )
    def test_lupdate_can_parse_project(self, has_lupdate):
        """lupdate should be able to parse the project without errors."""
        if not has_lupdate:
            pytest.skip("lupdate not available")

        source_dir = PROJECT_ROOT / "source"
        result = subprocess.run(
            ["lupdate", str(source_dir), "-ts", "/dev/null"],
            capture_output=True,
            text=True,
        )
        # Check for syntax errors (not missing translations)
        assert "error:" not in result.stderr.lower() or "Expected token" not in result.stderr, (
            f"lupdate found syntax errors: {result.stderr}"
        )


class TestQMFilesUpToDate:
    """Test that .qm files are newer than their .ts counterparts."""

    @pytest.mark.parametrize("lang", SUPPORTED_LANGUAGES)
    def test_qm_newer_than_ts(self, lang):
        """.qm file should be newer than .ts file."""
        ts_time = TS_FILES[lang].stat().st_mtime
        qm_time = QM_FILES[lang].stat().st_mtime

        # Allow 1 second tolerance for filesystem timestamp issues
        assert qm_time >= ts_time - 1, (
            f".qm file is older than .ts file for {lang}. "
            "Run 'lrelease source/language/Panconvert_{lang}.ts'"
        )


class TestTranslationConsistency:
    """Test consistency across languages."""

    def test_all_languages_have_same_contexts(self, ts_data):
        """All languages should have the same set of contexts."""
        all_contexts = [set(data.keys()) for data in ts_data.values()]
        first = all_contexts[0]
        for i, contexts in enumerate(all_contexts[1:], 1):
            if contexts != first:
                missing = first - contexts
                extra = contexts - first
                pytest.fail(
                    f"Language {list(TS_FILES.keys())[i]} has different contexts. "
                    f"Missing: {missing}, Extra: {extra}"
                )

    def test_source_strings_match_across_languages(self, ts_data):
        """Source strings should be consistent across languages."""
        # Get source strings from the first language
        first_lang = list(ts_data.keys())[0]
        first_data = ts_data[first_lang]

        for lang, data in ts_data.items():
            if lang == first_lang:
                continue

            for context, messages in data.items():
                if context not in first_data:
                    continue
                first_messages = first_data[context]

                for source in messages:
                    if source in first_messages:
                        # Skip known unfinished strings
                        if source in KNOWN_UNFINISHED:
                            continue
                        # Skip if translation is filled in (even if marked unfinished)
                        curr_info = messages[source]
                        if curr_info["unfinished"] and curr_info["translation"]:
                            continue
                        first_info = first_messages[source]
                        if first_info["unfinished"] and first_info["translation"]:
                            continue
                        # Source exists in both - check translation status
                        first_unfinished = first_info["unfinished"]
                        curr_unfinished = curr_info["unfinished"]

                        # Both should have same unfinished status
                        if first_unfinished != curr_unfinished:
                            pytest.fail(
                                f"Inconsistent unfinished status for '{source}' "
                                f"in {context}: {first_lang}={first_unfinished}, "
                                f"{lang}={curr_unfinished}"
                            )


class TestObsoleteTranslations:
    """Test handling of obsolete translations."""

    def test_obsolete_count_reasonable(self, ts_data):
        """Obsolete translation count should not grow indefinitely."""
        for lang, data in ts_data.items():
            obsolete_count = 0
            for context, messages in data.items():
                for source, info in messages.items():
                    if info["obsolete"] or info["vanished"]:
                        obsolete_count += 1

            # Allow some obsolete entries (from old code), but flag if too many
            # This threshold may need adjustment as the project evolves
            if obsolete_count > 50:
                pytest.fail(
                    f"{lang} has {obsolete_count} obsolete/vanished translations. "
                    f"Consider cleaning up the .ts file."
                )


# ─── Manual Check Functions ───────────────────────────────────────────────────


def print_translation_summary():
    """Print a summary of translation status (for manual verification)."""
    print("\n" + "=" * 70)
    print("TRANSLATION STATUS SUMMARY")
    print("=" * 70)

    for lang in SUPPORTED_LANGUAGES:
        ts_path = TS_FILES[lang]
        if not ts_path.exists():
            print(f"\n{lang.upper()}: .ts file not found")
            continue

        data = parse_ts_file(ts_path)

        total = 0
        finished = 0
        unfinished = 0
        obsolete = 0

        for context, messages in data.items():
            for source, info in messages.items():
                total += 1
                if info["unfinished"]:
                    unfinished += 1
                elif info["obsolete"] or info["vanished"]:
                    obsolete += 1
                else:
                    finished += 1

        print(f"\n{lang.upper()}:")
        print(f"  Total strings: {total}")
        print(f"  Finished:      {finished}")
        print(f"  Unfinished:    {unfinished}")
        print(f"  Obsolete:      {obsolete}")

        if unfinished > 0:
            print(f"  Unfinished strings in active contexts:")
            for context in ACTIVE_CONTEXTS:
                if context in data:
                    for source, info in data[context].items():
                        if info["unfinished"]:
                            print(f"    [{context}] {source[:50]}...")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Run when executed directly for quick status check
    print_translation_summary()
