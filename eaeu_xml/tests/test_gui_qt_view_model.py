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
        self.assertNotIn("wx", "\n".join(path.read_text(encoding="utf-8") for path in root.rglob("*.*") if path.suffix in {".py", ".qml"}))


if __name__ == "__main__": unittest.main()
