from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.053"
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
EXACT_DOC_NAME = (
    "Заявление о продлении срока действия исключительного права на товарный знак, "
    "знак обслуживания Евразийского экономического союза"
)


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
    rule_id = f"{MESSAGE}.T71.REQ.{code}{suffix}"
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
    valid = {
        R007: [{}],
        f"{R007}/ipsdo:TrademarkId": ["2026/RU-000001"],
    }
    _assert_pass(1, valid)

    missing = {
        R007: [{}],
    }
    _assert_fail(1, missing)


def test_req2_register_record_exact_one_cardinality():
    _assert_fail(2, {R007: []})
    _assert_pass(2, {R007: [{}]})
    _assert_fail(2, {R007: [{}, {}]})


def test_req3_end_datetime_forbidden():
    # Absent -> PASS
    valid_no_end = {
        R007: [{}],
        VALIDITY: [{}],
    }
    _assert_pass(3, valid_no_end)

    # Present -> FAIL
    invalid_with_end = {
        R007: [{}],
        f"{VALIDITY}/csdo:EndDateTime": ["2026-10-01T14:00:00+03:00"],
    }
    _assert_fail(3, invalid_with_end)


def test_req4_and_req5_document_kind_and_exact_fallback_literal():
    # REQ 4: Code present, Name absent -> PASS
    doc_with_code = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindCode": ["00053"],
    }
    _assert_pass(4, doc_with_code)
    _assert_pass(5, doc_with_code)

    # REQ 4: Code present, Name present -> FAIL REQ 4
    doc_with_both = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindCode": ["00053"],
        f"{R007}/ipsdo:IPDocKindName": [EXACT_DOC_NAME],
    }
    _assert_fail(4, doc_with_both)

    # REQ 5: Code absent, Name == EXACT_DOC_NAME -> PASS
    doc_exact_name = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindName": [EXACT_DOC_NAME],
    }
    _assert_pass(4, doc_exact_name)
    _assert_pass(5, doc_exact_name)

    # REQ 5: Code absent, Name != EXACT_DOC_NAME -> FAIL REQ 5
    doc_wrong_name = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindName": ["Неверное заявление"],
    }
    _assert_fail(5, doc_wrong_name)

    # REQ 5: Code absent, Name absent -> FAIL REQ 5
    doc_no_name = {
        R007: [{}],
    }
    _assert_fail(5, doc_no_name)


def test_table49_inherited_country_and_address_rules():
    # REQ 6: codeListId == "ВОИС ST.3"
    valid_cc = {f"{R007}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3"]}
    _assert_pass(6, valid_cc)
    _assert_fail(6, {f"{R007}/csdo:UnifiedCountryCode/@codeListId": ["ISO 3166"]})

    # REQ 7: Address requires AddressKindCode, UnifiedCountryCode, CityName, StreetName, BuildingNumberId
    addr = f"{R007}/ccdo:SubjectAddressDetails"
    valid_addr = {
        addr: [{}],
        f"{addr}/csdo:AddressKindCode": ["2"],
        f"{addr}/csdo:UnifiedCountryCode": ["RU"],
        f"{addr}/csdo:CityName": ["Москва"],
        f"{addr}/csdo:StreetName": ["Тверская"],
        f"{addr}/csdo:BuildingNumberId": ["1"],
    }
    _assert_pass(7, valid_addr)
    for missing_field in ("AddressKindCode", "UnifiedCountryCode", "CityName", "StreetName", "BuildingNumberId"):
        bad = dict(valid_addr)
        del bad[f"{addr}/csdo:{missing_field}"]
        _assert_fail(7, bad)

    # REQ 8: Communication requires ChannelCode and ChannelId, forbids ChannelName
    comm = f"{R007}/ccdo:CommunicationDetails"
    valid_comm = {
        comm: [{}],
        f"{comm}/csdo:CommunicationChannelCode": ["EM"],
        f"{comm}/csdo:CommunicationChannelId": ["test@example.com"],
    }
    _assert_pass(8, valid_comm)
    _assert_pass(9, valid_comm)

    bad_comm_name = dict(valid_comm, **{f"{comm}/csdo:CommunicationChannelName": ["Email"]})
    _assert_fail(8, bad_comm_name)

    missing_channel_id = dict(valid_comm)
    del missing_channel_id[f"{comm}/csdo:CommunicationChannelId"]
    _assert_fail(8, missing_channel_id)

    # REQ 9: ChannelCode in {"TE", "EM", "FX"}
    for valid_code in ("TE", "EM", "FX"):
        _assert_pass(9, dict(valid_comm, **{f"{comm}/csdo:CommunicationChannelCode": [valid_code]}))
    _assert_fail(9, dict(valid_comm, **{f"{comm}/csdo:CommunicationChannelCode": ["XX"]}))


