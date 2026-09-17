"""Presentation-only compact view for XML documents with very large text nodes.

The full XML string is always the source of truth.  Compact XML is only a GUI
representation and may never be passed to application/domain services.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import re
import string
from xml.parsers import expat


LARGE_TEXT_THRESHOLD = 10_000
ENCODED_PAYLOAD_THRESHOLD = 200
VISIBLE_PREFIX_LENGTH = 10
ENCODED_PAYLOAD_MIN_ALLOWED_RATIO = 0.97
ENCODED_PAYLOAD_MAX_WHITESPACE_RATIO = 0.03


class CompactSyncError(ValueError):
    """Raised when a compact edit cannot be mapped back to full XML safely."""


@dataclass(frozen=True)
class ProtectedMarker:
    """Current character range of a protected placeholder in compact text."""

    node_id: str
    start: int
    end: int


@dataclass(frozen=True)
class HiddenTextNode:
    """Exact raw payload plus its current full/compact character ranges."""

    node_id: str
    payload: str
    character_count: int
    kind: str
    full_start: int
    full_end: int
    display_start: int
    display_end: int
    placeholder: str


@dataclass(frozen=True)
class _TextSpan:
    start: int
    end: int
    kind: str
    character_count: int


_ENTITY = re.compile(r"&(?:amp|lt|gt|quot|apos|#\d+|#x[0-9A-Fa-f]+);")
_PLACEHOLDER_PATTERN = re.compile(r"⟪скрыто [0-9 ]+ символов⟫")
_ENCODED_PAYLOAD_CHARACTERS = frozenset(
    string.ascii_letters + string.digits + "+/=-_"
)


def _normalized_literal_length(value: str) -> int:
    """XML parsers normalize CR/LF pairs and lone CR characters to LF."""

    return len(value.replace("\r\n", "\n").replace("\r", "\n"))


def _xml_text_length(raw: str) -> int:
    """Count XML text characters, decoding the five/numeric XML references.

    Unknown DTD-defined entities are deliberately counted as one serialized
    reference.  Their raw spelling is still preserved byte-for-character in the
    full XML and never reconstructed from decoded content.
    """

    total = 0
    cursor = 0
    for match in _ENTITY.finditer(raw):
        total += _normalized_literal_length(raw[cursor : match.start()])
        total += 1
        cursor = match.end()
    total += _normalized_literal_length(raw[cursor:])
    return total


def _xml_text_prefix(raw: str, length: int = VISIBLE_PREFIX_LENGTH) -> str:
    """Return serialized XML covering at most ``length`` text characters.

    Entity references count as one text character, but remain serialized in the
    presentation so compact XML stays syntactically valid.
    """

    if length <= 0:
        return ""
    index = 0
    visible = 0
    while index < len(raw) and visible < length:
        if raw[index] == "&":
            entity = _ENTITY.match(raw, index)
            if entity is not None:
                index = entity.end()
                visible += 1
                continue
        if raw.startswith("\r\n", index):
            index += 2
        else:
            index += 1
        visible += 1
    return raw[:index]


def _looks_like_encoded_payload(raw: str, character_count: int) -> bool:
    """Presentation heuristic for Base64/Base64URL-like element text.

    Successful decoding is intentionally not required.  Natural-language text
    is protected from false positives by requiring an overwhelmingly encoded
    alphabet and very little whitespace.
    """

    if character_count < ENCODED_PAYLOAD_THRESHOLD or not raw:
        return False

    normalized = raw.replace("\r\n", "\n").replace("\r", "\n")
    total = len(normalized)
    if total < ENCODED_PAYLOAD_THRESHOLD:
        return False

    allowed = sum(char in _ENCODED_PAYLOAD_CHARACTERS for char in normalized)
    whitespace = sum(char.isspace() for char in normalized)
    return (
        allowed / total >= ENCODED_PAYLOAD_MIN_ALLOWED_RATIO
        and whitespace / total <= ENCODED_PAYLOAD_MAX_WHITESPACE_RATIO
    )


def _find_markup_end(text: str, start: int) -> int:
    quote = ""
    for index in range(start + 1, len(text)):
        char = text[index]
        if quote:
            if char == quote:
                quote = ""
        elif char in {"'", '"'}:
            quote = char
        elif char == ">":
            return index
    raise CompactSyncError("Незавершённая XML-конструкция.")


def _find_doctype_end(text: str, start: int) -> int:
    quote = ""
    bracket_depth = 0
    for index in range(start + 2, len(text)):
        char = text[index]
        if quote:
            if char == quote:
                quote = ""
            continue
        if char in {"'", '"'}:
            quote = char
        elif char == "[":
            bracket_depth += 1
        elif char == "]" and bracket_depth:
            bracket_depth -= 1
        elif char == ">" and bracket_depth == 0:
            return index
    raise CompactSyncError("Незавершённый DOCTYPE.")


def _scan_text_spans(text: str) -> tuple[_TextSpan, ...]:
    """Locate serialized element text/CDATA spans without rewriting XML."""

    spans: list[_TextSpan] = []
    index = 0
    depth = 0
    length = len(text)
    while index < length:
        if text[index] != "<":
            end = text.find("<", index)
            if end < 0:
                end = length
            if depth > 0 and end > index:
                raw = text[index:end]
                spans.append(_TextSpan(index, end, "text", _xml_text_length(raw)))
            index = end
            continue

        if text.startswith("<!--", index):
            end = text.find("-->", index + 4)
            if end < 0:
                raise CompactSyncError("Незавершённый XML-комментарий.")
            index = end + 3
            continue

        if text.startswith("<![CDATA[", index):
            content_start = index + len("<![CDATA[")
            content_end = text.find("]]>", content_start)
            if content_end < 0:
                raise CompactSyncError("Незавершённый CDATA-раздел.")
            if depth > 0:
                raw = text[content_start:content_end]
                spans.append(
                    _TextSpan(
                        content_start,
                        content_end,
                        "cdata",
                        _normalized_literal_length(raw),
                    )
                )
            index = content_end + 3
            continue

        if text.startswith("<?", index):
            end = text.find("?>", index + 2)
            if end < 0:
                raise CompactSyncError("Незавершённая XML processing instruction.")
            index = end + 2
            continue

        if text.startswith("<!DOCTYPE", index):
            index = _find_doctype_end(text, index) + 1
            continue

        end = _find_markup_end(text, index)
        markup = text[index : end + 1]
        if markup.startswith("</"):
            depth = max(0, depth - 1)
        elif not markup.startswith("<!") and not markup.rstrip().endswith("/>"):
            depth += 1
        index = end + 1
    return tuple(spans)


def _validate_xml(text: str) -> None:
    parser = expat.ParserCreate()
    try:
        parser.Parse(text, True)
    except expat.ExpatError as error:
        raise CompactSyncError(str(error)) from error


def _placeholder(payload: str, character_count: int, kind: str) -> str:
    if kind == "text":
        prefix = _xml_text_prefix(payload)
    else:
        prefix = payload[:VISIBLE_PREFIX_LENGTH]
    hidden_count = max(0, character_count - VISIBLE_PREFIX_LENGTH)
    hidden = f"{hidden_count:,}".replace(",", " ")
    return f"{prefix}… ⟪скрыто {hidden} символов⟫"


class XmlDisplayDocument:
    """Keep full XML separate from the compact text rendered by Qt."""

    def __init__(self, full_xml: str = "", *, threshold: int = LARGE_TEXT_THRESHOLD) -> None:
        self.threshold = int(threshold)
        self.full_xml = ""
        self.compact_xml = ""
        self.hidden_nodes: tuple[HiddenTextNode, ...] = ()
        self.parse_error = ""
        self.set_full_xml(full_xml)

    @property
    def has_large_nodes(self) -> bool:
        return bool(self.hidden_nodes)

    def set_full_xml(self, full_xml: str) -> None:
        """Replace source of truth and rebuild a safe compact representation."""

        full_xml = str(full_xml)
        self.full_xml = full_xml
        self.compact_xml = full_xml
        self.hidden_nodes = ()
        self.parse_error = ""
        if not full_xml:
            return
        try:
            _validate_xml(full_xml)
            spans = _scan_text_spans(full_xml)
        except CompactSyncError as error:
            # Invalid XML remains fully editable in Original mode.  Compact mode
            # is deliberately unavailable because safe structural mapping cannot
            # be guaranteed.
            self.parse_error = str(error)
            return

        hidden_spans = [
            span
            for span in spans
            if span.character_count > self.threshold
            or _looks_like_encoded_payload(
                full_xml[span.start : span.end],
                span.character_count,
            )
        ]
        if not hidden_spans:
            return

        chunks: list[str] = []
        nodes: list[HiddenTextNode] = []
        full_cursor = 0
        display_cursor = 0
        for ordinal, span in enumerate(hidden_spans, 1):
            prefix = full_xml[full_cursor : span.start]
            chunks.append(prefix)
            display_cursor += len(prefix)
            payload = full_xml[span.start : span.end]
            placeholder = _placeholder(payload, span.character_count, span.kind)
            display_start = display_cursor
            chunks.append(placeholder)
            display_cursor += len(placeholder)
            nodes.append(
                HiddenTextNode(
                    node_id=f"large-text-{ordinal}",
                    payload=payload,
                    character_count=span.character_count,
                    kind=span.kind,
                    full_start=span.start,
                    full_end=span.end,
                    display_start=display_start,
                    display_end=display_cursor,
                    placeholder=placeholder,
                )
            )
            full_cursor = span.end
        chunks.append(full_xml[full_cursor:])
        self.full_xml = full_xml
        self.compact_xml = "".join(chunks)
        self.hidden_nodes = tuple(nodes)

    def protected_markers(self) -> tuple[ProtectedMarker, ...]:
        return tuple(
            ProtectedMarker(node.node_id, node.display_start, node.display_end)
            for node in self.hidden_nodes
        )

    def commit_compact(
        self,
        display_text: str,
        markers: tuple[ProtectedMarker, ...],
    ) -> str:
        """Safely apply ordinary compact edits while restoring exact payloads.

        Marker identity/ranges come from QTextDocument metadata rather than tag
        names or textual search.  Any ambiguity is rejected before full XML is
        replaced.
        """

        display_text = str(display_text)
        expected = {node.node_id: node for node in self.hidden_nodes}
        actual: dict[str, ProtectedMarker] = {}
        for marker in markers:
            if marker.node_id in actual:
                raise CompactSyncError("Защищённый marker продублирован.")
            actual[marker.node_id] = marker
        if set(actual) != set(expected):
            raise CompactSyncError(
                "Структура со скрытым большим объектом изменена. "
                "Переключитесь в режим оригинала для структурного редактирования."
            )

        marker_ranges = {(marker.start, marker.end) for marker in markers}
        placeholder_ranges = [
            (match.start(), match.end()) for match in _PLACEHOLDER_PATTERN.finditer(display_text)
        ]
        if any(
            not any(start <= placeholder_start and placeholder_end <= end for start, end in marker_ranges)
            for placeholder_start, placeholder_end in placeholder_ranges
        ):
            raise CompactSyncError(
                "Обнаружен немаркированный compact placeholder. "
                "Полный XML оставлен без изменений."
            )

        try:
            _validate_xml(display_text)
            text_spans = _scan_text_spans(display_text)
        except CompactSyncError as error:
            raise CompactSyncError(
                f"Compact XML временно некорректен: {error}. "
                "Полный XML оставлен без изменений."
            ) from error

        ordered: list[tuple[ProtectedMarker, HiddenTextNode]] = []
        last_end = -1
        for marker in sorted(markers, key=lambda item: item.start):
            node = expected[marker.node_id]
            if marker.start < 0 or marker.end > len(display_text) or marker.start >= marker.end:
                raise CompactSyncError("Повреждён диапазон защищённого placeholder.")
            if marker.start < last_end:
                raise CompactSyncError("Диапазоны защищённых placeholder пересекаются.")
            if display_text[marker.start : marker.end] != node.placeholder:
                raise CompactSyncError("Защищённый placeholder был изменён.")
            container = next(
                (
                    span
                    for span in text_spans
                    if span.start <= marker.start and marker.end <= span.end
                ),
                None,
            )
            if container is None or container.kind != node.kind:
                raise CompactSyncError(
                    "Большой объект перемещён в несовместимый XML-контекст. "
                    "Используйте режим оригинала."
                )
            ordered.append((marker, node))
            last_end = marker.end

        chunks: list[str] = []
        display_cursor = 0
        full_cursor = 0
        new_nodes: list[HiddenTextNode] = []
        for marker, node in ordered:
            prefix = display_text[display_cursor : marker.start]
            chunks.append(prefix)
            full_cursor += len(prefix)
            full_start = full_cursor
            chunks.append(node.payload)
            full_cursor += len(node.payload)
            new_nodes.append(
                replace(
                    node,
                    full_start=full_start,
                    full_end=full_cursor,
                    display_start=marker.start,
                    display_end=marker.end,
                )
            )
            display_cursor = marker.end
        chunks.append(display_text[display_cursor:])
        candidate = "".join(chunks)

        try:
            _validate_xml(candidate)
        except CompactSyncError as error:
            raise CompactSyncError(
                f"Изменение сделало полный XML некорректным: {error}. "
                "Последняя корректная полная версия сохранена."
            ) from error

        self.full_xml = candidate
        self.compact_xml = display_text
        self.hidden_nodes = tuple(new_nodes)
        self.parse_error = ""
        return candidate

    def full_position_to_display_position(self, full_position: int) -> int:
        position = max(0, min(int(full_position), len(self.full_xml)))
        removed = 0
        for node in sorted(self.hidden_nodes, key=lambda item: item.full_start):
            if position < node.full_start:
                break
            if node.full_start <= position < node.full_end:
                return node.display_start
            removed += len(node.payload) - len(node.placeholder)
        return max(0, position - removed)

    def full_line_column_to_display(self, line: int, column: int = 0) -> tuple[int, int]:
        """Map a full-XML diagnostic to compact line/column coordinates."""

        line = max(1, int(line))
        column = max(0, int(column))
        start = 0
        for _ in range(line - 1):
            newline = self.full_xml.find("\n", start)
            if newline < 0:
                start = len(self.full_xml)
                break
            start = newline + 1
        line_end = self.full_xml.find("\n", start)
        if line_end < 0:
            line_end = len(self.full_xml)
        zero_based_column = max(0, column - 1) if column else 0
        full_position = min(line_end, start + zero_based_column)
        display_position = self.full_position_to_display_position(full_position)
        display_line = self.compact_xml.count("\n", 0, display_position) + 1
        previous_newline = self.compact_xml.rfind("\n", 0, display_position)
        display_column = display_position - (previous_newline + 1) + 1
        return display_line, display_column
