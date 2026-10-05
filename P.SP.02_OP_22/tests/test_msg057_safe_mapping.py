import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.057"
FULL = {1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21}
SAFE_PARTIAL = {19, 22}
EXTERNAL = {4, 5}
UNMAPPED = EXTERNAL
INHERITED_T72 = {1, 2, 3, 4, 5, 6}
INHERITED_T74 = set(range(1, 20))
LOCAL_T75 = {20, 21, 22}


def raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def rules(code):
    prefix = f"{MESSAGE}.T75.REQ.{code}"
    return [
        rule for rule in raw()["structured_rules"]
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]


def test_inventory_and_classification_are_exact():
    audit = raw()["mapping_audit"]
    assert (audit["captured_row_count"], audit["expanded_requirement_count"]) == (4, 22)

    reqs = audit["requirements"]
    assert len(reqs) == 22

    full_codes = {int(r["requirement_code"]) for r in reqs if r["classification"] == "FULLY_MAPPABLE"}
    safe_partial_codes = {int(r["requirement_code"]) for r in reqs if r["classification"] == "SAFE_PARTIAL"}
    external_codes = {int(r["requirement_code"]) for r in reqs if r["classification"] == "EXTERNAL"}

    assert full_codes == FULL
    assert safe_partial_codes == SAFE_PARTIAL
    assert external_codes == EXTERNAL

    assert sum(audit["classification_counts"].values()) == 22
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 18,
        "SAFE_PARTIAL": 2,
        "EXTERNAL": 2,
        "AMBIGUOUS": 0,
        "ENGINE_UNSUPPORTED": 0,
        "SOURCE_CONFLICT": 0,
    }

    executable_codes = set()
    for rule in raw()["structured_rules"]:
        assert rule["rule_id"].startswith(f"{MESSAGE}.")
        req_num = int(rule["rule_id"].split(".REQ.")[1].split(".")[0])
        executable_codes.add(req_num)

    assert executable_codes == (FULL | SAFE_PARTIAL)
    assert len(executable_codes) == 20
    assert len(raw()["structured_rules"]) == 20
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
            "kind": "fixed_value",
            "target": {"field": "ccdo:SubjectAddressDetails/csdo:AddressKindCode"},
            "value": "2",
        },
    ]


def test_req4_req5_external_classifier_dependencies():
    inv4 = next(i for i in raw()["mapping_audit"]["requirements"] if i["requirement_code"] == "4")
    assert inv4["classification"] == "EXTERNAL"
    assert inv4["mapping_status"] == "UNMAPPED"
    assert inv4["external_dependency"] is not None
    assert not rules(4)

    inv5 = next(i for i in raw()["mapping_audit"]["requirements"] if i["requirement_code"] == "5")
    assert inv5["classification"] == "EXTERNAL"
    assert inv5["mapping_status"] == "UNMAPPED"
    assert inv5["external_dependency"] is not None
    assert not rules(5)


def test_req6_trademark_application_id():
    r6 = rules(6)[0]
    assert r6["kind"] == "presence"
    assert r6["target"] == "ipsdo:TrademarkApplicationId"
    assert r6["state"] == "REQUIRED"


def test_req7_and_req8_payment_details_rules():
    r7 = rules(7)[0]
    assert r7["kind"] == "for_each"
    assert r7["selector"] == {"collection": "ipcdo:IPPaymentDetails"}
    assert r7["assertions"] == [
        {"kind": "presence", "target": {"field": "ccdo:BankAccountDetails"}, "state": "FORBIDDEN"},
        {"kind": "presence", "target": {"field": "ccdo:PaymentSystemAccountDetails"}, "state": "FORBIDDEN"},
    ]

    r8 = rules(8)[0]
    assert r8["kind"] == "for_each"
    assert r8["selector"] == {"collection": "ipcdo:IPPaymentDetails"}
    assert r8["assertions"] == [
        {"kind": "presence", "target": {"field": "csdo:EventDateTime"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "ipcdo:IPPartyDetails"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "ipcdo:AccompanyingDocumentsDetails"}, "state": "REQUIRED"},
    ]


def test_req9_to_req14_party_details_rules():
    r9 = rules(9)[0]
    assert r9["kind"] == "selection_cardinality"
    assert r9["selector"] == {
        "collection": "ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails",
        "where": {"field": "ipsdo:IPPartyKindCode", "operator": "IN", "value": ["AP", "PA", "RE"]},
    }
    assert (r9["min_occurs"], r9["max_occurs"]) == (1, 1)

    r10 = rules(10)[0]
    assert r10["kind"] == "for_each"
    assert r10["selector"] == {"collection": "ipcdo:IPPaymentDetails/ipcdo:IPPartyDetails"}
    assert r10["assertions"] == [
        {"kind": "presence", "target": {"field": "csdo:UnifiedCountryCode"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "ipsdo:IPSubjectName"}, "state": "REQUIRED"},
    ]

    r11 = rules(11)[0]
    assert r11["kind"] == "for_each"
    assert r11["selector"]["where"] == {"field": "ipsdo:IPPartyKindCode", "operator": "EQ", "value": "AP"}
    assert r11["assertions"] == [
        {"kind": "fixed_value", "target": {"field": "ipsdo:IPSubjectName/@nameRepresentationKindCode"}, "value": "OR"},
        {"kind": "fixed_value", "target": {"field": "ipsdo:IPSubjectName/@languageCode"}, "value": "RU"},
    ]

    r12 = rules(12)[0]
    assert r12["kind"] == "for_each"
    assert r12["selector"]["where"] == {"field": "ipsdo:IPPartyKindCode", "operator": "EQ", "value": "PA"}
    assert r12["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:PatentAttorneyId"}, "state": "REQUIRED"},
    ]

    r13 = rules(13)[0]
    assert r13["kind"] == "for_each"
    assert r13["selector"]["where"] == {"field": "ipsdo:IPPartyKindCode", "operator": "IN", "value": ["PA", "RE"]}
    assert r13["assertions"] == [
        {"kind": "comparison", "left": {"field": "csdo:UnifiedCountryCode"}, "operator": "IN", "right_value": ["AM", "BY", "KZ", "KG", "RU"]},
    ]

    r14 = rules(14)[0]
    assert r14["kind"] == "for_each"
    assert r14["selector"]["where"] == {"field": "ipsdo:IPPartyKindCode", "operator": "IN", "value": ["PA", "RE"]}
    assert r14["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:IPSubjectName/@nameRepresentationKindCode"}, "state": "FORBIDDEN"},
        {"kind": "fixed_value", "target": {"field": "ipsdo:IPSubjectName/@languageCode"}, "value": "RU"},
    ]


