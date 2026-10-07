from pathlib import Path
import tempfile
import unittest

try:
    from eaeu_xml.gui_qt.view_model import GuiViewModel
except ModuleNotFoundError as error:
    if error.name != "PySide6": raise
    GuiViewModel = None

from eaeu_xml.application import EaeuXmlApplication


FIXTURES = Path(__file__).parent / "fixtures"


@unittest.skipUnless(GuiViewModel is not None, "PySide6 GUI extra is not installed")
class GuiQtViewModelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        app = EaeuXmlApplication(FIXTURES, drafts_root=Path(self.temp.name))
        self.model = GuiViewModel(FIXTURES, application=app)

    def tearDown(self):
        self.temp.cleanup()

    def test_backend_discovery_selection_and_form(self):
        self.assertEqual({item["code"] for item in self.model.processes}, {"P.TS.01", "P.VR.01"})
        self.model.selectProcess("P.TS.01")
        self.assertEqual(self.model.transactionCode, "P.TS.01.TRN.001")
        self.assertEqual(self.model.messageCode, "P.TS.01.MSG.001")
        self.assertTrue(self.model.fields)
        self.model.selectMessage("P.TS.01.MSG.002")
        self.assertEqual(self.model.messageCode, "P.TS.01.MSG.002")
        self.assertIn("P.TS.01.MSG.002", self.model.messageSummary)

    def test_test_data_generation_and_validation_use_controller(self):
        self.model.selectProcess("P.TS.01")
        self.model.applyTestData()
        self.assertTrue(self.model.controller.values)
        self.model.generateXml()
        self.assertIn("<soap", self.model.xml)
        self.model.validate()
        self.assertEqual(self.model.validationSummary, "Проверка пройдена")
        self.assertEqual(self.model.validationItems, [])

    def test_required_data_action_preserves_user_value_and_reports_idempotence(self):
        self.model.selectProcess("P.TS.01")
        field = next(item for item in self.model.fields if item["kind"] == "TEXT" and item["required"])
        self.model.setFieldValue(field["path"], "CUSTOM")
        self.model.applyRequiredData()
        self.assertEqual(self.model.controller.values[field["path"]], "CUSTOM")
        self.assertIn("обязательные поля", self.model.notice.casefold())
        self.model.applyRequiredData()
        self.assertEqual(self.model.notice, "Все обязательные поля уже заполнены.")

    def test_home_page_has_required_and_test_actions_next_to_each_other(self):
        home = (Path(__file__).parents[1] / "src" / "eaeu_xml" / "gui_qt" / "qml" / "pages" / "HomePage.qml").read_text(encoding="utf-8")
        actions = [home.index(f'text: "{label}"') for label in (
            "Обязательные данные", "Тестовые данные", "Сохранить черновик", "Создать XML")]
        self.assertEqual(actions, sorted(actions))
        self.assertIn('text: "* — обязательное поле"', home)
        self.assertEqual(home.count('modelData.required ? " *"'), 1)
        self.assertIn('function onFormSelectionChanged()', home)

    def test_form_selection_emits_scroll_reset_signal(self):
        emitted = []
        self.model.formSelectionChanged.connect(lambda: emitted.append(self.model.messageCode))
        self.model.selectProcess("P.TS.01")
        self.model.selectMessage("P.TS.01.MSG.002")
        self.assertEqual(emitted[-1], "P.TS.01.MSG.002")

    def test_editable_xml_is_preserved_formatted_and_saved(self):
        self.model.selectProcess("P.TS.01")
        self.model.applyTestData()
        self.model.generateXml()
        edited = "<manual><value>changed</value></manual>"
        self.model.setXml(edited)
        self.assertEqual(self.model.xml, edited)
        self.model.formatXml()
        self.assertIn("changed", self.model.xml)
        path = Path(self.temp.name) / "manual.xml"
        self.model.saveXml(str(path))
        self.assertEqual(path.read_text(encoding="utf-8"), self.model.xml)
        self.model.changeXmlFontSize(99)
        self.assertEqual(self.model.xmlFontSize, 32)
        self.model.resetXmlFontSize()
        self.assertEqual(self.model.xmlFontSize, 14)
        self.model.setXml("<manual>")
        self.model.validate()
        self.assertEqual(self.model.validationItems[0]["code"], "XML_PARSE_ERROR")

    def test_xml_formatting_is_idempotent_and_preserves_comments_namespaces(self):
        source = '<?xml version="1.0"?><root xmlns="urn:test"><!-- note --><child><value>text</value></child></root>'
        once = self.model.formattedXml(source)
        twice = self.model.formattedXml(once)
        five_times = self.model.formattedXml(self.model.formattedXml(self.model.formattedXml(self.model.formattedXml(once))))
        self.assertEqual(once, twice)
        self.assertEqual(once, five_times)
        self.assertIn("<!-- note -->", once)
        self.assertIn('xmlns="urn:test"', once)
        self.assertTrue(once.startswith("<?xml"))
        self.model.setXml("<broken>")
        self.model.formatXml()
        self.assertEqual(self.model.xml, "<broken>")

    def test_formatter_has_independent_text_and_file_save(self):
        self.model.setXml("<main/>")
        self.model.setFormatterXml("<formatter><value>one</value></formatter>")
        formatted = self.model.formattedFormatterXml(self.model.formatterXml)
        self.model.setFormatterXml(formatted)
        self.assertEqual(self.model.xml, "<main/>")
        path = Path(self.temp.name) / "formatter.xml"
        self.model.saveFormatterXml(str(path))
        self.assertEqual(path.read_text(encoding="utf-8"), formatted)

    def test_formatter_slot_updates_current_text_idempotently(self):
        source = '<root><item id="1"><name>Test</name></item></root>'
        self.model.setFormatterXml(source)
        self.model.formatFormatterXml()
        once = self.model.formatterXml
        self.assertIn("\n", once)
        self.assertIn("<item id=\"1\">", once)
        self.model.formatFormatterXml()
        self.assertEqual(self.model.formatterXml, once)

    def test_xml_position_mapping_script_clamps_safely(self):
        from PySide6.QtCore import QCoreApplication
        from PySide6.QtQml import QJSEngine
        self._qt_app = QCoreApplication.instance() or QCoreApplication([])
        script = (Path(__file__).parents[1] / "src" / "eaeu_xml" / "gui_qt" / "qml" / "components" / "XmlPosition.js").read_text(encoding="utf-8")
        engine = QJSEngine()
        engine.evaluate(script)
        offset = engine.globalObject().property("offsetFor")
        text = "one\ntwo\nlast"
        self.assertEqual(offset.call([text, 1, 1]).toInt(), 0)
        self.assertEqual(offset.call([text, 2, 2]).toInt(), 5)
        self.assertEqual(offset.call([text, 3, 999]).toInt(), len(text))
        self.assertEqual(offset.call([text, 4, 1]).toInt(), -1)

    def test_xml_diagnostic_navigation_emits_only_real_position(self):
        calls = []
        self.model.navigateToXmlPosition.connect(lambda line, column: calls.append((line, column)))
        self.model.goToXmlDiagnostic(7, 3)
        self.model.goToXmlDiagnostic(0, 1)
        self.assertEqual(calls, [(7, 3)])

    def test_qml_places_selectors_only_on_home_and_editor_is_editable(self):
        qml = Path(__file__).parents[1] / "src" / "eaeu_xml" / "gui_qt" / "qml"
        main = (qml / "Main.qml").read_text(encoding="utf-8")
        self.assertIn("root.currentIndex === 0", main)
        self.assertIn("ColumnLayout", (qml / "components" / "SelectorBar.qml").read_text(encoding="utf-8"))
        shared_editor = (qml / "components" / "XmlTextEditor.qml").read_text(encoding="utf-8")
        native_editor = (Path(__file__).parents[1] / "src" / "eaeu_xml" / "gui_qt" / "native_xml_editor.py").read_text(encoding="utf-8")
        self.assertNotIn("XmlTextEditor", main)
        self.assertIn("QPlainTextEdit", native_editor)
        self.assertIn("Flickable", shared_editor)
        self.assertIn("ScrollBar.AsNeeded", shared_editor)
        self.assertIn("TextEdit.PlainText", shared_editor)
        selector = (qml / "components" / "Selector.qml").read_text(encoding="utf-8")
        self.assertIn("hovered && fullText.length > 0", selector)

    def test_information_and_field_updates_are_real_controller_data(self):
        self.model.selectProcess("P.TS.01")
        field = next(item for item in self.model.fields if item["kind"] == "TEXT")
        self.model.setFieldValue(field["path"], "changed")
        self.assertEqual(self.model.controller.values[field["path"]], "changed")
        self.model.selectField(field["path"])
        self.assertIn(field["path"], self.model.selectedFieldInfo)
        info = {item["section"]: item["text"] for item in self.model.information}
        self.assertIn(self.model.processCode, info["Общие сведения"])
        self.assertIn(self.model.messageCode, info["Техническая информация"])

    def test_qt_module_does_not_depend_on_wx(self):
        root = Path(__file__).parents[1] / "src" / "eaeu_xml" / "gui_qt"
        self.assertTrue((root / "qml" / "Main.qml").is_file())
        self.assertNotIn("w" + "x", "\n".join(path.read_text(encoding="utf-8") for path in root.rglob("*.*") if path.suffix in {".py", ".qml"}))

    def test_field_info_is_in_scrollable_container(self):
        """TEST 1: Field info with long content is inside a scrollable container in QML."""
        qml = Path(__file__).parents[1] / "src" / "eaeu_xml" / "gui_qt" / "qml"
        home = (qml / "pages" / "HomePage.qml").read_text(encoding="utf-8")
        self.assertIn("ScrollView", home)
        self.assertIn("fieldInfoScroll", home)
        self.assertIn("selectedFieldInfo", home)
        self.assertIn("width: fieldInfoScroll.availableWidth", home)
        self.assertIn("clip: true", home)

    def test_user_input_field_is_editable(self):
        """TEST 2: USER_INPUT field creates editable row."""
        self.model.selectProcess("P.TS.01")
        user_inputs = [f for f in self.model.fields if not f["readOnly"] and f["kind"] == "TEXT"]
        self.assertTrue(len(user_inputs) > 0)
        first = user_inputs[0]
        self.assertFalse(first["readOnly"])
        field = self.model.controller.find_field(first["path"])
        self.assertEqual(field.ui_input_policy, "USER_INPUT")
        self.assertTrue(field.editable)

    def test_read_only_system_fixed_field_remains_non_editable(self):
        """TEST 3: read-only/system/fixed field remains non-editable."""
        self.model.selectProcess("P.TS.01")
        # In P.TS.01, Items/@code is AUTO_FIXED / READ_ONLY
        field_model = next((f for f in self.model.fields if f["path"] == "Items/@code"), None)
        self.assertIsNotNone(field_model)
        self.assertTrue(field_model["readOnly"])
        field = self.model.controller.find_field("Items/@code")
        self.assertFalse(field.editable)

    def test_unresolved_normative_with_user_input_ui_is_editable(self):
        """TEST 4: UNRESOLVED normative policy + UI policy USER_INPUT is not read-only."""
        # Find a field across processes that has UNRESOLVED_INPUT_POLICY and USER_INPUT
        for proc in self.model.controller.processes:
            self.model.selectProcess(proc.process_code)
            for f in self.model.fields:
                field = self.model.controller.find_field(f["path"])
                if field and field.normative_input_policy == "UNRESOLVED_INPUT_POLICY" and field.ui_input_policy == "USER_INPUT":
                    self.assertFalse(f["readOnly"], f"Field {field.path} should be editable")
                    self.assertTrue(field.editable)
                    return
        self.fail("No UNRESOLVED_INPUT_POLICY + USER_INPUT field found")

    def test_user_input_change_alters_xml_and_reloading_shows_value(self):
        """TEST 5 & 6: Editing a USER_INPUT field updates XML and repeated reading shows value."""
        self.model.selectProcess("P.TS.01")
        target_path = "Items/Name"
        self.model.setFieldValue(target_path, "ТестовоеНаименование123")
        self.assertEqual(self.model.controller.values[target_path], "ТестовоеНаименование123")
        # View model shows updated value
        f_model = next(f for f in self.model.fields if f["path"] == target_path)
        self.assertEqual(f_model["value"], "ТестовоеНаименование123")
        # Generate XML
        self.model.generateXml()
        self.assertTrue(self.model.xml)
        self.assertIn("ТестовоеНаименование123", self.model.xml)
        # Selecting field retains value and shows in help info
        self.model.selectField(target_path)
        self.assertIn(target_path, self.model.selectedFieldInfo)

    def test_cross_op_shared_behavior_for_elements_with_attributes(self):
        """TEST 7: Simple-content elements with attributes are editable across multiple OPs without hardcode."""
        root = Path(__file__).parents[2]
        model = GuiViewModel(root)
        self.model.selectProcess("P.TS.01")
        # Check fixture process first to verify shared logic
        items = next((f for f in self.model.fields if f["path"] == "Items/@code"), None)
        self.assertIsNotNone(items)

        # Check real processes across OPs
        for proc in ("P.MM.01", "P.SP.02", "P.SP.03", "P.DS.01"):
            model.selectProcess(proc)
            editable_inputs = [f for f in model.fields if not f["readOnly"] and f["kind"] in ("TEXT", "SELECT")]
            self.assertTrue(len(editable_inputs) > 0, f"Expected editable inputs in {proc}")

        # Specifically check element with attribute in P.MM.01.MSG.014
        model.selectProcess("P.MM.01")
        for trn in model.controller.transactions:
            model.selectTransaction(trn.transaction_code)
            for msg in model.controller.messages:
                if msg.message_code == "P.MM.01.MSG.014":
                    model.selectMessage(msg.message_code)
                    ucc = next((f for f in model.fields if f["path"] == "UnifiedCountryCode"), None)
                    self.assertIsNotNone(ucc)
                    self.assertEqual(ucc["kind"], "TEXT")
                    self.assertFalse(ucc["readOnly"])
                    model.applyRequiredData()
                    model.setFieldValue("UnifiedCountryCode", "RU")
                    model.setFieldValue("UnifiedCountryCode/@codeListId", "TEST_CL")
                    model.generateXml()
                    self.assertIn("csdo:UnifiedCountryCode", model.xml)
                    self.assertIn("RU", model.xml)
                    self.assertIn("TEST_CL", model.xml)
                    return
        self.fail("P.MM.01.MSG.014 not found")


if __name__ == "__main__": unittest.main()
