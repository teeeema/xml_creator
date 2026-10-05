import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.041"
APP = "ipcdo:TrademarkApplicationDetails"
FULL = {1,5,6,7,8,9,10,11,12,14,15,21,22,23,24,25,27,28,29,30,31,32,33,34,35}
EXECUTABLE = FULL | {4}
UNMAPPED = {2,3,13,16,17,18,19,20,26}

def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text())

def rules(code):
    prefix = f"{MESSAGE}.T59.REQ.{code}"
    return [r for r in raw()["structured_rules"] if r["rule_id"] == prefix or r["rule_id"].startswith(prefix + ".")]

def test_inventory_classification_and_executable_set_are_exact():
    data = raw()
    audit = data["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (12, 35)
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert audit["summary"]["SAFE_PARTIAL"] == [4]
    assert audit["summary"]["EXTERNAL"] == [2,3]
    assert audit["summary"]["AMBIGUOUS"] == [13]
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == [16,17,18,19,20,26]
    assert audit["summary"]["SOURCE_CONFLICT"] == []
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 25, "SAFE_PARTIAL": 1, "EXTERNAL": 2,
        "AMBIGUOUS": 1, "ENGINE_UNSUPPORTED": 6, "SOURCE_CONFLICT": 0,
    }
    actual = {int(r["rule_id"].split(".REQ.",1)[1].split(".",1)[0]) for r in data["structured_rules"]}
    assert actual == EXECUTABLE
    assert len(data["structured_rules"]) == 29
    for code in UNMAPPED:
        assert not rules(code)

def test_partial_req4_and_req5_are_exact():
    assert rules(4)[0]["assertions"] == [
        {"kind":"presence","target":{"field":"ipsdo:TrademarkApplicationId"},"state":"REQUIRED"}
    ]
    status = rules(5)[0]
    assert status["selector"] == {"collection": APP}
    fixed = [a for a in status["assertions"] if a["kind"] == "fixed_value"]
    assert fixed == [{"kind":"fixed_value","target":{"field":"ipcdo:IPEntityStatusDetails/csdo:StatusCode"},"value":"02"}]
    assert any(
        a["kind"] == "presence"
        and a["target"]["field"] == "ipcdo:IPEntityStatusDetails/csdo:StatusCode/@codeListId"
        and a["state"] == "FORBIDDEN"
        for a in status["assertions"]
    )

def test_inherited_rules_keep_table59_and_table44_provenance():
    for code in {6,7,8,9,10,11,12,14,15,21,22,23,24,25,27,28,29}:
        for rule in rules(code):
            tables = {str(ref["table"]) for ref in rule["source_refs"]}
            assert "59" in tables
            assert "44" in tables

def test_req30_31_32_have_exact_value_and_validity_semantics():
    req30 = rules(30)[0]
    assert req30["selector"] == {"collection": f"{APP}/ipcdo:TrademarkDetails"}
    assert req30["assertions"] == [
        {"kind":"fixed_value","target":{"field":"ipsdo:CollectiveMarkIndicator"},"value":"0"}
    ]
    req31 = rules(31)[0]
    req32 = rules(32)[0]
    assert req31["selector"] == {"collection":"ccdo:ResourceItemStatusDetails"}
    assert req31["assertions"][0]["target"]["field"].endswith("StartDateTime")
    assert req31["assertions"][0]["state"] == "REQUIRED"
    assert req32["selector"] == {"collection":"ccdo:ResourceItemStatusDetails"}
    assert req32["assertions"][0]["target"]["field"].endswith("EndDateTime")
    assert req32["assertions"][0]["state"] == "FORBIDDEN"

def test_signature_rules_are_scoped_to_signature_owner():
    signature = f"{APP}/ipcdo:SignatureDetails"
    assert rules(33)[0]["selector"] == {"collection": signature}
    assert rules(33)[1]["selector"] == {"collection": signature}
    assert rules(34)[0]["selector"] == {"collection": signature}
    assert rules(35)[0]["selector"] == {"qname":"ipcdo:OfficerDetails","under":signature}

def test_msg041_rule_ids_are_isolated_from_msg042():
    ids = {r["rule_id"] for r in raw()["structured_rules"]}
    assert ids
    assert all(x.startswith("P.SP.02.MSG.041.") for x in ids)
    assert not any("P.SP.02.MSG.042" in x for x in ids)
