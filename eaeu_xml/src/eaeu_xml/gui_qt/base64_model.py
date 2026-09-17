"""Qt presentation model for the independent Base64 utility."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from PySide6.QtCore import QObject, Property, QRunnable, QThreadPool, QTimer, Signal, Slot
from PySide6.QtGui import QGuiApplication

from eaeu_xml.application.base64_service import Base64Service, DecodedData, EncodedFile


BASE64_PREVIEW_THRESHOLD = 10_000
VISIBLE_PREFIX_LENGTH = 10


class _TaskRunnable(QRunnable):
    def __init__(self, work: Callable[[], object]) -> None:
        super().__init__()
        self.setAutoDelete(False)
        self.work = work
        self.result: object | None = None
        self.error = ""
        self.finished = False

    def run(self) -> None:
        try:
            self.result = self.work()
        except Exception as error:  # user-facing worker boundary
            self.error = str(error)
        finally:
            self.finished = True


class Base64UtilityModel(QObject):
    """Keep full payloads in Python and expose only presentation state to QML."""

    changed = Signal()
    operationFinished = Signal()

    def __init__(self, parent=None, *, service: Base64Service | None = None) -> None:
        super().__init__(parent)
        self.service = service or Base64Service()
        self._thread_pool = QThreadPool(self)
        self._thread_pool.setMaxThreadCount(1)
        self._task: _TaskRunnable | None = None
        self._done: Callable[[object], None] | None = None
        self._poll_timer = QTimer(self)
        self._poll_timer.setInterval(10)
        self._poll_timer.timeout.connect(self._poll_task)
        self._busy = False
        self._status = ""
        self._error = ""
        self._encoded_text = ""
        self._encoded_name = ""
        self._source_size = 0
        self._show_full = False
        self._decode_input = ""
        self._decoded_data = b""
        self._decoded_hint = ""
        self._has_decoded_result = False

    def _notify(self) -> None:
        self.changed.emit()

    def _start(self, status: str, work: Callable[[], object], done: Callable[[object], None]) -> None:
        if self._busy:
            return
        self._busy = True
        self._status = status
        self._error = ""
        self._notify()
        self._done = done
        self._task = _TaskRunnable(work)
        self._thread_pool.start(self._task)
        self._poll_timer.start()

    @Slot()
    def _poll_task(self) -> None:
        task = self._task
        if task is None or not task.finished:
            return
        self._poll_timer.stop()
        self._busy = False
        done = self._done
        self._task = None
        self._done = None
        if task.error:
            self._status = ""
            self._error = task.error
        else:
            try:
                if done is not None:
                    done(task.result)
            except Exception as error:
                self._status = ""
                self._error = str(error)
        self._notify()
        self.operationFinished.emit()

    @Property(bool, notify=changed)
    def busy(self) -> bool:
        return self._busy

    @Property(str, notify=changed)
    def status(self) -> str:
        return self._status

    @Property(str, notify=changed)
    def error(self) -> str:
        return self._error

    @Property(str, notify=changed)
    def encodedFileName(self) -> str:  # noqa: N802
        return self._encoded_name

    @Property(int, notify=changed)
    def sourceSize(self) -> int:  # noqa: N802
        return self._source_size

    @Property(int, notify=changed)
    def encodedSize(self) -> int:  # noqa: N802
        return len(self._encoded_text)

    @Property(bool, notify=changed)
    def canTogglePreview(self) -> bool:  # noqa: N802
        return len(self._encoded_text) > BASE64_PREVIEW_THRESHOLD

    @Property(bool, notify=changed)
    def showingFullPreview(self) -> bool:  # noqa: N802
        return self._show_full

    @Property(str, notify=changed)
    def encodedPreview(self) -> str:  # noqa: N802
        if self._show_full or len(self._encoded_text) <= BASE64_PREVIEW_THRESHOLD:
            return self._encoded_text
        hidden = len(self._encoded_text) - VISIBLE_PREFIX_LENGTH
        return f"{self._encoded_text[:VISIBLE_PREFIX_LENGTH]}… ⟪скрыто {hidden:,} символов⟫".replace(",", " ")

    @Property(str, notify=changed)
    def decodeInput(self) -> str:  # noqa: N802
        return self._decode_input

    @Property(int, notify=changed)
    def decodedSize(self) -> int:  # noqa: N802
        return len(self._decoded_data)

    @Property(str, notify=changed)
    def decodedFormatHint(self) -> str:  # noqa: N802
        return self._decoded_hint

    @Property(bool, notify=changed)
    def hasDecodedResult(self) -> bool:  # noqa: N802
        return self._has_decoded_result

    @Slot(str)
    def encodeFile(self, path: str) -> None:  # noqa: N802
        self._start("Кодирование...", lambda: self.service.encode_file(path), self._encoded_ready)

    def _encoded_ready(self, result: object) -> None:
        encoded = result
        if not isinstance(encoded, EncodedFile):
            raise TypeError("Неожиданный результат кодирования.")
        self._encoded_name = encoded.name
        self._source_size = encoded.source_size
        self._encoded_text = encoded.text
        self._show_full = False
        self._status = "Кодирование завершено."

    @Slot()
    def togglePreview(self) -> None:  # noqa: N802
        if self.canTogglePreview:
            self._show_full = not self._show_full
            self._notify()

    @Slot()
    def copyBase64(self) -> None:  # noqa: N802
        QGuiApplication.clipboard().setText(self._encoded_text)
        self._status = "Полный Base64 скопирован."
        self._error = ""
        self._notify()

    @Slot(str)
    def saveBase64(self, path: str) -> None:  # noqa: N802
        text = self._encoded_text
        self._start(
            "Сохранение...",
            lambda: Path(path).write_text(text, encoding="ascii"),
            lambda _result: self._set_status("Base64 сохранён."),
        )

    def _set_status(self, value: str) -> None:
        self._status = value

    @Slot()
    def clearEncode(self) -> None:  # noqa: N802
        if self._busy:
            return
        self._encoded_text = ""
        self._encoded_name = ""
        self._source_size = 0
        self._show_full = False
        self._status = ""
        self._error = ""
        self._notify()

    @Slot(str)
    def setDecodeInput(self, value: str) -> None:  # noqa: N802
        if value != self._decode_input:
            self._decode_input = str(value)
            self._decoded_data = b""
            self._decoded_hint = ""
            self._has_decoded_result = False
            self._error = ""
            self._notify()

    @Slot(str)
    def openBase64(self, path: str) -> None:  # noqa: N802
        self._start(
            "Открытие Base64...",
            lambda: Path(path).read_text(encoding="utf-8"),
            self._opened_base64,
        )

    def _opened_base64(self, result: object) -> None:
        self._decode_input = str(result)
        self._decoded_data = b""
        self._decoded_hint = ""
        self._has_decoded_result = False
        self._status = "Base64 открыт."

    @Slot()
    def decode(self) -> None:
        value = self._decode_input
        self._start("Декодирование...", lambda: self.service.decode_text(value), self._decoded_ready)

    def _decoded_ready(self, result: object) -> None:
        decoded = result
        if not isinstance(decoded, DecodedData):
            raise TypeError("Неожиданный результат декодирования.")
        self._decoded_data = decoded.data
        self._decoded_hint = decoded.format_hint
        self._has_decoded_result = True
        self._status = "Декодирование завершено."

    @Slot(str)
    def saveDecoded(self, path: str) -> None:  # noqa: N802
        if not self._has_decoded_result:
            self._status = ""
            self._error = "Сначала декодируйте Base64."
            self._notify()
            return
        data = self._decoded_data
        self._start(
            "Сохранение...",
            lambda: Path(path).write_bytes(data),
            lambda _result: self._set_status("Файл сохранён."),
        )

    @Slot()
    def clearDecode(self) -> None:  # noqa: N802
        if self._busy:
            return
        self._decode_input = ""
        self._decoded_data = b""
        self._decoded_hint = ""
        self._has_decoded_result = False
        self._status = ""
        self._error = ""
        self._notify()

    # Test-only read access; never exposed as a QML Property.
    def full_encoded_text(self) -> str:
        return self._encoded_text

    def decoded_bytes(self) -> bytes:
        return self._decoded_data
