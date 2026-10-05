"""Production extraction proof for Table70 REQ22 and REQ24."""
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = 'P.SP.02.MSG.052'

@pytest.fixture(scope='module')
def engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def extracted(engine, order, case):
    structure = engine.resolve_structure('R.IP.SP.02.007', mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    def child(parent, path, value=None, wrong=False):
        for qname in path.split('/'):
            prefix, local = qname.split(':')
            parent = ET.SubElement(parent, ET.QName('urn:wrong' if wrong else structure.imported_namespaces[prefix], local))
        parent.text = value
        return parent
    for role in order:
        rec = child(root, 'ipcdo:UnifiedRegisterRecordsDetails')
        child(rec, 'ipcdo:IPEntityStatusDetails/csdo:StatusCode', role)
        if role == '04':
            validity = child(rec, 'ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails')
            child(validity, 'csdo:StartDateTime', '2026-01-01T09:00:00+03:00')
            end = {'equal_start':'2026-01-01T06:00:00Z','equal_new':'2026-01-01T08:00:00Z','after_new':'2026-01-01T09:00:00Z','invalid':'bad'}.get(case,'2026-01-01T10:00:00+03:00')
            if case != 'missing_end':
                child(validity, 'csdo:EndDateTime', end, wrong=case=='wrong_date_qname')
            if case != 'misowned_id':
                child(rec, 'ipcdo:RegistrationCancellationDetails/ipcdo:ComplaintInvalidateProtectionTrademarkDetails/ipsdo:TrademarkNewId', 'OTHER' if case=='different_id' else 'NEW', wrong=case=='wrong_id_qname')
        else:
            child(rec, 'ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime', '2026-01-01T08:00:00Z')
            if case != 'missing_id': child(rec, 'ipsdo:TrademarkId', 'NEW')
            if case == 'misowned_id': child(rec, 'ipcdo:RegistrationCancellationDetails/ipcdo:ComplaintInvalidateProtectionTrademarkDetails/ipsdo:TrademarkNewId', 'NEW')
    parsed = ET.fromstring(ET.tostring(root))
    return engine.body_provider._values_from_element(structure, parsed)[0]


@pytest.mark.parametrize('order', [('04','01'),('01','04')], ids=['CANCEL_NEW','NEW_CANCEL'])
@pytest.mark.parametrize('case', ['valid','equal_start','equal_new','after_new','invalid','missing_end','wrong_date_qname','different_id','missing_id','misowned_id','wrong_id_qname'])
def test_msg052_production_date_and_equality(engine, order, case):
    values = extracted(engine, order, case)
    for code in (22,24):
        prefix = f'{MESSAGE}.T70.REQ.{code}'
        rules = [r for r in engine.rules[MESSAGE].structured_rules if r['rule_id']==prefix or r['rule_id'].startswith(prefix+'.')]
        assert rules
        statuses = [StructuredRuleEvaluator().evaluate(r,values).status for r in rules]
        bad = case in (['equal_start','equal_new','after_new','invalid','missing_end','wrong_date_qname'] if code==22 else ['different_id','missing_id','misowned_id','wrong_id_qname'])
        assert (RuleStatus.FAIL in statuses) == bad
        assert all(s in (RuleStatus.PASS, RuleStatus.FAIL) for s in statuses)
