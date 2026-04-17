"""Tests for the pure transliteration functions."""

from __future__ import annotations

import pytest

from uzbek_translit import to_cyrillic, to_latin, transliterate


class TestToCyrillic:
    """Latin → Cyrillic conversion."""

    def test_simple_greeting(self) -> None:
        assert to_cyrillic("Assalomu alaykum") == "Ассалому алайкум"

    def test_basic_alphabet_sample(self) -> None:
        # "kitob" (book) is uncontroversial — no TS / YE / YA ambiguities
        assert to_cyrillic("kitob") == "китоб"

    def test_ts_lexicon_word(self) -> None:
        # "абзац" is in the TS_WORDS lexicon (abzats → абзац, not абзатс)
        assert to_cyrillic("abzats") == "абзац"

    def test_non_uzbek_chars_pass_through(self) -> None:
        # digits, punctuation, and latin-only words stay as-is
        result = to_cyrillic("year 2026!")
        assert "2026" in result
        assert "!" in result

    def test_empty_string(self) -> None:
        assert to_cyrillic("") == ""

    def test_apostrophe_form_o_gh(self) -> None:
        # Uzbek Latin uses oʻ / gʻ for the o-with-stroke and gain sounds
        assert to_cyrillic("oʻzbek") == "ўзбек"


class TestToLatin:
    """Cyrillic → Latin conversion."""

    def test_simple_greeting(self) -> None:
        assert to_latin("Ассалому алайкум") == "Assalomu alaykum"

    def test_basic_word(self) -> None:
        assert to_latin("китоб") == "kitob"

    def test_o_with_stroke(self) -> None:
        assert to_latin("ўзбек") == "oʻzbek"

    def test_empty_string(self) -> None:
        assert to_latin("") == ""

    def test_non_cyrillic_passes_through(self) -> None:
        result = to_latin("hello 2026")
        assert "2026" in result


class TestTransliterate:
    """Dispatcher function."""

    @pytest.mark.parametrize(
        ("text", "direction", "expected"),
        [
            ("kitob", "cyrillic", "китоб"),
            ("китоб", "latin", "kitob"),
            ("", "cyrillic", ""),
            ("", "latin", ""),
        ],
    )
    def test_valid_directions(self, text: str, direction: str, expected: str) -> None:
        assert transliterate(text, direction) == expected  # type: ignore[arg-type]

    def test_invalid_direction_raises(self) -> None:
        with pytest.raises(ValueError, match="invalid to_variant"):
            transliterate("kitob", "klingon")  # type: ignore[arg-type]


class TestRoundTrip:
    """Latin → Cyrillic → Latin is not always lossless (intentional)."""

    def test_stable_word(self) -> None:
        # "kitob" is unambiguous in both directions
        assert to_latin(to_cyrillic("kitob")) == "kitob"

    def test_lexicon_word_roundtrip(self) -> None:
        # "abzats" (абзац) — one-way mapping, but the lexicon ensures
        # the Cyrillic ц converts back to ts, giving "abzats"
        result = to_latin(to_cyrillic("abzats"))
        assert result in ("abzats",)
