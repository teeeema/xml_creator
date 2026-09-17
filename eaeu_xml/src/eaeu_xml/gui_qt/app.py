"""Qt application bootstrap; QML remains a presentation layer."""

import argparse
import sys
from pathlib import Path

from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtWidgets import QApplication

from .production_window import ProductionMainWindow
from .view_model import GuiViewModel


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="ГИС_xml — Qt GUI")
    parser.add_argument("processes_root", type=Path)
    args = parser.parse_args(argv)
    QQuickStyle.setStyle("Basic")
    app = QApplication.instance() or QApplication(sys.argv if argv is None else [sys.argv[0], *argv])
    app.setApplicationName("ГИС_xml")
    view_model = GuiViewModel(args.processes_root)
    window = ProductionMainWindow(view_model)
    window.show()
    return app.exec()
