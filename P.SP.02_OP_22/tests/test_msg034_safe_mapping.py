import json
from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.034"
APP = "ipcdo:TrademarkApplicationDetails"
SIG = f"{APP}/ipcdo:SignatureDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
FALLBACK = "Документ, содержащий доказательства в подтверждение приобретения заявленным обозначением различительной способности"

FULL = {1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37}
PARTIAL = {2, 3, 4}
AMBIGUOUS = {13}
ENGINE = {16, 17, 18, 19, 20, 26}
INHERITED = set(range(6, 30))


def _raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def _rules(code):
    base = f"{MESSAGE}.T52.REQ.{code}"
    return [
        rule for rule in _raw()["structured_rules"]
        if rule["rule_id"] == base or rule["rule_id"].startswith(base + ".")
    ]


def _inventory(code):
    return next(item for item in _raw()["mapping_audit"]["inventory"] if item["requirement_code"] == str(code))


def test_expanded_inventory_and_classification_arithmetic():
    audit = _raw()["mapping_audit"]
    assert audit["captured_row_count"] == 14
    assert audit["expanded_requirement_count"] == 37
    assert len(audit["inventory"]) == 37
    assert {int(item["requirement_code"]) for item in audit["inventory"]} == set(range(1, 38))
    assert audit["summary"] == {
        "FULLY_MAPPABLE": sorted(FULL),
        "SAFE_PARTIAL": sorted(PARTIAL),
        "AMBIGUOUS": sorted(AMBIGUOUS),
        "ENGINE_UNSUPPORTED": sorted(ENGINE),
        "EXTERNAL": [],
        "SOURCE_CONFLICT": [],
    }
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 27,
        "SAFE_PARTIAL": 3,
        "AMBIGUOUS": 1,
        "ENGINE_UNSUPPORTED": 6,
        "EXTERNAL": 0,
        "SOURCE_CONFLICT": 0,
    }
    assert sum(audit["classification_counts"].values()) == 37


def test_inventory_primary_classification_sets_are_exact():
    groups = {}
    for item in _raw()["mapping_audit"]["inventory"]:
        groups.setdefault(item["classification"], set()).add(int(item["requirement_code"]))
        assert item["target_paths"]
        assert item["owner"]
        assert item["repeatability"]
        assert item["provenance_kind"] in {"DIRECT", "INHERITED"}
    assert groups["FULLY_MAPPABLE"] == FULL
    assert groups["SAFE_PARTIAL"] == PARTIAL
    assert groups["AMBIGUOUS"] == AMBIGUOUS
    assert groups["ENGINE_UNSUPPORTED"] == ENGINE


def test_normative_context_is_exact_msg034_trn029_prc010_r002_v100():
    context = _raw()["mapping_audit"]["normative_context"]
    assert context == {
        "message_code": MESSAGE,
        "message_name": "доказательство приобретения обозначением различительной способности",
        "structure_id": "R.IP.SP.02.002",
        "structure_version": "1.0.0",
        "root_qname": "{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails",
        "transaction": "P.SP.02.TRN.029",
        "procedure": "P.SP.02.PRC.010",
        "initiating_operation": "P.SP.02.OPR.037",
        "responding_operation": "P.SP.02.OPR.038",
        "initiating_participant": "P.SP.02.ACT.001",
        "responding_participant": "P.SP.02.ACT.002",
        "response_message": "P.SP.02.MSG.002",
        "source": "ОП_22.pdf",
        "table": "52",
        "pages": [746, 747, 748],
        "inherited_table": "44",
        "message_page": 635,
        "transaction_pages": [651, 652, 653],
    }


def test_inherited_req6_29_have_dual_table52_and_original_table44_provenance():
    for code in INHERITED:
        item = _inventory(code)
        assert item["provenance_kind"] == "INHERITED"
        assert len(item["source_refs"]) >= 2
        current, original = item["source_refs"][0], item["source_refs"][1]
        assert (current["table"], current["page"], current["item"]) == ("52", 747, "6-29")
        assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.034-T52-6-29"
        assert original["table"] == "44"
        assert original["item"] == str(code)
        assert original["source_id"].endswith(f"-T44-{code}")


