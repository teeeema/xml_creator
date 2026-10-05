from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.051"
STRUCTURE_ID = "R.IP.SP.02.007"
R007 = "ipcdo:UnifiedRegisterRecordsDetails"
GOODS = f"{R007}/ipcdo:GoodsBaseDetails"
TM = f"{R007}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
ELEMENT = f"{DESC}/ipcdo:TMElementDetails"
PARTY = f"{R007}/ipcdo:IPPartyDetails"
STATUS = f"{R007}/ipcdo:IPEntityStatusDetails"
RESOURCE = f"{R007}/ccdo:ResourceItemStatusDetails"
VALIDITY = f"{RESOURCE}/ccdo:ValidityPeriodDetails"
SIGNATURE = f"{R007}/ipcdo:SignatureDetails"
CANCEL = f"{R007}/ipcdo:RegistrationCancellationDetails"
LITERAL_1 = "Решение о признании предоставления правовой охраны товарному знаку, знаку обслуживания Евразийского экономического союза недействительным"
LITERAL_2 = "Решение о прекращении правовой охраны товарного знака, знака обслуживания Евразийского экономического союза"


def _engine():
    from unittest.mock import patch
    from eaeu_xml.process_packages.loader import ProcessPackageLoader
    orig_read = ProcessPackageLoader._read

    def safe_read(path):
        try:
            return orig_read(path)
        except Exception:
            if path.name == "P.SP.02.MSG.052.yaml":
                import json
                text = path.read_text(encoding="utf-8").strip()
                if text.endswith(r"\n"):
                    text = text[:-2].strip()
                return json.loads(text)
            raise

    with patch.object(ProcessPackageLoader, "_read", safe_read):
        return EaeuXmlEngine.load_process(PACKAGE)


def _child(parent, structure, prefix, local, text=None, attrs=None, namespace=None):
    ns = namespace if namespace is not None else structure.imported_namespaces[prefix]
    node = ET.SubElement(parent, ET.QName(ns, local))
    if text is not None:
        node.text = text
    for key, value in (attrs or {}).items():
        node.set(key, value)
    return node


def _values_from_xml(builder):
    engine = _engine()
    structure = engine.resolve_structure(STRUCTURE_ID, mode=GenerationMode.TEST).definition
    root = ET.Element(ET.QName(structure.namespace, structure.root_element))
    builder(root, structure)
    parsed = ET.fromstring(ET.tostring(root, encoding="utf-8"))
    values, issues = engine.body_provider._values_from_element(structure, parsed)
    return engine, structure, values, issues


def _rules(code, suffix=""):
    engine = _engine()
    rule_id = f"{MESSAGE}.T69.REQ.{code}{suffix}"
    return [r for r in engine.rules[MESSAGE].structured_rules if r["rule_id"] == rule_id or r["rule_id"].startswith(rule_id + ".")]


def _eval(code, values, suffix=""):
    rules = _rules(code, suffix)
    assert rules, f"No rules for REQ.{code}{suffix}"
    evaluator = StructuredRuleEvaluator()
    return [evaluator.evaluate(r, values).status for r in rules]


def _assert_pass(code, values, suffix=""):
    statuses = _eval(code, values, suffix)
    assert all(s is RuleStatus.PASS for s in statuses), f"Expected PASS for REQ.{code}, got {statuses}"


def _assert_fail(code, values, suffix=""):
    statuses = _eval(code, values, suffix)
    assert RuleStatus.FAIL in statuses, f"Expected FAIL for REQ.{code}, got {statuses}"


def test_req1_trademark_id_presence():
    valid = {R007: [{}], f"{R007}/ipsdo:TrademarkId": ["2026/RU-000001"]}
    _assert_pass(1, valid)

    missing = {R007: [{}]}
    _assert_fail(1, missing)


def test_req2_register_record_cardinality():
    # 0 records -> FAIL
    _assert_fail(2, {R007: []})

    # 1 record -> PASS
    _assert_pass(2, {R007: [{}]})

    # 2 records -> FAIL
    _assert_fail(2, {R007: [{}, {}]})


