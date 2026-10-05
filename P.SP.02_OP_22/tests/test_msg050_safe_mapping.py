import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.050"
R007 = "ipcdo:UnifiedRegisterRecordsDetails"
FULL = {18,
    2, 3,
    6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    20, 21, 22, 23,
}
SAFE_PARTIAL = {1, 4, 5}
ENGINE_UNSUPPORTED = {19}
UNMAPPED = ENGINE_UNSUPPORTED
INHERITED = set(range(6, 20))
EXACT_DOC_NAME = "Ходатайство об отказе от исключительного права на товарный знак, знак обслуживания Евразийского экономического союза"


def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def rules(code):
    prefix = f"{MESSAGE}.T68.REQ.{code}"
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
        "FULLY_MAPPABLE": 19,
        "SAFE_PARTIAL": 3,
        "EXTERNAL": 0,
        "AMBIGUOUS": 0,
        "ENGINE_UNSUPPORTED": 1,
        "SOURCE_CONFLICT": 0,
    }


def test_only_approved_requirements_are_executable():
    executable_codes = {
        int(rule["rule_id"].split(".REQ.")[1].split(".")[0])
        for rule in raw()["structured_rules"]
    }
    assert executable_codes == FULL | SAFE_PARTIAL
    assert len(executable_codes) == 22

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
    assert "external patent office registry" in inv1["unmapped_remainder"][0]


def test_req2_register_record_exact_one_cardinality():
    r2 = rules(2)[0]
    assert r2["kind"] == "selection_cardinality"
    assert r2["selector"] == {"collection": R007}
    assert (r2["min_occurs"], r2["max_occurs"]) == (1, 1)


def test_req3_validity_end_datetime_required_and_no_start_datetime():
    r3 = rules(3)[0]
    assert r3["kind"] == "for_each"
    assert r3["selector"] == {"collection": R007}
    assert r3["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime"},
            "state": "REQUIRED",
        }
    ]
    all_targets = [
        a["target"]["field"]
        for rule in raw()["structured_rules"]
        for a in rule.get("assertions", [])
        if "target" in a
    ]
    assert not any("StartDateTime" in t for t in all_targets)


def test_req4_and_req5_document_kind_rules():
    r4 = rules(4)[0]
    assert r4["kind"] == "conditional_presence"
    assert r4["scope"] == {"collection": R007}
    assert r4["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "NE", "value": None}
    assert r4["target"] == {"field": "ipsdo:IPDocKindName"}
    assert r4["state"] == "FORBIDDEN"

    r5 = rules(5)[0]
    assert r5["kind"] == "conditional_fixed_value"
    assert r5["scope"] == {"collection": R007}
    assert r5["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "EQ", "value": None}
    assert r5["target"] == {"field": "ipsdo:IPDocKindName"}
    assert r5["value"] == EXACT_DOC_NAME


def test_table49_inherited_requirements_have_dual_provenance():
    for item in raw()["mapping_audit"]["inventory"]:
        code = int(item["requirement_code"])
        if code not in INHERITED:
            continue
        current, original = item["source_refs"]
        assert (current["table"], current["page"], current["item"]) == ("68", 789, "6-19")
        assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.050-T68-6-19"
        assert original["table"] == "49"
        assert original["item"] == str(code)
        assert original["source_id"] == f"22OP-RULE-P.SP.02.MSG.050-T49-{code}"


def test_req20_status_code_05_and_event_date_and_codelist_forbidden():
    r20 = rules(20)[0]
    assert r20["kind"] == "for_each"
    assert r20["selector"] == {"collection": f"{R007}/ipcdo:IPEntityStatusDetails"}
    assert any(a["target"]["field"] == "csdo:StatusCode" and a["value"] == "05" for a in r20["assertions"])
    assert any(a["target"]["field"] == "csdo:EventDate" and a["state"] == "REQUIRED" for a in r20["assertions"])
    assert any(a["target"]["field"] == "csdo:StatusCode/@codeListId" and a["state"] == "FORBIDDEN" for a in r20["assertions"])


def test_req21_23_signature_and_officer_rules():
    r21 = rules(21)
    assert len(r21) == 2
    r21_pres = next(r for r in r21 if r["rule_id"].endswith(".PRESENCE"))
    r21_branch = next(r for r in r21 if r["rule_id"].endswith(".BRANCH"))
    assert r21_pres["kind"] == "selection_cardinality"
    assert r21_pres["min_occurs"] == 1
    assert r21_branch["assertions"][0]["condition"]["field"] == "ipcdo:OfficerDetails"
    assert r21_branch["assertions"][0]["target"]["field"] == "ccdo:FullNameDetails"
    assert r21_branch["assertions"][0]["state"] == "FORBIDDEN"

    r22 = rules(22)[0]
    assert r22["kind"] == "for_each"
    assert r22["assertions"][0]["condition"]["field"] == "ccdo:FullNameDetails"
    assert r22["assertions"][0]["target"]["field"] == "ipcdo:OfficerDetails"
    assert r22["assertions"][0]["state"] == "FORBIDDEN"

    r23 = rules(23)[0]
    assert r23["selector"] == {
        "qname": "ipcdo:OfficerDetails",
        "under": f"{R007}/ipcdo:SignatureDetails",
    }
    targets = {a["target"]["field"]: a["state"] for a in r23["assertions"]}
    assert targets == {
        "ccdo:FullNameDetails/csdo:LastName": "REQUIRED",
        "ccdo:FullNameDetails/csdo:FirstName": "REQUIRED",
        "csdo:PositionName": "REQUIRED",
        "ccdo:CommunicationDetails": "FORBIDDEN",
    }


def test_req18_and_req19_unmapped_proof():
    assert rules(18)
    assert not rules(19)
    inv = {item["requirement_code"]: item for item in raw()["mapping_audit"]["inventory"]}
    assert inv["18"]["classification"] == "FULLY_MAPPABLE"
    assert inv["18"]["mapping_status"] == "EXECUTABLE"
    assert inv["19"]["classification"] == "ENGINE_UNSUPPORTED"
    assert inv["19"]["mapping_status"] == "UNMAPPED"
