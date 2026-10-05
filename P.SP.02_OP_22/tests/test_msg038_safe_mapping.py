import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.038"
APP = "ipcdo:TrademarkApplicationDetails"
FULL = {1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36, 37}
UNMAPPED = ({2, 3, 13, 16, 17, 18, 19, 20, 26, 31}) - {16, 17, 18, 19, 20, 26}

def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text())

def rules(code):
    p = f"{MESSAGE}.T56.REQ.{code}"
    return [r for r in raw()["structured_rules"] if r["rule_id"] == p or r["rule_id"].startswith(p + ".")]

def test_inventory_and_classification_are_exact():
    a = raw()["mapping_audit"]
    assert (a["captured_row_count"], a["expanded_requirement_count"]) == (14, 37)
    assert a["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert a["summary"]["SAFE_PARTIAL"] == [4]
    assert a["summary"]["EXTERNAL"] == [2, 3, 31]
    assert a["summary"]["AMBIGUOUS"] == [13]
    assert a["summary"]["ENGINE_UNSUPPORTED"] == []
    assert sum(a["classification_counts"].values()) == 37

def test_only_safe_req4_and_confirmed_requirements_are_executable():
    assert rules(4)[0]["assertions"] == [{"kind": "presence", "target": {"field": "ipsdo:TrademarkApplicationId"}, "state": "REQUIRED"}]
    for code in UNMAPPED:
        assert not rules(code)
    assert rules(5)[0]["selector"] == {"collection": f"{APP}/ipcdo:TrademarkPriorityDetails"}

def test_req30_and_req32_have_exact_per_parent_scope():
    r30, = rules(30)
    assert r30["selector"] == {"collection": f"{APP}/ipcdo:TrademarkPriorityDetails"}
    assert {x["target"]["field"] for x in r30["assertions"]} == {"ipsdo:PriorityKindCode", "ipsdo:PriorityDate", "csdo:UnifiedCountryCode"}
    r32, = rules(32)
    assert r32["selector"] == {"qname": "ipcdo:AccompanyingDocumentsDetails"}
    assert {x["target"]["field"] for x in r32["assertions"]} == {"csdo:DocName", "csdo:DocId", "csdo:DocCreationDate", "csdo:DescriptionText", "csdo:PageQuantity"}
    assert "csdo:DocBinaryText" not in {x["target"]["field"] for x in r32["assertions"]}