def test_req15_to_req19_accompanying_documents_rules():
    r15 = rules(15)[0]
    assert r15["kind"] == "selection_cardinality"
    assert r15["selector"] == {"collection": "ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails"}
    assert (r15["min_occurs"], r15["max_occurs"]) == (1, 1)

    r16 = rules(16)[0]
    assert r16["kind"] == "for_each"
    assert r16["selector"] == {"collection": "ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails"}
    assert r16["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:IPDocKindName"}, "state": "FORBIDDEN"},
    ]

    r17 = rules(17)[0]
    assert r17["kind"] == "for_each"
    assert r17["selector"] == {"collection": "ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails"}
    assert r17["assertions"] == [
        {"kind": "fixed_value", "target": {"field": "ipsdo:IPDocKindCode"}, "value": "07015"},
    ]

    r18 = rules(18)[0]
    assert r18["kind"] == "for_each"
    assert r18["selector"] == {"collection": "ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails"}
    assert r18["assertions"] == [
        {"kind": "presence", "target": {"field": "csdo:DocId"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "csdo:DocCreationDate"}, "state": "REQUIRED"},
    ]

    r19 = rules(19)[0]
    assert r19["kind"] == "for_each"
    assert r19["selector"] == {"collection": "ipcdo:IPPaymentDetails/ipcdo:AccompanyingDocumentsDetails"}
    assert r19["assertions"][0] == {"kind": "presence", "target": {"field": "csdo:DocBinaryText"}, "state": "REQUIRED"}
    assert r19["assertions"][1]["kind"] == "comparison"
    assert r19["assertions"][1]["left"] == {"field": "csdo:DocBinaryText/@mediaTypeCode"}
    assert r19["assertions"][1]["operator"] == "IN"
    assert "pdf" in r19["assertions"][1]["right_value"]
    inv19 = next(i for i in raw()["mapping_audit"]["requirements"] if i["requirement_code"] == "19")
    assert inv19["classification"] == "SAFE_PARTIAL"
    assert inv19["unmapped_remainder"]


def test_req20_req21_req22_duty_payment_indicator_and_amount_rules():
    r20 = rules(20)[0]
    assert r20["kind"] == "presence"
    assert r20["target"] == "ipsdo:DutyPaymentIndicator"
    assert r20["state"] == "REQUIRED"

    r21 = rules(21)[0]
    assert r21["kind"] == "conditional_fixed_value"
    assert r21["scope"] == {"collection": "ccdo:EDocHeader"}
    assert r21["condition"] == {"field": "ipsdo:DutyPaymentIndicator", "operator": "EQ", "value": "true"}
    assert r21["target"] == {"field": "csdo:PaymentAmount"}
    assert r21["value"] == "0"

    r22 = rules(22)[0]
    assert r22["kind"] == "conditional_presence"
    assert r22["scope"] == {"collection": "ccdo:EDocHeader"}
    assert r22["condition"] == {"field": "ipsdo:DutyPaymentIndicator", "operator": "EQ", "value": "false"}
    assert r22["target"] == {"field": "csdo:PaymentAmount"}
    assert r22["state"] == "REQUIRED"
    assert r22["mapping_status"] == "PARTIAL"

    inv22 = next(i for i in raw()["mapping_audit"]["requirements"] if i["requirement_code"] == "22")
    assert inv22["classification"] == "SAFE_PARTIAL"
    assert inv22["engine_gap"] == "NUMERIC_DECIMAL_COMPARISON_NOT_SUPPORTED"
    assert inv22["unmapped_remainder"]


def test_provenance_and_source_refs():
    for item in raw()["mapping_audit"]["requirements"]:
        code = int(item["requirement_code"])
        if code in LOCAL_T75:
            assert item["provenance_kind"] == "DIRECT"
            ref = item["source_refs"][0]
            assert (ref["table"], ref["item"]) == ("75", str(code))
        else:
            assert item["provenance_kind"] == "INHERITED"
            t75_ref = item["source_refs"][0]
            assert (t75_ref["table"], t75_ref["page"], t75_ref["item"]) == ("75", 807, "1-19")
