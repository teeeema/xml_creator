import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.035"
APP = "ipcdo:TrademarkApplicationDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
FULL = ({1, 4, 5, *range(6, 13), 14, 15, *range(21, 26), 27, 28, 29}) | {16, 17, 18, 19, 20, 26}
PARTIAL = {2, 3}
UNMAPPED = ({13, 16, 17, 18, 19, 20, 26}) - {16, 17, 18, 19, 20, 26}


def _raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def _rules(code):
    prefix = f"{MESSAGE}.T53.REQ.{code}"
    return [r for r in _raw()["structured_rules"] if r["rule_id"] == prefix or r["rule_id"].startswith(prefix + ".")]


def _inventory(code):
    return next(x for x in _raw()["mapping_audit"]["inventory"] if x["requirement_code"] == str(code))


def test_inventory_classification_and_mapped_sets_are_exact():
    data = _raw()
    audit = data["mapping_audit"]
    assert audit["captured_row_count"] == 6
    assert audit["expanded_requirement_count"] == 29
    assert {int(x["requirement_code"]) for x in audit["inventory"]} == set(range(1, 30))
    assert audit["summary"] == {
        "FULLY_MAPPABLE": sorted(FULL),
        "SAFE_PARTIAL": sorted(PARTIAL),
        "AMBIGUOUS": [13],
        "ENGINE_UNSUPPORTED": [],
        "EXTERNAL": [],
        "SOURCE_CONFLICT": [],
    }
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 26,
        "SAFE_PARTIAL": 2,
        "AMBIGUOUS": 1,
        "ENGINE_UNSUPPORTED": 0,
        "EXTERNAL": 0,
        "SOURCE_CONFLICT": 0,
    }
    mapped = {int(r["rule_id"].split(".REQ.", 1)[1].split(".", 1)[0]) for r in data["structured_rules"]}
    assert mapped == FULL | PARTIAL
    assert mapped.isdisjoint(UNMAPPED)
    assert len(data["structured_rules"]) == len({r["rule_id"] for r in data["structured_rules"]}) == 31
    assert all(r["rule_id"].startswith(MESSAGE + ".") for r in data["structured_rules"])


def test_direct_req1_to_req5_use_exact_local_fragments_and_owners():
    req1, = _rules(1)
    assert req1["selector"] == {"collection": APP}
    assert (req1["min_occurs"], req1["max_occurs"]) == (1, 1)

    req2, = _rules(2)
    assert req2["mapping_status"] == "PARTIAL"
    assert req2["selector"] == {"collection": APP}
    assert req2["assertions"] == [{"kind": "presence", "target": {"field": "ipsdo:IPDocKindCode"}, "state": "REQUIRED"}]
    assert _inventory(2)["safe_fragment"].startswith("Direct TrademarkApplicationDetails/ipsdo:IPDocKindCode")
    assert "classifier" in _inventory(2)["external_dependency"]

    req3, = _rules(3)
    assert req3["mapping_status"] == "PARTIAL"
    assert req3["selector"] == {"collection": APP}
    assert req3["assertions"] == [{"kind": "presence", "target": {"field": "ipsdo:TrademarkApplicationId"}, "state": "REQUIRED"}]
    assert len(_inventory(3)["unmapped_remainder"]) == 4

    req4, = _rules(4)
    req5, = _rules(5)
    assert req4["selector"] == req5["selector"] == {"collection": RESOURCE}
    assert req4["assertions"] == [{"kind": "presence", "target": {"field": "ccdo:ValidityPeriodDetails/csdo:StartDateTime"}, "state": "REQUIRED"}]
    assert req5["assertions"] == [{"kind": "presence", "target": {"field": "ccdo:ValidityPeriodDetails/csdo:EndDateTime"}, "state": "FORBIDDEN"}]


def test_inherited_requirements_keep_table53_plus_original_table44_provenance():
    for code in range(6, 30):
        item = _inventory(code)
        refs = item["source_refs"]
        assert refs[0]["table"] == "53"
        assert refs[0]["item"] == "6-29"
        assert refs[0]["source_id"] == "22OP-RULE-P.SP.02.MSG.035-T53-6-29"
        assert refs[1]["table"] == "44"
        assert refs[1]["item"] == str(code)
        assert item["provenance_kind"] == "INHERITED"
        for rule in _rules(code):
            assert [ref["table"] for ref in rule["source_refs"]] == ["53", "44"]


def test_new_mappings_preserve_sources_and_remaining_unmapped_requirements():
    data = _raw()
    inventory = data['mapping_audit']['inventory']
    by_code = {item['requirement_code']: item for item in inventory}
    assert by_code['13']['classification'] == 'AMBIGUOUS'
    for item in inventory:
        code = item['requirement_code']
        prefix = MESSAGE + '.T' + item['source_refs'][0]['table'] + '.REQ.' + code
        executable = [r for r in data['structured_rules'] if r['rule_id'] == prefix or r['rule_id'].startswith(prefix + '.')]
        if item['classification'] in ('EXTERNAL', 'AMBIGUOUS', 'ENGINE_UNSUPPORTED', 'SOURCE_CONFLICT'):
            assert not executable
        if code in ('16', '17', '18', '19', '20', '26'):
            assert item['classification'] == 'FULLY_MAPPABLE'
            assert item['mapping_status'] == 'EXECUTABLE'
            assert item['engine_gap'] is None
            assert executable
            assert all(r['source_refs'] == item['source_refs'] for r in executable)
            if code == '26':
                assert 'any' in executable[0]['assertions'][0]['condition']


def test_req27_preserves_same_trademark_code_or_name_trigger():
    req27, = _rules(27)
    assert req27["selector"] == {"collection": f"{APP}/ipcdo:TrademarkDetails"}
    assert {a["target"]["field"] for a in req27["assertions"]} == {"ipsdo:TrademarkPicture", "ipsdo:TrademarkColourName"}
    for assertion in req27["assertions"]:
        assert set(assertion["condition"]) == {"any"}
        assert {x["field"] for x in assertion["condition"]["any"]} == {"ipsdo:TrademarkKindCode", "ipsdo:TrademarkKindName"}


def test_normative_context_and_rule_ids_are_msg035_specific():
    ctx = _raw()["mapping_audit"]["normative_context"]
    assert ctx["transaction"] == "P.SP.02.TRN.030"
    assert ctx["procedure"] == "P.SP.02.PRC.011"
    assert ctx["initiating_operation"] == "P.SP.02.OPR.044"
    assert ctx["responding_operation"] == "P.SP.02.OPR.045"
    assert ctx["initiating_participant"] == "P.SP.02.ACT.002"
    assert ctx["responding_participant"] == "P.SP.02.ACT.001"
    assert ctx["response_message"] == "P.SP.02.MSG.002"
    assert ctx["table"] == "53"
