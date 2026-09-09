from pathlib import Path
from time import perf_counter
import unittest
from xml.etree import ElementTree as ET

from eaeu_xml.application import EaeuXmlApplication, FieldVisibilityFilter, FormDisplayMode
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.gui.guide_details import build_guide_node_details


PACKAGE = Path(__file__).parents[1]
ROOT = PACKAGE.parent


class Pmm01ApplicationFacadeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = EaeuXmlApplication(ROOT)

    def test_discovery_counts_and_all_catalog_branches(self):
        process = next(item for item in self.app.list_processes() if item.process_code == "P.MM.01")
        self.assertEqual(process.version, "1.1.0")
        transactions = self.app.list_transactions("P.MM.01")
        self.assertEqual(len(transactions), 19)
        self.assertEqual(sum(len(self.app.list_messages("P.MM.01", item.transaction_code)) for item in transactions), 43)

    def test_known_generation_statuses_are_explainable(self):
        unresolved = self.app.list_messages("P.MM.01", "P.MM.01.TRN.004")[0]
        conflict = self.app.list_messages("P.MM.01", "P.MM.01.TRN.002")[0]
        verified = self.app.list_messages("P.MM.01", "P.MM.01.TRN.005")[0]
        self.assertEqual(unresolved.generation_status, "VERSION_PLACEHOLDER_TEST")
        self.assertEqual(conflict.generation_status, "NORMATIVE_CONFLICT")
        self.assertEqual(verified.generation_status, "VERSION_PLACEHOLDER_TEST")

    def test_unresolved_and_conflict_are_results_not_stack_traces(self):
        unresolved = self.app.generate_test_xml("P.MM.01", "P.MM.01.TRN.004", "P.MM.01.MSG.005")
        conflict = self.app.generate_test_xml("P.MM.01", "P.MM.01.TRN.002", "P.MM.01.MSG.002")
        self.assertTrue(unresolved.success); self.assertEqual(unresolved.status, "VERSION_PLACEHOLDER_TEST")
        self.assertTrue(unresolved.metadata["uses_version_placeholders"]); self.assertIn("Y.Y.Y",unresolved.xml); self.assertIn("X.X.X",unresolved.xml)
        root=ET.fromstring(unresolved.xml);ns={"soap":"http://www.w3.org/2003/05/soap-envelope","wsa":"http://www.w3.org/2005/08/addressing"}
        self.assertEqual(root.findtext("soap:Header/wsa:To",namespaces=ns),"EAEU://EEC/CP/P.MM.01/P.ACT.001")
        self.assertEqual(root.findtext("soap:Header/wsa:ReplyTo/wsa:Address",namespaces=ns),"EAEU://RU/CP/P.MM.01/P.MM.01.ACT.001")
        self.assertLess(unresolved.xml.index("<!--"),unresolved.xml.index("<soap:Header")); ET.fromstring(unresolved.xml)
        self.assertIn("Y.Y.Y — версия структуры электронного документа R.007",unresolved.xml)
        self.assertIn("X.X.X — версия базисной модели данных",unresolved.xml)
        self.assertIn("Коллегии ЕЭК от 25.10.2016 № 122",unresolved.xml)
        self.assertEqual(unresolved.metadata["unresolved_structures"],("R.007",)); self.assertEqual(unresolved.metadata["placeholder_versions"],("Y.Y.Y","X.X.X"))
        self.assertFalse(conflict.success); self.assertEqual(conflict.status, "NORMATIVE_CONFLICT")

    def test_r006_and_r007_placeholders_are_independent_and_strictly_unresolved(self):
        engine=self.app._engine("P.MM.01")
        r006=engine.resolve_structure("R.006",mode=GenerationMode.TEST); r007=engine.resolve_structure("R.007",mode=GenerationMode.TEST)
        self.assertEqual(r006.definition.namespace,"urn:EEC:R:ProcessingResultDetails:vY.Y.Y")
        self.assertEqual(r007.definition.namespace,"urn:EEC:R:ResourceStatusDetails:vY.Y.Y")
        self.assertIsNot(r006.definition,r007.definition)
        for structure in ("R.006","R.007"):
            with self.assertRaisesRegex(Exception,"Active version"):engine.resolve_structure(structure,mode=GenerationMode.STRICT)
        values=self.app.generate_test_data("P.MM.01","P.MM.01.TRN.005","P.MM.01.MSG.009",seed=3)
        strict=self.app.validate("P.MM.01","P.MM.01.TRN.005","P.MM.01.MSG.009",values,mode=GenerationMode.STRICT)
        self.assertFalse(strict.is_valid); self.assertEqual(strict.status,"UNRESOLVED_STRUCTURE_VERSION")

    def test_classifier_warning_produces_test_only_xml(self):
        values = self.app.generate_test_data("P.MM.01", "P.MM.01.TRN.001", "P.MM.01.MSG.001", seed=11)
        validation = self.app.validate("P.MM.01", "P.MM.01.TRN.001", "P.MM.01.MSG.001", values)
        result = self.app.generate_test_xml("P.MM.01", "P.MM.01.TRN.001", "P.MM.01.MSG.001", values)
        self.assertTrue(validation.is_valid); self.assertEqual(validation.status, "VERSION_PLACEHOLDER_TEST")
        self.assertIn("CLASSIFIER_DATASET_NOT_AVAILABLE", {item.code for item in validation.warnings})
        self.assertTrue(result.success); self.assertEqual(result.status, "VERSION_PLACEHOLDER_TEST")
        ET.fromstring(result.xml)

    def test_generated_header_body_values_use_public_form_context(self):
        values = self.app.generate_test_data("P.MM.01", "P.MM.01.TRN.005", "P.MM.01.MSG.007", seed=11)
        self.assertEqual(next(value for path, value in values.items() if path.endswith("/InfEnvelopeCode")), "P.MM.01.MSG.007")
        self.assertEqual(next(value for path, value in values.items() if path.endswith("/EDocCode")), "R.HC.MM.01.007")

    def test_known_field_input_policies_are_message_scoped(self):
        def by_name(transaction, message):
            form = self.app.get_form("P.MM.01", transaction, message)
            return {field.xml_name: field for field in self.app._walk_fields(form.fields) if field.xml_name}
        request = by_name("P.MM.01.TRN.004", "P.MM.01.MSG.005")
        response = by_name("P.MM.01.TRN.004", "P.MM.01.MSG.006")
        self.assertEqual(request["InfEnvelopeCode"].input_policy, "AUTO_FIXED")
        self.assertEqual(request["EDocCode"].input_policy, "AUTO_FIXED")
        self.assertEqual(request["EDocId"].input_policy, "AUTO_GENERATED")
        self.assertEqual(request["EDocRefId"].input_policy, "UNRESOLVED_INPUT_POLICY")
        self.assertEqual(request["EDocDateTime"].input_policy, "UNRESOLVED_INPUT_POLICY")
        self.assertEqual(response["EDocRefId"].input_policy, "CORRELATION")
        self.assertEqual(response["UpdateDateTime"].input_policy, "EXTERNAL_SYSTEM")
        self.assertNotEqual(response["UpdateDateTime"].input_policy, "AUTO_DATETIME")
        self.assertEqual(request["UnifiedCountryCode"].input_policy, "CLASSIFIER")

    def test_classifier_attribute_summary_and_large_structure_policy(self):
        form = self.app.get_form("P.MM.01", "P.MM.01.TRN.005", "P.MM.01.MSG.007")
        fields = tuple(self.app._walk_fields(form.fields))
        code_list = next(field for field in fields if field.path == "UnifiedCountryCode/@codeListId")
        self.assertEqual(code_list.input_policy, "CLASSIFIER")
        summary = self.app.get_message_input_summary("P.MM.01", "P.MM.01.TRN.001", "P.MM.01.MSG.001")
        self.assertGreater(summary.total_fields, 400)
        self.assertGreater(sum(field.normative_input_policy == "CLASSIFIER" for field in fields), 0)
        self.assertGreater(summary.user_input, 0)

    def test_ui_policy_keeps_normative_source_separate_and_forms_usable(self):
        cases = {
            "P.MM.01.MSG.005": "P.MM.01.TRN.004",
            "P.MM.01.MSG.007": "P.MM.01.TRN.005",
            "P.MM.01.MSG.001": "P.MM.01.TRN.001",
            "P.MM.01.MSG.019": "P.MM.01.TRN.012",
        }
        for message, transaction in cases.items():
            with self.subTest(message=message):
                form = self.app.get_form("P.MM.01", transaction, message)
                fields = tuple(self.app._walk_fields(form.fields))
                self.assertGreater(sum(field.ui_input_policy == "USER_INPUT" for field in fields), 0)
                unresolved = [field for field in fields if field.normative_input_policy == "UNRESOLVED_INPUT_POLICY" and field.visibility != "HIDDEN"]
                self.assertTrue(unresolved)
                self.assertTrue(all(field.ui_input_policy == "USER_INPUT" for field in unresolved))
                self.assertTrue(all(field.ui_policy_origin in {"PROJECT_UI_DEFAULT", "MANUAL_OVERRIDE"} for field in unresolved))

    def test_structured_message_guides_cover_key_messages(self):
        def flat(guide): return tuple(self.app._guide_service._walk(guide.fields))
        msg005=self.app.get_message_guide("P.MM.01","P.MM.01.MSG.005")
        self.assertEqual(msg005.structure_id,"R.007");self.assertIn("Y.Y.Y",msg005.version_description)
        self.assertTrue(any(field.path=="EDocHeader" for field in flat(msg005)))
        self.assertFalse(any(field.path=="UpdateDateTime" for field in flat(msg005)))
        msg006=self.app.get_message_guide("P.MM.01","P.MM.01.MSG.006")
        update=next(field for field in flat(msg006) if field.path=="UpdateDateTime")
        self.assertEqual((update.normative_input_policy,update.ui_input_policy),("EXTERNAL_SYSTEM","EXTERNAL_SYSTEM"))
        for code in ("P.MM.01.MSG.007","P.MM.01.MSG.001","P.MM.01.MSG.019"):
            guide=self.app.get_message_guide("P.MM.01",code);self.assertTrue(guide.fields);self.assertGreater(guide.total_fields,0)
        conflict=self.app.get_message_guide("P.MM.01","P.MM.01.MSG.002")
        self.assertTrue(conflict.conflicts);self.assertIsNone(conflict.body_example)

    def test_process_guide_and_trn004_participants_come_from_package(self):
        guide=self.app.get_process_guide("P.MM.01")
        self.assertEqual((guide.message_count,guide.transaction_count),(28,19))
        trn=next(item for item in guide.transactions if item.transaction_code=="P.MM.01.TRN.004")
        self.assertEqual((trn.initiating_participant,trn.responding_participant),("P.MM.01.ACT.001","P.ACT.001"))
        hits=self.app.search_guide("P.MM.01","UpdateDateTime")
        self.assertTrue(any(hit.message_code=="P.MM.01.MSG.006" and hit.field_path=="UpdateDateTime" for hit in hits))

    def test_priority_field_examples_are_safe_and_origin_traced(self):
        def named(message,transaction,name):
            fields=self.app._walk_fields(self.app.get_form("P.MM.01",transaction,message).fields)
            return next(field for field in fields if field.xml_name==name)
        edoc=named("P.MM.01.MSG.005","P.MM.01.TRN.004","EDocDateTime")
        language=named("P.MM.01.MSG.005","P.MM.01.TRN.004","LanguageCode")
        self.assertEqual((edoc.example_value,edoc.example_origin),("2026-08-24T15:24:00+03:00","DATATYPE_EXAMPLE"))
        self.assertEqual((language.example_value,language.example_origin),("ru","DATATYPE_EXAMPLE"))
        for name in ("ApplicationId","RegistrationNumberId"):
            field=named("P.MM.01.MSG.001","P.MM.01.TRN.001",name)
            self.assertEqual((field.example_value,field.example_origin),("[идентификатор]","PROJECT_DOCUMENTATION"))
            self.assertNotIn("550e8400",field.example_value)
        doc_name=named("P.MM.01.MSG.001","P.MM.01.TRN.001","DocName")
        doc_date=named("P.MM.01.MSG.001","P.MM.01.TRN.001","DocCreationDate")
        entity=named("P.MM.01.MSG.001","P.MM.01.TRN.001","BusinessEntityName")
        country=named("P.MM.01.MSG.001","P.MM.01.TRN.001","UnifiedCountryCode")
        code_list=named("P.MM.01.MSG.001","P.MM.01.TRN.001","codeListId")
        update=named("P.MM.01.MSG.006","P.MM.01.TRN.004","UpdateDateTime")
        self.assertEqual(doc_name.example_value,"Пример текстового значения")
        self.assertEqual(doc_date.example_value,"2026-08-24")
        self.assertEqual((entity.example_value,entity.example_origin),("ООО «Пример»","PROJECT_DOCUMENTATION"))
        self.assertEqual((country.example_value,country.example_origin),("[значение выбирается из классификатора]","CLASSIFIER_EXAMPLE"))
        self.assertEqual(code_list.example_value,"[идентификатор]")
        self.assertEqual((update.example_value,update.ui_input_policy),("2026-08-24T15:24:00+03:00","EXTERNAL_SYSTEM"))

    def test_unresolved_ui_audit_preserves_conditional_policy(self):
        guide=self.app.get_message_guide("P.MM.01","P.MM.01.MSG.001")
        unresolved=[field for field in self.app._guide_service._walk(guide.fields) if field.ui_input_policy=="UNRESOLVED_UI_POLICY"]
        self.assertTrue(unresolved)
        self.assertTrue(all(field.normative_input_policy=="CONDITIONAL" for field in unresolved))
        self.assertTrue(all(field.unresolved_ui_reason=="CONDITIONAL_SOURCE_UNKNOWN" for field in unresolved))

    def test_process_issues_are_aggregated_from_generic_package_metadata(self):
        issues=self.app.list_process_issues("P.MM.01")
        unresolved=[item for item in issues if item.category=="UNRESOLVED_VERSION"]
        conflicts=[item for item in issues if item.category=="NORMATIVE_CONFLICT"]
        classifiers=[item for item in issues if item.category=="EXTERNAL_CLASSIFIER"]
        external=[item for item in issues if item.category=="EXTERNAL_SOURCE"]
        self.assertEqual({item.affected_structures[0] for item in unresolved},{"R.006","R.007"})
        self.assertTrue(all(not item.blocks_test_generation and item.blocks_strict_generation for item in unresolved))
        self.assertEqual({message for item in conflicts for message in item.affected_messages},{"P.MM.01.MSG.002","P.MM.01.MSG.023","P.MM.01.MSG.024"})
        self.assertEqual(len(conflicts),5); self.assertEqual(len(classifiers),1); self.assertEqual(len(external),1)
        conflict=next(item for item in conflicts if item.code=="NORMATIVE_CONFLICT-001")
        self.assertIn("hcsdo:ChildJuvenileIndicator",conflict.referenced_fields); self.assertTrue(conflict.source_display)

    def test_request_response_session_uses_decision5_correlation(self):
        session = self.app.start_transaction("P.MM.01", "P.MM.01.TRN.005", seed=5)
        request_values = self.app.generate_test_data("P.MM.01", "P.MM.01.TRN.005", "P.MM.01.MSG.007", seed=5)
        request_edoc = next(value for path, value in request_values.items() if path.endswith("/EDocId"))
        response_form = self.app.get_form("P.MM.01", "P.MM.01.TRN.005", "P.MM.01.MSG.008")
        def walk(fields):
            for field in fields:
                yield field
                yield from walk(field.children)
        ref_path = next(field.path for field in walk(response_form.fields) if field.xml_name == "EDocRefId")
        request = session.generate_initial_message(request_values)
        response = session.generate_response("P.MM.01.MSG.008", body_correlations={ref_path: request_edoc})
        self.assertTrue(request.success); self.assertTrue(response.success)
        self.assertNotEqual(response.metadata["message_id"], request.metadata["message_id"])
        self.assertEqual(response.metadata["relates_to"], request.metadata["message_id"])
        self.assertEqual(response.metadata["procedure_id"], request.metadata["procedure_id"])
        self.assertEqual(response.metadata["conversation_id"], request.metadata["conversation_id"])
        request_root=ET.fromstring(request.xml);response_root=ET.fromstring(response.xml);ns={"soap":"http://www.w3.org/2003/05/soap-envelope","wsa":"http://www.w3.org/2005/08/addressing"}
        self.assertEqual(request_root.findtext("soap:Header/wsa:To",namespaces=ns),"EAEU://EEC/CP/P.MM.01/P.ACT.001")
        self.assertEqual(response_root.findtext("soap:Header/wsa:To",namespaces=ns),"EAEU://RU/CP/P.MM.01/P.MM.01.ACT.001")
        self.assertIn(request_edoc, response.xml)

    def test_large_message_form_filters_preserve_counts_hierarchy_and_performance(self):
        form=self.app.get_form("P.MM.01","P.MM.01.TRN.001","P.MM.01.MSG.001")
        filter_service=FieldVisibilityFilter()
        all_fields=filter_service.apply(form,mode=FormDisplayMode.ALL)
        required=filter_service.apply(form,mode=FormDisplayMode.REQUIRED)
        user_fields=filter_service.apply(form,mode=FormDisplayMode.USER_FIELDS)
        summary=self.app.get_message_input_summary("P.MM.01","P.MM.01.TRN.001","P.MM.01.MSG.001")
        self.assertEqual((summary.visible_fields,summary.manual_fields),(401,308))
        self.assertEqual((len(all_fields.visible_paths),len(required.visible_paths),len(user_fields.visible_paths)),(401,168,399))
        search=filter_service.apply(form,query="DocName")
        self.assertTrue(search.matching_paths)
        self.assertTrue(all(path.endswith("DocName") or "DocName" in path for path in search.matching_paths))
        self.assertTrue(any(field.children for field in search.fields))
        started=perf_counter()
        for _ in range(100):filter_service.apply(form,mode=FormDisplayMode.USER_FIELDS,query="DocName")
        self.assertLess(perf_counter()-started,1.0)

    def test_small_repeatable_and_conflict_messages_support_generic_filters(self):
        filter_service=FieldVisibilityFilter()
        cases=(("P.MM.01.TRN.004","P.MM.01.MSG.005"),("P.MM.01.TRN.008","P.MM.01.MSG.019"),("P.MM.01.TRN.002","P.MM.01.MSG.002"))
        for transaction,message in cases:
            with self.subTest(message=message):
                form=self.app.get_form("P.MM.01",transaction,message)
                self.assertTrue(filter_service.apply(form,mode=FormDisplayMode.ALL).fields)
                self.assertTrue(filter_service.apply(form,mode=FormDisplayMode.USER_FIELDS).fields)

    def test_conditional_rules_audit_is_conservative_and_does_not_compile_text(self):
        priority=("P.MM.01.MSG.001","P.MM.01.MSG.002","P.MM.01.MSG.003","P.MM.01.MSG.008","P.MM.01.MSG.011","P.MM.01.MSG.026",
                  "P.MM.01.MSG.005","P.MM.01.MSG.006","P.MM.01.MSG.019")
        self.assertTrue(all(not self.app.get_conditional_rules("P.MM.01",message) for message in priority))
        counts={};seen=set()
        for transaction in self.app.list_transactions("P.MM.01"):
            for message in self.app.list_messages("P.MM.01",transaction.transaction_code):
                if message.message_code in seen:continue
                seen.add(message.message_code)
                summary=self.app.get_message_input_summary("P.MM.01",transaction.transaction_code,message.message_code,{})
                counts[message.message_code]=summary.conditional_total
                self.assertEqual(summary.conditional_unknown,summary.conditional_total)
                self.assertEqual((summary.conditional_active,summary.conditional_inactive),(0,0))
        self.assertEqual(sum(counts.values()),133)
        self.assertEqual(counts["P.MM.01.MSG.001"],17)
        self.assertEqual(counts["P.MM.01.MSG.002"],85)
        self.assertEqual(counts["P.MM.01.MSG.019"],6)
        guide=self.app.get_message_guide("P.MM.01","P.MM.01.MSG.001")
        conditional=[field for field in self.app._guide_service._walk(guide.fields) if field.normative_input_policy=="CONDITIONAL"]
        self.assertEqual(len(conditional),16);self.assertTrue(all(not field.automatic_condition_check for field in conditional))

    def test_guide_inf_envelope_and_group_details_are_complete(self):
        guide=self.app.get_message_guide("P.MM.01","P.MM.01.MSG.001")
        fields=tuple(self.app._guide_service._walk(guide.fields))
        inf=next(field for field in fields if field.path=="EDocHeader/InfEnvelopeCode")
        details=build_guide_node_details(inf)
        self.assertIn("Название: Код сообщения общего процесса",details)
        self.assertIn("XML name: csdo:InfEnvelopeCode",details)
        self.assertIn("Обязательность: Обязательно",details)
        self.assertIn("Заполнение в программе: формируется программой; ручное изменение недоступно",details)
        self.assertIn("Пример: P.MM.01.MSG.001",details)
        self.assertIn("Нормативный источник:",details)
        group=next(field for field in guide.fields if field.path=="EDocHeader")
        group_details=build_guide_node_details(group)
        self.assertIn("Тип: Структурный блок",group_details);self.assertIn("Дочерних реквизитов:",group_details)

    def test_trn004_assisted_identifier_and_datetime_capabilities(self):
        request=self.app.get_form("P.MM.01","P.MM.01.TRN.004","P.MM.01.MSG.005")
        response=self.app.get_form("P.MM.01","P.MM.01.TRN.004","P.MM.01.MSG.006")
        def fields(form):
            result=[];stack=list(form.fields)
            while stack:
                field=stack.pop();result.append(field);stack.extend(field.children)
            return {field.path:field for field in result}
        request_fields=fields(request);response_fields=fields(response)
        identifier=request_fields["EDocHeader/EDocId"]
        self.assertTrue(identifier.editable);self.assertTrue(identifier.manual_edit_allowed)
        self.assertTrue(identifier.show_identifier_generator)
        self.assertEqual(identifier.assisted_input_kind,"IDENTIFIER")
        date_time=request_fields["EDocHeader/EDocDateTime"]
        self.assertTrue(date_time.editable);self.assertTrue(date_time.show_now_button)
        self.assertTrue(date_time.show_timezone_picker)
        self.assertEqual(date_time.assisted_input_kind,"DATETIME")
        self.assertFalse(request_fields["EDocHeader/InfEnvelopeCode"].editable)
        self.assertFalse(request_fields["EDocHeader/EDocCode"].editable)
        update=response_fields["UpdateDateTime"]
        self.assertEqual(update.ui_input_policy,"EXTERNAL_SYSTEM")
        self.assertFalse(update.show_now_button);self.assertFalse(update.manual_edit_allowed)


if __name__ == "__main__": unittest.main()
