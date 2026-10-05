import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.055"
FULL = {1, 2, 3, 6, 8, 9}
SAFE_PARTIAL = {4, 5}
ENGINE_UNSUPPORTED = {7}
UNMAPPED = ENGINE_UNSUPPORTED
INHERITED = set(range(1, 7))


def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def rules(code):
    prefix = f"{MESSAGE}.T73.REQ.{code}"
    return [
        rule for rule in raw()["structured_rules"]
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]


def test_inventory_and_classification_are_exact():
    audit = raw()["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (4, 9)

    reqs = audit["requirements"]
    assert len(reqs) == 9

    full_codes = {int(r["requirement_code"]) for r in reqs if r["classification"] == "FULLY_MAPPABLE"}
    safe_partial_codes = {int(r["requirement_code"]) for r in reqs if r["classification"] == "SAFE_PARTIAL"}
    engine_unsupported_codes = {int(r["requirement_code"]) for r in reqs if r["classification"] == "ENGINE_UNSUPPORTED"}

    assert full_codes == FULL
    assert safe_partial_codes == SAFE_PARTIAL
    assert engine_unsupported_codes == ENGINE_UNSUPPORTED

    assert sum(audit["counts"].values()) == 9
    assert audit["counts"] == {
        "FULLY_MAPPABLE": 6,
        "SAFE_PARTIAL": 2,
        "EXTERNAL": 0,
        "AMBIGUOUS": 0,
        "ENGINE_UNSUPPORTED": 1,
        "SOURCE_CONFLICT": 0,
    }

    executable_codes = set()
    for rule in raw()["structured_rules"]:
        assert rule["rule_id"].startswith(f"{MESSAGE}.")
        req_num = int(rule["rule_id"].split(".REQ.")[1].split(".")[0])
        executable_codes.add(req_num)

    assert executable_codes == (FULL | SAFE_PARTIAL)
    assert len(executable_codes) == 8
    assert len(raw()["structured_rules"]) == 8
    assert executable_codes.isdisjoint(UNMAPPED)

    for code in UNMAPPED:
        assert not rules(code), f"Requirement {code} must not have executable rules"


def test_req1_req2_req3_patent_authority_rules():
    r1 = rules(1)[0]
    assert r1["kind"] == "for_each"
    assert r1["selector"] == {"collection": "ipcdo:PatentAuthorityDetails"}
    assert r1["assertions"] == [
        {"kind": "presence", "target": {"field": "csdo:UnifiedCountryCode"}, "state": "REQUIRED"}
    ]

    r2 = rules(2)[0]
    assert r2["kind"] == "for_each"
    assert r2["selector"] == {"collection": "ipcdo:PatentAuthorityDetails"}
    assert r2["assertions"] == [
        {"kind": "presence", "target": {"field": "csdo:AuthorityName"}, "state": "REQUIRED"}
    ]

    r3 = rules(3)[0]
    assert r3["kind"] == "for_each"
    assert r3["selector"] == {"collection": "ipcdo:PatentAuthorityDetails"}
    assert r3["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ccdo:SubjectAddressDetails/csdo:AddressKindCode"},
            "state": "REQUIRED",
        },
        {
            "kind": "fixed_value",
            "target": {"field": "ccdo:SubjectAddressDetails/csdo:AddressKindCode"},
            "value": "2",
        },
    ]


def test_req4_and_req5_legal_action_kind_rules_and_remainders():
    r4 = rules(4)[0]
    assert r4["kind"] == "conditional_presence"
    assert r4["scope"] == {"collection": "ccdo:EDocHeader"}
    assert r4["condition"] == {"field": "ipsdo:IPLegalActionKindCode", "operator": "NE", "value": None}
    assert r4["target"] == {"field": "ipsdo:IPLegalActionKindName"}
    assert r4["state"] == "FORBIDDEN"

    r5 = rules(5)[0]
    assert r5["kind"] == "conditional_presence"
    assert r5["scope"] == {"collection": "ccdo:EDocHeader"}
    assert r5["condition"] == {"field": "ipsdo:IPLegalActionKindCode", "operator": "EQ", "value": None}
    assert r5["target"] == {"field": "ipsdo:IPLegalActionKindName"}
    assert r5["state"] == "REQUIRED"

    inv4 = next(i for i in raw()["mapping_audit"]["requirements"] if i["requirement_code"] == "4")
    assert inv4["classification"] == "SAFE_PARTIAL"
    assert inv4["unmapped_remainder"]

    inv5 = next(i for i in raw()["mapping_audit"]["requirements"] if i["requirement_code"] == "5")
    assert inv5["classification"] == "SAFE_PARTIAL"
    assert inv5["unmapped_remainder"]


def test_req6_trademark_application_id_required():
    r6 = rules(6)[0]
    assert r6["kind"] == "presence"
    assert r6["target"] == "ipsdo:TrademarkApplicationId"
    assert r6["state"] == "REQUIRED"


def test_req7_unmapped_engine_unsupported():
    inv7 = next(i for i in raw()["mapping_audit"]["requirements"] if i["requirement_code"] == "7")
    assert inv7["classification"] == "ENGINE_UNSUPPORTED"
    assert inv7["mapping_status"] == "UNMAPPED"
    assert inv7["engine_gap"] is not None
    assert not rules(7)


def test_req8_and_req9_payment_forbidden_fields():
    r8 = rules(8)[0]
    assert r8["kind"] == "for_each"
    assert r8["selector"] == {"qname": "ipcdo:IPPaymentDetails"}
    r8_targets = [a["target"]["field"] for a in r8["assertions"]]
    assert r8_targets == [
        "ipcdo:IPPaymentDetails/csdo:EventDateTime",
        "ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails",
        "ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails",
    ]
    assert all(a["state"] == "FORBIDDEN" for a in r8["assertions"])

    r9 = rules(9)[0]
    assert r9["kind"] == "for_each"
    assert r9["selector"] == {"qname": "ipcdo:IPPaymentDetails"}
    r9_targets = [a["target"]["field"] for a in r9["assertions"]]
    assert r9_targets == [
        "ipcdo:IPPaymentDetails/ipsdo:TrademarkApplicationId",
        "ipcdo:IPPaymentDetails/csdo:DocId",
        "ipcdo:IPPaymentDetails/csdo:PaymentAmount",
        "ipcdo:IPPaymentDetails/ipsdo:DutyPaymentIndicator",
    ]
    assert all(a["state"] == "FORBIDDEN" for a in r9["assertions"])


def test_table72_inherited_requirements_have_dual_provenance():
    for item in raw()["mapping_audit"]["requirements"]:
        code = int(item["requirement_code"])
        if code not in INHERITED:
            continue
        current, original = item["source_refs"]
        assert (current["table"], current["page"], current["item"]) == ("73", 803, "1-6")
        assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.055-T73-1-6"
        assert original["table"] == "72"
        assert original["item"] == str(code)
        assert original["source_id"] == f"22OP-RULE-P.SP.02.MSG.054-T72-{code}"