def test_table49_inherited_patent_authority_and_party_rules():
    pa = f"{R007}/ipcdo:PatentAuthorityDetails"
    valid_pa = {
        pa: [{}],
        f"{pa}/csdo:UnifiedCountryCode": ["RU"],
        f"{pa}/csdo:AuthorityName": ["Роспатент"],
        f"{pa}/csdo:AuthorityBriefName": ["ФИПС"],
    }
    _assert_pass(10, valid_pa)
    for missing in ("UnifiedCountryCode", "AuthorityName", "AuthorityBriefName"):
        bad = dict(valid_pa)
        del bad[f"{pa}/csdo:{missing}"]
        _assert_fail(10, bad)

    # REQ 11: IPPartyDetails RH cardinality 1..1
    _assert_fail(11, {PARTY: []})
    party_rh = {
        PARTY: [{}],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["RH"],
    }
    _assert_pass(11, party_rh)
    party_two_rh = {
        PARTY: [{}, {}],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["RH", "RH"],
    }
    _assert_fail(11, party_two_rh)

    # REQ 12: IPPartyDetails RH requires Country, Name, Address, Communication
    valid_rh = {
        PARTY: [{}],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["RH"],
        f"{PARTY}/csdo:UnifiedCountryCode": ["RU"],
        f"{PARTY}/ipsdo:IPSubjectName": ["Правообладатель"],
        f"{PARTY}/ccdo:SubjectAddressDetails": [{}],
        f"{PARTY}/ccdo:CommunicationDetails": [{}],
    }
    _assert_pass(12, valid_rh)
    for missing in (
        f"{PARTY}/csdo:UnifiedCountryCode",
        f"{PARTY}/ipsdo:IPSubjectName",
        f"{PARTY}/ccdo:SubjectAddressDetails",
        f"{PARTY}/ccdo:CommunicationDetails",
    ):
        bad = dict(valid_rh)
        del bad[missing]
        _assert_fail(12, bad)

    # REQ 13: IPPartyDetails RH AddressKindCode == "2"
    valid_rh_addr = dict(valid_rh, **{f"{PARTY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["2"]})
    _assert_pass(13, valid_rh_addr)
    bad_rh_addr = dict(valid_rh, **{f"{PARTY}/ccdo:SubjectAddressDetails/csdo:AddressKindCode": ["1"]})
    _assert_fail(13, bad_rh_addr)


def test_table49_inherited_trademark_and_goods_rules():
    # REQ 14: TrademarkDetails required fields
    valid_tm = {
        TM: [{}],
        f"{TM}/ipsdo:TrademarkPicture": ["base64"],
        f"{TM}/ipcdo:TMDescriptionDetails": [{}],
        f"{TM}/ipsdo:TrademarkKindName": ["Словесный"],
        f"{TM}/ipsdo:CollectiveMarkIndicator": ["0"],
    }
    _assert_pass(14, valid_tm)
    for missing in ("TrademarkPicture", "TMDescriptionDetails", "TrademarkKindName", "CollectiveMarkIndicator"):
        bad = dict(valid_tm)
        key = f"{TM}/ipcdo:{missing}" if missing == "TMDescriptionDetails" else f"{TM}/ipsdo:{missing}"
        del bad[key]
        _assert_fail(14, bad)

    # REQ 15: TMDescriptionDetails and TMElementDetails
    valid_desc = {
        DESC: [{}],
        f"{DESC}/csdo:DescriptionText": ["Описание"],
        f"{DESC}/ipcdo:TMElementDetails": [{}],
        f"{ELEMENT}/ipsdo:TrademarkCFECode": ["01.01.01"],
        f"{ELEMENT}/csdo:DesignationName": ["Элемент"],
        f"{ELEMENT}/ipsdo:TMLocalizedName": ["Перевод"],
        f"{ELEMENT}/ipsdo:TMTransliterationName": ["Translit"],
    }
    _assert_pass(15, valid_desc)
    for missing in (
        f"{DESC}/csdo:DescriptionText",
        f"{DESC}/ipcdo:TMElementDetails",
        f"{ELEMENT}/ipsdo:TrademarkCFECode",
        f"{ELEMENT}/csdo:DesignationName",
        f"{ELEMENT}/ipsdo:TMLocalizedName",
        f"{ELEMENT}/ipsdo:TMTransliterationName",
    ):
        bad = dict(valid_desc)
        del bad[missing]
        _assert_fail(15, bad)

    # REQ 16: GoodsBaseDetails cardinality 1..*, required fields
    _assert_fail(16, {GOODS: []})
    valid_goods = {
        GOODS: [{}, {}],
        f"{GOODS}/ipsdo:GoodsClassCode": ["09", "42"],
        f"{GOODS}/ipsdo:GoodsClassName": ["Класс 09", "Класс 42"],
        f"{GOODS}/ipsdo:GoodsName": ["Товар 1", "Услуга 1"],
        f"{GOODS}/ipsdo:TrademarkDecisionIndicator": ["1", "1"],
        f"{GOODS}/ipsdo:TrademarkApplicationId": ["2026/RU-000001", "2026/RU-000001"],
    }
    _assert_pass(16, valid_goods)
    for missing in ("GoodsClassCode", "GoodsClassName", "GoodsName", "TrademarkDecisionIndicator", "TrademarkApplicationId"):
        bad = dict(valid_goods)
        del bad[f"{GOODS}/ipsdo:{missing}"]
        _assert_fail(16, bad)

    # REQ 17: GoodsBaseDetails forbidden fields
    _assert_pass(17, valid_goods)
    for forbidden in ("TrademarkId", "ApellationOfOriginEAEUId", "TrademarkRegRefusalReasonText"):
        bad = dict(valid_goods, **{f"{GOODS}/ipsdo:{forbidden}": ["Value", None]})
        _assert_fail(17, bad)


def test_req20_status_code_03_and_event_date():
    valid = {
        STATUS: [{}],
        f"{STATUS}/csdo:StatusCode": ["03"],
        f"{STATUS}/csdo:EventDate": ["2026-09-30"],
    }
    _assert_pass(20, valid)

    # Wrong StatusCode -> FAIL
    for bad_code in ("01", "02", "04", "05"):
        bad_status = dict(valid, **{f"{STATUS}/csdo:StatusCode": [bad_code]})
        _assert_fail(20, bad_status)

    # Missing EventDate -> FAIL
    missing_date = {
        STATUS: [{}],
        f"{STATUS}/csdo:StatusCode": ["03"],
    }
    _assert_fail(20, missing_date)

    # codeListId present on StatusCode -> FAIL
    with_codelist = dict(valid, **{f"{STATUS}/csdo:StatusCode/@codeListId": ["SOME_LIST"]})
    _assert_fail(20, with_codelist)


def test_req24_26_signatures_mutual_exclusion_and_repeatable_parents():
    # 0 signatures -> FAIL REQ 24 presence
    _assert_fail(24, {SIGNATURE: []}, suffix=".PRESENCE")

    # Form A: OfficerDetails only -> PASS
    sig_officer = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
    }
    _assert_pass(24, sig_officer)
    _assert_pass(25, sig_officer)
    _assert_pass(26, sig_officer)

    # Form B: FullNameDetails directly under signature -> PASS
    sig_person = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ccdo:FullNameDetails": [{}],
    }
    _assert_pass(24, sig_person)
    _assert_pass(25, sig_person)

    # Conflict: Both OfficerDetails and sibling FullNameDetails present -> FAIL REQ 24 & REQ 25
    sig_both = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
        f"{SIGNATURE}/ccdo:FullNameDetails": [{}],
    }
    _assert_fail(24, sig_both, suffix=".BRANCH")
    _assert_fail(25, sig_both)

    # Repeatable signatures: 2 signatures (Officer + Person) -> PASS
    sig_two = {
        SIGNATURE: [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов", None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван", None],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт", None],
        f"{SIGNATURE}/ccdo:FullNameDetails": [None, {}],
    }
    _assert_pass(24, sig_two)
    _assert_pass(25, sig_two)
    _assert_pass(26, sig_two)

    # REQ 26: Officer missing PositionName -> FAIL
    sig_no_pos = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
    }
    _assert_fail(26, sig_no_pos)

    # REQ 26: Officer with CommunicationDetails -> FAIL
    sig_with_comm = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:CommunicationDetails": [{}],
    }
    _assert_fail(26, sig_with_comm)


def test_xml_extraction_and_repeatable_structure():
    def build_xml(root, s):
        r007 = _child(root, s, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(r007, s, "ipsdo", "TrademarkId", "2026/RU-000001")
        _child(r007, s, "ipsdo", "IPDocKindCode", "00053")

        status = _child(r007, s, "ipcdo", "IPEntityStatusDetails")
        _child(status, s, "csdo", "StatusCode", "03")
        _child(status, s, "csdo", "EventDate", "2026-09-30")

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

        # Note: ResourceItemStatusDetails with NO EndDateTime
        _child(r007, s, "ccdo", "ResourceItemStatusDetails")

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
