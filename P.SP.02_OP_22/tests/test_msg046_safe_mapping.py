import json
from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.046"
ROOT = "ipcdo:UnifiedRegisterRecordsDetails"
SIG = f"{ROOT}/ipcdo:SignatureDetails"
FALLBACK = (
    "Ходатайство о преобразовании аннулированной регистрации товарного знака, "
    "знака обслуживания Евразийского экономического союза в национальную заявку "
    "на регистрацию товарного знака, знака обслуживания"
)
FULL = {4, 5, 6, 7, 8, 9}
PARTIAL = {1, 2, 3}


def _raw():
    return json.loads(
        (PACKAGE / "message_rules" / f"{MESSAGE}.yaml").read_text(encoding="utf-8")
    )


def _rules(code):
    prefix = f"{MESSAGE}.T64.REQ.{code}"
    return [
        rule
        for rule in _raw()["structured_rules"]
        if rule["rule_id"] == prefix or rule["rule_id"].startswith(prefix + ".")
    ]


def _inventory(code):
    return next(
        item
        for item in _raw()["mapping_audit"]["inventory"]
        if item["requirement_code"] == str(code)
    )


def test_inventory_counts_and_classification_sets_are_exact():
    audit = _raw()["mapping_audit"]
    assert audit["captured_row_count"] == 9
    assert audit["expanded_requirement_count"] == 9
    assert len(audit["inventory"]) == 9
    assert {int(item["requirement_code"]) for item in audit["inventory"]} == set(range(1, 10))
    assert audit["summary"] == {
        "FULLY_MAPPABLE": sorted(FULL),
        "SAFE_PARTIAL": sorted(PARTIAL),
        "EXTERNAL": [],
        "AMBIGUOUS": [],
        "ENGINE_UNSUPPORTED": [],
        "SOURCE_CONFLICT": [],
    }
    assert audit["classification_counts"] == {
        "FULLY_MAPPABLE": 6,
        "SAFE_PARTIAL": 3,
        "EXTERNAL": 0,
        "AMBIGUOUS": 0,
        "ENGINE_UNSUPPORTED": 0,
        "SOURCE_CONFLICT": 0,
    }
    assert len(_raw()["structured_rules"]) == 12


def test_normative_context_is_exact_msg046_trn041_prc023_r007_v100():
    assert _raw()["mapping_audit"]["normative_context"] == {
        "message_code": MESSAGE,
        "message_name": "сведения о преобразовании аннулированной регистрации ТЗ Союза в национальную заявку на регистрацию ТЗ",
        "structure_id": "R.IP.SP.02.007",
        "structure_version": "1.0.0",
        "root_qname": "{urn:EEC:R:IP:SP:02:TrademarkRegisterDetails:v1.0.0}TrademarkRegisterDetails",
        "transaction": "P.SP.02.TRN.041",
        "procedure": "P.SP.02.PRC.023",
        "initiating_operation": "P.SP.02.OPR.112",
        "responding_operation": "P.SP.02.OPR.113",
        "initiating_participant": "P.SP.02.ACT.001",
        "responding_participant": "P.SP.02.ACT.002",
        "response_message": "P.SP.02.MSG.002",
        "source": "ОП_22.pdf",
        "table": "64",
        "pages": [778, 779],
        "message_page": 636,
        "transaction_page": 680,
    }


def test_req1_req2_classifier_mapping_is_only_safe_local_fragment():
    req1, = _rules(1)
    assert req1["kind"] == "conditional_presence"
    assert req1["mapping_status"] == "PARTIAL"
    assert req1["scope"] == {"collection": ROOT}
    assert req1["condition"] == {
        "field": "ipsdo:IPDocKindCode",
        "operator": "NE",
        "value": None,
    }
    assert req1["target"] == {"field": "ipsdo:IPDocKindName"}
    assert req1["state"] == "FORBIDDEN"
    assert _inventory(1)["unmapped_remainder"] == [
        "authoritative classifier membership predicate for the specified document kind"
    ]

    req2, = _rules(2)
    assert req2["kind"] == "conditional_fixed_value"
    assert req2["mapping_status"] == "PARTIAL"
    assert req2["scope"] == {"collection": ROOT}
    assert req2["condition"] == {
        "field": "ipsdo:IPDocKindCode",
        "operator": "EQ",
        "value": None,
    }
    assert req2["target"] == {"field": "ipsdo:IPDocKindName"}
    assert req2["value"] == FALLBACK
    assert _inventory(2)["unmapped_remainder"] == [
        "authoritative classifier-absence predicate for the specified document kind"
    ]


def test_req3_maps_only_message_local_trademark_id_presence():
    req3, = _rules(3)
    assert req3["mapping_status"] == "PARTIAL"
    assert req3["selector"] == {"collection": ROOT}
    assert req3["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ipsdo:TrademarkId"},
            "state": "REQUIRED",
        }
    ]
    assert _inventory(3)["unmapped_remainder"] == [
        "national patent-office resource lookup, status=04, EndDateTime presence, and TrademarkId equality against the message"
    ]


