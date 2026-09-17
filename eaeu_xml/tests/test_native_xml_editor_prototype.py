from pathlib import Path
import unittest

try:
    from PySide6.QtQuickWidgets import QQuickWidget
    from PySide6.QtWidgets import QApplication
except ModuleNotFoundError:
    QApplication = None


@unittest.skipUnless(QApplication is not None, "PySide6 GUI extra is not installed")
class NativeXmlEditorPrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        if not isinstance(cls.app, QApplication):
            raise unittest.SkipTest("Native widget tests require QApplication")

    def test_qml_and_qplaintextedit_share_one_supported_widget_hierarchy(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditor
        from eaeu_xml.gui_qt.native_xml_editor_prototype import NativeXmlEditorPrototypeWindow
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        model = GuiViewModel(Path(__file__).parent / "fixtures")
        window = NativeXmlEditorPrototypeWindow(model)
        try:
            window.show()
            self.app.processEvents()
            self.assertIsInstance(window.qml_toolbar, QQuickWidget)
            self.assertEqual(window.qml_toolbar.status(), QQuickWidget.Status.Ready)
            self.assertIsInstance(window.editor, NativeXmlEditor)
            self.assertIs(window.editor.parentWidget(), window)
            self.assertIs(window.qml_toolbar.parentWidget(), window)
        finally:
            window.close()
            window.deleteLater()
            self.app.processEvents()


if __name__ == "__main__":
    unittest.main()

