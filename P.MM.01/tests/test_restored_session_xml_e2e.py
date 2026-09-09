from dataclasses import asdict,replace
from pathlib import Path
import gc
import json
import tempfile
import unittest
from xml.etree import ElementTree as ET

from eaeu_xml.application import EaeuXmlApplication,SessionPersistenceService,SessionRestoreStatus
from eaeu_xml.core.enums import SignalKind
from eaeu_xml.decision5.models import FaultReasonText,FaultSubcode,SoapFault
from eaeu_xml.decision5.models.action import ApplicationAction
from eaeu_xml.gui.controller import GuiController


ROOT=Path(__file__).parents[2]
NS={"soap":"http://www.w3.org/2003/05/soap-envelope","wsa":"http://www.w3.org/2005/08/addressing","int":"urn:EEC:Interaction:v1.0"}


def parsed(xml):return ET.fromstring(xml)
def header_text(root,prefix,name):
    item=root.find(f"./soap:Header/{prefix}:{name}",NS)
    return item.text if item is not None else None
def body_signature(root):
    body=root.find("./soap:Body",NS)
    def node(item):return (item.tag,tuple(sorted(item.attrib.items())),(item.text or "").strip(),tuple(node(child) for child in item))
    return tuple(node(child) for child in body)
def header_shape(root):
    header=root.find("./soap:Header",NS)
    return tuple(item.tag for item in header)
def local_values(root,name):return tuple((item.text or "").strip() for item in root.iter() if item.tag.rsplit("}",1)[-1]==name)


