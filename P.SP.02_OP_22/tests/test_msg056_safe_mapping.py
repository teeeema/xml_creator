import json
from pathlib import Path

PACKAGE=Path(__file__).resolve().parents[1]
MESSAGE='P.SP.02.MSG.056'

def test_inventory_and_mapping_boundary():
    data=json.loads((PACKAGE/'message_rules'/f'{MESSAGE}.yaml').read_text()); audit=data['mapping_audit']
    assert (audit['captured_row_count'],audit['expanded_requirement_count']) == (15,20)
    assert audit['summary']['FULLY_MAPPABLE'] == [1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,20]
    assert audit['summary']['SAFE_PARTIAL'] == [19]
    assert audit['summary']['EXTERNAL'] == [4,5]
    assert len(data['structured_rules']) == 21
    rule_ids={rule['rule_id'] for rule in data['structured_rules']}
    assert {
        f'{MESSAGE}.T74.REQ.20',
        f'{MESSAGE}.T74.REQ.20.DOC_ID',
        f'{MESSAGE}.T74.REQ.20.DUTY_PAYMENT_INDICATOR',
        f'{MESSAGE}.T74.REQ.20.PAYMENT_AMOUNT',
    } <= rule_ids
    assert {r['rule_id'].split('.REQ.',1)[1].split('.',1)[0] for r in data['structured_rules']} == {str(x) for x in [1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]}
    assert all(r['source_refs'] for r in data['structured_rules'])
