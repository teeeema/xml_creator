from collections import Counter
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

from eaeu_xml.core.enums import SignalKind, TimeoutKind, TransactionPattern, TransactionState
from eaeu_xml.decision5.models import ProcedureId, ProcedureInstance, TransactionDefinition as D5Definition, TransactionInstance, TransactionParameters
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.services.identifier_service import IdentifierService
from eaeu_xml.services.transaction_engine import TransactionEngine

from all_transactions_matrix import EXAMPLES, PACKAGE, artifact_path, evaluate_matrix, participant_address


class AllTransactionsE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = EaeuXmlEngine.load_process(PACKAGE)
        cls.results = evaluate_matrix(cls.engine)

    def test_catalog_driven_matrix_covers_every_branch_once(self):
        expected = {(tx.transaction_code, "initiating", tx.initiating_message) for tx in self.engine.transactions.values()}
        expected |= {(tx.transaction_code, "response", message) for tx in self.engine.transactions.values() for message in tx.response_messages}
        actual = {(result.transaction_code, result.branch, result.message_code) for result in self.results}
        self.assertEqual(len(self.engine.transactions), 19)
        self.assertEqual(len(expected), 43)
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), len(self.results))

    def test_every_branch_is_typed_and_expected_counts_are_stable(self):
        allowed = {"VERIFIED_SOAP", "UNRESOLVED_STRUCTURE_VERSION", "VERSION_PLACEHOLDER_TEST", "NORMATIVE_CONFLICT", "NEEDS_EXTERNAL_SOURCE", "TEST_ONLY", "INITIAL_MESSAGE_BLOCKED"}
        self.assertTrue(all(result.status in allowed for result in self.results))
        self.assertEqual(Counter(result.status for result in self.results), {
            "VERSION_PLACEHOLDER_TEST": 37, "NORMATIVE_CONFLICT": 3, "INITIAL_MESSAGE_BLOCKED": 3,
        })

    def test_actions_body_soap_and_response_correlation(self):
        ns = {"soap": "http://www.w3.org/2003/05/soap-envelope", "wsa": "http://www.w3.org/2005/08/addressing", "int": "urn:EEC:Interaction:v1.0"}
        for result in self.results:
            with self.subTest(transaction=result.transaction_code, message=result.message_code):
                action = self.engine.build_application_action(result.transaction_code, result.message_code).serialize()
                self.assertIn(f"/{result.procedure_code}/{result.transaction_code}/{result.message_code}", action)
                if not result.xml: continue
                root = ET.fromstring(result.xml)
                self.assertEqual(root.tag, "{http://www.w3.org/2003/05/soap-envelope}Envelope")
                self.assertEqual(root.findtext("soap:Header/wsa:Action", namespaces=ns), action)
                body = root.find("soap:Body", namespaces=ns)
                self.assertEqual(len(body), 1)
                structure = self.engine.get_structure(result.message_code,mode="TEST")
                self.assertEqual(body[0].tag, f"{{{structure.namespace}}}{structure.root_element}")
                self.assertEqual(root.findtext("soap:Header/int:ProcedureID", namespaces=ns) is not None, True)
                self.assertEqual(root.findtext("soap:Header/int:ConversationID", namespaces=ns) is not None, True)
                transaction=self.engine.get_transaction(result.transaction_code)
                initiator=participant_address(self.engine,transaction.initiating_participant).serialize()
                respondent=participant_address(self.engine,transaction.responding_participant).serialize()
                expected_to=respondent if result.branch=="initiating" else initiator
                expected_reply=initiator if result.branch=="initiating" else respondent
                self.assertEqual(root.findtext("soap:Header/wsa:To",namespaces=ns),expected_to)
                self.assertEqual(root.findtext("soap:Header/wsa:ReplyTo/wsa:Address",namespaces=ns),expected_reply)
                if result.branch == "response":
                    self.assertNotEqual(result.response_message_id, result.request_message_id)
                    self.assertEqual(root.findtext("soap:Header/wsa:RelatesTo", namespaces=ns), result.request_message_id)
                    structure = self.engine.get_structure(result.message_code,mode="TEST")
                    ref_field = next((field for field in structure.fields if field.xml_name == "EDocRefId"), None)
                    if ref_field and result.request_edoc_id:
                        namespace = structure.imported_namespaces.get(ref_field.namespace_prefix, structure.namespace)
                        self.assertEqual(root.findtext(f".//{{{namespace}}}EDocRefId"), result.request_edoc_id)
                        self.assertNotEqual(result.request_edoc_id, result.request_message_id)

    def test_artifacts_cover_matrix_and_are_machine_readable(self):
        expected = {artifact_path(result) for result in self.results}
        actual = {path for path in EXAMPLES.glob("TRN.*/*") if path.is_file()}
        self.assertEqual(actual, expected)
        for result in self.results:
            path = artifact_path(result)
            if path.suffix == ".xml": ET.parse(path)
            else:
                text = path.read_text(encoding="utf-8")
                for marker in ("transaction:", "procedure:", "message:", "structure:", "active_version:", "status:", "blocking_rule:", "source_refs:", "strict_mode:", "test_mode:"):
                    self.assertIn(marker, text)

    def test_transaction_metadata_is_available_for_all_19(self):
        for transaction in self.engine.transactions.values():
            with self.subTest(transaction=transaction.transaction_code):
                self.assertIsInstance(transaction.timeouts, dict)
                self.assertEqual(set(transaction.timeouts), {"receive_confirmation", "processing_confirmation", "response"})
                self.assertIsNotNone(transaction.retry_count)
                self.assertIn("required", transaction.authorization)
                self.assertIn("required", transaction.signature_requirements)
                self.assertIsNotNone(transaction.initiating_operation)
                self.assertIsNotNone(transaction.initiating_role)
                if transaction.response_messages:
                    self.assertIsNotNone(transaction.responding_operation)
                    self.assertIsNotNone(transaction.responding_role)
                self.assertIn(transaction.initiating_participant,self.engine.participants)
                self.assertIn(transaction.responding_participant,self.engine.participants)

    def _instance(self, code):
        source = self.engine.get_transaction(code)
        ids = IdentifierService()
        definition = D5Definition(TransactionPattern[source.pattern], TransactionParameters(retry_count=source.retry_count or 0), True)
        procedure = ProcedureInstance(source.procedure_code, ProcedureId.root(ids))
        return TransactionInstance(code, ids.new_conversation_id(), procedure, definition=definition)

    def test_notification_flows_use_signal_without_fake_business_response(self):
        for code in ("P.MM.01.TRN.011", "P.MM.01.TRN.013"):
            transaction = self.engine.get_transaction(code)
            self.assertEqual(transaction.response_messages, ())
            instance = self._instance(code); runtime = TransactionEngine()
            self.assertIs(runtime.start_transaction(instance), TransactionState.WAITING_RECEIVED)
            self.assertIs(runtime.receive_signal(instance, SignalKind.RECEIVED), TransactionState.COMPLETED)

    def test_mutual_obligations_use_generic_state_machine(self):
        for code in ("P.MM.01.TRN.008", "P.MM.01.TRN.012"):
            instance = self._instance(code); runtime = TransactionEngine()
            self.assertIs(runtime.start_transaction(instance), TransactionState.WAITING_RECEIVED)
            self.assertIs(runtime.receive_signal(instance, SignalKind.RECEIVED), TransactionState.WAITING_PROCESSING)
            self.assertIs(runtime.receive_signal(instance, SignalKind.ACCEPTED_FOR_PROCESSING), TransactionState.WAITING_RESPONSE)
            self.assertIs(runtime.receive_application_message(instance), TransactionState.WAITING_RESPONSE_RECEIVED)
            self.assertIs(runtime.send_signal(instance, SignalKind.RECEIVED), TransactionState.WAITING_RESPONSE_PROCESSING)
            self.assertIs(runtime.send_signal(instance, SignalKind.ACCEPTED_FOR_PROCESSING), TransactionState.WAITING_FINAL_ERROR_WINDOW)
            runtime.handle_timeout(instance, TimeoutKind.PROCESSING_CONFIRMATION)
            self.assertIs(instance.state, TransactionState.COMPLETED)
            failed = self._instance(code); runtime.start_transaction(failed)
            self.assertIs(runtime.receive_signal(failed, SignalKind.ERROR), TransactionState.ROLLBACK_REQUIRED)


if __name__ == "__main__": unittest.main()
