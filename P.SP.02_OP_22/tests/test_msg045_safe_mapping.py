import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.045"
APP = "ipcdo:TrademarkApplicationDetails"
FULL = {
    1, 3,
    6, 7, 8, 9, 10, 11, 12,
    14, 15,
    21, 22, 23, 24, 25,
    27, 28, 29,
    31, 32, 33, 34, 35,
}
EXTERNAL = {2, 4, 5}
AMBIGUOUS = {13}
ENGINE_UNSUPPORTED = {16, 17, 18, 19, 20, 26, 30}
UNMAPPED = EXTERNAL | AMBIGUOUS | ENGINE_UNSUPPORTED


def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text())


def rules(code):
    prefix = f"{MESSAGE}.T63.REQ.{code}"
    return [
        rule for rule in raw()["structured_rules"]
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]


def test_inventory_and_classification_are_exact():
    audit = raw()["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (12, 35)
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert audit["summary"]["SAFE_PARTIAL"] == []
    assert audit["summary"]["EXTERNAL"] == sorted(EXTERNAL)
    assert audit["summary"]["AMBIGUOUS"] == sorted(AMBIGUOUS)
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == sorted(ENGINE_UNSUPPORTED)
    assert audit["summary"]["SOURCE_CONFLICT"] == []
    assert sum(audit["classification_counts"].values()) == 35
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 24,
        "SAFE_PARTIAL": 0,
        "EXTERNAL": 3,
        "AMBIGUOUS": 1,
        "ENGINE_UNSUPPORTED": 7,
        "SOURCE_CONFLICT": 0,
    }


def test_only_approved_requirements_are_executable():
    executable_codes = {
        int(rule["rule_id"].split(".REQ.")[1].split(".")[0])
        for rule in raw()["structured_rules"]
    }
    assert executable_codes == FULL
    assert len(executable_codes) == 24

    for code in UNMAPPED:
        assert not rules(code), f"Requirement {code} must not have executable rules"


def test_req1_exact_one_application_cardinality():
    r1 = rules(1)[0]
    assert r1["kind"] == "selection_cardinality"
    assert r1["selector"] == {"collection": APP}
    assert r1["min_occurs"] == 1
    assert r1["max_occurs"] == 1


def test_req3_root_resource_end_datetime_forbidden():
    r3 = rules(3)[0]
    assert r3["kind"] == "for_each"
    assert r3["selector"] == {"collection": "ccdo:ResourceItemStatusDetails"}
    assert r3["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ccdo:ValidityPeriodDetails/csdo:EndDateTime"},
            "state": "FORBIDDEN",
        }
    ]


def test_req31_and_req32_application_status_rules():
    # REQ 31: direct application status container, StatusCode 02, codeListId forbidden
    r31 = rules(31)[0]
    assert any(a["target"]["field"] == "ipcdo:IPEntityStatusDetails/csdo:StatusCode" and a["state"] == "REQUIRED" for a in r31["assertions"])
    assert any(a["kind"] == "fixed_value" and a["value"] == "02" for a in r31["assertions"])
    assert any(a["target"]["field"] == "ipcdo:IPEntityStatusDetails/csdo:StatusCode/@codeListId" and a["state"] == "FORBIDDEN" for a in r31["assertions"])

    # REQ 32: status details under IPEntityStatusDetails
    r32 = rules(32)[0]
    assert r32["selector"] == {"collection": f"{APP}/ipcdo:IPEntityStatusDetails"}
    targets = {a["target"]["field"]: a["state"] for a in r32["assertions"]}
    assert targets == {
        "csdo:EventDate": "REQUIRED",
        "csdo:DocId": "REQUIRED",
        "ipsdo:IPDocReceiptDate": "REQUIRED",
        "csdo:DescriptionText": "REQUIRED",
    }


def test_req33_35_signature_and_officer_rules():
    r33 = rules(33)
    assert len(r33) == 2
    r33_pres = next(r for r in r33 if r["rule_id"].endswith(".PRESENCE"))
    r33_branch = next(r for r in r33 if r["rule_id"].endswith(".BRANCH"))
    assert r33_pres["kind"] == "selection_cardinality"
    assert r33_pres["min_occurs"] == 1

    r34 = rules(34)[0]
    assert r34["kind"] == "for_each"

    r35 = rules(35)[0]
    assert r35["selector"] == {
        "qname": "ipcdo:OfficerDetails",
        "under": f"{APP}/ipcdo:SignatureDetails",
    }
    targets = {a["target"]["field"]: a["state"] for a in r35["assertions"]}
    assert targets == {
        "ccdo:FullNameDetails/csdo:LastName": "REQUIRED",
        "ccdo:FullNameDetails/csdo:FirstName": "REQUIRED",
        "csdo:PositionName": "REQUIRED",
        "ccdo:CommunicationDetails": "FORBIDDEN",
    }


def test_req26_and_req30_unmapped_proof():
    assert not rules(26)
    assert not rules(30)
    audit = raw()["mapping_audit"]
    inv_by_code = {item["requirement_code"]: item for item in audit["inventory"]}
    assert inv_by_code["26"]["classification"] == "ENGINE_UNSUPPORTED"
    assert inv_by_code["26"]["mapping_status"] == "UNMAPPED"
    assert inv_by_code["30"]["classification"] == "ENGINE_UNSUPPORTED"
    assert inv_by_code["30"]["mapping_status"] == "UNMAPPED"