def test_req1_exactly_one_application():
    rule, = _rules(1)
    assert rule["kind"] == "selection_cardinality"
    assert rule["selector"] == {"collection": APP}
    assert (rule["min_occurs"], rule["max_occurs"]) == (1, 1)


def test_req2_req3_are_classifier_safe_partials_without_fake_lookup():
    req2, = _rules(2)
    assert req2["mapping_status"] == "PARTIAL"
    assert req2["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "NE", "value": None}
    assert req2["target"] == {"field": "ipsdo:IPDocKindName"}
    assert req2["state"] == "FORBIDDEN"
    assert _inventory(2)["external_dependency"] == "classifier of document/material kinds"

    req3, = _rules(3)
    assert req3["mapping_status"] == "PARTIAL"
    assert req3["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "EQ", "value": None}
    assert req3["target"] == {"field": "ipsdo:IPDocKindName"}
    assert req3["value"] == FALLBACK
    assert _inventory(3)["unmapped_remainder"] == ["authoritative classifier-absence predicate"]


def test_req4_maps_only_independently_required_local_application_id():
    rule, = _rules(4)
    assert rule["mapping_status"] == "PARTIAL"
    assert rule["selector"] == {"collection": APP}
    assert rule["assertions"] == [
        {"kind": "presence", "target": {"field": "ipsdo:TrademarkApplicationId"}, "state": "REQUIRED"}
    ]
    item = _inventory(4)
    assert item["classification"] == "SAFE_PARTIAL"
    assert item["external_dependency"] == "national patent-office application information resource"
    assert len(item["unmapped_remainder"]) == 4


def test_req5_is_per_existing_accompanying_document_and_vacuous_when_absent():
    rule, = _rules(5)
    assert rule["kind"] == "for_each"
    assert rule["selector"] == {"qname": "ipcdo:AccompanyingDocumentsDetails"}
    assert {a["target"]["field"] for a in rule["assertions"]} == {
        "ipsdo:IPDocKindCode", "csdo:DocId", "csdo:DocCreationDate",
        "csdo:DescriptionText", "csdo:PageQuantity", "csdo:DocBinaryText",
    }


def test_req13_and_req16_20_and_req26_are_intentionally_unmapped():
    assert not _rules(13)
    assert _inventory(13)["classification"] == "AMBIGUOUS"
    for code in range(16, 21):
        assert not _rules(code)
        assert _inventory(code)["classification"] == "ENGINE_UNSUPPORTED"
        assert "correlation" in _inventory(code)["engine_gap"]
    assert not _rules(26)
    req26 = _inventory(26)
    assert req26["classification"] == "ENGINE_UNSUPPORTED"
    assert " OR " in req26["reason"]
    assert "disjunctive" in req26["engine_gap"]


def test_req27_preserves_same_parent_code_or_name_condition():
    rule, = _rules(27)
    assert rule["selector"] == {"collection": f"{APP}/ipcdo:TrademarkDetails"}
    assert {a["target"]["field"] for a in rule["assertions"]} == {"ipsdo:TrademarkPicture", "ipsdo:TrademarkColourName"}
    for assertion in rule["assertions"]:
        assert set(assertion["condition"]) == {"any"}
        assert {part["field"] for part in assertion["condition"]["any"]} == {
            "ipsdo:TrademarkKindCode", "ipsdo:TrademarkKindName"
        }


def test_req30_34_use_exact_structure_owners():
    req30, = _rules(30)
    assert req30["kind"] == "selection_cardinality"
    assert req30["selector"] == {"collection": f"{APP}/ipcdo:NamingAbilityProofDetails"}
    assert (req30["min_occurs"], req30["max_occurs"]) == (1, None)

    req31, = _rules(31)
    assert req31["selector"] == {"collection": APP}
    assert {a["target"]["field"] for a in req31["assertions"]} == {
        "ipcdo:TrademarkNationalApplicationDetails", "ipcdo:ApplicantChangeDetails",
        "ipcdo:ComplaintDetails", "ipcdo:ApplicantComplainResponseDetails", "ipcdo:TrademarkClaimDetails",
    }
    assert all(a["state"] == "FORBIDDEN" for a in req31["assertions"])

    req32, = _rules(32)
    assert req32["selector"] == {"collection": "ipcdo:RefusalDetails"}
    assert (req32["min_occurs"], req32["max_occurs"]) == (0, 0)

    req33, = _rules(33)
    assert req33["assertions"] == [
        {"kind": "presence", "target": {"field": "ccdo:ValidityPeriodDetails/csdo:StartDateTime"}, "state": "REQUIRED"}
    ]
    req34, = _rules(34)
    assert req34["assertions"] == [
        {"kind": "presence", "target": {"field": "ccdo:ValidityPeriodDetails/csdo:EndDateTime"}, "state": "FORBIDDEN"}
    ]


def test_req35_37_are_exact_same_signature_and_officer_scoped():
    req35 = _rules(35)
    assert len(req35) == 2
    presence = next(r for r in req35 if r["rule_id"].endswith(".PRESENCE"))
    branch = next(r for r in req35 if r["rule_id"].endswith(".BRANCH"))
    assert presence["kind"] == "selection_cardinality"
    assert presence["selector"] == {"collection": SIG}
    assert (presence["min_occurs"], presence["max_occurs"]) == (1, None)
    assert branch["kind"] == "for_each"
    assert branch["selector"] == {"collection": SIG}
    branch_assertion, = branch["assertions"]
    assert branch_assertion["condition"] == {"field": "ipcdo:OfficerDetails", "operator": "NE", "value": None}
    assert branch_assertion["target"] == {"field": "ccdo:FullNameDetails"}
    assert branch_assertion["state"] == "FORBIDDEN"

    req36, = _rules(36)
    assert req36["kind"] == "for_each"
    assert req36["selector"] == {"collection": SIG}
    req36_assertion, = req36["assertions"]
    assert req36_assertion["condition"] == {"field": "ccdo:FullNameDetails", "operator": "NE", "value": None}
    assert req36_assertion["target"] == {"field": "ipcdo:OfficerDetails"}

    req37, = _rules(37)
    assert req37["selector"] == {"qname": "ipcdo:OfficerDetails", "under": SIG}
    assert {a["target"]["field"] for a in req37["assertions"]} == {
        "ccdo:FullNameDetails/csdo:LastName", "ccdo:FullNameDetails/csdo:FirstName",
        "csdo:PositionName", "ccdo:CommunicationDetails",
    }


def test_exact_msg034_specific_structure_paths_exist_with_expected_owner():
    structure = json.loads((PACKAGE / "structures" / "R.IP.SP.02.002" / "1.0.0.yaml").read_text(encoding="utf-8"))
    fields = {field["path"]: field for field in structure["fields"]}
    expected = {
        f"{APP}/ipcdo:NamingAbilityProofDetails",
        f"{APP}/ipcdo:AccompanyingDocumentsDetails",
        f"{APP}/ipcdo:NamingAbilityProofDetails/ipcdo:ProofDocTextDetails/ipcdo:AccompanyingDocumentsDetails",
        "ipcdo:RefusalDetails",
        f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:StartDateTime",
        f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:EndDateTime",
        SIG,
        f"{SIG}/ipcdo:OfficerDetails",
        f"{SIG}/ccdo:FullNameDetails",
        f"{SIG}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName",
        f"{SIG}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName",
        f"{SIG}/ipcdo:OfficerDetails/csdo:PositionName",
        f"{SIG}/ipcdo:OfficerDetails/ccdo:CommunicationDetails",
    }
    assert expected <= fields.keys()
    assert fields["ipcdo:RefusalDetails"]["parent"] is None
    assert fields[f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:StartDateTime"]["parent"] == "4.1"
    assert fields[SIG]["parent"] == "2"


def test_rule_identity_is_pairwise_disjoint_from_msg031_msg032_msg033():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    codes = ("P.SP.02.MSG.031", "P.SP.02.MSG.032", "P.SP.02.MSG.033", MESSAGE)
    by_message = {code: {rule["rule_id"] for rule in engine.rules[code].structured_rules} for code in codes}
    assert all(by_message.values())
    for code, ids in by_message.items():
        assert all(rule_id.startswith(code + ".") for rule_id in ids)
    for i, left in enumerate(codes):
        for right in codes[i + 1:]:
            assert by_message[left].isdisjoint(by_message[right])
