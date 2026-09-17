"""Compare the current QML XML editor with QPlainTextEdit on large documents.

This is a diagnostic prototype only.  It is intentionally not wired into the
application UI.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from PySide6.QtCore import Q_ARG, QEventLoop, QMetaObject, QPropertyAnimation, QTimer, Qt
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtQuick import QQuickView
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtWidgets import QApplication, QPlainTextEdit

from eaeu_xml.gui_qt.fonts import fixed_font_family


DEFAULT_LINES = (1_000, 5_000, 10_000, 25_000, 50_000)
VIEWPORT_SIZE = (1200, 700)


@dataclass(frozen=True)
class Measurement:
    editor: str
    lines: int
    load_ms: float
    scroll_wall_ms: float
    scroll_cpu_ms: float
    cursor_ms: float
    typing_ms: float
    selection_ms: float
    scroll_layout_changes: int = 0
    scroll_content_y_changes: int = 0


def make_document(line_count: int) -> str:
    return "\n".join(
        f'<item id="{index:06d}">value-{index:06d}</item>'
        for index in range(line_count)
    )


def timed(callable_):
    wall_start = time.perf_counter()
    cpu_start = time.process_time()
    callable_()
    return (
        (time.perf_counter() - wall_start) * 1_000,
        (time.process_time() - cpu_start) * 1_000,
    )


def drain_events(app: QApplication, cycles: int = 3) -> None:
    for _ in range(cycles):
        app.processEvents()


def run_loop_for_animation(animation: QPropertyAnimation, timeout_ms: int = 1_500) -> None:
    loop = QEventLoop()
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(loop.quit)
    animation.finished.connect(loop.quit)
    timer.start(timeout_ms)
    animation.start()
    loop.exec()
    animation.stop()


class QmlEditorBenchmark:
    name = "QML_TextArea"

    def __init__(self, app: QApplication, qml_path: Path, family: str) -> None:
        self.app = app
        self.view = QQuickView()
        self.view.rootContext().setContextProperty("fixedFontFamily", family)
        self.view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
        self.view.resize(*VIEWPORT_SIZE)
        self.view.setSource(qml_path.resolve().as_uri())
        if self.view.status() != QQuickView.Status.Ready:
            raise RuntimeError("; ".join(error.toString() for error in self.view.errors()))
        self.view.show()
        drain_events(app)
        self.root = self.view.rootObject()
        self.root.setProperty("syncInterval", 3_600_000)
        self.editor = self.root.findChild(type(self.root), "xmlEditor")
        self.viewport = self.root.findChild(type(self.root), "xmlEditorViewport")
        if self.editor is None or self.viewport is None:
            raise RuntimeError("XmlTextEditor benchmark objects were not found")

    def close(self) -> None:
        self.view.close()
        self.view.deleteLater()
        drain_events(self.app)

    def _set_document(self, document: str) -> None:
        self.root.setProperty("updatingFromModel", True)
        self.editor.setProperty("text", document)
        self.root.setProperty("updatingFromModel", False)
        self.root.setProperty("syncPending", False)
        drain_events(self.app, 5)

    def _flick_scroll(self) -> None:
        maximum = max(
            0.0,
            float(self.viewport.property("contentHeight")) - float(self.viewport.property("height")),
        )
        self.viewport.setProperty("contentY", 0.0)
        drain_events(self.app)
        animation = QPropertyAnimation(self.viewport, b"contentY")
        animation.setStartValue(0.0)
        animation.setEndValue(maximum)
        animation.setDuration(600)
        run_loop_for_animation(animation)

    def _instrument_scroll(self) -> tuple[int, int]:
        layout_changes = 0
        content_y_changes = 0
        previous_geometry = None
        previous_y = None

        def sample():
            nonlocal layout_changes, content_y_changes, previous_geometry, previous_y
            geometry = (
                self.editor.property("width"),
                self.editor.property("height"),
                self.editor.property("contentWidth"),
                self.editor.property("contentHeight"),
            )
            content_y = self.viewport.property("contentY")
            if previous_geometry is not None and geometry != previous_geometry:
                layout_changes += 1
            if previous_y is not None and content_y != previous_y:
                content_y_changes += 1
            previous_geometry = geometry
            previous_y = content_y

        sampler = QTimer()
        sampler.setInterval(0)
        sampler.timeout.connect(sample)
        sample()
        sampler.start()
        self._flick_scroll()
        sampler.stop()
        sample()
        return layout_changes, content_y_changes

    def measure(self, line_count: int) -> Measurement:
        document = make_document(line_count)
        load_ms, _ = timed(lambda: self._set_document(document))

        scroll_wall_ms, scroll_cpu_ms = timed(self._flick_scroll)
        layout_changes, content_y_changes = self._instrument_scroll()

        length = len(document)
        positions = [int(length * fraction / 20) for fraction in range(1, 20)]

        def move_cursor():
            for position in positions:
                self.editor.setProperty("cursorPosition", position)
                self.app.processEvents()

        cursor_ms, _ = timed(move_cursor)

        self.editor.setProperty("cursorPosition", length)
        self.editor.forceActiveFocus()
        drain_events(self.app)

        def type_text():
            position = length
            for character in "diagnostic":
                QMetaObject.invokeMethod(
                    self.editor,
                    "insert",
                    Qt.ConnectionType.DirectConnection,
                    Q_ARG(int, position),
                    Q_ARG(str, character),
                )
                position += 1
                self.app.processEvents()

        typing_ms, _ = timed(type_text)
        drain_events(self.app)

        def select_ranges():
            for position in positions:
                self.editor.setProperty("cursorPosition", position)
                QMetaObject.invokeMethod(
                    self.editor,
                    "select",
                    Qt.ConnectionType.DirectConnection,
                    Q_ARG(int, position),
                    Q_ARG(int, min(position + 32, len(self.editor.property("text")))),
                )
                self.app.processEvents()

        selection_ms, _ = timed(select_ranges)
        return Measurement(
            self.name,
            line_count,
            load_ms,
            scroll_wall_ms,
            scroll_cpu_ms,
            cursor_ms,
            typing_ms,
            selection_ms,
            layout_changes,
            content_y_changes,
        )


class PlainTextEditorBenchmark:
    name = "QPlainTextEdit"

    def __init__(self, app: QApplication, family: str) -> None:
        self.app = app
        self.editor = QPlainTextEdit()
        self.editor.resize(*VIEWPORT_SIZE)
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        font = QFont(family)
        font.setPixelSize(14)
        self.editor.setFont(font)
        self.editor.show()
        drain_events(app)

    def close(self) -> None:
        self.editor.close()
        self.editor.deleteLater()
        drain_events(self.app)

    def _scroll(self) -> None:
        bar = self.editor.verticalScrollBar()
        bar.setValue(bar.minimum())
        drain_events(self.app)
        animation = QPropertyAnimation(bar, b"value")
        animation.setStartValue(bar.minimum())
        animation.setEndValue(bar.maximum())
        animation.setDuration(600)
        run_loop_for_animation(animation)

    def _instrument_scroll(self) -> tuple[int, int]:
        layout_changes = 0
        scroll_value_changes = 0
        previous_geometry = None
        previous_value = None
        bar = self.editor.verticalScrollBar()

        def sample():
            nonlocal layout_changes, scroll_value_changes, previous_geometry, previous_value
            geometry = (
                self.editor.viewport().size().width(),
                self.editor.viewport().size().height(),
                self.editor.document().size().width(),
                self.editor.document().size().height(),
            )
            value = bar.value()
            if previous_geometry is not None and geometry != previous_geometry:
                layout_changes += 1
            if previous_value is not None and value != previous_value:
                scroll_value_changes += 1
            previous_geometry = geometry
            previous_value = value

        sampler = QTimer()
        sampler.setInterval(0)
        sampler.timeout.connect(sample)
        sample()
        sampler.start()
        self._scroll()
        sampler.stop()
        sample()
        return layout_changes, scroll_value_changes

    def measure(self, line_count: int) -> Measurement:
        document = make_document(line_count)

        def load():
            self.editor.setPlainText(document)
            drain_events(self.app, 5)

        load_ms, _ = timed(load)
        scroll_wall_ms, scroll_cpu_ms = timed(self._scroll)
        layout_changes, scroll_value_changes = self._instrument_scroll()

        length = len(document)
        positions = [int(length * fraction / 20) for fraction in range(1, 20)]

        def move_cursor():
            cursor = self.editor.textCursor()
            for position in positions:
                cursor.setPosition(position)
                self.editor.setTextCursor(cursor)
                self.app.processEvents()

        cursor_ms, _ = timed(move_cursor)

        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()
        drain_events(self.app)

        def type_text():
            cursor = self.editor.textCursor()
            for character in "diagnostic":
                cursor.insertText(character)
                self.editor.setTextCursor(cursor)
                self.app.processEvents()

        typing_ms, _ = timed(type_text)
        drain_events(self.app)

        def select_ranges():
            cursor = self.editor.textCursor()
            for position in positions:
                cursor.setPosition(position)
                cursor.setPosition(min(position + 32, self.editor.document().characterCount() - 1), QTextCursor.MoveMode.KeepAnchor)
                self.editor.setTextCursor(cursor)
                self.app.processEvents()

        selection_ms, _ = timed(select_ranges)
        return Measurement(
            self.name,
            line_count,
            load_ms,
            scroll_wall_ms,
            scroll_cpu_ms,
            cursor_ms,
            typing_ms,
            selection_ms,
            layout_changes,
            scroll_value_changes,
        )


def median_measurements(items: list[Measurement]) -> Measurement:
    first = items[0]
    numeric_fields = (
        "load_ms",
        "scroll_wall_ms",
        "scroll_cpu_ms",
        "cursor_ms",
        "typing_ms",
        "selection_ms",
        "scroll_layout_changes",
        "scroll_content_y_changes",
    )
    values = {field: statistics.median(getattr(item, field) for item in items) for field in numeric_fields}
    return Measurement(first.editor, first.lines, **values)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--lines", type=int, nargs="+", default=DEFAULT_LINES)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    QQuickStyle.setStyle("Basic")
    app = QApplication.instance() or QApplication([])
    family = fixed_font_family()
    qml_path = Path(__file__).parents[1] / "src" / "eaeu_xml" / "gui_qt" / "qml" / "components" / "XmlTextEditor.qml"

    results: list[Measurement] = []
    for benchmark_type in (QmlEditorBenchmark, PlainTextEditorBenchmark):
        benchmark = benchmark_type(app, qml_path, family) if benchmark_type is QmlEditorBenchmark else benchmark_type(app, family)
        try:
            for line_count in args.lines:
                samples = [benchmark.measure(line_count) for _ in range(args.repeats)]
                result = median_measurements(samples)
                results.append(result)
                print(json.dumps(asdict(result), ensure_ascii=False))
        finally:
            benchmark.close()

    payload = {
        "platform": os.environ.get("QT_QPA_PLATFORM", "native"),
        "fixed_font_family": family,
        "repeats": args.repeats,
        "results": [asdict(result) for result in results],
    }
    if args.json:
        args.json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
