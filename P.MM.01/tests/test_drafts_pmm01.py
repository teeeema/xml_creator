from pathlib import Path
from base64 import b64encode
import tempfile
import unittest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.gui.controller import GuiController


ROOT = Path(__file__).parents[2]


class Pmm01DraftIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory()
        self.controller=GuiController(EaeuXmlApplication(ROOT,drafts_root=Path(self.temporary.name)))

    def tearDown(self):self.temporary.cleanup()

    def select(self,transaction,message):
        self.controller.select_process("P.MM.01"); self.controller.select_transaction(transaction); self.controller.select_message(message)

    def test_msg007_draft_roundtrip_revalidates_and_generates(self):
        self.select("P.MM.01.TRN.005","P.MM.01.MSG.007")
        values=self.controller.apply_test_data(); path=Path(self.temporary.name)/"msg007.eaeudraft.json"
        self.controller.save_draft(path)
        restored=GuiController(EaeuXmlApplication(ROOT,drafts_root=Path(self.temporary.name)))
        result=restored.load_draft(path)
        self.assertEqual(restored.values,values); self.assertTrue(result.validation.is_valid)
        generated=restored.generate_xml(); self.assertTrue(generated.success); self.assertIn("P.MM.01.MSG.007",generated.xml)

    def test_large_registry_form_preserves_all_generated_paths(self):
        self.select("P.MM.01.TRN.001","P.MM.01.MSG.001")
        values=self.controller.apply_test_data(); self.assertGreaterEqual(len(values),10)
        path=Path(self.temporary.name)/"large.eaeudraft.json"; self.controller.save_draft(path)
        result=self.controller.load_draft(path)
        self.assertEqual(dict(result.compatible_values),values); self.assertFalse(result.unmapped_values)

    def test_placeholder_message_draft_generates_test_xml_but_not_strict(self):
        self.select("P.MM.01.TRN.004","P.MM.01.MSG.005")
        self.controller.apply_test_data()
        path=Path(self.temporary.name)/"blocked.eaeudraft.json"; self.controller.save_draft(path)
        self.controller.load_draft(path)
        self.assertEqual(self.controller.generate_xml().status,"VERSION_PLACEHOLDER_TEST")
        settings=self.controller.settings
        self.controller.apply_settings(type(settings)(settings.processes_root,"STRICT",settings.seed,settings.autosave_enabled,settings.autosave_delay_seconds,settings.drafts_directory))
        self.select("P.MM.01.TRN.004","P.MM.01.MSG.005")
        self.assertEqual(self.controller.generate_xml().status,"UNRESOLVED_STRUCTURE_VERSION")

    def test_binary_payload_and_boolean_survive_draft_without_file_path(self):
        self.select("P.MM.01.TRN.001","P.MM.01.MSG.001")
        values=self.controller.apply_test_data()
        binary_path="DrugRegistrationDetails/RegistrationDossierDocDetails/DocCopyBinaryText"
        binary_value=b64encode(b"small document").decode("ascii")
        values[binary_path]=binary_value
        boolean_field=next(field for field in self.controller.application._walk_fields(self.controller.form.fields)
                           if "indicator" in (field.datatype or "").lower() or "boolean" in (field.datatype or "").lower())
        values[boolean_field.path]=True
        self.controller.set_values(values)
        path=Path(self.temporary.name)/"binary-boolean.eaeudraft.json"
        self.controller.save_draft(path)
        restored=GuiController(EaeuXmlApplication(ROOT,drafts_root=Path(self.temporary.name)))
        restored.load_draft(path)
        self.assertEqual(restored.values[binary_path],binary_value)
        self.assertIs(restored.values[boolean_field.path],True)
        self.assertNotIn("/Users/",path.read_text(encoding="utf-8"))
        restored.set_values({**restored.values,boolean_field.path:False})
        self.assertIs(restored.values[boolean_field.path],False)


if __name__ == "__main__": unittest.main()
