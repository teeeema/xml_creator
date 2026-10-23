"""Presentation-only cleanup for text extracted from normative documents.

The helpers in this module never mutate source/package data.  They only prepare
strings for human-facing GUI surfaces.
"""

from __future__ import annotations

import re
import unicodedata


_PARSER_SPILLOVER = re.compile(r"\s*<PARSED TEXT FOR PAGE\b.*$", re.IGNORECASE | re.DOTALL)
_INVISIBLE_EXTRACTION_ARTIFACTS = {"\u00ad", "\u200b", "\u2060", "\ufeff"}


def is_unicode_noncharacter(character: str) -> bool:
    """Return whether *character* is one of Unicode's reserved noncharacters."""
    codepoint = ord(character)
    return 0xFDD0 <= codepoint <= 0xFDEF or (codepoint & 0xFFFF) in {0xFFFE, 0xFFFF}


def _wordlike(character: str | None) -> bool:
    return bool(character and (character.isalnum() or character == "_"))


def _artifact_run_replacement(left: str | None, right: str | None) -> str:
    # U+FFFE commonly replaced a hyphen during PDF extraction in OP22.  Only
    # restore a hyphen when it is between word/regex token characters; in other
    # contexts dropping the invalid code point is safer than inventing syntax.
    return "-" if _wordlike(left) and _wordlike(right) else ""


def sanitize_presentation_text(value: object | None) -> str:
    """Return a GUI-safe representation without changing the source value.

    This removes known parser spillover, Unicode noncharacters, replacement
    characters that reached the parsed source, unsafe controls and invisible
    extraction artifacts.  Normal regex/XML punctuation is left untouched.
    """
    if value is None:
        return ""
    text = _PARSER_SPILLOVER.sub("", str(value))
    result: list[str] = []
    index = 0
    while index < len(text):
        character = text[index]

        if is_unicode_noncharacter(character) or character == "\ufffd":
            start = index
            while index < len(text) and (
                is_unicode_noncharacter(text[index]) or text[index] == "\ufffd"
            ):
                index += 1
            left = text[start - 1] if start else None
            right = text[index] if index < len(text) else None
            result.append(_artifact_run_replacement(left, right))
            continue

        if character in _INVISIBLE_EXTRACTION_ARTIFACTS:
            index += 1
            continue

        category = unicodedata.category(character)
        if character == "\r":
            # Normalize CR and CRLF without creating duplicate newlines.
            result.append("\n")
            if index + 1 < len(text) and text[index + 1] == "\n":
                index += 2
            else:
                index += 1
            continue
        if category == "Cc" and character not in {"\n", "\t"}:
            result.append(" ")
            index += 1
            continue
        if category in {"Zl", "Zp"}:
            result.append("\n")
            index += 1
            continue
        if category == "Zs" and character != " ":
            result.append(" ")
            index += 1
            continue

        result.append(character)
        index += 1

    return "".join(result).strip()


def has_presentation_garbage(value: object | None) -> bool:
    """Detect artifacts that must never reach the normal GUI."""
    if value is None:
        return False
    text = str(value)
    if "<PARSED TEXT FOR PAGE" in text.upper():
        return True
    for character in text:
        if is_unicode_noncharacter(character) or character == "\ufffd":
            return True
        if character in _INVISIBLE_EXTRACTION_ARTIFACTS:
            return True
        category = unicodedata.category(character)
        if category == "Cc" and character not in {"\n", "\r", "\t"}:
            return True
        if category in {"Zl", "Zp"}:
            return True
    return False


def normalize_extracted_regex(pattern: object | None) -> str:
    """Normalize regex text when the readable source proves spaces are artifacts.

    OP22's readable RTF contains no significant whitespace in its ``Шаблон``
    values.  The old PDF extraction introduced spaces inside ranges and before
    tokens, and sometimes appended table multiplicity/next-row text.  This
    helper is intentionally used only for that source-verified presentation
    path.
    """
    value = sanitize_presentation_text(pattern)
    if not value:
        return ""
    # Old table extraction can append the current row multiplicity followed by
    # the next row.  Multiplicity is not part of any OP22 RTF regex.
    value = re.split(r"\s+(?:0|1)(?:\.\.(?:1|\*))?(?=\s|$)", value, maxsplit=1)[0]
    return re.sub(r"\s+", "", value)
