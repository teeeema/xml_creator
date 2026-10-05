import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.015"
ROOT = "ipcdo:UnifiedRegisterRecordsDetails"

FULL = {4, 5, 6}
SAFE_PARTIAL = {3}
EXTERNAL = {1, 2}
UNMAPPED = EXTERNAL


def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def rules(code):
    prefix = f"{MESSAGE}.T48.REQ.{code}"
    return [
        rule for rule in raw()["structured_rules"]
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]


def inventory(code):
    return next(
        item for item in raw()["mapping_audit"]["inventory"]
        if item["requirement_code"] == str(code)
    )


def test_inventory_counts_and_classification_arithmetic():
    audit = raw()["mapping_audit"]
    assert audit["captured_row_count"] == 6
    assert audit["expanded_requirement_count"] == 6

    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert audit["summary"]["SAFE_PARTIAL"] == sorted(SAFE_PARTIAL)
    assert audit["summary"]["EXTERNAL"] == sorted(EXTERNAL)
    assert audit["summary"]["AMBIGUOUS"] == []
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == []
    assert audit["summary"]["SOURCE_CONFLICT"] == []

    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 3,
        "SAFE_PARTIAL": 1,
        "EXTERNAL": 2,
        "AMBIGUOUS": 0,
        "ENGINE_UNSUPPORTED": 0,
        "SOURCE_CONFLICT": 0,
    }
    assert sum(audit["classification_counts"].values()) == 6

    executable_codes = set()
    for rule in raw()["structured_rules"]:
        assert rule["rule_id"].startswith(f"{MESSAGE}.")
        req_num = int(rule["rule_id"].split(".REQ.")[1].split(".")[0])
        executable_codes.add(req_num)

    assert executable_codes == (FULL | SAFE_PARTIAL)
    assert len(executable_codes) == 4
    assert executable_codes.isdisjoint(UNMAPPED)
    assert len(raw()["structured_rules"]) == 6


def test_req1_req2_external_no_executable_rules():
    for code in (1, 2):
        assert not rules(code), f"Requirement {code} must have zero executable rules"
        inv = inventory(code)
        assert inv["classification"] == "EXTERNAL"
        assert inv["mapping_status"] == "UNMAPPED"
        assert inv["external_dependency"]
        assert inv["reason"]


def test_req3_safe_partial_trademark_id():
    r3 = rules(3)
    assert len(r3) == 1
    rule = r3[0]
    assert rule["kind"] == "for_each"
    assert rule["mapping_status"] == "PARTIAL"
    assert rule["selector"] == {"collection": ROOT}
    assert rule["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:TrademarkId"}, "state": "REQUIRED"}
    ]

    inv = inventory(3)
    assert inv["classification"] == "SAFE_PARTIAL"
    assert inv["mapping_status"] == "PARTIAL"
    assert inv["safe_fragment"]
    assert inv["unmapped_remainder"]


def test_req4_fully_mappable_national_application():
    r4 = rules(4)
    assert len(r4) == 2

    pres = next(r for r in r4 if r["rule_id"].endswith(".PRESENCE"))
    assert pres["kind"] == "for_each"
    assert pres["selector"] == {"collection": ROOT}
    assert pres["assertions"] == [
        {"kind": "presence", "target": {"field": "ipcdo:TrademarkNationalApplicationDetails"}, "state": "REQUIRED"}
    ]

    flds = next(r for r in r4 if r["rule_id"].endswith(".FIELDS"))
    assert flds["kind"] == "for_each"
    assert flds["selector"] == {"collection": f"{ROOT}/ipcdo:TrademarkNationalApplicationDetails"}
    assert flds["assertions"] == [
        {"kind": "presence", "target": {"field": "csdo:UnifiedCountryCode"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "ipsdo:NationalApplicationId"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "ipsdo:NationalApplicationReceiptDate"}, "state": "REQUIRED"},
    ]


def test_req5_fully_mappable_status_details():
    r5 = rules(5)
    assert len(r5) == 2

    pres = next(r for r in r5 if r["rule_id"].endswith(".PRESENCE"))
    assert pres["kind"] == "for_each"
    assert pres["selector"] == {"collection": ROOT}
    assert pres["assertions"] == [
        {"kind": "presence", "target": {"field": "ipcdo:IPEntityStatusDetails"}, "state": "REQUIRED"}
    ]

    flds = next(r for r in r5 if r["rule_id"].endswith(".FIELDS"))
    assert flds["kind"] == "for_each"
    assert flds["selector"] == {"collection": f"{ROOT}/ipcdo:IPEntityStatusDetails"}
    assert flds["assertions"] == [
        {"kind": "fixed_value", "target": {"field": "csdo:StatusCode"}, "value": "06"},
        {"kind": "presence", "target": {"field": "csdo:EventDate"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "csdo:StatusCode/@codeListId"}, "state": "FORBIDDEN"},
    ]


def test_req6_fully_mappable_end_date_time():
    r6 = rules(6)
    assert len(r6) == 1
    rule = r6[0]
    assert rule["kind"] == "for_each"
    assert rule["selector"] == {"collection": ROOT}
    assert rule["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime"},
            "state": "REQUIRED",
        }
    ]


def test_provenance_table48():
    for item in raw()["mapping_audit"]["inventory"]:
        ref = item["source_refs"][0]
        assert ref["table"] == "48"
        assert ref["page"] in (559, 560)
        assert ref["source_id"].startswith("22OP-RULE-P.SP.02.MSG.015-T48-")
