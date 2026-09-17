from pathlib import Path
import tempfile
import unittest
from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.presentation.controller import GuiController, GuiSettings


FIXTURES = Path(__file__).parent / "fixtures"


class GuiControllerTests(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory()
        self.drafts=Path(self.temporary.name)
        self.controller = GuiController(EaeuXmlApplication(FIXTURES,drafts_root=self.drafts), test_seed=12345)

    def tearDown(self):self.temporary.cleanup()

    def test_process_transaction_message_selection(self):
        self.assertEqual({item.process_code for item in self.controller.processes}, {"P.TS.01", "P.VR.01"})
        self.controller.select_process("P.TS.01")
        self.assertEqual(self.controller.transaction_code, "P.TS.01.TRN.001")
        self.assertEqual(len(self.controller.messages), 2)
        self.assertEqual(self.controller.message_code, "P.TS.01.MSG.001")

    def test_form_to_control_mapping_preserves_groups_repeatable_attribute_and_policy(self):
        self.controller.select_process("P.TS.01")
        items, note = self.controller.control_models()
        self.assertEqual(items.control_kind, "GROUP"); self.assertTrue(items.repeatable)
        self.assertEqual(items.children[0].control_kind, "TEXT")
        self.assertTrue(items.children[1].is_attribute); self.assertTrue(items.children[1].read_only)
        self.assertEqual(note.visibility, "HIDDEN")

    def test_test_data_application_collection_clear_and_validation_presentation(self):
        self.controller.select_process("P.TS.01")
        values = self.controller.apply_test_data()
        self.assertEqual(values, self.controller.get_values())
        self.assertTrue(self.controller.validate().is_valid)
        self.controller.set_values({})
        invalid = self.controller.validate()
        self.assertFalse(invalid.is_valid); self.assertTrue(invalid.errors)
        self.controller.clear()
        self.assertEqual(self.controller.values, {"Items/@code": "FIXED"})

    def test_generation_result_and_session_state(self):
        self.controller.select_process("P.TS.01"); self.controller.apply_test_data()
        request = self.controller.generate_xml()
        self.assertTrue(request.success); self.assertTrue(self.controller.save_enabled)
        self.assertEqual(self.controller.active_tab,"XML")
        conversation = request.metadata["conversation_id"]
        self.controller.select_message("P.TS.01.MSG.002"); self.controller.apply_test_data()
        response = self.controller.generate_xml()
        self.assertTrue(response.success)
        self.assertEqual(response.metadata["conversation_id"], conversation)
        self.assertEqual(response.metadata["relates_to"], request.metadata["message_id"])

    def test_field_help_example_long_text_issue_mapping_and_settings(self):
        self.controller.select_process("P.TS.01")
        field=self.controller.find_field("Items/@code")
        help_text=self.controller.field_help(field)
        self.assertIn("XML-атрибут",help_text); self.assertIn("Fixed value: FIXED",help_text)
        self.assertEqual(field.example_value,"FIXED")
        shortened=self.controller.short_text("P.TS.01.MSG.001","Очень длинное официальное название "*8,limit=50)
        self.assertLessEqual(len(shortened),50); self.assertTrue(shortened.endswith("…"))
        self.controller.set_values({}); validation=self.controller.validate()
        self.assertIsNotNone(self.controller.find_field(validation.errors[0].field_path))
        self.controller.apply_settings(GuiSettings(FIXTURES,"STRICT",77,drafts_directory=self.drafts))
        self.assertEqual(self.controller.settings.mode,"STRICT"); self.assertEqual(self.controller.test_seed,77)

    def test_verified_presentation_and_generation_button_rule(self):
        self.controller.select_process("P.TS.01")
        presentation=self.controller.message_presentation()
        self.assertEqual(presentation.severity,"SUCCESS"); self.assertTrue(presentation.can_generate)
        self.assertTrue(self.controller.generation_enabled); self.assertEqual(self.controller.message_marker(presentation.status),"[OK]")
        self.assertFalse(self.controller.save_enabled)

    def test_dirty_manual_save_load_and_autosave_recovery(self):
        self.assertFalse(self.controller.dirty)
        values=self.controller.apply_test_data(); self.assertTrue(self.controller.requires_dirty_confirmation)
        path=self.drafts/"sample.eaeudraft.json"; self.controller.save_draft(path)
        self.assertFalse(self.controller.dirty); self.assertTrue(path.is_file())
        self.controller.set_values({}); self.assertTrue(self.controller.dirty)
        result=self.controller.load_draft(path)
        self.assertEqual(self.controller.values,values); self.assertFalse(self.controller.dirty); self.assertTrue(result.validation.is_valid)
        self.controller.set_values({}); autosave=self.controller.autosave_if_due(now=float("inf"))
        self.assertEqual(autosave,self.controller.application.drafts.autosave_path); self.assertTrue(self.controller.has_autosave_recovery)
        recovered=self.controller.recover_autosave()
        self.assertEqual(recovered.document.values,{}); self.assertTrue(self.controller.dirty); self.assertIsNone(self.controller.current_draft_path)


if __name__ == "__main__": unittest.main()
