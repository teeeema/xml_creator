"""Qt application bootstrap; QML remains a presentation layer."""

import argparse
import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

from .view_model import GuiViewModel


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="ГИС_xml — Qt GUI")
    parser.add_argument("processes_root", type=Path)
    args = parser.parse_args(argv)
    QQuickStyle.setStyle("Basic")
    app = QGuiApplication(sys.argv if argv is None else [sys.argv[0], *argv])
    app.setApplicationName("ГИС_xml")
    engine = QQmlApplicationEngine()
    view_model = GuiViewModel(args.processes_root)
    # Keep the bridge alive for the complete lifetime of the QML engine.
    engine._view_model = view_model
    engine.rootContext().setContextProperty("viewModel", view_model)
    engine.load(QUrl.fromLocalFile(str(Path(__file__).with_name("qml") / "Main.qml")))
    if not engine.rootObjects(): return 1
    return app.exec()
