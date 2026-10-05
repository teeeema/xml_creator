import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.036"
APP = "ipcdo:TrademarkApplicationDetails"
DOCS = f"{APP}/ipcdo:AccompanyingDocumentsDetails"

FULL = {1, 4, 5, *range(6, 13), 14, 15, *range(21, 26), *range(27, 32)}
PARTIAL = {2, 3}


def _raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def _rules(code):
    prefix = f"{MESSAGE}.T54.REQ.{code}"
    return [rule for rule in _raw()["structured_rules"] if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")]


def test_complete_table54_inventory_and_classification_arithmetic():
    audit = _raw()["mapping_audit"]
    assert audit["captured_row_count"] == 8
    assert audit["expanded_requirement_count"] == 31
    assert {int(item["requirement_code"]) for item in audit["inventory"]} == set(range(1, 32))
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 22,
        "SAFE_PARTIAL": 2,
        "AMBIGUOUS": 1,
        "ENGINE_UNSUPPORTED": 6,
        "EXTERNAL": 0,
        "SOURCE_CONFLICT": 0,
    }
    assert sum(audit["classification_counts"].values()) == 31


def test_only_safe_local_parts_of_classifier_and_external_requirements_are_mapped():
    req2, = _rules(2)
    req3, = _rules(3)
    assert req2["mapping_status"] == "PARTIAL"
    assert req2["selector"] == {"collection": APP}
    assert req2["assertions"] == [{"kind": "presence", "target": {"field": "ipsdo:IPDocKindCode"}, "state": "REQUIRED"}]
    assert req3["mapping_status"] == "PARTIAL"
    assert req3["assertions"] == [{"kind": "presence", "target": {"field": "ipsdo:TrademarkApplicationId"}, "state": "REQUIRED"}]
    inventory = {int(item["requirement_code"]): item for item in _raw()["mapping_audit"]["inventory"]}
    assert inventory[2]["classification"] == "SAFE_PARTIAL"
    assert "classifier" in inventory[2]["external_dependency"]
    assert inventory[3]["classification"] == "SAFE_PARTIAL"
    assert "national patent-office" in inventory[3]["external_dependency"]


def test_table54_direct_requirements_have_exact_owners_and_no_or_to_and_conversion():
    req1, = _rules(1)
    assert req1["selector"] == {"collection": APP}
    assert (req1["min_occurs"], req1["max_occurs"]) == (1, 1)
    req4 = _rules(4)
    assert req4[0]["selector"] == {"collection": DOCS}
    assert (req4[0]["min_occurs"], req4[0]["max_occurs"]) == (1, None)
    assert req4[1]["selector"] == {"collection": DOCS}
    assert {item["target"]["field"] for item in req4[1]["assertions"]} == {
        "ipsdo:IPDocKindCode", "csdo:DocId", "csdo:DocCreationDate",
        "csdo:DescriptionText", "csdo:PageQuantity", "csdo:DocBinaryText",
    }
    req5, = _rules(5)
    assert req5["selector"] == {"qname": "ipcdo:RefusalDetails"}
    assert (req5["min_occurs"], req5["max_occurs"]) == (0, 0)
    req30, = _rules(30)
    req31, = _rules(31)
    assert req30["selector"] == req31["selector"] == {"collection": "ccdo:ResourceItemStatusDetails"}
    assert req30["assertions"][0]["target"]["field"].endswith("csdo:StartDateTime")
    assert req31["assertions"][0]["target"]["field"].endswith("csdo:EndDateTime")
    assert req31["assertions"][0]["state"] == "FORBIDDEN"
    assert not _rules(13)
    for code in [16, 17, 18, 19, 20, 26]:
        assert not _rules(code)
