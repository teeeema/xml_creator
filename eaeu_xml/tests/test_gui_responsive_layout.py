from pathlib import Path
import tempfile
import unittest

import wx

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.gui.main_frame import MainFrame


FIXTURES = Path(__file__).parent / "fixtures"
DISPLAY_AVAILABLE = wx.App.IsDisplayAvailable()


@unittest.skipUnless(DISPLAY_AVAILABLE, "requires an active wx display")
class GuiResponsiveLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wx_app = wx.GetApp() or wx.App(False)

    def test_narrow_resize_keeps_actions_and_both_form_scroll_axes_available(self):
        with tempfile.TemporaryDirectory() as drafts:
            frame = MainFrame(EaeuXmlApplication(FIXTURES, drafts_root=Path(drafts)))
            try:
                frame.Show(); frame.SetSize((700, 560)); self.wx_app.Yield()
                frame._apply_responsive_layout(); self.wx_app.Yield()

                self.assertEqual(frame.GetMinSize(), wx.Size(700, 560))
                style = frame.form_panel.GetWindowStyleFlag()
                self.assertTrue(style & wx.HSCROLL)
                self.assertTrue(style & wx.VSCROLL)

                client_width = frame.data_tab.GetClientSize().width
                for label in (
                    "Открыть черновик", "Сохранить черновик", "Заполнить тестовыми",
                    "Проверить", "Очистить", "Начать новую транзакцию", "Сформировать XML",
                ):
                    button = frame.buttons[label]
                    self.assertTrue(button.IsShown())
                    self.assertLessEqual(button.GetPosition().x + button.GetSize().width, client_width)

                frame.SetSize((1100, 760)); self.wx_app.Yield()
                frame._apply_responsive_layout(); self.wx_app.Yield()
                self.assertGreater(frame.form_panel.GetClientSize().width, 0)
                self.assertGreater(frame.form_panel.GetClientSize().height, 0)
            finally:
                frame.Destroy(); self.wx_app.Yield()


if __name__ == "__main__": unittest.main()
