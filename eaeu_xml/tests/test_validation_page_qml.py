from pathlib import Path
import unittest
from unittest.mock import patch

try:
    from PySide6.QtCore import QObject
    from PySide6.QtTest import QTest
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlApplicationEngine
except ModuleNotFoundError:
    QGuiApplication = None

from eaeu_xml.application.xml_validation_service import XmlDiagnostic, XmlValidationResult


@unittest.skipUnless(QGuiApplication is not None, "PySide6 GUI extra is not installed")
class ValidationPageQmlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from eaeu_xml.gui_qt.view_model import GuiViewModel
        cls.app = QGuiApplication.instance() or QGuiApplication([])
        cls.model = GuiViewModel(Path(__file__).parent / "fixtures")
        cls.model._xml_validation = XmlValidationResult((
            XmlDiagnostic("ERROR", "E", "error", "XML", 2, 1),
            XmlDiagnostic("WARNING", "W", "warning", "Header"),
        ))
        cls.engine = QQmlApplicationEngine(); cls.engine._view_model = cls.model
        cls.engine.rootContext().setContextProperty("viewModel", cls.model)
        cls.engine.load((Path(__file__).parents[1] / "src" / "eaeu_xml" / "gui_qt" / "qml" / "Main.qml").resolve().as_uri())
        cls.root = cls.engine.rootObjects()[0]

    def test_filter_buttons_change_only_visible_diagnostics(self):
        expected = (("validationAll", 2), ("validationErrors", 1), ("validationWarnings", 1), ("validationInfos", 0), ("validationAll", 2))
        listing = self.root.findChild(QObject, "validationDiagnosticList")
        original = list(self.model.validationItems)
        for name, count in expected:
            self.root.findChild(QObject, name).clicked.emit()
            self.app.processEvents()
            self.assertEqual(listing.property("count"), count)
        self.assertEqual(self.model.validationItems, original)

    def test_main_editor_debounces_model_sync(self):
        editor = self.root.findChild(QObject, "mainXmlEditor")
        updates = []
        self.model.changed.connect(lambda: updates.append(1))
        editor.setProperty("text", "<root>" + "x" * 100)
        self.app.processEvents()
        self.assertEqual(updates, [])
        QTest.qWait(360)
        self.assertEqual(len(updates), 1)

    def test_formatter_editor_debounces_large_paste_sync(self):
        editor = self.root.findChild(QObject, "formatterEditor")
        updates = []
        self.model.changed.connect(lambda: updates.append(1))
        editor.setProperty("text", "\n".join("<item>value</item>" for _ in range(10000)))
        self.app.processEvents()
        self.assertEqual(updates, [])
        QTest.qWait(360)
        self.assertEqual(len(updates), 1)

    def test_large_document_scrolling_does_not_call_backend(self):
        """Scrolling is a Qt-only operation, even after a large local edit."""
        editor = self.root.findChild(QObject, "mainXmlEditor")
        viewport = self.root.findChild(QObject, "mainXmlEditorViewport")
        self.assertIsNotNone(viewport)

        for line_count in (100, 1_000, 5_000, 10_000, 25_000):
            with self.subTest(lines=line_count):
                editor.setProperty("text", "\n".join("<item>value</item>" for _ in range(line_count)))
                QTest.qWait(360)
                self.assertGreater(viewport.property("contentHeight"), viewport.property("height"))

        model_updates = []
        self.model.changed.connect(lambda: model_updates.append(1))
        with patch("eaeu_xml.application.xml_formatter.XmlFormatter.format") as format_xml, \
             patch("eaeu_xml.application.xml_validation_service.XmlValidationService.validate") as validate_xml, \
             patch("eaeu_xml.gui_qt.view_model.minidom.parseString") as parse_xml:
            maximum_y = viewport.property("contentHeight") - viewport.property("height")
            for fraction in (0.05, 0.25, 0.5, 0.75, 1.0):
                viewport.setProperty("contentY", maximum_y * fraction)
                viewport.setProperty("contentX", 20)
                self.app.processEvents()

        self.assertEqual(model_updates, [])
        format_xml.assert_not_called()
        validate_xml.assert_not_called()
        parse_xml.assert_not_called()


if __name__ == "__main__":
    unittest.main()
