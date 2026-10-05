import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.051"
R007 = "ipcdo:UnifiedRegisterRecordsDetails"
FULL = {
    2, 5,
    6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    20, 21, 22, 23,
}
SAFE_PARTIAL = {1, 3, 4}
ENGINE_UNSUPPORTED = {18, 19}
UNMAPPED = ENGINE_UNSUPPORTED
INHERITED = set(range(6, 20))
LITERAL_1 = "Решение о признании предоставления правовой охраны товарному знаку, знаку обслуживания Евразийского экономического союза недействительным"
LITERAL_2 = "Решение о прекращении правовой охраны товарного знака, знака обслуживания Евразийского экономического союза"


def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def rules(code):
    prefix = f"{MESSAGE}.T69.REQ.{code}"
    return [
        rule for rule in raw()["structured_rules"]
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]


def test_inventory_and_classification_are_exact():
    audit = raw()["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (10, 23)
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert audit["summary"]["SAFE_PARTIAL"] == sorted(SAFE_PARTIAL)
    assert audit["summary"]["EXTERNAL"] == []
    assert audit["summary"]["AMBIGUOUS"] == []
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == sorted(ENGINE_UNSUPPORTED)
    assert audit["summary"]["SOURCE_CONFLICT"] == []
    assert sum(audit["classification_counts"].values()) == 23
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 18,
        "SAFE_PARTIAL": 3,
        "EXTERNAL": 0,
        "AMBIGUOUS": 0,
        "ENGINE_UNSUPPORTED": 2,
        "SOURCE_CONFLICT": 0,
    }


def test_only_approved_requirements_are_executable():
    executable_codes = {
        int(rule["rule_id"].split(".REQ.")[1].split(".")[0])
        for rule in raw()["structured_rules"]
    }
    assert executable_codes == FULL | SAFE_PARTIAL
    assert len(executable_codes) == 21

    for code in UNMAPPED:
        assert not rules(code), f"Requirement {code} must not have executable rules"


def test_req1_partial_trademark_id_required():
    r1 = rules(1)[0]
    assert r1["kind"] == "for_each"
    assert r1["mapping_status"] == "PARTIAL"
    assert r1["selector"] == {"collection": R007}
    assert r1["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:TrademarkId"}, "state": "REQUIRED"}
    ]
    inv1 = next(item for item in raw()["mapping_audit"]["inventory"] if item["requirement_code"] == "1")
    assert inv1["classification"] == "SAFE_PARTIAL"
    assert "filing office external patent office registry" in inv1["unmapped_remainder"][0]


def test_req2_register_record_exact_one_cardinality():
    r2 = rules(2)[0]
    assert r2["kind"] == "selection_cardinality"
    assert r2["selector"] == {"collection": R007}
    assert (r2["min_occurs"], r2["max_occurs"]) == (1, 1)


def test_req3_and_req4_document_kind_rules():
    r3 = rules(3)[0]
    assert r3["kind"] == "conditional_presence"
    assert r3["scope"] == {"collection": R007}
    assert r3["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "NE", "value": None}
    assert r3["target"] == {"field": "ipsdo:IPDocKindName"}
    assert r3["state"] == "FORBIDDEN"

    r4 = rules(4)[0]
    assert r4["kind"] == "for_each"
    assert r4["selector"] == {
        "collection": R007,
        "where": {"field": "ipsdo:IPDocKindCode", "operator": "EQ", "value": None}
    }
    assert any(a["kind"] == "presence" and a["target"]["field"] == "ipsdo:IPDocKindName" and a["state"] == "REQUIRED" for a in r4["assertions"])
    comp = next(a for a in r4["assertions"] if a["kind"] == "comparison")
    assert comp["left"] == "ipsdo:IPDocKindName"
    assert comp["operator"] == "IN"
    assert comp["right_value"] == [LITERAL_1, LITERAL_2]


def test_req5_registration_cancellation_details():
    r5 = rules(5)[0]
    assert r5["kind"] == "for_each"
    assert r5["selector"] == {"collection": R007}
    targets = {a["target"]["field"]: a["state"] for a in r5["assertions"]}
    assert targets == {
        "ipcdo:RegistrationCancellationDetails": "REQUIRED",
        "ipcdo:RegistrationCancellationDetails/ipsdo:CancellationTrademarkRegistrationReasonCode": "REQUIRED",
        "ipcdo:RegistrationCancellationDetails/ipcdo:NationalPatentDecisionDetails": "REQUIRED",
    }


def test_table49_inherited_requirements_have_dual_provenance():
    for item in raw()["mapping_audit"]["inventory"]:
        code = int(item["requirement_code"])
        if code not in INHERITED:
            continue
        current, original = item["source_refs"]
        assert (current["table"], current["page"], current["item"]) == ("69", 791, "6-19")
        assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.051-T69-6-19"
        assert original["table"] == "49"
        assert original["item"] == str(code)
        assert original["source_id"] == f"22OP-RULE-P.SP.02.MSG.051-T49-{code}"


def test_req20_22_signature_and_officer_rules():
    r20 = rules(20)
    assert len(r20) == 2
    r20_pres = next(r for r in r20 if r["rule_id"].endswith(".PRESENCE"))
    r20_branch = next(r for r in r20 if r["rule_id"].endswith(".BRANCH"))
    assert r20_pres["kind"] == "selection_cardinality"
    assert r20_pres["min_occurs"] == 1
    assert r20_branch["assertions"][0]["condition"]["field"] == "ipcdo:OfficerDetails"
    assert r20_branch["assertions"][0]["target"]["field"] == "ccdo:FullNameDetails"
    assert r20_branch["assertions"][0]["state"] == "FORBIDDEN"

    r21 = rules(21)[0]
    assert r21["kind"] == "for_each"
    assert r21["assertions"][0]["condition"]["field"] == "ccdo:FullNameDetails"
    assert r21["assertions"][0]["target"]["field"] == "ipcdo:OfficerDetails"
    assert r21["assertions"][0]["state"] == "FORBIDDEN"

    r22 = rules(22)[0]
    assert r22["selector"] == {
        "qname": "ipcdo:OfficerDetails",
        "under": f"{R007}/ipcdo:SignatureDetails",
    }
    targets = {a["target"]["field"]: a["state"] for a in r22["assertions"]}
    assert targets == {
        "ccdo:FullNameDetails/csdo:LastName": "REQUIRED",
        "ccdo:FullNameDetails/csdo:FirstName": "REQUIRED",
        "csdo:PositionName": "REQUIRED",
        "ccdo:CommunicationDetails": "FORBIDDEN",
    }


def test_req23_start_datetime_required_and_no_end_datetime_requirement():
    r23 = rules(23)[0]
    assert r23["kind"] == "for_each"
    assert r23["selector"] == {"collection": R007}
    assert r23["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime"},
            "state": "REQUIRED",
        }
    ]
    # Verify no EndDateTime requirement in MSG051
    all_targets = [
        a["target"]["field"]
        for rule in raw()["structured_rules"]
        for a in rule.get("assertions", [])
        if "target" in a
    ]
    assert not any("EndDateTime" in t for t in all_targets)


def test_req18_and_req19_unmapped_proof():
    assert not rules(18)
    assert not rules(19)
    inv = {item["requirement_code"]: item for item in raw()["mapping_audit"]["inventory"]}
    assert inv["18"]["classification"] == "ENGINE_UNSUPPORTED"
    assert inv["18"]["mapping_status"] == "UNMAPPED"
    assert inv["19"]["classification"] == "ENGINE_UNSUPPORTED"
    assert inv["19"]["mapping_status"] == "UNMAPPED"
