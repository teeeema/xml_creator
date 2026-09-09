from pathlib import Path
import unittest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.gui.controller import GuiController


FIXTURES = Path(__file__).parent / "fixtures"


class GuideTests(unittest.TestCase):
    def setUp(self): self.app = EaeuXmlApplication(FIXTURES)

    def test_process_message_and_field_guides_are_generated(self):
        process = self.app.get_process_guide("P.TS.01")
        self.assertEqual((process.transaction_count, process.message_count), (1, 2))
        message = self.app.get_message_guide("P.TS.01", "P.TS.01.MSG.001")
        self.assertEqual(message.root_element, "TestPayload")
        field = self.app.get_field_guide("P.TS.01", "P.TS.01.MSG.001", "Items/Name")
        self.assertEqual(field.path, "Items/Name")
        self.assertTrue(field.sources)
        self.assertIsNotNone(field.example_value)

    def test_hierarchy_attribute_repeatability_requirement_and_policy_are_preserved(self):
        guide = self.app.get_message_guide("P.TS.01", "P.TS.01.MSG.001")
        items = guide.fields[0]
        self.assertTrue(items.repeatable)
        self.assertEqual(items.requirement, "Обязательно")
        attribute = next(field for field in items.children if field.path == "Items/@code")
        self.assertEqual(attribute.xml_kind, "XML-атрибут")
        self.assertEqual((attribute.normative_input_policy, attribute.ui_input_policy), ("AUTO_FIXED", "READ_ONLY"))
        name = next(field for field in items.children if field.path == "Items/Name")
        self.assertEqual(name.requirement, "Обязательно")
        self.assertEqual(name.ui_input_policy, "USER_INPUT")

    def test_search_by_xml_name_path_and_description(self):
        self.assertTrue(any(hit.field_path == "Items/Name" for hit in self.app.search_guide("P.TS.01", "Name")))
        self.assertTrue(any(hit.field_path == "Items/Name" for hit in self.app.search_guide("P.TS.01", "Items/Name")))
        self.assertTrue(any(hit.field_path for hit in self.app.search_guide("P.TS.01", "Описание реквизита отсутствует")))

    def test_controller_exposes_current_context_for_guide(self):
        controller = GuiController(self.app)
        controller.select_process("P.TS.01"); controller.select_transaction("P.TS.01.TRN.001"); controller.select_message("P.TS.01.MSG.001")
        self.assertEqual(controller.guide_context("Items/Name"), ("P.TS.01", "P.TS.01.MSG.001", "Items/Name"))

    def test_guide_generation_is_consistent(self):
        first=self.app.get_message_guide("P.TS.01","P.TS.01.MSG.001")
        second=self.app.get_message_guide("P.TS.01","P.TS.01.MSG.001")
        self.assertEqual(first,second)


if __name__ == "__main__": unittest.main()