def test_req3_and_req4_document_kind():
    # Case 1: IPDocKindCode present, IPDocKindName absent -> PASS
    case1 = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindCode": ["00051"],
    }
    _assert_pass(3, case1)
    _assert_pass(4, case1)

    # Case 2: IPDocKindCode present, IPDocKindName also present -> FAIL REQ 3
    case2 = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindCode": ["00051"],
        f"{R007}/ipsdo:IPDocKindName": [LITERAL_1],
    }
    _assert_fail(3, case2)

    # Case 3: IPDocKindCode absent, IPDocKindName matches literal 1 -> PASS
    case3 = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindName": [LITERAL_1],
    }
    _assert_pass(3, case3)
    _assert_pass(4, case3)

    # Case 4: IPDocKindCode absent, IPDocKindName matches literal 2 -> PASS
    case4 = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindName": [LITERAL_2],
    }
    _assert_pass(3, case4)
    _assert_pass(4, case4)

    # Case 5: IPDocKindCode absent, IPDocKindName has wrong literal -> FAIL REQ 4
    case5 = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindName": ["Неверное решение"],
    }
    _assert_fail(4, case5)

    # Case 6: Both absent -> FAIL REQ 4
    case6 = {R007: [{}]}
    _assert_fail(4, case6)


def test_req5_registration_cancellation_details():
    valid = {
        R007: [{}],
        CANCEL: [{}],
        f"{CANCEL}/ipsdo:CancellationTrademarkRegistrationReasonCode": ["01"],
        f"{CANCEL}/ipcdo:NationalPatentDecisionDetails": [{}],
    }
    _assert_pass(5, valid)

    # Missing container -> FAIL
    missing_container = {R007: [{}]}
    _assert_fail(5, missing_container)

    # Missing reason code -> FAIL
    missing_reason = {
        R007: [{}],
        CANCEL: [{}],
        f"{CANCEL}/ipcdo:NationalPatentDecisionDetails": [{}],
    }
    _assert_fail(5, missing_reason)

    # Missing NationalPatentDecisionDetails -> FAIL
    missing_decision = {
        R007: [{}],
        CANCEL: [{}],
        f"{CANCEL}/ipsdo:CancellationTrademarkRegistrationReasonCode": ["01"],
    }
    _assert_fail(5, missing_decision)


