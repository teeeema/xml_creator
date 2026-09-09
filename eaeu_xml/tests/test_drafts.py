import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from xml.etree import ElementTree as ET

from eaeu_xml.application import DraftError, DraftService, EaeuXmlApplication


FIXTURES=Path(__file__).parent/"fixtures"


class DraftServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name); self.service=DraftService(self.root)
        self.document=self.service.new_document(process_code="P.TS.01",process_version="1.0",transaction_code="P.TS.01.TRN.001",
            message_code="P.TS.01.MSG.001",structure_id="R.TEST.001",structure_version="2.0.0",generation_mode="TEST",
            values={"Text":"Русский текст","@attribute":"A","Nested/Value":1,"Repeated":["A","B"],"Complex":[None,None],"Any":ET.Element("Payload")})
    def tearDown(self):self.temp.cleanup()

    def test_save_load_roundtrip_nested_repeatable_attributes_unicode_and_xml(self):
        path=self.root/"roundtrip.eaeudraft.json"; self.service.save_draft(self.document,path); loaded=self.service.load_draft(path)
        self.assertEqual(loaded.values["Text"],"Русский текст"); self.assertEqual(loaded.values["Repeated"],["A","B"])
        self.assertEqual(loaded.values["Complex"],[None,None]); self.assertEqual(loaded.values["@attribute"],"A")
        self.assertEqual(loaded.values["Any"].tag,"Payload"); self.assertNotIn("pickle",path.read_text(encoding="utf-8"))

    def test_invalid_json_unsupported_version_and_nonserializable_value(self):
        invalid=self.root/"bad.json"; invalid.write_text("{broken",encoding="utf-8")
        with self.assertRaises(DraftError) as raised:self.service.load_draft(invalid)
        self.assertEqual(raised.exception.code,"DRAFT_INVALID_JSON")
        data=json.loads(json.dumps({**self.document.__dict__,"values":{}})); data["draft_version"]=999; invalid.write_text(json.dumps(data),encoding="utf-8")
        with self.assertRaises(DraftError) as raised:self.service.load_draft(invalid)
        self.assertEqual(raised.exception.code,"UNSUPPORTED_DRAFT_VERSION")
        bad=self.service.new_document(process_code="P",process_version="1",transaction_code="T",message_code="M",structure_id="R",structure_version="1",generation_mode="TEST",values={"x":object()})
        with self.assertRaises(DraftError) as raised:self.service.save_draft(bad,self.root/"x.json")
        self.assertEqual(raised.exception.code,"DRAFT_VALUE_NOT_SERIALIZABLE")

    def test_atomic_write_uses_replace_and_leaves_no_temp_file(self):
        path=self.root/"atomic.eaeudraft.json"
        import eaeu_xml.application.drafts as drafts
        real_replace=drafts.os.replace
        with patch.object(drafts.os,"replace",wraps=real_replace) as replace:self.service.save_draft(self.document,path)
        replace.assert_called_once(); self.assertTrue(path.is_file()); self.assertEqual(list(self.root.glob("*.tmp")),[])

    def test_autosave_recovery_and_clean_shutdown_marker(self):
        self.service.autosave(self.document); self.assertTrue(self.service.has_recoverable_autosave())
        self.service.mark_clean_shutdown(); self.assertFalse(self.service.has_recoverable_autosave())
        self.service.clear_autosave(); self.assertFalse(self.service.autosave_path.exists())


class DraftFacadeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name); self.app=EaeuXmlApplication(FIXTURES,drafts_root=self.root)
    def tearDown(self):self.temp.cleanup()

    def _save(self,values=None):
        path=self.root/"fixture.eaeudraft.json"; self.app.save_draft(path,process_code="P.TS.01",transaction_code="P.TS.01.TRN.001",message_code="P.TS.01.MSG.001",values=values or {"Items":None,"Items/Name":"Draft"}); return path

    def test_facade_load_revalidates_and_reports_unknown_fields_and_new_required(self):
        path=self._save({"Unknown/Old":"kept"}); result=self.app.load_draft(path)
        self.assertEqual(result.unmapped_values,{"Unknown/Old":"kept"}); self.assertIn("UNMAPPED_DRAFT_FIELDS",result.warnings[0])
        self.assertFalse(result.validation.is_valid); self.assertIn("MIN_OCCURS",{item.code for item in result.validation.errors})

    def test_version_mismatch_is_warning_and_compatible_values_load(self):
        path=self._save(); data=json.loads(path.read_text(encoding="utf-8")); data["structure_version"]="1.0.0"; path.write_text(json.dumps(data),encoding="utf-8")
        result=self.app.load_draft(path); self.assertEqual(result.compatible_values["Items/Name"],"Draft")
        self.assertTrue(any(item.startswith("STRUCTURE_VERSION_MISMATCH") for item in result.warnings))

    def test_unmapped_values_survive_subsequent_manual_save(self):
        path=self._save({"Items/Name":"Draft","Unknown/Old":"kept"}); loaded=self.app.load_draft(path)
        self.app.save_draft(path,process_code="P.TS.01",transaction_code="P.TS.01.TRN.001",message_code="P.TS.01.MSG.001",
            values={"Items/Name":"Changed"},previous_document=loaded.document)
        document=self.app.drafts.load_draft(path)
        self.assertEqual(document.values["Items/Name"],"Changed"); self.assertEqual(document.values["Unknown/Old"],"kept")

    def test_unknown_process_transaction_and_message_are_typed(self):
        for key,value,code in (("process_code","P.UNKNOWN","DRAFT_PROCESS_UNKNOWN"),("transaction_code","P.TS.01.TRN.999","DRAFT_TRANSACTION_UNKNOWN"),("message_code","P.TS.01.MSG.999","DRAFT_MESSAGE_UNKNOWN")):
            path=self._save(); data=json.loads(path.read_text(encoding="utf-8")); data[key]=value; path.write_text(json.dumps(data),encoding="utf-8")
            with self.subTest(key=key),self.assertRaises(DraftError) as raised:self.app.load_draft(path)
            self.assertEqual(raised.exception.code,code)


if __name__=="__main__":unittest.main()
