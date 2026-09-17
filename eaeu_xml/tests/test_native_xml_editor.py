from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

try:
    from PySide6.QtGui import QTextCursor
    from PySide6.QtWidgets import QApplication, QPlainTextEdit
    from PySide6.QtTest import QTest
except ModuleNotFoundError:
    QApplication = None


@unittest.skipUnless(QApplication is not None, "PySide6 GUI extra is not installed")
class NativeXmlEditorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        if not isinstance(cls.app, QApplication):
            raise unittest.SkipTest("Native widget tests require QApplication")

    def setUp(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditor
        self.editor = NativeXmlEditor(debounce_ms=60)
        self.editor.resize(900, 500)
        self.editor.show()
        self.app.processEvents()

    def tearDown(self):
        self.editor.close()
        self.editor.deleteLater()
        self.app.processEvents()

    def test_editor_feature_parity_and_debounced_commit(self):
        self.assertEqual(self.editor.lineWrapMode(), QPlainTextEdit.LineWrapMode.NoWrap)
        self.assertTrue(self.editor.font().fixedPitch())

        commits = []
        self.editor.commitRequested.connect(commits.append)
        self.editor.set_xml("<root>one</root>")
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.editor.setTextCursor(cursor)
        cursor.insertText("x")
        self.assertEqual(commits, [])
        QTest.qWait(90)
        self.assertEqual(commits, ["<root>one</root>x"])

        self.editor.insertPlainText("y")
        self.editor.flush()
        self.assertEqual(commits[-1], "<root>one</root>xy")

    def test_format_replacement_is_single_undoable_edit(self):
        source = "<root><item>value</item></root>"
        formatted = "<root>\n    <item>value</item>\n</root>"
        self.editor.set_xml(source)
        self.assertTrue(self.editor.replace_xml(formatted))
        self.assertEqual(self.editor.xml(), formatted)
        self.assertTrue(self.editor.document().isUndoAvailable())
        self.editor.undo()
        self.assertEqual(self.editor.xml(), source)
        self.editor.redo()
        self.assertEqual(self.editor.xml(), formatted)

    def test_navigation_changes_cursor_and_scroll_without_changing_xml(self):
        source = "\n".join(f"<item>{index}</item>" for index in range(300))
        self.editor.set_xml(source)
        before = self.editor.xml()
        self.assertTrue(self.editor.go_to_position(250, 4))
        cursor = self.editor.textCursor()
        self.assertEqual(cursor.blockNumber(), 249)
        self.assertEqual(cursor.positionInBlock(), 3)
        self.assertEqual(self.editor.xml(), before)
        self.assertTrue(self.editor.extraSelections())

    def test_viewmodel_sync_format_navigation_and_scroll_are_isolated(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml("<root><item>value</item></root>")
        self.assertEqual(self.editor.xml(), model.xml)

        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(" ")
        self.assertNotEqual(self.editor.xml(), model.xml)
        QTest.qWait(90)
        self.assertEqual(self.editor.xml(), model.xml)

        self.editor.set_xml("<root><item>value</item></root>")
        model.setXml(self.editor.xml())
        self.assertTrue(binding.formatXml())
        once = self.editor.xml()
        self.assertIn("\n", once)
        self.assertTrue(binding.formatXml())
        self.assertEqual(self.editor.xml(), once)
        self.assertEqual(model.xml, once)

        before = self.editor.xml()
        model.goToXmlDiagnostic(2, 3)
        self.assertEqual(self.editor.textCursor().blockNumber(), 1)
        self.assertEqual(self.editor.textCursor().positionInBlock(), 2)
        self.assertEqual(self.editor.xml(), before)

        large_xml = "<root>\n" + "\n".join(
            f"  <item id=\"{index}\">value</item>" for index in range(5000)
        ) + "\n</root>"
        model.setXml(large_xml)
        self.app.processEvents()
        bar = self.editor.verticalScrollBar()
        self.assertGreater(bar.maximum(), 0)

        changes = []
        model.changed.connect(lambda: changes.append(1))
        with patch("eaeu_xml.application.xml_formatter.XmlFormatter.format") as formatter, \
             patch("eaeu_xml.application.xml_validation_service.XmlValidationService.validate") as validator, \
             patch("eaeu_xml.gui_qt.view_model.minidom.parseString") as parser:
            for value in (bar.minimum(), bar.maximum() // 2, bar.maximum()):
                bar.setValue(value)
                self.app.processEvents()
        self.assertEqual(changes, [])
        formatter.assert_not_called()
        validator.assert_not_called()
        parser.assert_not_called()

    def test_actions_flush_current_editor_text_before_viewmodel_action(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml("<root/>")

        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.editor.setTextCursor(cursor)
        self.editor.insertPlainText("local")
        self.assertNotEqual(model.xml, self.editor.xml())

        with patch.object(model, "validate") as validate:
            binding.validateXml()
            self.assertEqual(model.xml, self.editor.xml())
            validate.assert_called_once_with()

        self.editor.insertPlainText("-save")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "prototype.xml"
            binding.saveXml(str(path))
            self.assertEqual(path.read_text(encoding="utf-8"), self.editor.xml())
            self.assertEqual(model.xml, self.editor.xml())

    def test_500k_compact_edit_keeps_full_xml_for_copy_save_validation_and_format(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        payload = "A" * 500_000
        source = f"<Document><Code>123</Code><BinaryData>{payload}</BinaryData></Document>"
        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml(source)
        self.app.processEvents()

        self.assertTrue(binding.hasLargeNodes)
        self.assertFalse(binding.showingOriginal)
        self.assertLess(len(self.editor.xml()), 200)
        self.assertIn("AAAAAAAAAA… ⟪скрыто 499 990 символов⟫", self.editor.xml())
        self.assertNotIn(payload[:1000], self.editor.xml())
        self.assertEqual(model.xml, source)

        code_cursor = self.editor.document().find("123")
        self.assertFalse(code_cursor.isNull())
        code_cursor.insertText("456")
        self.assertTrue(binding.flush())
        expected = source.replace("<Code>123</Code>", "<Code>456</Code>")
        self.assertEqual(model.xml, expected)
        self.assertIn(payload, model.xml)
        self.assertNotIn("⟪скрыто", model.xml)

        captured_format = []
        with patch.object(
            model,
            "formattedXml",
            side_effect=lambda value: captured_format.append(value) or value,
        ):
            self.assertTrue(binding.formatXml())
        self.assertEqual(captured_format, [expected])
        self.assertNotIn("⟪скрыто", captured_format[0])

        binding.copyXml()
        self.assertEqual(QApplication.clipboard().text(), expected)
        self.assertNotIn("⟪скрыто", QApplication.clipboard().text())

        captured_validation = []
        with patch.object(
            model,
            "validate",
            side_effect=lambda: captured_validation.append(model.xml),
        ):
            binding.validateXml()
        self.assertEqual(captured_validation, [expected])
        self.assertNotIn("⟪скрыто", captured_validation[0])

        with TemporaryDirectory() as directory:
            path = Path(directory) / "large.xml"
            binding.saveXml(str(path))
            saved = path.read_text(encoding="utf-8")
        self.assertEqual(saved, expected)
        self.assertIn(payload, saved)
        self.assertNotIn("⟪скрыто", saved)

    def test_short_encoded_payload_compact_edit_and_save_preserve_exact_full_value(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        pattern = "MIIGQAYJKoZIhvcNAQcCoIIGMTCCBi0CAQExDjAMBg+/="
        payload = (pattern * 12)[:500]
        source = f"<Document><Code>123</Code><AnyValue>{payload}</AnyValue></Document>"
        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml(source)
        self.app.processEvents()

        self.assertTrue(binding.hasLargeNodes)
        self.assertFalse(binding.showingOriginal)
        self.assertIn("MIIGQAYJKo… ⟪скрыто 490 символов⟫", self.editor.xml())
        protected = self.editor._protected_ranges_qt()[0]
        _, start, end = protected
        protected_text = self.editor.toPlainText()[start:end]
        self.assertEqual(protected_text, "MIIGQAYJKo… ⟪скрыто 490 символов⟫")

        code_cursor = self.editor.document().find("123")
        code_cursor.insertText("456")
        self.assertTrue(binding.flush())
        expected = source.replace("<Code>123</Code>", "<Code>456</Code>")
        self.assertEqual(model.xml, expected)
        self.assertIn(payload, model.xml)

        with TemporaryDirectory() as directory:
            path = Path(directory) / "encoded.xml"
            binding.saveXml(str(path))
            saved = path.read_text(encoding="utf-8")
        self.assertEqual(saved, expected)
        self.assertIn(payload, saved)
        self.assertNotIn("⟪скрыто", saved)

    def test_many_encoded_payload_sizes_keep_qplaintextedit_compact(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        pattern = "MIIGQAYJKoZIhvcNAQcCoIIGMTCCBi0CAQExDjAMBg+/=_-"
        sizes = (200, 500, 1_000, 5_000, 500_000)
        payloads = {
            size: (pattern * ((size // len(pattern)) + 1))[:size]
            for size in sizes
        }
        ordinary = "".join(f"<Item>{index}</Item>" for index in range(100))
        encoded = "".join(
            f'<Payload size="{size}">{payloads[size]}</Payload>'
            for size in sizes
        )
        source = f"<root>{ordinary}{encoded}</root>"
        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml(source)
        self.app.processEvents()

        display = self.editor.xml()
        self.assertEqual(len(binding.display_document.hidden_nodes), len(sizes))
        self.assertGreater(len(model.xml), 500_000)
        self.assertLess(len(display), 5_000)
        for size, payload in payloads.items():
            self.assertNotIn(payload, display)
            self.assertIn(
                payload[:10]
                + f"… ⟪скрыто {size - 10:,} символов⟫".replace(",", " "),
                display,
            )

    def test_compact_placeholder_is_cursor_protected_and_corruption_is_fail_safe(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        payload = "P" * 30_000
        source = f"<root><Code>123</Code><Data>{payload}</Data></root>"
        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml(source)
        self.app.processEvents()

        marker = self.editor._protected_ranges_qt()[0]
        _, start, end = marker
        cursor = self.editor.textCursor()
        cursor.setPosition((start + end) // 2)
        self.editor.setTextCursor(cursor)
        guarded_position = self.editor.textCursor().position()
        self.assertIn(guarded_position, (start, end))

        # Bypass widget input guards deliberately to emulate corrupted document
        # metadata/text.  The binding must reject the commit and keep full XML.
        corrupt_cursor = QTextCursor(self.editor.document())
        corrupt_cursor.setPosition(start + 1)
        corrupt_cursor.deleteChar()
        self.assertFalse(binding.flush())
        self.assertEqual(model.xml, source)
        self.assertEqual(binding.display_document.full_xml, source)
        self.assertIn("placeholder", model.notice.lower())

    def test_original_compact_roundtrip_preserves_payload_edit(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        payload = "A" * 20_000
        source = f"<root><Code>123</Code><Data>{payload}</Data></root>"
        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml(source)
        self.app.processEvents()

        self.assertTrue(binding.toggleLargeText())
        self.assertTrue(binding.showingOriginal)
        self.assertEqual(self.editor.xml(), source)

        payload_cursor = self.editor.document().find("AAAAA")
        self.assertFalse(payload_cursor.isNull())
        payload_cursor.insertText("BBBBB")
        self.assertTrue(binding.toggleLargeText())
        self.assertFalse(binding.showingOriginal)
        self.assertIn("BBBBBAAAAA… ⟪скрыто 19 990 символов⟫", self.editor.xml())
        self.assertIn("BBBBB", model.xml)
        self.assertNotIn("⟪скрыто", model.xml)

        self.assertTrue(binding.toggleLargeText())
        self.assertTrue(binding.showingOriginal)
        self.assertEqual(self.editor.xml(), model.xml)
        self.assertIn("BBBBB", self.editor.xml())

    def test_compact_undo_redo_preserves_hidden_payload(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        payload = "U" * 25_000
        source = f"<root><Code>123</Code><Data>{payload}</Data></root>"
        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml(source)
        self.app.processEvents()

        code_cursor = self.editor.document().find("123")
        code_cursor.insertText("456")
        self.assertTrue(binding.flush())
        self.assertIn("<Code>456</Code>", model.xml)
        self.assertIn(payload, model.xml)

        self.editor.undo()
        self.assertTrue(binding.flush())
        self.assertEqual(model.xml, source)
        self.assertIn(payload, model.xml)

        self.editor.redo()
        self.assertTrue(binding.flush())
        self.assertIn("<Code>456</Code>", model.xml)
        self.assertIn(payload, model.xml)
        self.assertNotIn("⟪скрыто", model.xml)

    def test_large_document_format_is_idempotent_and_undoable_without_payload_loss(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        payload = "Q" * 22_000
        source = f"<root><Data>{payload}</Data><Code>123</Code></root>"
        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml(source)
        self.app.processEvents()

        self.assertTrue(binding.formatXml())
        formatted_full = model.xml
        formatted_display = self.editor.xml()
        self.assertIn("\n", formatted_full)
        self.assertIn(payload, formatted_full)
        self.assertNotIn("⟪скрыто", formatted_full)
        self.assertIn("QQQQQQQQQQ… ⟪скрыто 21 990 символов⟫", formatted_display)

        self.assertTrue(binding.formatXml())
        self.assertEqual(model.xml, formatted_full)
        self.assertEqual(self.editor.xml(), formatted_display)

        self.editor.undo()
        self.assertTrue(binding.flush())
        self.assertEqual(model.xml, source)
        self.assertIn(payload, model.xml)

        self.editor.redo()
        self.assertTrue(binding.flush())
        self.assertEqual(model.xml, formatted_full)
        self.assertIn(payload, model.xml)

    def test_compact_diagnostic_navigation_targets_placeholder_without_expanding(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        payload = "A\n" * 6000
        source = "<root>\n  <before>1</before>\n  <Data>" + payload + "</Data>\n  <after>2</after>\n</root>"
        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml(source)
        self.app.processEvents()
        node = binding.display_document.hidden_nodes[0]

        hidden_line = source.count("\n", 0, node.full_start) + 100
        self.assertTrue(binding.goToFullPosition(hidden_line, 1))
        compact_line = self.editor.textCursor().blockNumber() + 1
        placeholder_line = self.editor.xml().count("\n", 0, node.display_start) + 1
        self.assertEqual(compact_line, placeholder_line)
        self.assertLess(len(self.editor.xml()), 300)

    def test_1m_compact_editor_stays_small_and_scroll_does_no_backend_work(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeXmlEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        payload = "X" * 1_000_000
        ordinary_lines = "\n".join(f"  <item>{index}</item>" for index in range(250))
        source = f"<root>\n{ordinary_lines}\n  <Data>{payload}</Data>\n</root>"
        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeXmlEditorBinding(self.editor, model)
        model.setXml(source)
        self.app.processEvents()

        display = self.editor.xml()
        self.assertLess(len(display), 10_000)
        self.assertNotIn(payload[:1000], display)
        self.assertIn("XXXXXXXXXX… ⟪скрыто 999 990 символов⟫", display)

        changes = []
        model.changed.connect(lambda: changes.append(1))
        with patch("eaeu_xml.application.xml_formatter.XmlFormatter.format") as formatter, \
             patch("eaeu_xml.application.xml_validation_service.XmlValidationService.validate") as validator, \
             patch.object(binding.display_document, "commit_compact", wraps=binding.display_document.commit_compact) as reconstruct:
            bar = self.editor.verticalScrollBar()
            for value in (bar.minimum(), bar.maximum() // 2, bar.maximum()):
                bar.setValue(value)
                self.app.processEvents()
        self.assertEqual(changes, [])
        formatter.assert_not_called()
        validator.assert_not_called()
        reconstruct.assert_not_called()

    def test_formatter_large_document_actions_use_full_xml_and_open_defaults_compact(self):
        from eaeu_xml.gui_qt.native_xml_editor import NativeFormatterEditorBinding
        from eaeu_xml.gui_qt.view_model import GuiViewModel

        payload = "F" * 120_000
        source = f"<root><Code>123</Code><Data>{payload}</Data></root>"
        model = GuiViewModel(Path(__file__).parent / "fixtures")
        binding = NativeFormatterEditorBinding(self.editor, model)
        model.setFormatterXml(source)
        self.app.processEvents()

        self.assertTrue(binding.hasLargeNodes)
        self.assertFalse(binding.showingOriginal)
        self.assertNotIn(payload[:1000], self.editor.xml())
        self.assertIn("FFFFFFFFFF… ⟪скрыто 119 990 символов⟫", self.editor.xml())

        captured_format = []
        with patch.object(
            model,
            "formattedFormatterXml",
            side_effect=lambda value: captured_format.append(value) or value,
        ):
            self.assertTrue(binding.formatXml())
        self.assertEqual(captured_format, [source])
        self.assertNotIn("⟪скрыто", captured_format[0])

        binding.copyXml()
        self.assertEqual(QApplication.clipboard().text(), source)
        with TemporaryDirectory() as directory:
            save_path = Path(directory) / "formatter-large.xml"
            binding.saveXml(str(save_path))
            self.assertEqual(save_path.read_text(encoding="utf-8"), source)

            loaded_payload = "L" * 130_000
            loaded = f"<loaded><Data>{loaded_payload}</Data></loaded>"
            load_path = Path(directory) / "open.xml"
            load_path.write_text(loaded, encoding="utf-8")
            binding.loadXml(str(load_path))
            self.app.processEvents()
            self.assertEqual(model.formatterXml, loaded)
            self.assertTrue(binding.hasLargeNodes)
            self.assertFalse(binding.showingOriginal)
            self.assertIn("LLLLLLLLLL… ⟪скрыто 129 990 символов⟫", self.editor.xml())
            self.assertNotIn(loaded_payload[:1000], self.editor.xml())

        binding.clearXml()
        self.assertEqual(model.formatterXml, "")
        self.assertEqual(self.editor.xml(), "")
        self.assertFalse(binding.hasLargeNodes)


if __name__ == "__main__":
    unittest.main()
