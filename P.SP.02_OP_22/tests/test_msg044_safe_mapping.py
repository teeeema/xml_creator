import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.044"
APP = "ipcdo:TrademarkApplicationDetails"
FULL = {1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34}
UNMAPPED = {2, 3, 4, 13, 16, 17, 18, 19, 20, 26}


def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text())


def rules(code):
    prefix = f"{MESSAGE}.T62.REQ.{code}"
    return [rule for rule in raw()["structured_rules"] if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")]


def test_inventory_and_classification_are_exact():
    audit = raw()["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (11, 34)
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert audit["summary"]["SAFE_PARTIAL"] == []
    assert audit["summary"]["EXTERNAL"] == [2, 3, 4]
    assert audit["summary"]["AMBIGUOUS"] == [13]
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == [16, 17, 18, 19, 20, 26]
    assert sum(audit["classification_counts"].values()) == 34


def test_only_approved_requirements_are_executable():
    for code in UNMAPPED:
        assert not rules(code)
    executable = {
        int(rule["rule_id"].split(".REQ.", 1)[1].split(".", 1)[0])
        for rule in raw()["structured_rules"]
    }
    assert executable == FULL
    status = rules(5)[0]
    assert status["selector"] == {"collection": APP}
    assert {item.get("value") for item in status["assertions"] if item["kind"] == "fixed_value"} == {"30"}
    assert any(item["target"]["field"] == "ipcdo:IPEntityStatusDetails/csdo:StatusCode/@codeListId" and item["state"] == "FORBIDDEN" for item in status["assertions"])
    assert any(item["target"]["field"] == "ipcdo:IPEntityStatusDetails/csdo:EventDate" and item["state"] == "REQUIRED" for item in status["assertions"])


def test_req4_is_external_and_completely_unmapped():
    audit = raw()["mapping_audit"]
    item = next(item for item in audit["inventory"] if item["requirement_code"] == "4")
    assert item["classification"] == "EXTERNAL"
    assert item["mapping_status"] == "UNMAPPED"
    assert item["safe_fragment"] is None
    assert not rules(4)


def test_executable_rules_have_msg044_identity_and_dual_table44_provenance():
    structured = raw()["structured_rules"]
    assert structured
    assert all(rule["rule_id"].startswith(MESSAGE + ".") for rule in structured)
    inherited = FULL & set(range(6, 30))
    for code in inherited:
        refs = [ref for rule in rules(code) for ref in rule["source_refs"]]
        assert any(ref.get("table") == "62" for ref in refs)
        assert any(ref.get("table") == "44" for ref in refs)


def test_signature_and_date_rules_have_exact_owners():
    assert rules(30)[0]["selector"] == {"collection": f"{APP}/ipcdo:SignatureDetails"}
    assert rules(31)[0]["selector"] == {"collection": f"{APP}/ipcdo:SignatureDetails"}
    assert rules(32)[0]["selector"] == {"qname": "ipcdo:OfficerDetails", "under": f"{APP}/ipcdo:SignatureDetails"}
    assert rules(33)[0]["assertions"][0]["target"]["field"].endswith("StartDateTime")
    assert rules(34)[0]["assertions"][0]["target"]["field"].endswith("EndDateTime")
