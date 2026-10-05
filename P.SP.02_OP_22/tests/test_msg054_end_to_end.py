from pathlib import Path
from xml.etree import ElementTree as ET

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.054"
STRUCTURE_ID = "R.IP.SP.03.003"
AUTHORITY = "ipcdo:PatentAuthorityDetails"
ADDRESS = f"{AUTHORITY}/ccdo:SubjectAddressDetails"

APPROVED_NAME = (
    "Регистрация товарного (коллективного) знака Союза и выдача свидетельства "
    "на товарный (коллективный) знак Союза"
)


def valid_values():
    return {
        "ccdo:EDocHeader": [None],
        "ccdo:EDocHeader/csdo:InfEnvelopeCode": MESSAGE,
        "ccdo:EDocHeader/csdo:EDocCode": STRUCTURE_ID,
        "ccdo:EDocHeader/csdo:EDocId": "00000000-0000-0000-0000-000000000054",
        "ccdo:EDocHeader/csdo:EDocDateTime": "2026-09-30T15:00:00+03:00",
        AUTHORITY: [None],
        f"{AUTHORITY}/csdo:UnifiedCountryCode": "RU",
        f"{AUTHORITY}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
        f"{AUTHORITY}/csdo:AuthorityName": "Роспатент",
        ADDRESS: [""],
        f"{ADDRESS}/csdo:AddressKindCode": "2",
        f"{AUTHORITY}/ipsdo:OriginOfficeIndicator": "1",
        "ipsdo:IPLegalActionKindName": APPROVED_NAME,
        "ipsdo:TrademarkApplicationId": "2026/RU-000054",
    }


def extracted_valid():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    body = engine.build_body(MESSAGE, valid_values(), mode=GenerationMode.TEST)
    parsed = ET.fromstring(ET.tostring(body.serialize_xml_element(), encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    assert not issues
    return engine, structure, parsed, values


def test_build_serialize_parse_extract_validate_roundtrip():
    engine, _, _, values = extracted_valid()
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert result.is_valid, [(issue.rule_id, issue.message) for issue in result.issues]


def test_e2e_req3_and_req6_negative_cases():
    engine, _, _, values = extracted_valid()

    bad_address = dict(values)
    bad_address[f"{ADDRESS}/csdo:AddressKindCode"] = "1"
    result = engine.validate_body(MESSAGE, bad_address, mode=GenerationMode.TEST)
    assert any(issue.rule_id == f"{MESSAGE}.T72.REQ.3" for issue in result.issues)

    missing_application = dict(values)
    del missing_application["ipsdo:TrademarkApplicationId"]
    result = engine.validate_body(MESSAGE, missing_application, mode=GenerationMode.TEST)
    assert any(issue.rule_id == f"{MESSAGE}.T72.REQ.6" for issue in result.issues)


def test_e2e_req7_root_forbidden_fields_including_payment_details():
    engine, structure, parsed, _ = extracted_valid()
    cases = [
        ("ipsdo", "ApellationOfOriginApplicationId", "AO-054"),
        ("csdo", "DocId", "DOC-054"),
        ("ipcdo", "IPPaymentDetails", None),
        ("ipsdo", "DutyPaymentIndicator", "1"),
        ("csdo", "PaymentAmount", "100"),
    ]

    for prefix, local, text in cases:
        root = ET.fromstring(ET.tostring(parsed, encoding="utf-8"))
        node = ET.SubElement(root, ET.QName(structure.imported_namespaces[prefix], local))
        if text is not None:
            node.text = text
        values, _ = engine.body_provider._values_from_element(structure, root)
        result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
        assert any(issue.rule_id == f"{MESSAGE}.T72.REQ.7" for issue in result.issues), local


def test_critical_message_isolation_from_msg055():
    engine = EaeuXmlEngine.load_process(PACKAGE)
    ours = {rule["rule_id"] for rule in engine.rules[MESSAGE].structured_rules}
    theirs = {rule["rule_id"] for rule in engine.rules["P.SP.02.MSG.055"].structured_rules}
    assert ours
    assert all(rule_id.startswith(f"{MESSAGE}.") for rule_id in ours)
    assert ours.isdisjoint(theirs)
