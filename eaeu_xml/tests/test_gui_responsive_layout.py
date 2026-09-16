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
                for label in ("Сохранить черновик", "Заполнить тестовыми", "Сформировать XML"):
                    button = frame.buttons[label]
                    self.assertTrue(button.IsShownOnScreen())
                    self.assertLessEqual(frame.data_tab.ScreenToClient(button.GetScreenPosition()).x + button.GetSize().width, client_width)

                frame.SetSize((1100, 760)); self.wx_app.Yield()
                frame._apply_responsive_layout(); self.wx_app.Yield()
                self.assertGreater(frame.form_panel.GetClientSize().width, 0)
                self.assertGreater(frame.form_panel.GetClientSize().height, 0)
                for size in ((700, 560), (900, 650), (1280, 860)):
                    frame.SetSize(size); self.wx_app.Yield()
                    for index in range(4):
                        frame._select_tab(index); self.wx_app.Yield()
                        self.assertEqual(frame.home_actions.IsShownOnScreen(), index == 0)
                        self.assertGreater(frame.notebook.GetCurrentPage().GetClientSize().height, 100)
                        for choice in (frame.process_choice, frame.transaction_choice, frame.message_choice):
                            self.assertLessEqual(choice.GetScreenRect().right, frame.GetScreenRect().right)
            finally:
                frame.Destroy(); self.wx_app.Yield()


if __name__ == "__main__": unittest.main()
