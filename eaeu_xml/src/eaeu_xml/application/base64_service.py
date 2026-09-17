"""Independent Base64 utility service."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EncodedFile:
    name: str
    source_size: int
    text: str

    @property
    def encoded_size(self) -> int:
        return len(self.text)


@dataclass(frozen=True)
class DecodedData:
    data: bytes
    format_hint: str = ""


class Base64Service:
    """Convert bytes/files to standard Base64 and back."""

    @staticmethod
    def encode_bytes(data: bytes) -> str:
        return base64.b64encode(data).decode("ascii")

    def encode_file(self, path: str | Path) -> EncodedFile:
        source = Path(path)
        data = source.read_bytes()
        return EncodedFile(source.name, len(data), self.encode_bytes(data))

    @staticmethod
    def _normalized_input(value: str) -> bytes:
        try:
            return "".join(str(value).split()).encode("ascii")
        except UnicodeEncodeError as error:
            raise ValueError("Base64 содержит недопустимые символы.") from error

    @staticmethod
    def _format_hint(data: bytes) -> str:
        signatures = (
            (b"%PDF-", "PDF"),
            (b"PK\x03\x04", "ZIP"),
            (b"\x89PNG\r\n\x1a\n", "PNG"),
            (b"\xff\xd8\xff", "JPEG"),
            (b"GIF87a", "GIF"),
            (b"GIF89a", "GIF"),
        )
        return next((name for signature, name in signatures if data.startswith(signature)), "")

    def decode_text(self, value: str) -> DecodedData:
        normalized = self._normalized_input(value)
        try:
            data = base64.b64decode(normalized, validate=True)
        except (ValueError, base64.binascii.Error) as error:
            raise ValueError("Некорректный Base64: проверьте символы и padding '='.") from error
        return DecodedData(data, self._format_hint(data))