def test_req6_to_13_inherited_table49_rules():
    # REQ 6: UnifiedCountryCode/@codeListId == "ВОИС ST.3"
    valid_cc = {R007: [{}], f"{R007}/csdo:UnifiedCountryCode": ["RU"], f"{R007}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3"]}
    _assert_pass(6, valid_cc)
    bad_cc = {R007: [{}], f"{R007}/csdo:UnifiedCountryCode": ["RU"], f"{R007}/csdo:UnifiedCountryCode/@codeListId": ["OTHER"]}
    _assert_fail(6, bad_cc)

    # REQ 7: SubjectAddressDetails required fields
    addr = f"{R007}/ccdo:SubjectAddressDetails"
    valid_addr = {
        R007: [{}],
        addr: [{}],
        f"{addr}/csdo:AddressKindCode": ["2"],
        f"{addr}/csdo:UnifiedCountryCode": ["RU"],
        f"{addr}/csdo:CityName": ["Москва"],
        f"{addr}/csdo:StreetName": ["Тверская"],
        f"{addr}/csdo:BuildingNumberId": ["10"],
    }
    _assert_pass(7, valid_addr)
    missing_street = dict(valid_addr, **{f"{addr}/csdo:StreetName": [None]})
    _assert_fail(7, missing_street)

    # REQ 8 & 9: CommunicationDetails
    comm = f"{R007}/ccdo:CommunicationDetails"
    valid_comm = {
        R007: [{}],
        comm: [{}],
        f"{comm}/csdo:CommunicationChannelCode": ["EM"],
        f"{comm}/csdo:CommunicationChannelId": ["info@eaeu.org"],
    }
    _assert_pass(8, valid_comm)
    _assert_pass(9, valid_comm)

    comm_name_present = dict(valid_comm, **{f"{comm}/csdo:CommunicationChannelName": ["Email"]})
    _assert_fail(8, comm_name_present)

    comm_invalid_code = dict(valid_comm, **{f"{comm}/csdo:CommunicationChannelCode": ["XX"]})
    _assert_fail(9, comm_invalid_code)

    # REQ 10: PatentAuthorityDetails
    pa = f"{R007}/ipcdo:PatentAuthorityDetails"
    valid_pa = {
        pa: [{}],
        f"{pa}/csdo:UnifiedCountryCode": ["RU"],
        f"{pa}/csdo:AuthorityName": ["Роспатент"],
        f"{pa}/csdo:AuthorityBriefName": ["ФИПС"],
    }
    _assert_pass(10, valid_pa)
    missing_pa_field = dict(valid_pa, **{f"{pa}/csdo:AuthorityBriefName": [None]})
    _assert_fail(10, missing_pa_field)

    # REQ 11: IPPartyDetails RH cardinality (exactly 1 RH required)
    _assert_fail(11, {PARTY: []})
    _assert_fail(11, {PARTY: [{}], f"{PARTY}/ipsdo:IPPartyKindCode": ["PA"]})
    valid_rh = {PARTY: [{}], f"{PARTY}/ipsdo:IPPartyKindCode": ["RH"]}
    _assert_pass(11, valid_rh)
    two_rh = {PARTY: [{}, {}], f"{PARTY}/ipsdo:IPPartyKindCode": ["RH", "RH"]}
    _assert_fail(11, two_rh)

    # REQ 12 & 13: IPPartyDetails completeness and AddressKindCode == "2"
    party_addr = f"{PARTY}/ccdo:SubjectAddressDetails"
    valid_party = {
        PARTY: [{}],
        f"{PARTY}/csdo:UnifiedCountryCode": ["RU"],
        f"{PARTY}/ipsdo:IPSubjectName": ["ООО Правообладатель"],
        party_addr: [{}],
        f"{PARTY}/ccdo:CommunicationDetails": [{}],
        f"{party_addr}/csdo:AddressKindCode": ["2"],
    }
    _assert_pass(12, valid_party)
    _assert_pass(13, valid_party)

    missing_party_name = dict(valid_party, **{f"{PARTY}/ipsdo:IPSubjectName": [None]})
    _assert_fail(12, missing_party_name)

    bad_addr_kind = dict(valid_party, **{f"{party_addr}/csdo:AddressKindCode": ["1"]})
    _assert_fail(13, bad_addr_kind)


def test_req14_and_15_tm_details_and_repeatable_element_alignment():
    # REQ 14: TrademarkDetails required fields
    valid_tm = {
        TM: [{}],
        f"{TM}/ipsdo:TrademarkPicture": ["base64data"],
        f"{TM}/ipcdo:TMDescriptionDetails": [{}],
        f"{TM}/ipsdo:TrademarkKindName": ["Словесный"],
        f"{TM}/ipsdo:CollectiveMarkIndicator": ["0"],
    }
    _assert_pass(14, valid_tm)
    missing_pic = dict(valid_tm, **{f"{TM}/ipsdo:TrademarkPicture": [None]})
    _assert_fail(14, missing_pic)

    # REQ 15: TMDescriptionDetails & TMElementDetails
    valid_desc = {
        DESC: [{}],
        f"{DESC}/csdo:DescriptionText": ["Описание знака"],
        ELEMENT: [{}, {}],
        f"{ELEMENT}/ipsdo:TrademarkCFECode": ["01.01.01", "02.01.01"],
        f"{ELEMENT}/csdo:DesignationName": ["Элемент 1", "Элемент 2"],
        f"{ELEMENT}/ipsdo:TMLocalizedName": ["Перевод 1", "Перевод 2"],
        f"{ELEMENT}/ipsdo:TMTransliterationName": ["Translit 1", "Translit 2"],
    }
    _assert_pass(15, valid_desc)

    bad_elem = dict(valid_desc, **{f"{ELEMENT}/ipsdo:TrademarkCFECode": [None, "02.01.01"]})
    _assert_fail(15, bad_elem)


