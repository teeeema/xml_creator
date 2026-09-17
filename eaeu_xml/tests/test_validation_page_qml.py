from pathlib import Path
import unittest

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
        from eaeu_xml.gui_qt.fonts import fixed_font_family
        from eaeu_xml.gui_qt.view_model import GuiViewModel
        cls.app = QGuiApplication.instance() or QGuiApplication([])
        cls.model = GuiViewModel(Path(__file__).parent / "fixtures")
        cls.model._xml_validation = XmlValidationResult((
            XmlDiagnostic("ERROR", "E", "error", "XML", 2, 1),
            XmlDiagnostic("WARNING", "W", "warning", "Header"),
        ))
        cls.engine = QQmlApplicationEngine(); cls.engine._view_model = cls.model
        cls.engine.rootContext().setContextProperty("fixedFontFamily", fixed_font_family())
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

    def test_production_qml_contains_no_large_text_editor(self):
        self.assertIsNone(self.root.findChild(QObject, "mainXmlEditor"))
        self.assertIsNone(self.root.findChild(QObject, "formatterEditor"))


if __name__ == "__main__":
    unittest.main()
