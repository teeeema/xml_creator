import json
from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.033"
APP = "ipcdo:TrademarkApplicationDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
SIG = f"{APP}/ipcdo:SignatureDetails"
OFFICER = f"{SIG}/ipcdo:OfficerDetails"
RESPONSE = f"{APP}/ipcdo:ApplicantComplainResponseDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
FALLBACK = (
    "Заключение национального патентного ведомства по результатам экспертизы "
    "заявленного обозначения о возможности (невозможности) регистрации товарного знака, "
    "знака обслуживания Евразийского экономического союза"
)

FULL = {1, 2, 6, 7, 8, 9, 10, 11, 12, 14, 15, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37}
PARTIAL = {3, 4, 5}
AMBIGUOUS = {13}
ENGINE = {16, 17, 18, 19, 20, 26}
INHERITED = set(range(6, 30))


def _raw():
    return json.loads((PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8"))


def _rules(code):
    rid = f"{MESSAGE}.T51.REQ.{code}"
    return [rule for rule in _raw()["structured_rules"] if rule["rule_id"] == rid]


def _inventory(code):
    return next(item for item in _raw()["mapping_audit"]["inventory"] if item["requirement_code"] == str(code))


def test_expanded_normative_inventory_has_exactly_37_requirements():
    data = _raw()
    inventory = data["mapping_audit"]["inventory"]
    assert len(inventory) == 37
    assert data["mapping_audit"]["expanded_requirement_count"] == 37
    assert {int(item["requirement_code"]) for item in inventory} == set(range(1, 38))
    assert all(item["table"] == "51" for item in inventory)
    assert all(item["branch"] == "R.IP.SP.02.002" for item in inventory)


def test_mapping_classification_is_complete_and_non_approximating():
    summary = _raw()["mapping_audit"]["summary"]
    assert summary == {
        "FULLY_MAPPABLE": sorted(FULL),
        "SAFE_PARTIAL": sorted(PARTIAL),
        "AMBIGUOUS": sorted(AMBIGUOUS),
        "ENGINE_UNSUPPORTED": sorted(ENGINE),
        "EXTERNAL": [],
        "SOURCE_CONFLICT": [],
    }
    mapped = {int(rule["rule_id"].rsplit(".", 1)[1]) for rule in _raw()["structured_rules"]}
    assert mapped == FULL | PARTIAL
    assert not mapped.intersection(AMBIGUOUS | ENGINE)


def test_normative_context_is_msg033_trn028_prc007_and_r002():
    context = _raw()["mapping_audit"]["normative_context"]
    assert context["message_code"] == MESSAGE
    assert context["message_name"] == "сведения о результатах внутригосударственного обжалования решения по экспертизе"
    assert context["structure_id"] == "R.IP.SP.02.002"
    assert context["structure_version"] == "1.0.0"
    assert context["root_qname"] == "{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails"
    assert context["transaction"] == "P.SP.02.TRN.028"
    assert context["procedure"] == "P.SP.02.PRC.007"
    assert context["initiating_operation"] == "P.SP.02.OPR.025"
    assert context["responding_operation"] == "P.SP.02.OPR.026"
    assert context["initiating_participant"] == "P.SP.02.ACT.002"
    assert context["responding_participant"] == "P.SP.02.ACT.001"
    assert context["response_message"] == "P.SP.02.MSG.002"
    assert context["pages"] == [743, 744, 745, 746]


def test_inherited_req6_29_have_dual_table51_and_original_table44_provenance():
    for code in INHERITED:
        item = _inventory(code)
        current, original = item["source_refs"]
        assert (current["table"], current["page"], current["item"]) == ("51", 745, "6-29")
        assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.033-T51-6-29"
        assert original["table"] == "44"
        assert original["item"] == str(code)
        assert original["source_id"].endswith(f"-T44-{code}")

    for rule in _raw()["structured_rules"]:
        code = int(rule["rule_id"].rsplit(".", 1)[1])
        if code in INHERITED:
            current, original = rule["source_refs"]
            assert current["source_id"] == "22OP-RULE-P.SP.02.MSG.033-T51-6-29"
            assert original["table"] == "44"
            assert original["item"] == str(code)


def test_req1_application_cardinality_is_exactly_one():
    rule, = _rules(1)
    assert rule["kind"] == "selection_cardinality"
    assert rule["selector"] == {"collection": APP}
    assert (rule["min_occurs"], rule["max_occurs"]) == (1, 1)


def test_req2_uses_allowed_status_set_and_forbids_status_codelistid_in_same_application():
    rule, = _rules(2)
    assert rule["kind"] == "for_each"
    assert rule["selector"] == {"collection": APP}
    assert rule["assertions"] == [
        {
            "kind": "comparison",
            "left": {"field": "ipcdo:IPEntityStatusDetails/csdo:StatusCode"},
            "operator": "IN",
            "right_value": ["10", "20"],
        },
        {
            "kind": "presence",
            "target": {"field": "ipcdo:IPEntityStatusDetails/csdo:StatusCode/@codeListId"},
            "state": "FORBIDDEN",
        },
    ]


def test_req3_req4_classifier_logic_is_only_safe_local_partial():
    req3, = _rules(3)
    assert req3["mapping_status"] == "PARTIAL"
    assert req3["scope"] == {"collection": APP}
    assert req3["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "NE", "value": None}
    assert req3["target"] == {"field": "ipsdo:IPDocKindName"}
    assert req3["state"] == "FORBIDDEN"
    assert _inventory(3)["classification"] == "SAFE_PARTIAL"
    assert _inventory(3)["external_dependency"] == "classifier of document/material kinds"

    req4, = _rules(4)
    assert req4["mapping_status"] == "PARTIAL"
    assert req4["scope"] == {"collection": APP}
    assert req4["condition"] == {"field": "ipsdo:IPDocKindCode", "operator": "EQ", "value": None}
    assert req4["target"] == {"field": "ipsdo:IPDocKindName"}
    assert req4["value"] == FALLBACK
    assert _inventory(4)["classification"] == "SAFE_PARTIAL"


def test_req5_maps_only_independently_required_application_id():
    rule, = _rules(5)
    assert rule["mapping_status"] == "PARTIAL"
    assert rule["selector"] == {"collection": APP}
    assert rule["assertions"] == [{"kind": "presence", "target": {"field": "ipsdo:TrademarkApplicationId"}, "state": "REQUIRED"}]
    item = _inventory(5)
    assert item["classification"] == "SAFE_PARTIAL"
    assert item["external_dependency"] == "filing-office information resource"
    assert len(item["unmapped_remainder"]) == 4


def test_req13_is_ambiguous_and_unmapped():
    assert not _rules(13)
    item = _inventory(13)
    assert item["classification"] == "AMBIGUOUS"
    assert item["mapping_status"] == "UNMAPPED"
    assert "PA/RE" in item["reason"]


def test_req16_20_are_engine_unsupported_and_unmapped():
    for code in range(16, 21):
        assert not _rules(code)
        item = _inventory(code)
        assert item["classification"] == "ENGINE_UNSUPPORTED"
        assert item["mapping_status"] == "UNMAPPED"
        assert item["engine_gap"] == "missing exact nested repeated correlation/filter semantics"


def test_req26_normative_or_is_unmapped_without_strengthening_to_and():
    assert not _rules(26)
    item = _inventory(26)
    assert item["classification"] == "ENGINE_UNSUPPORTED"
    assert " OR " in item["reason"]
    assert "AND" in item["reason"]
    assert [ref["table"] for ref in item["source_refs"]] == ["51", "44"]


def test_req27_uses_same_trademark_code_or_name_condition():
    rule, = _rules(27)
    assert rule["selector"] == {"collection": f"{APP}/ipcdo:TrademarkDetails"}
    assert {item["target"]["field"] for item in rule["assertions"]} == {"ipsdo:TrademarkPicture", "ipsdo:TrademarkColourName"}
    for assertion in rule["assertions"]:
        condition = assertion["condition"]
        assert set(condition) == {"any"}
        assert {part["field"] for part in condition["any"]} == {"ipsdo:TrademarkKindCode", "ipsdo:TrademarkKindName"}


def test_req30_registration_code_and_req34_response_use_exact_application_owner():
    req30, = _rules(30)
    assert req30["selector"] == {"collection": APP}
    assert req30["assertions"] == [{"kind": "presence", "target": {"field": "ipsdo:TrademarkRegistrationCode"}, "state": "REQUIRED"}]
    req34, = _rules(34)
    assert req34["selector"] == {"collection": APP}
    assert req34["assertions"] == [{"kind": "presence", "target": {"field": "ipcdo:ApplicantComplainResponseDetails"}, "state": "REQUIRED"}]


def test_req31_33_signature_rules_are_scoped_to_exact_signature_and_officer_owners():
    req31 = _rules(31)
    assert len(req31) == 2
    assert any(r["kind"] == "selection_cardinality" and r["selector"] == {"collection": SIG} for r in req31)
    branch = next(r for r in req31 if r["kind"] == "for_each")
    assert branch["selector"] == {"collection": SIG}
    assert branch["assertions"][0]["condition"]["field"] == "ipcdo:OfficerDetails"
    assert branch["assertions"][0]["target"]["field"] == "ccdo:FullNameDetails"

    req32, = _rules(32)
    assert req32["selector"] == {"collection": SIG}
    assert req32["assertions"][0]["condition"]["field"] == "ccdo:FullNameDetails"
    assert req32["assertions"][0]["target"]["field"] == "ipcdo:OfficerDetails"

    req33, = _rules(33)
    assert req33["selector"] == {"qname": "ipcdo:OfficerDetails", "under": SIG}
    assert {a["target"]["field"] for a in req33["assertions"]} == {
        "ccdo:FullNameDetails/csdo:LastName",
        "ccdo:FullNameDetails/csdo:FirstName",
        "csdo:PositionName",
        "ccdo:CommunicationDetails",
    }


def test_req35_37_use_exact_refusal_and_validity_period_paths():
    req35, = _rules(35)
    assert req35["selector"] == {"collection": "ipcdo:RefusalDetails"}
    assert (req35["min_occurs"], req35["max_occurs"]) == (0, 0)

    req36, = _rules(36)
    assert req36["selector"] == {"collection": RESOURCE}
    assert req36["assertions"] == [{"kind": "presence", "target": {"field": "ccdo:ValidityPeriodDetails/csdo:StartDateTime"}, "state": "REQUIRED"}]

    req37, = _rules(37)
    assert req37["selector"] == {"collection": RESOURCE}
    assert req37["assertions"] == [{"kind": "presence", "target": {"field": "ccdo:ValidityPeriodDetails/csdo:EndDateTime"}, "state": "FORBIDDEN"}]


def test_exact_structure_paths_exist_for_all_msg033_specific_targets():
    structure = json.loads((PACKAGE / "structures" / "R.IP.SP.02.002" / "1.0.0.yaml").read_text(encoding="utf-8"))
    paths = {field["path"] for field in structure["fields"]}
    expected = {
        APP,
        f"{APP}/ipsdo:IPDocKindCode",
        f"{APP}/ipsdo:IPDocKindName",
        f"{APP}/ipsdo:TrademarkApplicationId",
        STATUS,
        f"{STATUS}/csdo:StatusCode",
        f"{APP}/ipsdo:TrademarkRegistrationCode",
        SIG,
        OFFICER,
        f"{OFFICER}/ccdo:FullNameDetails/csdo:LastName",
        f"{OFFICER}/ccdo:FullNameDetails/csdo:FirstName",
        f"{OFFICER}/csdo:PositionName",
        f"{OFFICER}/ccdo:CommunicationDetails",
        f"{SIG}/ccdo:FullNameDetails",
        RESPONSE,
        "ipcdo:RefusalDetails",
        RESOURCE,
        f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:StartDateTime",
        f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:EndDateTime",
    }
    assert expected <= paths


def test_rule_identity_is_pairwise_disjoint_from_msg031_and_msg032():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    codes = ("P.SP.02.MSG.031", "P.SP.02.MSG.032", MESSAGE)
    by_message = {code: {rule["rule_id"] for rule in engine.rules[code].structured_rules} for code in codes}
    assert all(by_message.values())
    for code, ids in by_message.items():
        assert all(rule_id.startswith(code + ".") for rule_id in ids)
    assert by_message[codes[0]].isdisjoint(by_message[codes[1]])
    assert by_message[codes[0]].isdisjoint(by_message[codes[2]])
    assert by_message[codes[1]].isdisjoint(by_message[codes[2]])
