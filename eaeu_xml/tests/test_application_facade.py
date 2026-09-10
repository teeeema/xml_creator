from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

from eaeu_xml.application import EaeuXmlApplication, ProcessDiscoveryService
from eaeu_xml.application.models import FieldView
from eaeu_xml.application.services import TestDataGenerator


FIXTURES = Path(__file__).parent / "fixtures"
PROJECT_ROOT = Path(__file__).parents[2]


class ApplicationFacadeTests(unittest.TestCase):
    def setUp(self):
        self.app = EaeuXmlApplication(FIXTURES)

    def test_process_discovery_uses_explicit_root_and_skips_non_packages(self):
        processes = ProcessDiscoveryService().discover_processes(FIXTURES)
        self.assertEqual({item.process_code for item in processes}, {"P.TS.01", "P.VR.01"})
        self.assertTrue(all(item.path.parent == FIXTURES.resolve() for item in processes))

    def test_transaction_and_message_views(self):
        transaction = self.app.list_transactions("P.TS.01")[0]
        self.assertEqual(transaction.transaction_code, "P.TS.01.TRN.001")
        messages = self.app.list_messages("P.TS.01", transaction.transaction_code)
        self.assertEqual([item.direction for item in messages], ["initiating", "response"])
        self.assertTrue(all(item.generation_status == "VERIFIED_SOAP" for item in messages))
        self.assertEqual(self.app.list_process_issues("P.TS.01"), ())

    def test_nested_repeatable_attribute_forbidden_and_fixed_form_fields(self):
        form = self.app.get_form("P.TS.01", "P.TS.01.TRN.001", "P.TS.01.MSG.001")
        items, note = form.fields
        self.assertTrue(items.repeatable)
        self.assertEqual(items.children[0].path, "Items/Name")
        attribute = items.children[1]
        self.assertTrue(attribute.is_attribute)
        self.assertFalse(attribute.editable)
        self.assertEqual(attribute.fixed_value, "FIXED")
        self.assertEqual(note.visibility, "HIDDEN")
        self.assertFalse(note.editable)
        self.assertEqual(attribute.example_value, "FIXED")
        self.assertEqual(attribute.xml_qname, "code")
        self.assertEqual(items.cardinality_display, "1..unbounded")

    def test_simple_empty_structure_form_is_stable(self):
        form = self.app.get_form("P.VR.01", "P.VR.01.TRN.001", "P.VR.01.MSG.001")
        self.assertEqual(form.structure_id, "R.006")
        self.assertEqual(form.active_version, "1.0.0")
        self.assertEqual(form.fields, ())

    def test_test_data_is_minimal_valid_and_seeded(self):
        first = self.app.generate_test_data("P.TS.01", "P.TS.01.TRN.001", "P.TS.01.MSG.001", seed=123)
        second = self.app.generate_test_data("P.TS.01", "P.TS.01.TRN.001", "P.TS.01.MSG.001", seed=123)
        self.assertEqual(first, second)
        self.assertEqual(first["Items/Name"], "TEST")
        self.assertEqual(first["Items/@code"], "FIXED")
        self.assertNotIn("Note", first)
        self.assertTrue(self.app.validate("P.TS.01", "P.TS.01.TRN.001", "P.TS.01.MSG.001", first).is_valid)

    def test_ds01_test_data_satisfies_executable_structured_rules(self):
        application = EaeuXmlApplication(PROJECT_ROOT)
        values = application.generate_test_data(
            "P.DS.01", "P.DS.01.TRN.001", "P.DS.01.MSG.001", seed=12345,
        )

        validation = application.validate(
            "P.DS.01", "P.DS.01.TRN.001", "P.DS.01.MSG.001", values,
        )

        self.assertEqual(validation.errors, ())
        self.assertIn("VERSION_PLACEHOLDER", {issue.code for issue in validation.warnings})

    def test_test_data_generator_uses_decimal_value_for_payment_amount(self):
        field = FieldView("Amount", "Amount", "Amount", None, "ELEMENT", "ds01sdo:PaymentAmountType", True, 1, 1, False, False)
        self.assertEqual(TestDataGenerator._value(field, __import__("random").Random(1)), "10.50")

    def test_validation_returns_dto_instead_of_low_level_exception(self):
        result = self.app.validate("P.TS.01", "P.TS.01.TRN.001", "P.TS.01.MSG.001", {})
        self.assertFalse(result.is_valid)
        self.assertIn("MIN_OCCURS", {issue.code for issue in result.errors})

    def test_full_soap_generation_and_session_correlation(self):
        initial = self.app.generate_test_xml("P.TS.01", "P.TS.01.TRN.001", "P.TS.01.MSG.001", seed=7)
        self.assertTrue(initial.success)
        ET.fromstring(initial.xml)
        self.assertTrue(initial.metadata["action"].endswith("/P.TS.01.MSG.001"))

        session = self.app.start_transaction("P.TS.01", "P.TS.01.TRN.001", seed=7)
        request = session.generate_initial_message()
        response = session.generate_response("P.TS.01.MSG.002")
        self.assertTrue(request.success); self.assertTrue(response.success)
        self.assertNotEqual(request.metadata["message_id"], response.metadata["message_id"])
        self.assertEqual(response.metadata["relates_to"], request.metadata["message_id"])
        self.assertEqual(response.metadata["procedure_id"], request.metadata["procedure_id"])
        self.assertEqual(response.metadata["conversation_id"], request.metadata["conversation_id"])


if __name__ == "__main__": unittest.main()
