"""Offscreen rendering of the actual read-only Qt information page."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys,time
R=Path(__file__).resolve().parents[4];sys.path.insert(0,str(R/'eaeu_xml/src'))
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQuickControls2 import QQuickStyle
from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.gui_qt.view_model import GuiViewModel
QQuickStyle.setStyle('Basic');app=QApplication([])
with TemporaryDirectory() as directory:
 model=GuiViewModel(R,application=EaeuXmlApplication(R,drafts_root=Path(directory)));model.selectProcess('P.MM.01')
 widget=QQuickWidget();widget.setResizeMode(QQuickWidget.SizeRootObjectToView);widget.rootContext().setContextProperty('viewModel',model)
 widget.setSource(QUrl.fromLocalFile(str(R/'eaeu_xml/src/eaeu_xml/gui_qt/qml/pages/InformationPage.qml')))
 assert widget.status()==QQuickWidget.Ready,widget.errors()
 widget.rootObject().setProperty('selected',len(model.information)-1);widget.resize(1150,700);widget.show()
 for i in range(8):app.processEvents();time.sleep(.03)
 image=widget.grabFramebuffer();assert not image.isNull()
 assert image.save(str(R/'codex_reports/OP26_P_MM_01/V130_STAGE3/verification/gui_editions.png'))
 print(model.information[-1]);print(image.size());widget.close();app.processEvents()
