from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

try:
    from PySide6.QtCore import QObject, Qt
    from PySide6.QtGui import QColor, QPalette, QTextCursor
    from PySide6.QtQuickWidgets import QQuickWidget
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication
except ModuleNotFoundError:
    QApplication = None


FIXTURES = Path(__file__).parent / "fixtures"


@unittest.skipUnless(QApplication is not None, "PySide6 GUI extra is not installed")
class ProductionWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        if not isinstance(cls.app, QApplication):
            raise unittest.SkipTest("Production widget tests require QApplication")

    def setUp(self):
        from eaeu_xml.gui_qt.production_window import ProductionMainWindow
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        self.model = GuiViewModel(FIXTURES)
        self.window = ProductionMainWindow(self.model)
        self.window.resize(1200, 760)
        self.window.show()
        self.app.processEvents()

    def tearDown(self):
        self.window.close()
        self.window.deleteLater()
        self.app.processEvents()

    def test_supported_shell_navigation_and_editor_persistence(self):
        for widget in (
            self.window.navigation,
            self.window.qml_pages,
            self.window.xml_page.toolbar,
            self.window.formatter_page.toolbar,
        ):
            self.assertIsInstance(widget, QQuickWidget)
            self.assertEqual(widget.status(), QQuickWidget.Status.Ready)

        xml_editor_id = id(self.window.xml_editor)
        formatter_editor_id = id(self.window.formatter_editor)
        expected_stack = {0: 0, 1: 1, 2: 0, 3: 2, 4: 0, 5: 0, 6: 0}
        for index, stack_index in expected_stack.items():
            self.window.select_page(index)
            self.app.processEvents()
            self.assertEqual(self.window.current_index, index)
            self.assertEqual(self.window.pages.currentIndex(), stack_index)
        self.assertEqual(id(self.window.xml_editor), xml_editor_id)
        self.assertEqual(id(self.window.formatter_editor), formatter_editor_id)

    def test_base64_page_is_in_navigation_without_affecting_native_editor_state(self):
        navigation = self.window.navigation.rootObject()
        main = (Path(__file__).parents[1] / "src" / "eaeu_xml" / "gui_qt" / "qml" / "components" / "TopNavigation.qml").read_text(encoding="utf-8")
        self.assertIn('"Base64"', main)
        self.model.setXml("<main/>")
        self.model.setFormatterXml("<formatter/>")
        self.app.processEvents()
        self.window.select_page(4)
        self.app.processEvents()
        self.assertEqual(self.window.current_index, 4)
        self.assertEqual(self.window.pages.currentIndex(), self.window.QML_PAGE_INDEX)
        self.assertEqual(self.window.xml_editor.xml(), "<main/>")
        self.assertEqual(self.window.formatter_editor.xml(), "<formatter/>")
        self.assertIsNotNone(self.window.base64_model)

    def test_hybrid_shell_backgrounds_are_explicitly_light(self):
        app_background = QColor("#f5f7fa")
        surface_background = QColor("#ffffff")

        for widget in (self.window.navigation, self.window.qml_pages, self.window.notice):
            self.assertEqual(widget.quickWindow().color(), app_background)
            self.assertEqual(widget.rootObject().property("color"), app_background)
            self.assertTrue(widget.autoFillBackground())

        for widget in (self.window.xml_page.toolbar, self.window.formatter_page.toolbar):
            self.assertEqual(widget.quickWindow().color(), surface_background)
            self.assertEqual(widget.rootObject().property("color"), surface_background)
            self.assertTrue(widget.autoFillBackground())

        for widget in (self.window, self.window.pages):
            self.assertTrue(widget.autoFillBackground())
            self.assertEqual(
                widget.palette().color(QPalette.ColorRole.Window),
                app_background,
            )

        for widget in (self.window.xml_page, self.window.formatter_page):
            self.assertTrue(widget.testAttribute(Qt.WidgetAttribute.WA_StyledBackground))
            self.assertEqual(
                widget.palette().color(QPalette.ColorRole.Window),
                surface_background,
            )

    def test_main_and_formatter_state_are_independent_and_debounced(self):
        self.model.setXml("<main/>")
        self.model.setFormatterXml("<formatter/>")
        self.app.processEvents()
        self.assertEqual(self.window.xml_editor.xml(), "<main/>")
        self.assertEqual(self.window.formatter_editor.xml(), "<formatter/>")

        self.window.xml_editor.moveCursor(QTextCursor.MoveOperation.End)
        self.window.xml_editor.insertPlainText("local")
        self.assertEqual(self.model.xml, "<main/>")
        QTest.qWait(340)
        self.assertEqual(self.model.xml, "<main/>local")

        self.window.formatter_editor.moveCursor(QTextCursor.MoveOperation.End)
        self.window.formatter_editor.insertPlainText("local")
        self.assertEqual(self.model.formatterXml, "<formatter/>")
        QTest.qWait(340)
        self.assertEqual(self.model.formatterXml, "<formatter/>local")
        self.assertEqual(self.model.xml, "<main/>local")

    def test_validation_tab_force_flushes_latest_text(self):
        self.model.setXml("<root/>")
        self.app.processEvents()
        self.window.xml_editor.selectAll()
        self.window.xml_editor.insertPlainText("<broken>")
        self.assertEqual(self.model.xml, "<root/>")

        self.window.select_page(2)
        self.assertEqual(self.model.xml, "<broken>")
        self.model.validate()
        self.assertEqual(self.model.validationItems[0]["code"], "XML_PARSE_ERROR")

    def test_tab_roundtrip_preserves_cursor_and_scroll(self):
        source = "\n".join(f"<item>{index}</item>" for index in range(5000))
        self.model.setXml(source)
        self.app.processEvents()
        editor = self.window.xml_editor
        editor.go_to_position(3000, 5)
        self.app.processEvents()
        cursor_position = editor.textCursor().position()
        scroll_value = editor.verticalScrollBar().value()

        self.window.select_page(2)
        self.window.select_page(1)
        self.app.processEvents()
        self.assertEqual(editor.textCursor().position(), cursor_position)
        self.assertEqual(editor.verticalScrollBar().value(), scroll_value)

        formatter_source = "\n".join(f"<line>{index}</line>" for index in range(3000))
        self.model.setFormatterXml(formatter_source)
        self.app.processEvents()
        formatter = self.window.formatter_editor
        formatter.go_to_position(2000, 3)
        self.app.processEvents()
        formatter_cursor = formatter.textCursor().position()
        formatter_scroll = formatter.verticalScrollBar().value()
        self.window.select_page(4)
        self.window.select_page(3)
        self.app.processEvents()
        self.assertEqual(formatter.textCursor().position(), formatter_cursor)
        self.assertEqual(formatter.verticalScrollBar().value(), formatter_scroll)

    def test_diagnostic_navigation_switches_to_native_xml_without_editing(self):
        source = "\n".join(f"<item>{index}</item>" for index in range(400))
        self.model.setXml(source)
        self.app.processEvents()
        self.window.select_page(2)
        self.model.goToXmlDiagnostic(250, 4)
        self.app.processEvents()

        self.assertEqual(self.window.current_index, 1)
        self.assertEqual(self.window.xml_editor.textCursor().blockNumber(), 249)
        self.assertEqual(self.window.xml_editor.textCursor().positionInBlock(), 3)
        self.assertEqual(self.window.xml_editor.xml(), source)
        self.assertTrue(self.window.xml_editor.extraSelections())

        self.window.select_page(2)
        self.model.goToXmlDiagnostic(0, 1)
        self.app.processEvents()
        self.assertEqual(self.window.current_index, 2)

    def test_format_save_copy_and_formatter_independence(self):
        main_source = "<root><item>main</item></root>"
        formatter_source = "<root><item>formatter</item></root>"
        self.model.setXml(main_source)
        self.model.setFormatterXml(formatter_source)
        self.app.processEvents()

        self.assertTrue(self.window.xml_binding.formatXml())
        main_once = self.window.xml_editor.xml()
        self.assertTrue(self.window.xml_binding.formatXml())
        self.assertEqual(self.window.xml_editor.xml(), main_once)
        self.assertIn("main", main_once)

        self.assertTrue(self.window.formatter_binding.formatXml())
        formatter_once = self.window.formatter_editor.xml()
        self.assertTrue(self.window.formatter_binding.formatXml())
        self.assertEqual(self.window.formatter_editor.xml(), formatter_once)
        self.assertIn("formatter", formatter_once)
        self.assertEqual(self.window.xml_editor.xml(), main_once)

        self.window.xml_binding.copyXml()
        self.assertEqual(QApplication.clipboard().text(), main_once)
        with TemporaryDirectory() as directory:
            path = Path(directory) / "production.xml"
            self.window.xml_binding.saveXml(str(path))
            self.assertEqual(path.read_text(encoding="utf-8"), main_once)

            formatter_path = Path(directory) / "formatter.xml"
            self.window.formatter_binding.copyXml()
            self.assertEqual(QApplication.clipboard().text(), formatter_once)
            self.window.formatter_binding.saveXml(str(formatter_path))
            self.assertEqual(formatter_path.read_text(encoding="utf-8"), formatter_once)

    def test_50k_scroll_has_no_backend_work(self):
        source = "\n".join(f'<item id="{index}">value</item>' for index in range(50_000))
        self.model.setXml(source)
        self.app.processEvents()
        editor = self.window.xml_editor
        self.assertEqual(editor.document().blockCount(), 50_000)
        bar = editor.verticalScrollBar()
        self.assertGreater(bar.maximum(), 0)

        model_changes = []
        self.model.changed.connect(lambda: model_changes.append(1))
        with patch("eaeu_xml.application.xml_formatter.XmlFormatter.format") as formatter, \
             patch("eaeu_xml.application.xml_validation_service.XmlValidationService.validate") as validator, \
             patch("eaeu_xml.gui_qt.view_model.minidom.parseString") as parser:
            for value in (bar.minimum(), bar.maximum() // 4, bar.maximum() // 2, bar.maximum()):
                bar.setValue(value)
                self.app.processEvents()

        self.assertEqual(model_changes, [])
        formatter.assert_not_called()
        validator.assert_not_called()
        parser.assert_not_called()

    def test_large_text_toggle_is_available_on_both_toolbars_and_states_are_independent(self):
        encoded_pattern = "MIIGQAYJKoZIhvcNAQcCoIIGMTCCBi0CAQExDjAMBg+/="
        main_payload = (encoded_pattern * 12)[:500]
        formatter_payload = "F" * 30_000
        main_xml = f"<root><Data>{main_payload}</Data></root>"
        formatter_xml = f"<root><Data>{formatter_payload}</Data></root>"

        self.model.setXml(main_xml)
        self.model.setFormatterXml(formatter_xml)
        self.app.processEvents()

        xml_toggle = self.window.xml_page.toolbar.rootObject().findChild(
            QObject,
            "nativeXmlLargeTextToggle",
        )
        formatter_toggle = self.window.formatter_page.toolbar.rootObject().findChild(
            QObject,
            "nativeFormatterLargeTextToggle",
        )
        self.assertIsNotNone(xml_toggle)
        self.assertIsNotNone(formatter_toggle)
        self.assertTrue(xml_toggle.property("enabled"))
        self.assertTrue(formatter_toggle.property("enabled"))
        self.assertEqual(xml_toggle.property("text"), "Показать оригинал")
        self.assertEqual(formatter_toggle.property("text"), "Показать оригинал")

        self.assertTrue(self.window.xml_binding.toggleLargeText())
        self.app.processEvents()
        self.assertTrue(self.window.xml_binding.showingOriginal)
        self.assertFalse(self.window.formatter_binding.showingOriginal)
        self.assertEqual(self.window.xml_editor.xml(), main_xml)
        self.assertNotEqual(self.window.formatter_editor.xml(), formatter_xml)
        self.assertEqual(xml_toggle.property("text"), "Скрыть большие объекты")
        self.assertEqual(formatter_toggle.property("text"), "Показать оригинал")

        self.assertTrue(self.window.formatter_binding.toggleLargeText())
        self.app.processEvents()
        self.assertTrue(self.window.xml_binding.showingOriginal)
        self.assertTrue(self.window.formatter_binding.showingOriginal)
        self.assertEqual(self.window.formatter_editor.xml(), formatter_xml)

    def test_production_diagnostic_inside_hidden_payload_targets_placeholder(self):
        payload = "A\n" * 6000
        source = "<root>\n  <before>1</before>\n  <Data>" + payload + "</Data>\n  <after>2</after>\n</root>"
        self.model.setXml(source)
        self.app.processEvents()
        node = self.window.xml_binding.display_document.hidden_nodes[0]
        hidden_line = source.count("\n", 0, node.full_start) + 200

        self.window.select_page(2)
        self.model.goToXmlDiagnostic(hidden_line, 1)
        self.app.processEvents()

        self.assertEqual(self.window.current_index, 1)
        placeholder_line = self.window.xml_editor.xml().count("\n", 0, node.display_start) + 1
        self.assertEqual(self.window.xml_editor.textCursor().blockNumber() + 1, placeholder_line)
        self.assertLess(len(self.window.xml_editor.xml()), 300)


if __name__ == "__main__":
    unittest.main()