def test_req16_and_17_goods_repeatable_alignment_and_forbidden_fields():
    # REQ 16: GoodsBaseDetails required fields
    valid_goods = {
        GOODS: [{}, {}],
        f"{GOODS}/ipsdo:GoodsClassCode": ["09", "42"],
        f"{GOODS}/ipsdo:GoodsClassName": ["Приборы", "Услуги ПО"],
        f"{GOODS}/ipsdo:GoodsName": ["Программы", "Разработка"],
        f"{GOODS}/ipsdo:TrademarkDecisionIndicator": ["1", "1"],
        f"{GOODS}/ipsdo:TrademarkApplicationId": ["2026/RU-000001", "2026/RU-000001"],
    }
    _assert_pass(16, valid_goods)
    _assert_pass(17, valid_goods)

    # Missing goods class code in second parent -> FAIL REQ 16
    bad_goods = dict(valid_goods, **{f"{GOODS}/ipsdo:GoodsClassCode": ["09", None]})
    _assert_fail(16, bad_goods)

    # REQ 17: Forbidden fields
    forbidden_tm = dict(valid_goods, **{f"{GOODS}/ipsdo:TrademarkId": [None, "TM-001"]})
    _assert_fail(17, forbidden_tm)

    forbidden_appellation = dict(valid_goods, **{f"{GOODS}/ipsdo:ApellationOfOriginEAEUId": ["AO-001", None]})
    _assert_fail(17, forbidden_appellation)

    forbidden_refusal = dict(valid_goods, **{f"{GOODS}/ipsdo:TrademarkRegRefusalReasonText": ["Refusal", None]})
    _assert_fail(17, forbidden_refusal)


def test_req20_22_signatures_mutual_exclusion_and_repeatable_parents():
    # 0 signatures -> FAIL REQ 20 presence
    _assert_fail(20, {SIGNATURE: []}, suffix=".PRESENCE")

    # Form A: OfficerDetails only -> PASS
    sig_officer = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
    }
    _assert_pass(20, sig_officer)
    _assert_pass(21, sig_officer)
    _assert_pass(22, sig_officer)

    # Form B: FullNameDetails directly under signature -> PASS
    sig_person = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ccdo:FullNameDetails": [{}],
    }
    _assert_pass(20, sig_person)
    _assert_pass(21, sig_person)

    # Conflict: Both OfficerDetails and sibling FullNameDetails present -> FAIL REQ 20 & REQ 21
    sig_both = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
        f"{SIGNATURE}/ccdo:FullNameDetails": [{}],
    }
    _assert_fail(20, sig_both, suffix=".BRANCH")
    _assert_fail(21, sig_both)

    # Repeatable signatures: 2 signatures (Officer + Person) -> PASS
    sig_two = {
        SIGNATURE: [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов", None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван", None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт", None],
        f"{SIGNATURE}/ccdo:FullNameDetails": [None, {}],
    }
    _assert_pass(20, sig_two)
    _assert_pass(21, sig_two)
    _assert_pass(22, sig_two)

    # REQ 22: Officer missing PositionName -> FAIL
    sig_no_pos = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
    }
    _assert_fail(22, sig_no_pos)

    # REQ 22: Officer with forbidden CommunicationDetails -> FAIL
    sig_with_comm = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:CommunicationDetails": [{}],
    }
    _assert_fail(22, sig_with_comm)


def test_req23_start_datetime_required():
    valid = {
        R007: [{}],
        f"{R007}/ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime": ["2026-09-30T14:00:00+03:00"],
    }
    _assert_pass(23, valid)

    missing = {R007: [{}]}
    _assert_fail(23, missing)


