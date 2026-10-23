import os
os.environ['QT_QPA_PLATFORM']='offscreen'
from pathlib import Path
import json,importlib.util
from xml.etree import ElementTree as ET
from PySide6.QtGui import QGuiApplication
from eaeu_xml.gui_qt.view_model import GuiViewModel
from eaeu_xml.application import EaeuXmlApplication
out=Path(__file__).resolve().parent;root=out.parents[2];qt=QGuiApplication.instance() or QGuiApplication([])
app=EaeuXmlApplication(root);model=GuiViewModel(root,application=app);model.selectProcess('P.SP.02');model.selectTransaction('P.SP.02.TRN.003');model.selectMessage('P.SP.02.MSG.004')
spec=importlib.util.spec_from_file_location('fixture004',root/'P.SP.02_OP_22/tests/test_msg004_end_to_end.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.APP+'/ipsdo:IPDocKindCode';n=m.APP+'/ipsdo:IPDocKindName'
model.controller.values=m._generation_values();model.setFieldValue(c,'99999');model.setFieldValue(n,'FORBIDDEN');model.generateXml();g=model.controller.generation
assert g.success,(g.status,g.errors)
x=ET.fromstring(g.xml);s=app._engine('P.SP.02').get_structure(m.MESSAGE,mode=__import__('eaeu_xml.process_packages.body',fromlist=['GenerationMode']).GenerationMode.TEST);ns=s.imported_namespaces;owners=list(x.iter('{'+ns['ipcdo']+'}TrademarkApplicationDetails'));assert len(owners)==1
assert owners[0].find('{'+ns['ipsdo']+'}IPDocKindCode').text=='07320'
assert owners[0].find('{'+ns['ipsdo']+'}IPDocKindName') is None
(out/'GUI_GENERATED.xml').write_text(g.xml)
(out/'gui_evidence.json').write_text(json.dumps({'mode':'Qt offscreen GuiViewModel, real setFieldValue and generateXml; no desktop visual inspection','generation_status':g.status,'success':g.success,'fields':model.fields,'xml':'GUI_GENERATED.xml','fixed_tamper_sanitized':True},ensure_ascii=False,indent=2,default=str))
print('Qt GUI actual generation:',g.status,'code07320; directName absent')
