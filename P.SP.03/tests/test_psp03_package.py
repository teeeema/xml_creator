from pathlib import Path
from unittest import TestCase
from xml.etree import ElementTree as ET

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.core.enums import SignalKind, TransactionState
from eaeu_xml.gui.controller import GuiController
from eaeu_xml.process_packages.loader import ProcessPackageLoader


ROOT = Path(__file__).parents[2]
PACKAGE_PATH = ROOT / "P.SP.03"


class Psp03PackageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = ProcessPackageLoader.load(PACKAGE_PATH)

    def test_catalog_and_structure_counts(self):
        package = self.package
        self.assertEqual(len(package.participants), 5)
        self.assertEqual(len(package.procedures), 12)
        self.assertEqual(len(package.operations), 64)
        self.assertEqual(len(package.transactions), 19)
        self.assertEqual(len(package.messages), 27)
        self.assertEqual(len(package.structures), 5)
        self.assertNotIn("P.SP.03.MSG.000", package.messages)
        fields = [field for structure in package.structures.values() for field in structure.fields]
        self.assertEqual(sum(field.kind == "ELEMENT" for field in fields), 597)
        self.assertEqual(sum(field.kind == "ATTRIBUTE" for field in fields), 100)

    def test_message_rule_tables_match_normative_pdf(self):
        self.assertEqual(len(self.package.rules), 21)
        self.assertEqual(sum(len(rules.business_rules) for rules in self.package.rules.values()), 400)
        coverage = 0
        for rules in self.package.rules.values():
            numbers = set()
            for rule in rules.business_rules:
                code = str(rule["requirement_code"])
                if "-" in code:
                    start, end = map(int, code.split("-", 1))
                    numbers.update(range(start, end + 1))
                else:
                    numbers.add(int(code))
                self.assertTrue(rule["source_text"])
                self.assertTrue(rule["source_refs"])
            self.assertEqual(numbers, set(range(1, max(numbers) + 1)))
            coverage += len(numbers)
        self.assertEqual(coverage, 710)
        self.assertEqual(
            [rule["requirement_code"] for rule in self.package.rules["P.SP.03.MSG.018"].business_rules],
            ["1", "2"],
        )

    def test_facade_discovers_package_and_all_messages_generate_parseable_xml(self):
        application = EaeuXmlApplication(ROOT)
        self.assertIn("P.SP.03", {item.process_code for item in application.list_processes()})
        initial = GuiController(application, test_seed=2303)
        initial.select_process("P.SP.03")
        transaction_for_message = {}
        for transaction in initial.transactions:
            initial.select_transaction(transaction.transaction_code)
            for message in initial.messages:
                transaction_for_message.setdefault(message.message_code, transaction.transaction_code)
        self.assertEqual(len(transaction_for_message), 27)

        for message_code, transaction_code in sorted(transaction_for_message.items()):
            with self.subTest(message=message_code):
                controller = GuiController(application, test_seed=2303)
                controller.select_process("P.SP.03")
                controller.select_transaction(transaction_code)
                initiating_code = controller.messages[0].message_code
                if message_code != initiating_code:
                    controller.select_message(initiating_code)
                    controller.apply_test_data()
                    self.assertTrue(controller.generate_xml().success)
                    while controller.session.transaction.state in {
                        TransactionState.WAITING_RECEIVED,
                        TransactionState.WAITING_PROCESSING,
                    }:
                        kind = (
                            SignalKind.RECEIVED
                            if controller.session.transaction.state is TransactionState.WAITING_RECEIVED
                            else SignalKind.ACCEPTED_FOR_PROCESSING
                        )
                        controller.session.runtime.receive_signal(controller.session.transaction, kind)
                controller.select_message(message_code)
                controller.apply_test_data()
                self.assertTrue(controller.validate().is_valid)
                result = controller.generate_xml()
                self.assertTrue(result.success)
                ET.fromstring(result.xml)
