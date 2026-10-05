import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.052"
R007 = "ipcdo:UnifiedRegisterRecordsDetails"
FULL = {3,18,22, 24, 1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 23, 29, 30, 31}
SAFE_PARTIAL = {5, 20, 25, 26, 27, 28}
ENGINE_UNSUPPORTED = {19, 21}
INHERITED = set(range(6, 20))
CANCEL_LITERAL = "Решение об аннулировании регистрации товарного знака, знака обслуживания Евразийского экономического союза"
NEW_LITERAL = "решение о регистрации товарного знака, знака обслуживания Евразийского экономического союза в отношении всех заявленных товаров и (или) услуг"

def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))

def rules(code):
    prefix = f"{MESSAGE}.T70.REQ.{code}"
    return [r for r in raw()["structured_rules"] if r["rule_id"] == prefix or r["rule_id"].startswith(prefix + ".")]

def test_inventory_and_classification_are_exact():
    audit = raw()["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (18, 31)
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 23, "SAFE_PARTIAL": 6, "EXTERNAL": 0,
        "AMBIGUOUS": 0, "ENGINE_UNSUPPORTED": 2, "SOURCE_CONFLICT": 0,
    }
    assert audit["summary"]["FULLY_MAPPABLE"] == sorted(FULL)
    assert audit["summary"]["SAFE_PARTIAL"] == sorted(SAFE_PARTIAL)
    assert audit["summary"]["ENGINE_UNSUPPORTED"] == sorted(ENGINE_UNSUPPORTED)
    assert len(audit["inventory"]) == 31
    assert [int(x["requirement_code"]) for x in audit["inventory"]] == list(range(1, 32))

def test_only_authorized_requirements_are_executable():
    executable = {int(r["rule_id"].split(".REQ.")[1].split(".")[0]) for r in raw()["structured_rules"]}
    assert executable == FULL | SAFE_PARTIAL
    for code in ENGINE_UNSUPPORTED:
        assert not rules(code)

def test_role_rules_are_semantic_not_ordinal():
    for code, status in [(2, "04"), (4, "01"), (5, "04"), (20, "01"), (23, "04"), (25, "04"), (26, "04"), (27, "01"), (28, "01")]:
        for rule in rules(code):
            selector = rule.get("selector", {})
            if "where" in selector:
                assert selector["where"] == {
                    "field": "ipcdo:IPEntityStatusDetails/csdo:StatusCode",
                    "operator": "EQ",
                    "value": status,
                }
            text = json.dumps(rule, ensure_ascii=False)
            assert "[0]" not in text and "[1]" not in text
            assert "first" not in text.lower() and "second" not in text.lower()

def test_req1_and_req2_shapes():
    r1 = rules(1)[0]
    assert r1["kind"] == "selection_cardinality"
    assert (r1["min_occurs"], r1["max_occurs"]) == (1, 2)
    r2 = rules(2)
    assert any(r["kind"] == "selection_cardinality" and r["min_occurs"] == 1 and r["max_occurs"] == 1 for r in r2)
    details = next(r for r in r2 if r["rule_id"].endswith(".DETAILS"))
    targets = {a["target"]["field"]: a for a in details["assertions"]}
    assert targets["ipcdo:IPEntityStatusDetails/csdo:EventDate"]["state"] == "REQUIRED"
    assert targets["ipcdo:IPEntityStatusDetails/csdo:StatusCode"]["value"] == "04"
    assert targets["ipcdo:IPEntityStatusDetails/csdo:StatusCode/@codeListId"]["state"] == "FORBIDDEN"

def test_partial_trademark_id_rules_and_remainders():
    assert rules(5)[0]["mapping_status"] == "PARTIAL"
    assert rules(20)[0]["mapping_status"] == "PARTIAL"
    inv = {int(x["requirement_code"]): x for x in raw()["mapping_audit"]["inventory"]}
    assert "external" in inv[5]["unmapped_remainder"][0]
    assert "uniqueness" in inv[20]["unmapped_remainder"][0]

def test_table49_inherited_requirements_have_dual_provenance():
    inv = {int(x["requirement_code"]): x for x in raw()["mapping_audit"]["inventory"]}
    for code in INHERITED:
        current, original = inv[code]["source_refs"]
        assert (current["table"], current["item"], current["source_id"]) == (
            "70", "6-19", "22OP-RULE-P.SP.02.MSG.052-T70-6-19"
        )
        assert original["table"] == "49"
        assert original["item"] == str(code)
        assert original["source_id"] == f"22OP-RULE-P.SP.02.MSG.052-T49-{code}"

def test_req23_cancellation_details_same_record():
    rule = rules(23)[0]
    assert rule["selector"]["where"]["value"] == "04"
    targets = {a["target"]["field"]: a["state"] for a in rule["assertions"]}
    assert targets == {
        "ipcdo:RegistrationCancellationDetails": "REQUIRED",
        "ipcdo:RegistrationCancellationDetails/ipcdo:ComplaintInvalidateProtectionTrademarkDetails": "REQUIRED",
        "ipcdo:RegistrationCancellationDetails/ipcdo:ComplaintInvalidateProtectionTrademarkDetails/ipsdo:CancellationRegistrationTrademarkCode": "REQUIRED",
        "ipcdo:RegistrationCancellationDetails/ipcdo:ComplaintInvalidateProtectionTrademarkDetails/ipsdo:SolutionCancellationRegistrationTrademarkCode": "REQUIRED",
    }

def test_req25_28_role_scoped_document_kind_partials():
    expected = {25: "04", 26: "04", 27: "01", 28: "01"}
    for code, status in expected.items():
        rule = rules(code)[0]
        assert rule["kind"] == "for_each"
        assert rule["selector"]["where"]["value"] == status
        assert rule["mapping_status"] == "PARTIAL"
    assert rules(26)[0]["assertions"][0]["value"] == CANCEL_LITERAL
    assert rules(28)[0]["assertions"][0]["value"] == NEW_LITERAL
    assert NEW_LITERAL.startswith("решение")

def test_req29_31_signature_rules_are_same_parent():
    r29 = rules(29)
    presence = next(r for r in r29 if r["rule_id"].endswith(".PRESENCE"))
    branch = next(r for r in r29 if r["rule_id"].endswith(".BRANCH"))
    assert presence["selector"] == {"collection": R007}
    assert presence["assertions"] == [{"kind": "presence", "target": {"field": "ipcdo:SignatureDetails"}, "state": "REQUIRED"}]
    assert branch["selector"] == {"collection": f"{R007}/ipcdo:SignatureDetails"}
    assert rules(30)[0]["selector"] == {"collection": f"{R007}/ipcdo:SignatureDetails"}
    assert rules(31)[0]["selector"] == {"qname": "ipcdo:OfficerDetails", "under": f"{R007}/ipcdo:SignatureDetails"}
