from pathlib import Path
import unittest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.application.xml_validation_service import XmlValidationService


class XmlValidationServiceTests(unittest.TestCase):
    def setUp(self):
        self.app = EaeuXmlApplication(Path(__file__).parent / "fixtures")
        self.engine = self.app._engine("P.TS.01")
        self.result = self.app.generate_test_xml("P.TS.01", "P.TS.01.TRN.001", "P.TS.01.MSG.001")

    def validate(self, xml):
        return XmlValidationService().validate(xml, engine=self.engine,
            transaction_code="P.TS.01.TRN.001", message_code="P.TS.01.MSG.001", mode="TEST")

    def test_generated_xml_passes_available_xml_checks(self):
        self.assertTrue(self.validate(self.result.xml).is_valid)

    def test_malformed_xml_reports_actual_line_and_column(self):
        issue = self.validate("<soap:Envelope>").diagnostics[0]
        self.assertEqual(issue.code, "XML_PARSE_ERROR")
        self.assertEqual(issue.location, "XML")
        self.assertIsNotNone(issue.line)
        self.assertIsNotNone(issue.column)

    def test_changed_action_and_body_namespace_are_detected(self):
        changed_action = self.result.xml.replace("P.TS.01.MSG.001", "P.TS.01.MSG.002", 1)
        self.assertIn("D5_ACTION_UNEXPECTED", {item.code for item in self.validate(changed_action).diagnostics})
        changed_namespace = self.result.xml.replace("urn:test:structure:v2.0.0", "urn:test:wrong", 1)
        self.assertIn("BODY_ROOT_UNEXPECTED", {item.code for item in self.validate(changed_namespace).diagnostics})

    def test_structural_diagnostics_keep_real_element_positions(self):
        wrong_envelope = '<?xml version="1.0"?>\n<soap:Envelope xmlns:soap="WRONG_NAMESPACE">\n  <soap:Header/>\n  <soap:Body/>\n</soap:Envelope>'
        issue = self.validate(wrong_envelope).diagnostics[0]
        self.assertEqual((issue.code, issue.location, issue.line), ("D5_SOAP_ENVELOPE_NAMESPACE", "Envelope", 2))
        wrong_action = self.result.xml.replace("P.TS.01.MSG.001", "P.TS.01.MSG.002", 1)
        action_issue = next(item for item in self.validate(wrong_action).diagnostics if item.code == "D5_ACTION_UNEXPECTED")
        self.assertIsNotNone(action_issue.line)


if __name__ == "__main__":
    unittest.main()
