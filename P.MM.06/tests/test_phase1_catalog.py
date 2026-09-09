import unittest
from pathlib import Path

from eaeu_xml.process_packages import ProcessPackageLoader, ProcessRegistry


PACKAGE = Path(__file__).parents[1]
ROOT = PACKAGE.parent


class Pmm06Phase1CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = ProcessPackageLoader.load(PACKAGE)

    def test_registry_process_version_and_catalog_counts(self):
        registered = ProcessRegistry(ROOT).get_process("P.MM.06")
        self.assertEqual(registered.process.process_code, "P.MM.06")
        self.assertEqual(registered.profile.process_version, "1.1.0")
        self.assertEqual(len(registered.participants), 7)
        self.assertEqual(len(registered.procedures), 15)
        self.assertEqual(len(registered.operations), 44)
        self.assertEqual(len(registered.transactions), 15)
        self.assertEqual(len(registered.messages), 24)

    def test_codes_are_unique_and_missing_operations_are_not_fabricated(self):
        for values in (
            self.package.participants,
            self.package.procedures,
            self.package.operations,
            self.package.transactions,
            self.package.messages,
        ):
            self.assertEqual(len(values), len(set(values)))
        self.assertNotIn("P.MM.06.OPR.007", self.package.operations)
        self.assertNotIn("P.MM.06.OPR.008", self.package.operations)

    def test_procedure_and_initiating_operation_mapping(self):
        starts = [1, 4, 9, 12, 15, 18, 21, 24, 26, 29, 32, 35, 38, 41, 44]
        for number, operation in enumerate(starts, 1):
            transaction = self.package.transactions[f"P.MM.06.TRN.{number:03d}"]
            self.assertEqual(transaction.procedure_code, f"P.MM.06.PRC.{number:03d}")
            self.assertEqual(transaction.initiating_operation, f"P.MM.06.OPR.{operation:03d}")
            self.assertIn(transaction.initiating_operation, self.package.operations)
            self.assertIn(transaction.responding_operation, self.package.operations)

    def test_transaction_message_topology_and_alternative_responses(self):
        expected = {
            1: (1, (4,)), 2: (2, (4,)), 3: (3, (4,)), 4: (5, (6,)),
            5: (7, (8, 9)), 6: (10, (11, 9)), 7: (12, (13,)),
            8: (17, ()), 9: (15, (4,)), 10: (14, (4,)), 11: (16, (4,)),
            12: (18, (4,)), 13: (19, (20, 9)), 14: (21, (22, 9)),
            15: (23, (24, 9)),
        }
        for number, (request, responses) in expected.items():
            transaction = self.package.transactions[f"P.MM.06.TRN.{number:03d}"]
            self.assertEqual(transaction.initiating_message, f"P.MM.06.MSG.{request:03d}")
            self.assertEqual(
                transaction.response_messages,
                tuple(f"P.MM.06.MSG.{response:03d}" for response in responses),
            )

    def test_transaction_008_is_notification_without_response(self):
        transaction = self.package.transactions["P.MM.06.TRN.008"]
        self.assertEqual(transaction.pattern, "NOTIFICATION")
        self.assertEqual(transaction.initiating_message, "P.MM.06.MSG.017")
        self.assertEqual(transaction.response_messages, ())
        self.assertEqual(transaction.timeouts, {"receive_confirmation": "PT3M"})
        self.assertTrue(transaction.authorization["required"])
        self.assertFalse(transaction.signature_requirements["required"])
        self.assertIsNone(transaction.retry_count)

    def test_message_structure_references_match_audit(self):
        expected = {
            "R.HC.MM.06.001": (1, 2, 3, 8, 11, 17), "R.006": (4, 9),
            "R.007": (5, 6, 7, 10), "R.HC.MM.06.002": (14, 15, 16),
            "R.HC.MM.06.003": (18, 19, 20, 21, 22),
            "R.HC.MM.06.004": (12, 13), "R.HC.MM.06.005": (23, 24),
        }
        for structure, numbers in expected.items():
            for number in numbers:
                self.assertEqual(
                    self.package.messages[f"P.MM.06.MSG.{number:03d}"].structure_id,
                    structure,
                )

    def test_placeholders_remain_unresolved_and_structures_are_reference_only(self):
        self.assertEqual(self.package.profile.models, {"base": "X.X.X", "healthcare": "Z.Z.Z"})
        self.assertIsNone(self.package.profile.structures["R.006"].active_version)
        self.assertIsNone(self.package.profile.structures["R.007"].active_version)
        self.assertEqual({definition.version for definition in self.package.structures.values()}, {"1.1.0", "Y.Y.Y"})
        self.assertTrue(all(not definition.fields for definition in self.package.structures.values()))
        self.assertTrue(all(not rules.business_rules and not rules.structured_rules for rules in self.package.rules.values()))

    def test_act004_linkage_was_not_fabricated(self):
        code = "P.MM.06.ACT.004"
        self.assertIn(code, self.package.participants)
        self.assertNotIn(code, {operation.participant_role for operation in self.package.operations.values()})
        self.assertNotIn(code, {transaction.initiating_participant for transaction in self.package.transactions.values()})
        self.assertNotIn(code, {transaction.responding_participant for transaction in self.package.transactions.values()})


if __name__ == "__main__":
    unittest.main()
