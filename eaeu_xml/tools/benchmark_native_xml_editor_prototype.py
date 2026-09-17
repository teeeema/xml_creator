"""Benchmark the integrated QPlainTextEdit/ViewModel prototype."""

from __future__ import annotations

import argparse
import json
import statistics
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from PySide6.QtCore import QEventLoop, QPropertyAnimation, QTimer
from PySide6.QtGui import QTextCursor
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditor, NativeXmlEditorBinding
from eaeu_xml.gui_qt.view_model import GuiViewModel


DEFAULT_LINES = (1_000, 5_000, 10_000, 25_000, 50_000)


@dataclass(frozen=True)
class Measurement:
    lines: int
    load_ms: float
    scroll_wall_ms: float
    scroll_cpu_ms: float
    typing_ms: float
    selection_ms: float
    navigation_ms: float
    sync_ms: float
    viewmodel_calls_during_scroll: int


def make_document(lines: int) -> str:
    return "\n".join(f'<item id="{index:06d}">value-{index:06d}</item>' for index in range(lines))


def drain(app: QApplication, cycles: int = 3) -> None:
    for _ in range(cycles):
        app.processEvents()


def timed(callable_):
    wall = time.perf_counter()
    cpu = time.process_time()
    callable_()
    return (time.perf_counter() - wall) * 1000, (time.process_time() - cpu) * 1000


def run_animation(animation: QPropertyAnimation) -> None:
    loop = QEventLoop()
    timeout = QTimer()
    timeout.setSingleShot(True)
    timeout.timeout.connect(loop.quit)
    animation.finished.connect(loop.quit)
    timeout.start(1500)
    animation.start()
    loop.exec()
    animation.stop()


class IntegratedNativeBenchmark:
    def __init__(self, app: QApplication, processes_root: Path) -> None:
        self.app = app
        self.model = GuiViewModel(processes_root)
        self.editor = NativeXmlEditor(debounce_ms=3_600_000)
        self.editor.resize(1200, 700)
        self.binding = NativeXmlEditorBinding(self.editor, self.model)
        self.editor.show()
        drain(app)

    def close(self) -> None:
        self.editor.close()
        self.editor.deleteLater()
        drain(self.app)

    def _scroll(self) -> None:
        bar = self.editor.verticalScrollBar()
        bar.setValue(bar.minimum())
        drain(self.app)
        animation = QPropertyAnimation(bar, b"value")
        animation.setStartValue(bar.minimum())
        animation.setEndValue(bar.maximum())
        animation.setDuration(600)
        run_animation(animation)

    def measure(self, line_count: int) -> Measurement:
        document = make_document(line_count)

        def load():
            self.model.setXml(document)
            drain(self.app, 5)

        load_ms, _ = timed(load)

        changed_calls = []
        self.model.changed.connect(lambda: changed_calls.append(1))
        changed_calls.clear()
        scroll_wall_ms, scroll_cpu_ms = timed(self._scroll)
        scroll_model_calls = len(changed_calls)

        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()
        drain(self.app)
        typing_ms, _ = timed(lambda: QTest.keyClicks(self.editor, "diagnostic"))
        drain(self.app)

        length = self.editor.document().characterCount() - 1
        positions = [int(length * fraction / 20) for fraction in range(1, 20)]

        def select_ranges():
            local = self.editor.textCursor()
            for position in positions:
                local.setPosition(position)
                local.setPosition(min(position + 32, length), QTextCursor.MoveMode.KeepAnchor)
                self.editor.setTextCursor(local)
                self.app.processEvents()

        selection_ms, _ = timed(select_ranges)
        navigation_ms, _ = timed(lambda: self.editor.go_to_position(max(1, line_count // 2), 6))
        sync_ms, _ = timed(self.editor.flush)

        return Measurement(
            line_count,
            load_ms,
            scroll_wall_ms,
            scroll_cpu_ms,
            typing_ms,
            selection_ms,
            navigation_ms,
            sync_ms,
            scroll_model_calls,
        )


def median(items: list[Measurement]) -> Measurement:
    first = items[0]
    fields = (
        "load_ms", "scroll_wall_ms", "scroll_cpu_ms", "typing_ms", "selection_ms",
        "navigation_ms", "sync_ms", "viewmodel_calls_during_scroll",
    )
    values = {name: statistics.median(getattr(item, name) for item in items) for name in fields}
    return Measurement(first.lines, **values)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--processes-root", type=Path, default=Path(__file__).parents[1] / "tests" / "fixtures")
    parser.add_argument("--lines", type=int, nargs="+", default=DEFAULT_LINES)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    app = QApplication.instance() or QApplication([])
    benchmark = IntegratedNativeBenchmark(app, args.processes_root)
    results = []
    try:
        for line_count in args.lines:
            result = median([benchmark.measure(line_count) for _ in range(args.repeats)])
            results.append(result)
            print(json.dumps(asdict(result), ensure_ascii=False))
    finally:
        benchmark.close()

    if args.json:
        args.json.write_text(
            json.dumps({"repeats": args.repeats, "results": [asdict(item) for item in results]}, indent=2),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