def test_xml_extraction_and_repeatable_structure():
    def build_xml(root, s):
        r007 = _child(root, s, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(r007, s, "ipsdo", "TrademarkId", "2026/RU-000001")
        _child(r007, s, "ipsdo", "IPDocKindCode", "00051")

        cancel = _child(r007, s, "ipcdo", "RegistrationCancellationDetails")
        _child(cancel, s, "ipsdo", "CancellationTrademarkRegistrationReasonCode", "01")
        dec = _child(cancel, s, "ipcdo", "NationalPatentDecisionDetails")
        _child(dec, s, "ipsdo", "NationalPatentDecisionNumberId", "DEC-001")

        pa = _child(r007, s, "ipcdo", "PatentAuthorityDetails")
        _child(pa, s, "csdo", "UnifiedCountryCode", "RU", {"codeListId": "ВОИС ST.3"})
        _child(pa, s, "csdo", "AuthorityName", "Роспатент")
        _child(pa, s, "csdo", "AuthorityBriefName", "ФИПС")
        _child(pa, s, "ipsdo", "OriginOfficeIndicator", "1")

        party = _child(r007, s, "ipcdo", "IPPartyDetails")
        _child(party, s, "ipsdo", "IPPartyKindCode", "RH")
        _child(party, s, "csdo", "UnifiedCountryCode", "RU", {"codeListId": "ВОИС ST.3"})
        _child(party, s, "ipsdo", "IPSubjectName", "ООО Ромашка")
        addr = _child(party, s, "ccdo", "SubjectAddressDetails")
        _child(addr, s, "csdo", "AddressKindCode", "2")
        _child(addr, s, "csdo", "UnifiedCountryCode", "RU", {"codeListId": "ВОИС ST.3"})
        _child(addr, s, "csdo", "CityName", "Москва")
        _child(addr, s, "csdo", "StreetName", "Ленина")
        _child(addr, s, "csdo", "BuildingNumberId", "10")
        comm = _child(party, s, "ccdo", "CommunicationDetails")
        _child(comm, s, "csdo", "CommunicationChannelCode", "TE")
        _child(comm, s, "csdo", "CommunicationChannelId", "+74951234567")

        tm = _child(r007, s, "ipcdo", "TrademarkDetails")
        _child(tm, s, "ipsdo", "TrademarkPicture", "base64data")
        _child(tm, s, "ipsdo", "TrademarkKindName", "Словесный")
        _child(tm, s, "ipsdo", "CollectiveMarkIndicator", "0")
        desc = _child(tm, s, "ipcdo", "TMDescriptionDetails")
        _child(desc, s, "csdo", "DescriptionText", "Описание товарного знака")
        elem = _child(desc, s, "ipcdo", "TMElementDetails")
        _child(elem, s, "ipsdo", "TrademarkCFECode", "01.01.01")
        _child(elem, s, "csdo", "DesignationName", "Элемент")
        _child(elem, s, "ipsdo", "TMLocalizedName", "Перевод", {"languageCode": "ru"})
        _child(elem, s, "ipsdo", "TMTransliterationName", "Translit")

        g1 = _child(r007, s, "ipcdo", "GoodsBaseDetails")
        _child(g1, s, "ipsdo", "GoodsClassCode", "09")
        _child(g1, s, "ipsdo", "GoodsClassName", "Класс 09")
        _child(g1, s, "ipsdo", "GoodsName", "Товар 1")
        _child(g1, s, "ipsdo", "TrademarkDecisionIndicator", "1")
        _child(g1, s, "ipsdo", "TrademarkApplicationId", "2026/RU-000001")

        g2 = _child(r007, s, "ipcdo", "GoodsBaseDetails")
        _child(g2, s, "ipsdo", "GoodsClassCode", "42")
        _child(g2, s, "ipsdo", "GoodsClassName", "Класс 42")
        _child(g2, s, "ipsdo", "GoodsName", "Услуга 1")
        _child(g2, s, "ipsdo", "TrademarkDecisionIndicator", "1")
        _child(g2, s, "ipsdo", "TrademarkApplicationId", "2026/RU-000001")

        resource = _child(r007, s, "ccdo", "ResourceItemStatusDetails")
        val = _child(resource, s, "ccdo", "ValidityPeriodDetails")
        _child(val, s, "csdo", "StartDateTime", "2026-09-30T14:00:00+03:00")

        sig = _child(r007, s, "ipcdo", "SignatureDetails")
        _child(sig, s, "csdo", "DocCreationDate", "2026-09-30")
        officer = _child(sig, s, "ipcdo", "OfficerDetails")
        fn = _child(officer, s, "ccdo", "FullNameDetails")
        _child(fn, s, "csdo", "LastName", "Иванов")
        _child(fn, s, "csdo", "FirstName", "Иван")
        _child(officer, s, "csdo", "PositionName", "Эксперт")

    engine, structure, values, issues = _values_from_xml(build_xml)
    assert not issues, f"Extraction issues: {issues}"
    evaluator = StructuredRuleEvaluator()
    for rule in engine.rules[MESSAGE].structured_rules:
        result = evaluator.evaluate(rule, values)
        assert result.status is RuleStatus.PASS, f"Failed on rule {rule['rule_id']}: {result.message}"
