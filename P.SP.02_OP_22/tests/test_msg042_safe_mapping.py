import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.042"
APP = "ipcdo:TrademarkApplicationDetails"
FULL = {1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35}
UNMAPPED = ({2, 3, 13, 16, 17, 18, 19, 20, 26}) - {16, 17, 18, 19, 20, 26}


def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text())


def rules(code):
    prefix = f"{MESSAGE}.T60.REQ.{code}"
    return [rule for rule in raw()["structured_rules"] if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")]


def test_inventory_and_classification_are_exact():
    audit = raw()["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (12, 35)
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert audit["summary"]["SAFE_PARTIAL"] == [4]
    assert audit["summary"]["EXTERNAL"] == [2, 3]
    assert audit["summary"]["AMBIGUOUS"] == [13]
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == []
    assert sum(audit["classification_counts"].values()) == 35


def test_only_approved_requirements_are_executable():
    assert rules(4)[0]["assertions"] == [{"kind": "presence", "target": {"field": "ipsdo:TrademarkApplicationId"}, "state": "REQUIRED"}]
    for code in UNMAPPED:
        assert not rules(code)
    status = rules(5)[0]
    assert status["selector"] == {"collection": APP}
    assert {item.get("value") for item in status["assertions"] if item["kind"] == "fixed_value"} == {"02"}
    assert any(item["target"]["field"] == "ipcdo:IPEntityStatusDetails/csdo:StatusCode/@codeListId" and item["state"] == "FORBIDDEN" for item in status["assertions"])


def test_signature_validity_and_indicator_rules_have_exact_owners():
    # REQ 30: CollectiveMarkIndicator == "1" under TrademarkDetails
    assert rules(30)[0]["selector"] == {"collection": f"{APP}/ipcdo:TrademarkDetails"}
    assert rules(30)[0]["assertions"] == [{"kind": "fixed_value", "target": {"field": "ipsdo:CollectiveMarkIndicator"}, "value": "1"}]

    # REQ 31: StartDateTime REQUIRED
    assert rules(31)[0]["selector"] == {"collection": "ccdo:ResourceItemStatusDetails"}
    assert rules(31)[0]["assertions"][0]["target"]["field"].endswith("StartDateTime")
    assert rules(31)[0]["assertions"][0]["state"] == "REQUIRED"

    # REQ 32: EndDateTime FORBIDDEN
    assert rules(32)[0]["selector"] == {"collection": "ccdo:ResourceItemStatusDetails"}
    assert rules(32)[0]["assertions"][0]["target"]["field"].endswith("EndDateTime")
    assert rules(32)[0]["assertions"][0]["state"] == "FORBIDDEN"

    # REQ 33-35: Signature rules
    assert rules(33)[0]["selector"] == {"collection": f"{APP}/ipcdo:SignatureDetails"}
    assert rules(34)[0]["selector"] == {"collection": f"{APP}/ipcdo:SignatureDetails"}
    assert rules(35)[0]["selector"] == {"qname": "ipcdo:OfficerDetails", "under": f"{APP}/ipcdo:SignatureDetails"}


def test_req26_has_no_executable_mapping():
    data = raw()
    inventory = data['mapping_audit']['inventory']
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