def test_req4_req6_use_same_record_owners_and_do_not_require_start_datetime():
    presence, fields = _rules(4)
    assert presence["selector"] == {"collection": ROOT}
    assert presence["assertions"][0]["target"] == {
        "field": "ipcdo:TrademarkNationalApplicationDetails"
    }
    assert fields["selector"] == {
        "collection": f"{ROOT}/ipcdo:TrademarkNationalApplicationDetails"
    }
    assert {a["target"]["field"] for a in fields["assertions"]} == {
        "csdo:UnifiedCountryCode",
        "ipsdo:NationalApplicationId",
        "ipsdo:NationalApplicationReceiptDate",
    }

    req6, = _rules(6)
    assert req6["selector"] == {"collection": ROOT}
    assert req6["assertions"] == [
        {
            "kind": "presence",
            "target": {
                "field": "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime"
            },
            "state": "REQUIRED",
        }
    ]
    assert "StartDateTime" not in json.dumps(req6)


def test_req5_status_is_required_per_record_and_exactly_06_without_codelist():
    presence, fields = _rules(5)
    assert presence["selector"] == {"collection": ROOT}
    assert presence["assertions"] == [
        {
            "kind": "presence",
            "target": {"field": "ipcdo:IPEntityStatusDetails"},
            "state": "REQUIRED",
        }
    ]
    assert fields["selector"] == {
        "collection": f"{ROOT}/ipcdo:IPEntityStatusDetails"
    }
    assert fields["assertions"] == [
        {"kind": "fixed_value", "target": {"field": "csdo:StatusCode"}, "value": "06"},
        {
            "kind": "presence",
            "target": {"field": "csdo:EventDate"},
            "state": "REQUIRED",
        },
        {
            "kind": "presence",
            "target": {"field": "csdo:StatusCode/@codeListId"},
            "state": "FORBIDDEN",
        },
    ]


def test_req7_req9_are_same_signature_and_officer_scoped():
    req7 = _rules(7)
    presence = next(rule for rule in req7 if rule["rule_id"].endswith(".PRESENCE"))
    branch = next(rule for rule in req7 if rule["rule_id"].endswith(".BRANCH"))
    assert presence["selector"] == {"collection": ROOT}
    assert presence["assertions"][0]["target"] == {"field": "ipcdo:SignatureDetails"}
    assert branch["selector"] == {"collection": SIG}
    assert branch["assertions"][0]["condition"]["field"] == "ipcdo:OfficerDetails"
    assert branch["assertions"][0]["target"]["field"] == "ccdo:FullNameDetails"

    req8, = _rules(8)
    assert req8["selector"] == {"collection": SIG}
    assert req8["assertions"][0]["condition"]["field"] == "ccdo:FullNameDetails"
    assert req8["assertions"][0]["target"]["field"] == "ipcdo:OfficerDetails"

    req9, = _rules(9)
    assert req9["selector"] == {"qname": "ipcdo:OfficerDetails", "under": SIG}
    assert {a["target"]["field"] for a in req9["assertions"]} == {
        "ccdo:FullNameDetails/csdo:LastName",
        "ccdo:FullNameDetails/csdo:FirstName",
        "csdo:PositionName",
        "ccdo:CommunicationDetails",
    }


def test_structure_paths_and_message_rule_identity_are_exact():
    structure = json.loads(
        (PACKAGE / "structures" / "R.IP.SP.02.007" / "1.0.0.yaml").read_text(
            encoding="utf-8"
        )
    )
    paths = {field["path"] for field in structure["fields"]}
    expected = {
        ROOT,
        f"{ROOT}/ipsdo:TrademarkId",
        f"{ROOT}/ipcdo:TrademarkNationalApplicationDetails",
        f"{ROOT}/ipcdo:TrademarkNationalApplicationDetails/csdo:UnifiedCountryCode",
        f"{ROOT}/ipcdo:TrademarkNationalApplicationDetails/ipsdo:NationalApplicationId",
        f"{ROOT}/ipcdo:TrademarkNationalApplicationDetails/ipsdo:NationalApplicationReceiptDate",
        f"{ROOT}/ipcdo:IPEntityStatusDetails/csdo:StatusCode",
        f"{ROOT}/ipcdo:IPEntityStatusDetails/csdo:EventDate",
        f"{ROOT}/ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime",
        SIG,
        f"{SIG}/ipcdo:OfficerDetails",
        f"{SIG}/ccdo:FullNameDetails",
        f"{SIG}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName",
        f"{SIG}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName",
        f"{SIG}/ipcdo:OfficerDetails/csdo:PositionName",
        f"{SIG}/ipcdo:OfficerDetails/ccdo:CommunicationDetails",
    }
    assert expected <= paths

    engine = EaeuXmlEngine.load_process(PACKAGE)
    ids = {rule["rule_id"] for rule in engine.rules[MESSAGE].structured_rules}
    assert ids
    assert all(rule_id.startswith(MESSAGE + ".") for rule_id in ids)
    assert all(rule["applies_to_structure"] == "R.IP.SP.02.007" for rule in engine.rules[MESSAGE].structured_rules)
