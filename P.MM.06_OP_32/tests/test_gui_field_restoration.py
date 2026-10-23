import unittest
from pathlib import Path

from eaeu_xml.application.facade import EaeuXmlApplication
from eaeu_xml.core.errors import UnresolvedStructureVersionError
from eaeu_xml.process_packages.body import GenerationMode


PACKAGE = Path(__file__).parents[1]
ROOT = PACKAGE.parent


class Pmm06GuiFieldRestorationTests(unittest.TestCase):
    EXPECTED_DISPLAY_FIELDS = {
        "R.HC.MM.06.001": 136,
        "R.HC.MM.06.002": 22,
        "R.HC.MM.06.003": 31,
        "R.HC.MM.06.004": 9,
        "R.HC.MM.06.005": 18,
        "R.006": 10,
        "R.007": 11,
    }

    @classmethod
    def setUpClass(cls):
        cls.app = EaeuXmlApplication(ROOT)
        cls.engine = cls.app._engine("P.MM.06")
        cls.transactions_by_message = {}
        for transaction in cls.engine.package.transactions.values():
            for message_code in (transaction.initiating_message, *transaction.response_messages):
                cls.transactions_by_message.setdefault(message_code, transaction.transaction_code)

    @staticmethod
    def _walk(fields):
        for field in fields:
            yield field
            yield from Pmm06GuiFieldRestorationTests._walk(field.children)

    def test_all_24_messages_have_display_fields(self):
        self.assertEqual(len(self.transactions_by_message), 24)
        for message_code, message in self.engine.package.messages.items():
            with self.subTest(message_code=message_code):
                form = self.app.get_form(
                    "P.MM.06",
                    self.transactions_by_message[message_code],
                    message_code,
                )
                fields = tuple(self._walk(form.fields))
                self.assertEqual(len(fields), self.EXPECTED_DISPLAY_FIELDS[message.structure_id])
                self.assertTrue(fields)
                self.assertTrue(all(field.visibility == "VISIBLE" for field in fields))
                self.assertTrue(any(field.editable for field in fields if not field.children))

    def test_display_fields_do_not_become_serialization_fields(self):
        for structure in self.engine.package.structures.values():
            with self.subTest(structure_id=structure.structure_id):
                self.assertEqual(structure.fields, ())
                self.assertEqual(
                    len(structure.display_fields),
                    self.EXPECTED_DISPLAY_FIELDS[structure.structure_id],
                )
                self.assertIs(structure.presentation_fields, structure.display_fields)
                self.assertTrue(
                    all(field.status == "DISPLAY_ONLY_UNRESOLVED_QNAME" for field in structure.display_fields)
                )

    def test_generation_stays_blocked_until_serialization_qnames_are_resolved(self):
        for message_code, message in self.engine.package.messages.items():
            transaction_code = self.transactions_by_message[message_code]
            with self.subTest(message_code=message_code):
                form = self.app.get_form("P.MM.06", transaction_code, message_code)
                self.assertEqual(form.generation_status, "UNRESOLVED_STRUCTURE_VERSION")
                self.assertIn("точные QName/XSD", form.blocking_reason)
                self.assertEqual(self.app.generate_test_data("P.MM.06", transaction_code, message_code), {})
                with self.assertRaises(UnresolvedStructureVersionError):
                    self.engine.resolve_structure(message.structure_id, mode=GenerationMode.STRICT)

    def test_normative_placeholder_namespaces_remain_explicit(self):
        for structure in self.engine.package.structures.values():
            with self.subTest(structure_id=structure.structure_id):
                namespaces = tuple(structure.imported_namespaces.values())
                self.assertTrue(namespaces)
                self.assertTrue(any("X.X.X" in namespace or "Z.Z.Z" in namespace for namespace in namespaces))

    def test_message_guide_uses_display_fields(self):
        guide = self.app.get_message_guide("P.MM.06", "P.MM.06.MSG.001")
        self.assertEqual(guide.total_fields, 136)
        self.assertEqual(len(tuple(self._walk(guide.fields))), 136)


if __name__ == "__main__":
    unittest.main()
