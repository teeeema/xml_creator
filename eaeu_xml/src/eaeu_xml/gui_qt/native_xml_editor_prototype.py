"""Supported QWidget-host prototype for mixing QML chrome and QPlainTextEdit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from .native_xml_editor import NativeXmlEditor, NativeXmlEditorBinding
from .view_model import GuiViewModel


class NativeXmlEditorPrototypeWindow(QWidget):
    """Single supported widget hierarchy: QML toolbar above native editor."""

    def __init__(self, view_model, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("ГИС_xml — native editor prototype")
        self.resize(1200, 760)

        self.editor = NativeXmlEditor(self)
        self.binding = NativeXmlEditorBinding(self.editor, view_model, self)

        self.qml_toolbar = QQuickWidget(self)
        self.qml_toolbar.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.qml_toolbar.rootContext().setContextProperty("nativeBridge", self.binding)
        qml_path = Path(__file__).with_name("qml") / "prototypes" / "NativeXmlEditorPrototype.qml"
        self.qml_toolbar.setSource(QUrl.fromLocalFile(str(qml_path)))
        if self.qml_toolbar.status() != QQuickWidget.Status.Ready:
            raise RuntimeError("; ".join(error.toString() for error in self.qml_toolbar.errors()))
        self.qml_toolbar.setFixedHeight(58)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.qml_toolbar)
        layout.addWidget(self.editor, 1)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="QPlainTextEdit/QML integration prototype")
    parser.add_argument("processes_root", type=Path)
    args = parser.parse_args(argv)

    QQuickStyle.setStyle("Basic")
    app = QApplication.instance() or QApplication(sys.argv if argv is None else [sys.argv[0], *argv])
    model = GuiViewModel(args.processes_root)
    window = NativeXmlEditorPrototypeWindow(model)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

