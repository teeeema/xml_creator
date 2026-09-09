from pathlib import Path
from dataclasses import asdict,replace
import json
import tempfile
import unittest

from eaeu_xml.application import EaeuXmlApplication,SessionPersistenceService,SessionRestoreStatus
from eaeu_xml.application import FormDisplayMode
from eaeu_xml.gui.controller import GuiController,SessionMode
from eaeu_xml.gui.xml_panel import XmlPanel
from eaeu_xml.gui.field_controls import _group_instance_count


ROOT = Path(__file__).parents[2]


class Pmm01GuiControllerTests(unittest.TestCase):
    def setUp(self): self.controller = GuiController(EaeuXmlApplication(ROOT))

    def select(self, transaction, message):
        self.controller.select_process("P.MM.01"); self.controller.select_transaction(transaction); self.controller.select_message(message)

    def test_blocked_status_presentations(self):
        self.select("P.MM.01.TRN.004", "P.MM.01.MSG.005")
        self.assertTrue(self.controller.generation_enabled)
        self.assertIn("нормативные обозначения", self.controller.status_notice)
        self.controller.apply_test_data(); self.assertEqual(self.controller.generate_xml().status, "VERSION_PLACEHOLDER_TEST")
        self.assertEqual(self.controller.active_tab,"XML")
        self.select("P.MM.01.TRN.002", "P.MM.01.MSG.002")
        self.assertIn("нормативное правило", self.controller.status_notice)

    def test_test_only_warning_and_successful_generation(self):
        self.select("P.MM.01.TRN.001", "P.MM.01.MSG.001")
        self.assertEqual(self.controller.current_message.generation_status, "VERSION_PLACEHOLDER_TEST")
        self.assertIn("нормативные обозначения", self.controller.status_notice)
        self.controller.apply_test_data(); result=self.controller.generate_xml()
        self.assertTrue(result.success); self.assertEqual(result.status,"VERSION_PLACEHOLDER_TEST")

    def test_verified_form_and_validation(self):
        self.select("P.MM.01.TRN.005", "P.MM.01.MSG.007")
        self.assertEqual(len(self.controller.form.fields),7)
        self.controller.apply_test_data(); result=self.controller.validate()
        self.assertTrue(result.is_valid); self.assertEqual(result.status,"VERSION_PLACEHOLDER_TEST")

    def test_assisted_identifier_remains_manually_editable(self):
        self.select("P.MM.01.TRN.004","P.MM.01.MSG.005")
        path="EDocHeader/EDocId";generated=self.controller.assisted_value("GENERATE_IDENTIFIER")
        self.controller.set_values({path:generated});manual=generated[:-1]+("0" if generated[-1]!="0" else "1")
        self.controller.set_values({path:manual});self.assertEqual(self.controller.values[path],manual)
        regenerated=self.controller.assisted_value("GENERATE_IDENTIFIER")
        self.controller.set_values({path:regenerated});self.assertNotEqual(regenerated,manual)

    def test_datetime_helpers_support_utc_and_named_zone(self):
        self.select("P.MM.01.TRN.004","P.MM.01.MSG.005")
        self.assertTrue(self.controller.assisted_value("NOW",timezone_name="UTC").endswith("Z"))
        self.assertTrue(self.controller.assisted_value("NOW",timezone_name="Europe/Moscow").endswith("+03:00"))

    def test_msg001_test_data_keeps_required_repeatable_group_instance(self):
        self.select("P.MM.01.TRN.001","P.MM.01.MSG.001"); values=self.controller.apply_test_data()
        group=self.controller.find_field("DrugRegistrationDetails")
        self.assertTrue(group.repeatable); self.assertEqual(_group_instance_count(group,values),1)
        self.assertIn("DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime",values)
        self.assertTrue(self.controller.validate().is_valid)

    def test_human_title_hides_technical_qname_but_help_preserves_it(self):
        self.select("P.MM.01.TRN.005", "P.MM.01.MSG.007")
        header=self.controller.find_field("EDocHeader")
        self.assertEqual(header.display_name,"Заголовок электронного документа")
        self.assertNotIn("ccdo:EDocHeader",header.display_name)
        self.assertIn("XML: ccdo:EDocHeader",self.controller.field_help(header))
        self.assertIsNone(header.example_value)

    def test_all_binary_text_usages_have_generic_file_picker_capability(self):
        def walk(fields):
            for field in fields:
                yield field
                yield from walk(field.children)
        usages=[]
        seen_messages=set()
        self.controller.select_process("P.MM.01")
        for transaction in self.controller.transactions:
            self.controller.select_transaction(transaction.transaction_code)
            for message in self.controller.messages:
                if message.message_code in seen_messages:
                    continue
                seen_messages.add(message.message_code)
                self.controller.select_message(message.message_code)
                for field in walk(self.controller.form.fields):
                    if "binary" in (field.datatype or "").lower():
                        usages.append((message.message_code,field))
        self.assertEqual(len(usages),53)
        self.assertTrue(all(field.datatype == "csdo:BinaryTextType" for _,field in usages))
        self.assertTrue(all(field.supports_file_picker for _,field in usages))
        self.assertTrue(all(field.assisted_input_kind == "FILE" for _,field in usages))
        self.assertTrue(all(field.ui_input_policy == "GROUP" for _,field in usages))

    def test_binary_value_is_preserved_by_form_filters(self):
        self.select("P.MM.01.TRN.001","P.MM.01.MSG.001")
        path="DrugRegistrationDetails/RegistrationDossierDocDetails/DocCopyBinaryText"
        self.controller.set_values({path:"cGF5bG9hZA=="})
        for mode in (FormDisplayMode.REQUIRED,FormDisplayMode.USER_FIELDS,FormDisplayMode.FILLED,FormDisplayMode.ALL):
            self.controller.set_display_mode(mode)
            self.assertIsNotNone(self.controller.form_presentation)
            self.assertEqual(self.controller.values[path],"cGF5bG9hZA==")

    def test_typed_status_presentations_and_generation_rules(self):
        cases=(
            ("P.MM.01.TRN.005","P.MM.01.MSG.007","WARNING",True,"нормативные обозначения"),
            ("P.MM.01.TRN.001","P.MM.01.MSG.001","WARNING",True,"нормативные обозначения"),
            ("P.MM.01.TRN.004","P.MM.01.MSG.005","WARNING",True,"нормативные обозначения"),
            ("P.MM.01.TRN.002","P.MM.01.MSG.002","BLOCKED",False,"нормативное правило"),
        )
        for transaction,message,severity,enabled,text in cases:
            with self.subTest(message=message):
                self.select(transaction,message); presentation=self.controller.message_presentation()
                self.assertEqual(presentation.severity,severity); self.assertEqual(self.controller.generation_enabled,enabled)
                self.assertIn(text,presentation.description)
        conflict=self.controller.message_presentation()
        self.assertIn("NORMATIVE_CONFLICT-001","\n".join(conflict.details))
        self.assertIn("намеренно не подменяет",conflict.suggested_action)

    def test_unresolved_is_blocked_only_in_strict_mode(self):
        self.select("P.MM.01.TRN.004","P.MM.01.MSG.005")
        self.assertEqual(self.controller.message_marker(self.controller.current_message.generation_status),"[VERSION ?]")
        self.controller.apply_settings(type(self.controller.settings)(ROOT,"STRICT",12345,drafts_directory=self.controller.settings.drafts_directory))
        self.select("P.MM.01.TRN.004","P.MM.01.MSG.005")
        self.assertFalse(self.controller.generation_enabled); self.assertEqual(self.controller.message_presentation().severity,"BLOCKED")
        self.assertEqual(self.controller.generate_xml().status,"UNRESOLVED_STRUCTURE_VERSION")

    def test_placeholder_xml_warning_is_explicit(self):
        self.select("P.MM.01.TRN.004","P.MM.01.MSG.005"); self.controller.apply_test_data(); result=self.controller.generate_xml()
        warning=XmlPanel.warning_text(result)
        self.assertIn("ТЕСТОВЫЙ XML",warning); self.assertIn("Y.Y.Y / X.X.X",warning); self.assertIn("production",warning)

    def test_process_issue_filters_separate_blocks_and_warnings(self):
        self.controller.select_process("P.MM.01")
        all_issues=self.controller.filtered_process_issues(); blocking=self.controller.filtered_process_issues("BLOCKING"); warnings=self.controller.filtered_process_issues("WARNINGS")
        self.assertEqual(len(all_issues),len(blocking)+len(warnings)); self.assertTrue(all(item.blocks_test_generation for item in blocking)); self.assertTrue(all(not item.blocks_test_generation for item in warnings))

    def _session_request(self):
        self.select("P.MM.01.TRN.004","P.MM.01.MSG.005");self.controller.apply_test_data()
        request=self.controller.generate_xml();self.assertTrue(request.success)
        return request,self.controller.session.create_snapshot()

    @staticmethod
    def _write_candidate(path,snapshot):
        Path(path).write_text(json.dumps(asdict(snapshot),ensure_ascii=False),encoding="utf-8")

    def test_gui_controller_opens_restorable_snapshot_and_continue_preserves_ids(self):
        request,snapshot=self._session_request()
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"request.eaeusession.json";SessionPersistenceService().save(snapshot,path)
            fresh=GuiController(EaeuXmlApplication(ROOT));opened=fresh.open_session_snapshot(path)
            self.assertIs(opened.status,SessionRestoreStatus.RESTORABLE);self.assertTrue(fresh.session_continue_enabled);self.assertIsNone(fresh.session)
            restored=fresh.continue_session();self.assertIs(fresh.session,opened.restore.session);self.assertIs(fresh.session_mode,SessionMode.RESTORED)
            self.assertEqual(restored.transaction.procedure_instance.procedure_id.serialize(),snapshot.procedure_id)
            self.assertEqual(restored.transaction.conversation_id.serialize(),snapshot.conversation_id)
            self.assertEqual(restored.transaction.message_history[0].message_id.serialize(),snapshot.history[0].message_id)
            fresh.select_message("P.MM.01.MSG.006");fresh.apply_test_data();response=fresh.generate_xml()
            self.assertTrue(response.success);self.assertNotEqual(response.metadata["message_id"],request.metadata["message_id"])
            self.assertEqual(response.metadata["relates_to"],request.metadata["message_id"])
            self.assertEqual(response.metadata["procedure_id"],request.metadata["procedure_id"])
            self.assertEqual(response.metadata["conversation_id"],request.metadata["conversation_id"])

    def test_gui_controller_invalid_mismatch_timing_state_and_correlation_block_continue(self):
        _,snapshot=self._session_request()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            corrupted=root/"bad.eaeusession.json";corrupted.write_text("{broken",encoding="utf-8")
            mismatch=replace(snapshot,process_version="9.9.9",history=tuple(replace(item,action=item.action.replace("/1.1.0/","/9.9.9/")) for item in snapshot.history))
            mismatch_path=root/"mismatch.eaeusession.json";SessionPersistenceService().save(mismatch,mismatch_path)
            old="2020-01-01T00:00:00+00:00";stale=replace(snapshot,history=tuple(replace(item,created_at=old) for item in snapshot.history))
            stale_path=root/"stale.eaeusession.json";SessionPersistenceService().save(stale,stale_path)
            state_path=root/"state.eaeusession.json";self._write_candidate(state_path,replace(snapshot,current_state="COMPLETED"))
            for path,status in ((corrupted,SessionRestoreStatus.SNAPSHOT_INVALID),(mismatch_path,SessionRestoreStatus.PROCESS_VERSION_MISMATCH),
                                (stale_path,SessionRestoreStatus.TIMING_REVALIDATION_REQUIRED),(state_path,SessionRestoreStatus.STATE_INVALID)):
                with self.subTest(status=status):
                    opened=self.controller.open_session_snapshot(path);self.assertIs(opened.status,status);self.assertFalse(opened.continue_ready);self.assertFalse(self.controller.session_continue_enabled)

    def test_gui_controller_correlation_invalid_is_typed_and_never_continued(self):
        self.select("P.MM.01.TRN.004","P.MM.01.MSG.005");self.controller.apply_test_data();self.controller.generate_xml()
        self.controller.select_message("P.MM.01.MSG.006");self.controller.apply_test_data();self.assertTrue(self.controller.generate_xml().success)
        snapshot=self.controller.session.create_snapshot();bad=replace(snapshot,history=(*snapshot.history[:-1],replace(snapshot.history[-1],relates_to="urn:uuid:00000000-0000-4000-8000-000000000001")))
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"correlation.eaeusession.json";self._write_candidate(path,bad)
            opened=self.controller.open_session_snapshot(path);self.assertIs(opened.status,SessionRestoreStatus.CORRELATION_INVALID);self.assertFalse(opened.continue_ready)

    def test_open_body_draft_as_new_has_new_ids_and_no_history(self):
        _,old_snapshot=self._session_request()
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"body.eaeudraft.json";self.controller.save_draft(path)
            fresh=GuiController(EaeuXmlApplication(ROOT,drafts_root=Path(directory)));loaded,new=fresh.open_draft_as_new(path)
            self.assertTrue(loaded.compatible_count);self.assertFalse(new.transaction.message_history)
            self.assertNotEqual(new.transaction.procedure_instance.procedure_id.serialize(),old_snapshot.procedure_id)
            self.assertNotEqual(new.transaction.conversation_id.serialize(),old_snapshot.conversation_id)
            self.assertIs(fresh.session_mode,SessionMode.NEW)

    def test_active_session_save_uses_application_api_and_legacy_draft_cannot_continue(self):
        self._session_request()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);session_path=root/"saved.eaeusession.json";self.controller.save_session(session_path)
            self.assertTrue(session_path.is_file());self.assertIs(self.controller.open_session_snapshot(session_path).status,SessionRestoreStatus.RESTORABLE)
            draft_path=root/"legacy.eaeudraft.json";self.controller.save_draft(draft_path)
            self.assertIs(self.controller.open_session_snapshot(draft_path).status,SessionRestoreStatus.SNAPSHOT_INVALID);self.assertFalse(self.controller.session_continue_enabled)
            loaded=self.controller.load_draft(draft_path);self.assertIsNotNone(loaded);self.assertFalse(self.controller.session_continue_enabled)


if __name__ == "__main__": unittest.main()
