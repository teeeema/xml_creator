"""Generic file-to-form-value conversion; no wx or process-specific knowledge."""

from base64 import b64decode, b64encode
from dataclasses import dataclass
import mimetypes
from pathlib import Path


DEFAULT_LARGE_FILE_WARNING_BYTES = 20 * 1024 * 1024


@dataclass(frozen=True)
class FileInputValue:
    value: str
    filename: str
    size: int
    media_type: str | None
    exceeds_warning_threshold: bool = False


class FileInputService:
    """Reads bytes once and produces the lexical base64 value used by BinaryTextType."""

    def __init__(self, warning_threshold: int = DEFAULT_LARGE_FILE_WARNING_BYTES):
        self.warning_threshold = warning_threshold

    def load(self, path: Path) -> FileInputValue:
        path = Path(path)
        payload = path.read_bytes()
        media_type = mimetypes.guess_type(path.name, strict=False)[0]
        return FileInputValue(
            b64encode(payload).decode("ascii"),
            path.name,
            len(payload),
            media_type,
            len(payload) > self.warning_threshold,
        )

    @staticmethod
    def restored(value: str) -> FileInputValue:
        try:
            size = len(b64decode(value, validate=True))
        except (ValueError, TypeError):
            size = 0
        return FileInputValue(value, "Вложение из черновика", size, None, False)
