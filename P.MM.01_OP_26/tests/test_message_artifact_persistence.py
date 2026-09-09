from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.application.message_artifacts import PersistedMessageArtifact,SessionBundlePersistenceService
from eaeu_xml.application.session_snapshot import SessionSnapshotError

ROOT=Path(__file__).parents[2]


class MessageArtifactPersistenceTests(unittest.TestCase):
    def request_bundle(self,directory):
        app=EaeuXmlApplication(ROOT,drafts_root=directory);session=app.start_transaction("P.MM.01","P.MM.01.TRN.004",seed=91)
        values=app.generate_test_data("P.MM.01","P.MM.01.TRN.004","P.MM.01.MSG.005",seed=91);request=session.generate_initial_message(values);path=Path(directory)/"session.eaeusession.json";session.save_bundle(path)
        return app,session,request,values,path

    def test_body_roundtrip_is_immutable_and_supports_binary_bool_lists_nested_and_xml(self):
        values={"Binary":"cGF5bG9hZA==","Flag":True,"Items":["A",{"x":False}],"Nested":{"@id":"1"},"Any":ET.Element("X")}
        artifact=PersistedMessageArtifact.from_values(message_id_ref="urn:uuid:00000000-0000-4000-8000-000000000001",transaction_code="T",message_code="M",attempt_number=1,values=values)
        values["Binary"]="changed";restored=artifact.values()
        self.assertEqual(restored["Binary"],"cGF5bG9hZA==");self.assertTrue(restored["Flag"]);self.assertEqual(restored["Items"],["A",{"x":False}]);self.assertEqual(restored["Nested"],{"@id":"1"});self.assertEqual(restored["Any"].tag,"X")

    def test_bundle_restart_resolves_edoc_reference_without_soap_identifier(self):
        with tempfile.TemporaryDirectory() as directory:
            app,session,request,values,path=self.request_bundle(directory);original=session.artifact_for(request.metadata["message_id"]);self.assertEqual(original.values()["EDocHeader/EDocId"],values["EDocHeader/EDocId"])
            restored=EaeuXmlApplication(ROOT).open_transaction_session(path).restore.session
            response=restored.generate_response("P.MM.01.MSG.006");self.assertTrue(response.success)
            root=ET.fromstring(response.xml);edoc=root.findtext(".//{urn:EEC:M:SimpleDataObjects:vX.X.X}EDocRefId")
            self.assertEqual(edoc,values["EDocHeader/EDocId"]);self.assertNotEqual(edoc,response.metadata["relates_to"])

    def test_retry_after_restart_reuses_artifact_body_with_new_header(self):
        with tempfile.TemporaryDirectory() as directory:
            _,session,request,values,path=self.request_bundle(directory);restored=EaeuXmlApplication(ROOT).open_transaction_session(path).restore.session
            retry=restored.retry_with_payload(request.metadata["message_id"]);self.assertTrue(retry.success)
            root=ET.fromstring(retry.xml);self.assertNotEqual(retry.metadata["message_id"],request.metadata["message_id"]);self.assertIsNone(root.find(".//{http://www.w3.org/2005/08/addressing}RelatesTo"))
            self.assertEqual(restored.transaction.message_history[-1].retry_of.serialize(),request.metadata["message_id"]);self.assertEqual(len(restored.message_artifacts),2)
            body=root.find("{http://www.w3.org/2003/05/soap-envelope}Body");self.assertIsNotNone(body)

    def test_corrupt_or_history_mismatched_bundle_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            _,session,_,_,path=self.request_bundle(directory);bundle=SessionBundlePersistenceService().load(path);artifact=bundle.artifacts[0]
            corrupt=replace(artifact,payload_sha256="0"*64)
            with self.assertRaises(SessionSnapshotError):SessionBundlePersistenceService().save(bundle.snapshot,(corrupt,),Path(directory)/"corrupt.json")
            wrong=replace(artifact,message_id_ref="urn:uuid:00000000-0000-4000-8000-000000000002")
            with self.assertRaises(SessionSnapshotError):SessionBundlePersistenceService().save(bundle.snapshot,(wrong,),Path(directory)/"wrong.json")

    def test_missing_artifact_blocks_payload_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            _,session,request,_,path=self.request_bundle(directory);bundle=SessionBundlePersistenceService().load(path);empty=Path(directory)/"empty.eaeusession.json";SessionBundlePersistenceService().save(bundle.snapshot,(),empty)
            restored=EaeuXmlApplication(ROOT).open_transaction_session(empty).restore.session
            with self.assertRaises(ValueError):restored.retry_with_payload(request.metadata["message_id"])


if __name__=="__main__":unittest.main()