class RestoredSessionXmlEndToEndTests(unittest.TestCase):
    def _values(self,app,trn,msg,seed):return app.generate_test_data("P.MM.01",trn,msg,seed=seed)

    def _request_snapshot(self,directory,*,seed=51):
        app=EaeuXmlApplication(ROOT,drafts_root=directory);session=app.start_transaction("P.MM.01","P.MM.01.TRN.004",seed=seed)
        values=self._values(app,"P.MM.01.TRN.004","P.MM.01.MSG.005",seed);request=session.generate_initial_message(values)
        self.assertTrue(request.success);path=Path(directory)/"request.eaeusession.json";session.save_snapshot(path)
        return app,session,request,path

    def test_fresh_restart_restore_response_reaches_semantically_correct_final_xml(self):
        with tempfile.TemporaryDirectory() as directory:
            app,session,request,path=self._request_snapshot(directory);snapshot=session.create_snapshot();request_id=request.metadata["message_id"]
            del session,app;gc.collect()
            restarted=EaeuXmlApplication(ROOT,drafts_root=Path(directory));opened=restarted.open_transaction_session(path,seed=51)
            self.assertIs(opened.status,SessionRestoreStatus.RESTORABLE);restored=opened.restore.session
            response_values=self._values(restarted,"P.MM.01.TRN.004","P.MM.01.MSG.006",52)
            response=restored.generate_response("P.MM.01.MSG.006",response_values);self.assertTrue(response.success)
            root=parsed(response.xml);action=ApplicationAction.parse(header_text(root,"wsa","Action"))
            self.assertNotEqual(response.metadata["message_id"],request_id)
            self.assertEqual(header_text(root,"wsa","MessageID"),response.metadata["message_id"])
            self.assertEqual(header_text(root,"wsa","RelatesTo"),request_id)
            self.assertEqual(header_text(root,"int","ProcedureID"),snapshot.procedure_id)
            self.assertEqual(header_text(root,"int","ConversationID"),snapshot.conversation_id)
            self.assertEqual(header_text(root,"wsa","Action"),response.metadata["action"])
            self.assertEqual((action.process_code,action.process_version,action.procedure_code,action.transaction_code,action.message_code),
                ("P.MM.01","1.1.0","P.MM.01.PRC.007","P.MM.01.TRN.004","P.MM.01.MSG.006"))
            self.assertEqual(root.find("./soap:Body",NS)[0].tag,"{urn:EEC:R:ResourceStatusDetails:vY.Y.Y}ResourceStatusDetails")
            self.assertEqual(len(restored.transaction.message_history),2)
            self.assertEqual(restored.transaction.message_history[0].message_id.serialize(),request_id)
            self.assertTrue({NS["soap"],NS["wsa"],NS["int"]}.issubset({item.tag[1:].split("}",1)[0] for item in root.iter() if item.tag.startswith("{")}))
            for value in (*local_values(root,"EDocId"),*local_values(root,"EDocRefId")):
                self.assertNotIn(value,{response.metadata["message_id"],request_id,snapshot.procedure_id,snapshot.conversation_id})

    def test_continuous_and_restored_response_xml_have_equivalent_semantics(self):
        request_values=None;response_values=None
        app_a=EaeuXmlApplication(ROOT);continuous=app_a.start_transaction("P.MM.01","P.MM.01.TRN.004",seed=61)
        request_values=self._values(app_a,"P.MM.01.TRN.004","P.MM.01.MSG.005",61);response_values=self._values(app_a,"P.MM.01.TRN.004","P.MM.01.MSG.006",62)
        continuous_request=continuous.generate_initial_message(request_values);xml_a=continuous.generate_response("P.MM.01.MSG.006",response_values,body_correlations={"EDocHeader/EDocRefId":request_values["EDocHeader/EDocId"]}).xml
        with tempfile.TemporaryDirectory() as directory:
            app_b=EaeuXmlApplication(ROOT,drafts_root=Path(directory));before=app_b.start_transaction("P.MM.01","P.MM.01.TRN.004",seed=61)
            before.generate_initial_message(request_values);path=Path(directory)/"session.eaeusession.json";before.save_snapshot(path)
            del before,app_b;gc.collect();fresh=EaeuXmlApplication(ROOT,drafts_root=Path(directory));restored=fresh.open_transaction_session(path,seed=61).restore.session
            xml_b=restored.generate_response("P.MM.01.MSG.006",response_values,body_correlations={"EDocHeader/EDocRefId":request_values["EDocHeader/EDocId"]}).xml
        a,b=parsed(xml_a),parsed(xml_b)
        self.assertEqual(header_shape(a),header_shape(b));self.assertEqual(body_signature(a),body_signature(b))
        for prefix,name in (("wsa","To"),("wsa","Action")):
            self.assertEqual(header_text(a,prefix,name),header_text(b,prefix,name))
        self.assertIsNotNone(header_text(a,"wsa","RelatesTo"));self.assertIsNotNone(header_text(b,"wsa","RelatesTo"))

    def test_retry_history_survives_restore_but_retry_xml_payload_is_not_available(self):
        with tempfile.TemporaryDirectory() as directory:
            app,session,_,path=self._request_snapshot(directory);one=session.transaction.message_history[0];two=session.retry();session.save_snapshot(path)
            del session,app;gc.collect();restored=EaeuXmlApplication(ROOT).open_transaction_session(path).restore.session;three=restored.retry()
            ids=[item.message_id.serialize() for item in restored.transaction.message_history]
            self.assertEqual(len(ids),3);self.assertEqual(len(set(ids)),3);self.assertEqual(three.attempt_number,3);self.assertEqual(three.retry_of,two.message_id)
            self.assertEqual(ids[:2],[one.message_id.serialize(),two.message_id.serialize()])
            self.assertFalse(hasattr(restored,"generate_retry_xml"))

    def test_previous_body_correlation_is_not_persisted_and_must_be_supplied_externally(self):
        with tempfile.TemporaryDirectory() as directory:
            app,session,_,path=self._request_snapshot(directory,seed=71)
            request_edoc=session.request_body_values["EDocHeader/EDocId"]
            self.assertEqual(session.request_body_values["EDocHeader/EDocId"],request_edoc)
            del session,app;gc.collect();fresh=EaeuXmlApplication(ROOT);restored=fresh.open_transaction_session(path,seed=71).restore.session
            self.assertEqual(restored.request_body_values,{})
            response_values=self._values(fresh,"P.MM.01.TRN.004","P.MM.01.MSG.006",72)
            self.assertNotIn("EDocHeader/EDocRefId",response_values)
            response=restored.generate_response("P.MM.01.MSG.006",response_values,
                body_correlations={"EDocHeader/EDocRefId":request_edoc})
            self.assertTrue(response.success);root=parsed(response.xml)
            self.assertEqual(local_values(root,"EDocRefId"),(request_edoc,))
            self.assertNotEqual(request_edoc,response.metadata["relates_to"])

    def test_signal_and_fault_after_restore_serialize_with_preserved_context(self):
        app=EaeuXmlApplication(ROOT);session=app.start_transaction("P.MM.01","P.MM.01.TRN.008")
        initial=session.generate_initial_message();source=session.historical_application_message(initial.metadata["message_id"])
        first=session.create_signal(source,SignalKind.RECEIVED);snapshot=session.create_snapshot()
        restored=EaeuXmlApplication(ROOT).open_transaction_session(self._save_temp(snapshot)).restore.session
        source2=restored.historical_application_message(initial.metadata["message_id"]);second=restored.create_signal(source2,SignalKind.ACCEPTED_FOR_PROCESSING)
        signal_root=parsed(restored.serializer.serialize_signal(second))
        self.assertNotEqual(second.header.message_id,first.header.message_id);self.assertEqual(header_text(signal_root,"wsa","RelatesTo"),initial.metadata["message_id"])
        self.assertEqual(header_text(signal_root,"int","ProcedureID"),snapshot.procedure_id);self.assertEqual(header_text(signal_root,"int","ConversationID"),snapshot.conversation_id)
        self.assertEqual(restored.transaction.state.value,"WAITING_RESPONSE")

        request_app=EaeuXmlApplication(ROOT);request_session=request_app.start_transaction("P.MM.01","P.MM.01.TRN.004");request=request_session.generate_initial_message();request_snapshot=request_session.create_snapshot()
        fault_restored=EaeuXmlApplication(ROOT).open_transaction_session(self._save_temp(request_snapshot)).restore.session
        fault_source=fault_restored.historical_application_message(request.metadata["message_id"])
        fault=fault_restored.create_fault(fault_source,fault_source.header.reply_to.address,SoapFault(FaultSubcode.INVALID_HEADER,(FaultReasonText("Некорректный заголовок","ru"),)))
        fault_root=parsed(fault_restored.serializer.serialize_fault(fault))
        self.assertNotEqual(header_text(fault_root,"wsa","MessageID"),request.metadata["message_id"])
        self.assertEqual(header_text(fault_root,"wsa","RelatesTo"),request.metadata["message_id"])
        relates=fault_root.find("./soap:Header/wsa:RelatesTo",NS);self.assertEqual(relates.get(f"{{{NS['int']}}}RelatesAction"),request.metadata["action"])
        self.assertEqual(header_text(fault_root,"int","ProcedureID"),request_snapshot.procedure_id);self.assertEqual(header_text(fault_root,"int","ConversationID"),request_snapshot.conversation_id)
        self.assertIsNotNone(fault_root.find("./soap:Body/soap:Fault",NS))

    def test_notification_restore_keeps_notification_semantics_and_next_signal_xml(self):
        app=EaeuXmlApplication(ROOT);session=app.start_transaction("P.MM.01","P.MM.01.TRN.011");notification=session.generate_initial_message()
        root=parsed(notification.xml);self.assertIsNone(header_text(root,"wsa","RelatesTo"));snapshot=session.create_snapshot()
        restored=EaeuXmlApplication(ROOT).open_transaction_session(self._save_temp(snapshot)).restore.session
        source=restored.historical_application_message(notification.metadata["message_id"]);signal=restored.create_signal(source,SignalKind.RECEIVED)
        signal_root=parsed(restored.serializer.serialize_signal(signal));self.assertEqual(header_text(signal_root,"wsa","RelatesTo"),notification.metadata["message_id"])
        self.assertEqual(restored.transaction.state.value,"COMPLETED");self.assertEqual(len([item for item in restored.transaction.message_history if item.message_kind.value=="APPLICATION"]),1)

    def test_open_as_new_and_legacy_draft_xml_have_fresh_soap_context(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);old=GuiController(EaeuXmlApplication(ROOT,drafts_root=root));old.select_process("P.MM.01");old.select_transaction("P.MM.01.TRN.004");old.select_message("P.MM.01.MSG.005");old.apply_test_data();old_request=old.generate_xml();old_snapshot=old.session.create_snapshot()
            draft=root/"body.eaeudraft.json";old.save_draft(draft)
            fresh=GuiController(EaeuXmlApplication(ROOT,drafts_root=root));fresh.open_draft_as_new(draft);new=fresh.generate_xml();self.assertTrue(new.success)
            xml=parsed(new.xml);self.assertNotEqual(header_text(xml,"int","ProcedureID"),old_snapshot.procedure_id);self.assertNotEqual(header_text(xml,"int","ConversationID"),old_snapshot.conversation_id)
            self.assertNotEqual(header_text(xml,"wsa","MessageID"),old_request.metadata["message_id"]);self.assertIsNone(header_text(xml,"wsa","RelatesTo"));self.assertEqual(len(fresh.session.transaction.message_history),1)
            legacy_open=fresh.open_session_snapshot(draft);self.assertIs(legacy_open.status,SessionRestoreStatus.SNAPSHOT_INVALID);self.assertFalse(fresh.session_continue_enabled)

    def test_invalid_restore_statuses_cannot_generate_continuation_xml(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);app,session,_,_=self._request_snapshot(root);snapshot=session.create_snapshot()
            bad=root/"bad.eaeusession.json";bad.write_text("{bad",encoding="utf-8")
            mismatch=replace(snapshot,process_version="9.9.9",history=tuple(replace(item,action=item.action.replace("/1.1.0/","/9.9.9/")) for item in snapshot.history));mismatch_path=root/"mismatch.eaeusession.json";SessionPersistenceService().save(mismatch,mismatch_path)
            old="2020-01-01T00:00:00+00:00";stale=replace(snapshot,history=tuple(replace(item,created_at=old) for item in snapshot.history));stale_path=root/"stale.eaeusession.json";SessionPersistenceService().save(stale,stale_path)
            state_path=root/"state.eaeusession.json";state_path.write_text(json.dumps(asdict(replace(snapshot,current_state="COMPLETED"))),encoding="utf-8")
            for path,status in ((bad,SessionRestoreStatus.SNAPSHOT_INVALID),(mismatch_path,SessionRestoreStatus.PROCESS_VERSION_MISMATCH),(stale_path,SessionRestoreStatus.TIMING_REVALIDATION_REQUIRED),(state_path,SessionRestoreStatus.STATE_INVALID)):
                with self.subTest(status=status):
                    controller=GuiController(EaeuXmlApplication(ROOT,drafts_root=root));opened=controller.open_session_snapshot(path);self.assertIs(opened.status,status);self.assertFalse(controller.session_continue_enabled)
                    with self.assertRaises(ValueError):controller.continue_session()
                    controller.select_process("P.MM.01");controller.select_transaction("P.MM.01.TRN.004");controller.select_message("P.MM.01.MSG.006");controller.apply_test_data();result=controller.generate_xml()
                    self.assertFalse(result.success);self.assertEqual(result.status,"INITIAL_MESSAGE_REQUIRED")

    def test_failed_response_validation_does_not_mutate_restored_history(self):
        with tempfile.TemporaryDirectory() as directory:
            _,_,_,path=self._request_snapshot(directory);restored=EaeuXmlApplication(ROOT).open_transaction_session(path).restore.session
            before=restored.create_snapshot();failed=restored.generate_response("P.MM.01.MSG.006",{})
            self.assertFalse(failed.success);self.assertEqual(restored.create_snapshot(),before)

    def _save_temp(self,snapshot):
        directory=tempfile.mkdtemp();path=Path(directory)/"session.eaeusession.json";SessionPersistenceService().save(snapshot,path);self.addCleanup(lambda:__import__("shutil").rmtree(directory,ignore_errors=True));return path


if __name__=="__main__":unittest.main()
