from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

import wx

from eaeu_xml.application import EaeuXmlApplication,SessionRestoreStatus
from eaeu_xml.gui.main_frame import MainFrame


ROOT=Path(__file__).parents[2]
DISPLAY_AVAILABLE = wx.App.IsDisplayAvailable()


@unittest.skipUnless(DISPLAY_AVAILABLE, "requires an active wx display")
class GuiSessionControlsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.wx_app=wx.GetApp() or wx.App(False)

    def test_real_frame_save_restart_continue_response_and_invalid_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            work=Path(directory);snapshot_path=work/"request.eaeusession.json"
            first=MainFrame(EaeuXmlApplication(ROOT,drafts_root=work));first.Show();self.wx_app.Yield()
            first.controller.select_process("P.MM.01");first.controller.select_transaction("P.MM.01.TRN.004");first.controller.select_message("P.MM.01.MSG.005")
            first.controller.apply_test_data();request_edoc=first.controller.values["EDocHeader/EDocId"];request=first.controller.generate_xml();self.assertTrue(request.success)
            first._refresh_session_ui();first._save_session_path(snapshot_path);self.assertTrue(snapshot_path.is_file())
            original=first.controller.session.create_snapshot();first.Destroy();self.wx_app.Yield()

            restored_frame=MainFrame(EaeuXmlApplication(ROOT,drafts_root=work));restored_frame.Show();self.wx_app.Yield()
            try:
                opened=restored_frame._open_session_path(snapshot_path)
                self.assertIs(opened.status,SessionRestoreStatus.RESTORABLE)
                self.assertTrue(restored_frame.buttons["Продолжить сессию"].IsEnabled())
                restored_frame.on_continue_session(None)
                session=restored_frame.controller.session
                self.assertEqual(session.transaction.procedure_instance.procedure_id.serialize(),original.procedure_id)
                self.assertEqual(session.transaction.conversation_id.serialize(),original.conversation_id)
                self.assertEqual(session.transaction.message_history[0].message_id.serialize(),original.history[0].message_id)
                restored_frame.controller.select_message("P.MM.01.MSG.006");restored_frame.controller.apply_test_data()
                self.assertNotIn("EDocHeader/EDocRefId",restored_frame.controller.values)
                response=restored_frame.controller.generate_xml();self.assertTrue(response.success)
                xml=ET.fromstring(response.xml);namespaces={"soap":"http://www.w3.org/2003/05/soap-envelope","wsa":"http://www.w3.org/2005/08/addressing","int":"urn:EEC:Interaction:v1.0"}
                value=lambda prefix,name:xml.find(f"./soap:Header/{prefix}:{name}",namespaces).text
                self.assertNotEqual(response.metadata["message_id"],request.metadata["message_id"])
                self.assertEqual(response.metadata["relates_to"],request.metadata["message_id"])
                self.assertEqual(response.metadata["procedure_id"],request.metadata["procedure_id"])
                self.assertEqual(response.metadata["conversation_id"],request.metadata["conversation_id"])
                self.assertEqual(value("wsa","MessageID"),response.metadata["message_id"])
                self.assertEqual(value("wsa","RelatesTo"),request.metadata["message_id"])
                self.assertEqual(value("int","ProcedureID"),request.metadata["procedure_id"])
                self.assertEqual(value("int","ConversationID"),request.metadata["conversation_id"])
                self.assertEqual(value("wsa","Action"),response.metadata["action"])
                self.assertEqual(xml.findtext(".//{urn:EEC:M:SimpleDataObjects:vX.X.X}EDocRefId"),request_edoc)

                invalid=work/"invalid.eaeusession.json";invalid.write_text("not json",encoding="utf-8")
                bad=restored_frame._open_session_path(invalid)
                self.assertIs(bad.status,SessionRestoreStatus.SNAPSHOT_INVALID)
                self.assertFalse(restored_frame.buttons["Продолжить сессию"].IsEnabled())

                for size in ((1200,800),(900,650),(700,560),(1100,760)):
                    restored_frame.SetSize(size);self.wx_app.Yield();restored_frame._apply_responsive_layout();self.wx_app.Yield()
                    width=restored_frame.data_tab.GetClientSize().width
                    for label in ("Открыть сессию","Продолжить сессию","Открыть как новую","Сохранить сессию","ⓘ Сведения о сессии"):
                        button=restored_frame.buttons[label]
                        self.assertTrue(button.IsShown())
                        self.assertLessEqual(button.GetPosition().x+button.GetSize().width,width)
            finally:
                restored_frame.Destroy();self.wx_app.Yield()


if __name__=="__main__":unittest.main()
