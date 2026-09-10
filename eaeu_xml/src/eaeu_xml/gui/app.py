import argparse
import logging
from pathlib import Path
import sys

from eaeu_xml.application import EaeuXmlApplication


def main(argv=None):
    parser=argparse.ArgumentParser(description="ГИС_xml — настольное GUI-приложение")
    parser.add_argument("processes_root",nargs="?",type=Path,help="Directory containing external process packages")
    args=parser.parse_args(argv); logging.basicConfig(level=logging.INFO)
    try: import wx
    except ImportError:
        print('wxPython is required for GUI. Install with: pip install -e ".[gui]"',file=sys.stderr); return 2
    app=wx.App(False); root=args.processes_root
    if root is None:
        with wx.DirDialog(None,"Выберите корневую папку общих процессов",style=wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST) as dialog:
            if dialog.ShowModal()==wx.ID_CANCEL:return 0
            root=Path(dialog.GetPath())
    from eaeu_xml.gui.main_frame import MainFrame
    frame=MainFrame(EaeuXmlApplication(root)); frame.Show(); app.MainLoop(); return 0
