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
    assert len(data['structured_rules']) == 18
    assert {r['rule_id'].rsplit('.',1)[1] for r in data['structured_rules']} == {str(x) for x in [1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]}
    assert all(r['source_refs'] for r in data['structured_rules'])
