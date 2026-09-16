from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

import wx

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.gui.main_frame import MainFrame


@unittest.skipUnless(wx.App.IsDisplayAvailable(), "requires an active wx display")
class GuiWorkspaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = wx.GetApp() or wx.App(False)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.frame = MainFrame(EaeuXmlApplication(Path(__file__).parent / "fixtures", drafts_root=Path(self.temp.name)))
        self.frame.Show()
        self.app.Yield()

    def tearDown(self):
        timer = self.frame.autosave_timer
        self.frame.Destroy()
        self.assertFalse(timer.IsRunning())
        self.app.Yield()
        self.temp.cleanup()

    def test_navigation_and_home_actions(self):
        frame = self.frame
        self.assertTrue(frame.process_choice.GetStringSelection().startswith("P.TS.01"))
        self.assertTrue(frame.transaction_choice.GetStringSelection().startswith("TRN.001"))
        self.assertTrue(frame.message_choice.GetStringSelection().startswith("MSG.001"))
        self.assertEqual([frame.notebook.GetPageText(i) for i in range(4)], ["Главная", "XML", "Проверка", "Информация"])
        self.assertEqual(list(frame.sidebar_buttons), ["Главная", "Создание XML", "Транзакции", "Черновики", "Настройки"])
        self.assertEqual(list(frame.form_panel.sections), ["Общие сведения", "Сведения о заявителе", "Документы", "Дополнительные сведения"])
        for index in (1, 2, 3, 0):
            frame._select_tab(index)
            self.app.Yield()
            self.assertEqual(frame.notebook.GetSelection(), index)
            self.assertEqual(frame.home_actions.IsShownOnScreen(), index == 0)
        frame._select_tab(4)
        self.assertIs(frame.page_book.GetCurrentPage(), frame.settings_page)
        frame._select_tab(0)
        self.assertIs(frame.page_book.GetCurrentPage(), frame.creation_page)
        self.assertEqual([child.GetLabel() for child in frame.home_actions.GetChildren()], ["Тестовые данные", "Сохранить черновик", "Создать XML"])

    def test_generated_xml_format_and_download_preserve_document(self):
        frame = self.frame
        frame.on_test_data(None)
        frame.on_generate(None)
        self.assertEqual(frame.notebook.GetSelection(), 1)
        original = ET.fromstring(frame.xml_panel.get_xml_text())
        frame.xml_panel._on_format(None)
        target = Path(self.temp.name) / "message.xml"
        frame._save_current_xml(target)
        self.assertEqual(target.read_text(), frame.xml_panel.get_xml_text())
        self.assertEqual(ET.fromstring(target.read_text()).tag, original.tag)
        self.assertTrue(frame.buttons["Сохранить XML"].IsEnabled())
        frame._select_tab(0)
        frame._select_tab(1)
        self.assertFalse(frame.home_actions.IsShownOnScreen())

    def test_information_sections_follow_selected_message(self):
        frame = self.frame
        frame._select_tab(3)
        panel = frame.info_panel
        self.assertEqual(len(panel.menu_buttons), 7)
        for index in range(7):
            panel.select_section(index)
            self.app.Yield()
            self.assertGreater(panel.content.GetSizer().GetItemCount(), 0)
        self.assertEqual(panel.guide.message_code, frame.controller.message_code)
        frame.controller.select_message("P.TS.01.MSG.002")
        frame._refresh_form()
        self.assertEqual(frame.notebook.GetSelection(), 3)
        frame._select_tab(3)
        self.assertEqual(panel.guide.message_code, "P.TS.01.MSG.002")
        panel.select_section(0)
        text = "\n".join(value for _, value, _ in panel._wrapping)
        self.assertIn(frame.controller.process_code, text)
        self.assertIn(frame.controller.transaction_code, text)
        self.assertIn(frame.controller.message_code, text)
        frame._select_tab(0)
        frame._select_tab(3)
        self.assertFalse(frame.home_actions.IsShownOnScreen())

    def test_section_collapse_and_navigation_preserve_values_and_field_focus(self):
        frame = self.frame
        frame.on_test_data(None)
        values = frame.form_panel.get_values()
        for section in frame.form_panel.sections.values():
            section._toggle(None)
        frame._select_tab(1)
        frame._select_tab(0)
        self.assertEqual(frame.form_panel.get_values(), values)
        self.assertTrue(frame.form_panel.focus_field("Items/Name"))
        self.app.Yield()
        self.assertTrue(frame.form_panel.sections["Общие сведения"].expanded)
        self.assertIn("Наименование", frame.inspector_text.GetValue())

    def test_validation_uses_real_results_and_filtered_issue_paths(self):
        frame = self.frame
        frame.on_clear(None)
        frame._select_tab(2)
        frame.on_validate(None)
        result = frame.controller.validation
        self.assertFalse(result.is_valid)
        self.assertEqual(frame._all_validation_issues, (*result.errors, *result.warnings))
        frame._filter_validation("ERROR")
        self.assertEqual(frame.issue_list.GetItemCount(), len(result.errors))
        self.assertEqual(frame.issue_list.GetItemText(0, 3), result.errors[0].field_path)
        frame._filter_validation("INFO")
        self.assertEqual(frame.issue_list.GetItemCount(), 0)
        frame.on_test_data(None)
        frame.on_validate(None)
        self.assertTrue(frame.controller.validation.is_valid)
        self.assertIn("прошли проверку", frame.validation_summary.GetLabel())
        frame._select_tab(0)
        frame._select_tab(2)
        self.assertFalse(frame.home_actions.IsShownOnScreen())
