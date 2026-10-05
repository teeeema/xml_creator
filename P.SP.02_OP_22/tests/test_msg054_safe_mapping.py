import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
RULE_FILE = PACKAGE / "message_rules" / "P.SP.02.MSG.054.yaml"


def _data():
    return json.loads(RULE_FILE.read_text(encoding="utf-8"))


def test_msg054_audit_counts_and_executable_inventory():
    data = _data()
    audit = data["mapping_audit"]
    assert audit["expanded_requirement_count"] == 7
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 5,
        "SAFE_PARTIAL": 2,
        "ENGINE_UNSUPPORTED": 0,
        "EXTERNAL": 0,
        "AMBIGUOUS": 0,
        "SOURCE_CONFLICT": 0,
    }
    assert audit["summary"]["FULLY_MAPPABLE"] == [1, 2, 3, 6, 7]
    assert audit["summary"]["SAFE_PARTIAL"] == [4, 5]
    assert {item["requirement_code"] for item in audit["inventory"]} == set("1234567")
    assert all(rule["rule_id"].startswith("P.SP.02.MSG.054.") for rule in data["structured_rules"])


def test_msg054_owner_paths_and_req7_forbidden_set_are_exact():
    data = _data()
    inventory = {item["requirement_code"]: item for item in data["mapping_audit"]["inventory"]}
    assert inventory["1"]["target_paths"] == [
        "ipcdo:PatentAuthorityDetails/csdo:UnifiedCountryCode"
    ]
    assert inventory["2"]["target_paths"] == [
        "ipcdo:PatentAuthorityDetails/csdo:AuthorityName"
    ]
    assert inventory["3"]["target_paths"] == [
        "ipcdo:PatentAuthorityDetails/ccdo:SubjectAddressDetails",
        "ipcdo:PatentAuthorityDetails/ccdo:SubjectAddressDetails/csdo:AddressKindCode",
    ]
    assert inventory["6"]["target_paths"] == ["ipsdo:TrademarkApplicationId"]
    assert set(inventory["7"]["target_paths"]) == {
        "ipsdo:ApellationOfOriginApplicationId",
        "csdo:DocId",
        "ipcdo:IPPaymentDetails",
        "ipsdo:DutyPaymentIndicator",
        "csdo:PaymentAmount",
    }
    assert inventory["7"]["owner"] == "IPDutyDetails"


def test_msg054_partial_classifier_mapping_is_explicit_and_sourced():
    data = _data()
    inventory = {item["requirement_code"]: item for item in data["mapping_audit"]["inventory"]}
    for code in ("4", "5"):
        item = inventory[code]
        assert item["classification"] == "SAFE_PARTIAL"
        assert item["mapping_status"] == "PARTIAL_EXECUTABLE"
        assert item["external_dependency"]
        assert item["unmapped_remainder"]
        assert item["source_refs"][0]["source_id"] == f"22OP-RULE-P.SP.02.MSG.054-T72-{code}"

    rules5 = [r for r in data["structured_rules"] if r["rule_id"].startswith("P.SP.02.MSG.054.T72.REQ.5")]
    value_rule = next(r for r in rules5 if r["rule_id"].endswith(".VALUE"))
    names = value_rule["assertions"][0]["right_value"]
    assert len(names) == 4
    assert all(isinstance(name, str) and name for name in names)

