"""End-to-end benchmark for the production hybrid XML editor shell."""

from __future__ import annotations

import argparse
import json
import statistics
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import QEventLoop, QPropertyAnimation, QTimer
from PySide6.QtGui import QTextCursor
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from eaeu_xml.gui_qt.production_window import ProductionMainWindow
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
    paste_ms: float
    format_ms: float
    validation_ms: float
    navigation_ms: float
    tab_switch_ms: float
    viewmodel_calls_during_scroll: int
    formatter_calls_during_scroll: int
    validator_calls_during_scroll: int
    parser_calls_during_scroll: int


def make_document(line_count: int) -> str:
    item_count = max(1, line_count - 2)
    body = "\n".join(
        f'<item id="{index:06d}">value-{index:06d}</item>'
        for index in range(item_count)
    )
    return f"<root>\n{body}\n</root>"


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


def animate_scroll(editor) -> None:
    bar = editor.verticalScrollBar()
    bar.setValue(bar.minimum())
    animation = QPropertyAnimation(bar, b"value")
    animation.setStartValue(bar.minimum())
    animation.setEndValue(bar.maximum())
    animation.setDuration(600)
    loop = QEventLoop()
    timeout = QTimer()
    timeout.setSingleShot(True)
    timeout.timeout.connect(loop.quit)
    animation.finished.connect(loop.quit)
    timeout.start(1_500)
    animation.start()
    loop.exec()
    animation.stop()


def measure(app: QApplication, window: ProductionMainWindow, model: GuiViewModel, lines: int) -> Measurement:
    source = make_document(lines)
    editor = window.xml_editor

    def load():
        model.setXml(source)
        drain_events(app, 5)

    load_ms, _ = timed(load)
    window.select_page(1)
    drain_events(app)

    changes = []
    model.changed.connect(lambda: changes.append(1))
    with patch("eaeu_xml.application.xml_formatter.XmlFormatter.format") as formatter, \
         patch("eaeu_xml.application.xml_validation_service.XmlValidationService.validate") as validator, \
         patch("eaeu_xml.gui_qt.view_model.minidom.parseString") as parser:
        scroll_wall_ms, scroll_cpu_ms = timed(lambda: animate_scroll(editor))
        scroll_model_calls = len(changes)
        scroll_formatter_calls = formatter.call_count
        scroll_validator_calls = validator.call_count
        scroll_parser_calls = parser.call_count

    cursor = editor.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.End)
    editor.setTextCursor(cursor)
    editor.setFocus()
    typing_ms, _ = timed(lambda: QTest.keyClicks(editor, "diagnostic"))
    drain_events(app)

    load()
    length = max(0, editor.document().characterCount() - 1)
    positions = [int(length * fraction / 20) for fraction in range(1, 20)]

    def select_ranges():
        cursor = editor.textCursor()
        for position in positions:
            cursor.setPosition(position)
            cursor.setPosition(min(position + 32, length), QTextCursor.MoveMode.KeepAnchor)
            editor.setTextCursor(cursor)
            app.processEvents()

    selection_ms, _ = timed(select_ranges)

    load()
    cursor = editor.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.End)
    editor.setTextCursor(cursor)
    QApplication.clipboard().setText("<paste>value</paste>" * 100)
    paste_ms, _ = timed(editor.paste)
    drain_events(app)

    load()
    format_ms, _ = timed(window.xml_binding.formatXml)
    drain_events(app)

    load()
    window.select_page(2)
    validation_ms, _ = timed(model.validate)
    drain_events(app)

    target_line = max(1, min(lines, lines - 10))
    navigation_ms, _ = timed(lambda: model.goToXmlDiagnostic(target_line, 5))
    drain_events(app)

    def switch_tabs():
        window.select_page(2)
        window.select_page(1)
        drain_events(app)

    tab_switch_ms, _ = timed(switch_tabs)

    return Measurement(
        lines=lines,
        load_ms=load_ms,
        scroll_wall_ms=scroll_wall_ms,
        scroll_cpu_ms=scroll_cpu_ms,
        typing_ms=typing_ms,
        selection_ms=selection_ms,
        paste_ms=paste_ms,
        format_ms=format_ms,
        validation_ms=validation_ms,
        navigation_ms=navigation_ms,
        tab_switch_ms=tab_switch_ms,
        viewmodel_calls_during_scroll=scroll_model_calls,
        formatter_calls_during_scroll=scroll_formatter_calls,
        validator_calls_during_scroll=scroll_validator_calls,
        parser_calls_during_scroll=scroll_parser_calls,
    )


def median(items: list[Measurement]) -> Measurement:
    first = items[0]
    result = {}
    for field in Measurement.__dataclass_fields__:
        if field == "lines":
            continue
        result[field] = statistics.median(getattr(item, field) for item in items)
    return Measurement(lines=first.lines, **result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("processes_root", type=Path)
    parser.add_argument("--lines", type=int, nargs="+", default=DEFAULT_LINES)
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    QQuickStyle.setStyle("Basic")
    app = QApplication.instance() or QApplication([])
    model = GuiViewModel(args.processes_root)
    window = ProductionMainWindow(model)
    window.resize(1200, 760)
    window.show()
    drain_events(app, 5)

    results = []
    try:
        for line_count in args.lines:
            samples = [measure(app, window, model, line_count) for _ in range(args.repeats)]
            result = median(samples)
            results.append(result)
            print(json.dumps(asdict(result), ensure_ascii=False))
    finally:
        window.close()
        window.deleteLater()
        drain_events(app)

    if args.json:
        args.json.write_text(
            json.dumps([asdict(result) for result in results], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
