from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.047"
STRUCTURE_ID = "R.IP.SP.02.007"
R007 = "ipcdo:UnifiedRegisterRecordsDetails"
GOODS = f"{R007}/ipcdo:GoodsBaseDetails"
TM = f"{R007}/ipcdo:TrademarkDetails"
DESC = f"{TM}/ipcdo:TMDescriptionDetails"
ELEMENT = f"{DESC}/ipcdo:TMElementDetails"
PARTY = f"{R007}/ipcdo:IPPartyDetails"
STATUS = f"{R007}/ipcdo:IPEntityStatusDetails"
TRANS = f"{R007}/ipcdo:TransformationDetails"
RESOURCE = f"{R007}/ccdo:ResourceItemStatusDetails"
SIGNATURE = f"{R007}/ipcdo:SignatureDetails"
EXACT_DOC_NAME = (
    "Ходатайство о преобразовании коллективного знака Евразийского экономического союза "
    "в товарный знак, знак обслуживания Евразийского экономического союза"
)


def _engine():
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
    rule_id = f"{MESSAGE}.T65.REQ.{code}{suffix}"
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
    # REQ 1: TrademarkId is required locally under UnifiedRegisterRecordsDetails
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


def test_req3_status_code_03_and_event_date_and_codelist_id():
    # Valid: StatusCode == "03", EventDate present, no codeListId
    valid = {
        STATUS: [{}],
        f"{STATUS}/csdo:StatusCode": ["03"],
        f"{STATUS}/csdo:EventDate": ["2026-09-30"],
    }
    _assert_pass(3, valid)

    # Wrong StatusCode ("01" or "02" or "30") -> FAIL
    for bad_code in ("01", "02", "30"):
        bad_status = dict(valid, **{f"{STATUS}/csdo:StatusCode": [bad_code]})
        _assert_fail(3, bad_status)

    # Missing EventDate -> FAIL
    missing_date = {
        STATUS: [{}],
        f"{STATUS}/csdo:StatusCode": ["03"],
    }
    _assert_fail(3, missing_date)

    # codeListId present on StatusCode -> FAIL
    with_codelist = dict(valid, **{f"{STATUS}/csdo:StatusCode/@codeListId": ["SOME_LIST"]})
    _assert_fail(3, with_codelist)


def test_req4_and_req5_document_kind():
    # Case 1: IPDocKindCode present, IPDocKindName absent -> PASS
    case1 = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindCode": ["00042"],
    }
    _assert_pass(4, case1)
    _assert_pass(5, case1)

    # Case 2: IPDocKindCode present, IPDocKindName also present -> FAIL REQ 4
    case2 = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindCode": ["00042"],
        f"{R007}/ipsdo:IPDocKindName": [EXACT_DOC_NAME],
    }
    _assert_fail(4, case2)

    # Case 3: IPDocKindCode absent, IPDocKindName matches exact literal -> PASS
    case3 = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindName": [EXACT_DOC_NAME],
    }
    _assert_pass(4, case3)
    _assert_pass(5, case3)

    # Case 4: IPDocKindCode absent, IPDocKindName has wrong literal -> FAIL REQ 5
    case4 = {
        R007: [{}],
        f"{R007}/ipsdo:IPDocKindName": ["Неверное наименование документа"],
    }
    _assert_fail(5, case4)

    # Case 5: Both absent -> FAIL REQ 5
    case5 = {R007: [{}]}
    _assert_fail(5, case5)


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

    # If first element is missing CFE code -> FAIL
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


def test_req20_transformation_details_per_instance_without_container_requirement():
    # 0 instances of TransformationDetails -> PASS (container is NOT required to exist!)
    zero_trans = {R007: [{}]}
    _assert_pass(20, zero_trans)

    # 1 complete instance -> PASS
    one_complete = {
        TRANS: [{}],
        f"{TRANS}/ipsdo:TransformationKindName": ["Преобразование коллективного знака в товарный знак"],
        f"{TRANS}/ipsdo:IPObjectId": ["2026/RU-000001"],
        f"{TRANS}/csdo:EventDate": ["2026-09-30"],
    }
    _assert_pass(20, one_complete)

    # 1 incomplete instance (missing EventDate) -> FAIL
    incomplete_date = {
        TRANS: [{}],
        f"{TRANS}/ipsdo:TransformationKindName": ["Преобразование коллективного знака в товарный знак"],
        f"{TRANS}/ipsdo:IPObjectId": ["2026/RU-000001"],
        f"{TRANS}/csdo:EventDate": [None],
    }
    _assert_fail(20, incomplete_date)

    # 1 incomplete instance (missing IPObjectId) -> FAIL
    incomplete_id = {
        TRANS: [{}],
        f"{TRANS}/ipsdo:TransformationKindName": ["Преобразование коллективного знака в товарный знак"],
        f"{TRANS}/ipsdo:IPObjectId": [None],
        f"{TRANS}/csdo:EventDate": ["2026-09-30"],
    }
    _assert_fail(20, incomplete_id)

    # 2 instances: good + good -> PASS
    two_good = {
        TRANS: [{}, {}],
        f"{TRANS}/ipsdo:TransformationKindName": ["Вид 1", "Вид 2"],
        f"{TRANS}/ipsdo:IPObjectId": ["ID-1", "ID-2"],
        f"{TRANS}/csdo:EventDate": ["2026-09-30", "2026-09-30"],
    }
    _assert_pass(20, two_good)

    # 2 instances: good + bad -> FAIL
    good_and_bad = {
        TRANS: [{}, {}],
        f"{TRANS}/ipsdo:TransformationKindName": ["Вид 1", "Вид 2"],
        f"{TRANS}/ipsdo:IPObjectId": ["ID-1", None],
        f"{TRANS}/csdo:EventDate": ["2026-09-30", "2026-09-30"],
    }
    _assert_fail(20, good_and_bad)


def test_req21_collective_mark_indicator_zero():
    # Exact value "0" -> PASS
    valid_zero = {
        TM: [{}],
        f"{TM}/ipsdo:CollectiveMarkIndicator": ["0"],
    }
    _assert_pass(21, valid_zero)

    # Value "1" (collective mark, used by MSG048) -> FAIL
    invalid_one = {
        TM: [{}],
        f"{TM}/ipsdo:CollectiveMarkIndicator": ["1"],
    }
    _assert_fail(21, invalid_one)

    # Missing value -> FAIL
    missing_indicator = {
        TM: [{}],
        f"{TM}/ipsdo:CollectiveMarkIndicator": [None],
    }
    _assert_fail(21, missing_indicator)


def test_req22_validity_period_end_datetime_forbidden():
    # EndDateTime absent -> PASS
    valid = {RESOURCE: [{}]}
    _assert_pass(22, valid)

    # EndDateTime present -> FAIL
    invalid = {
        RESOURCE: [{}],
        f"{RESOURCE}/ccdo:ValidityPeriodDetails/csdo:EndDateTime": ["2026-10-01T14:00:00+03:00"],
    }
    _assert_fail(22, invalid)


def test_req23_25_signatures_mutual_exclusion_and_repeatable_parents():
    # 0 signatures -> FAIL REQ 23 presence
    _assert_fail(23, {SIGNATURE: []}, suffix=".PRESENCE")

    # Form A: OfficerDetails only -> PASS
    sig_officer = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
    }
    _assert_pass(23, sig_officer)
    _assert_pass(24, sig_officer)
    _assert_pass(25, sig_officer)

    # Form B: FullNameDetails directly under signature -> PASS
    sig_direct = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ccdo:FullNameDetails": [{}],
    }
    _assert_pass(23, sig_direct)
    _assert_pass(24, sig_direct)

    # Mutual exclusion violation in same parent (both officer and direct name present) -> FAIL
    both = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ccdo:FullNameDetails": [{}],
    }
    _assert_fail(23, both, suffix=".BRANCH")
    _assert_fail(24, both)

    # Multiple repeatable signatures: first has officer, second has direct name -> PASS without leakage
    repeatable_sigs = {
        SIGNATURE: [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, None],
        f"{SIGNATURE}/ccdo:FullNameDetails": [None, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Иванов"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Иван"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
    }
    _assert_pass(23, repeatable_sigs)
    _assert_pass(24, repeatable_sigs)
    _assert_pass(25, repeatable_sigs)

    # REQ 25: Missing PositionName under OfficerDetails -> FAIL
    missing_position = dict(sig_officer, **{f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": [None]})
    _assert_fail(25, missing_position)

    # REQ 25: CommunicationDetails present under OfficerDetails -> FAIL
    comm_in_officer = dict(sig_officer, **{f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:CommunicationDetails": [{}]})
    _assert_fail(25, comm_in_officer)


def test_r007_production_xml_extraction_and_rule_evaluation():
    # Build complete valid XML tree and evaluate
    def build(root, structure):
        records = _child(root, structure, "ipcdo", "UnifiedRegisterRecordsDetails")
        _child(records, structure, "ipsdo", "TrademarkId", "2026/RU-000001")
        _child(records, structure, "ipsdo", "IPDocKindCode", "00042")

        # Status
        status = _child(records, structure, "ipcdo", "IPEntityStatusDetails")
        _child(status, structure, "csdo", "StatusCode", "03")
        _child(status, structure, "csdo", "EventDate", "2026-09-30")

        # TransformationDetails (1 valid instance)
        trans = _child(records, structure, "ipcdo", "TransformationDetails")
        _child(trans, structure, "ipsdo", "TransformationKindName", EXACT_DOC_NAME)
        _child(trans, structure, "ipsdo", "IPObjectId", "2026/RU-000001")
        _child(trans, structure, "csdo", "EventDate", "2026-09-30")

        # TrademarkDetails
        tm = _child(records, structure, "ipcdo", "TrademarkDetails")
        _child(tm, structure, "ipsdo", "TrademarkPicture", "base64data")
        _child(tm, structure, "ipsdo", "TrademarkKindName", "Словесный")
        _child(tm, structure, "ipsdo", "CollectiveMarkIndicator", "0")

        # TMDescriptionDetails & TMElementDetails
        desc = _child(tm, structure, "ipcdo", "TMDescriptionDetails")
        _child(desc, structure, "csdo", "DescriptionText", "Описание знака")
        elem = _child(desc, structure, "ipcdo", "TMElementDetails")
        _child(elem, structure, "ipsdo", "TrademarkCFECode", "01.01.01")
        _child(elem, structure, "csdo", "DesignationName", "Знак")
        _child(elem, structure, "ipsdo", "TMLocalizedName", "Перевод")
        _child(elem, structure, "ipsdo", "TMTransliterationName", "Translit")

        # PatentAuthorityDetails
        pa = _child(records, structure, "ipcdo", "PatentAuthorityDetails")
        _child(pa, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
        _child(pa, structure, "csdo", "AuthorityName", "Роспатент")
        _child(pa, structure, "csdo", "AuthorityBriefName", "ФИПС")

        # IPPartyDetails (RH)
        party = _child(records, structure, "ipcdo", "IPPartyDetails")
        _child(party, structure, "ipsdo", "IPPartyKindCode", "RH")
        _child(party, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
        _child(party, structure, "ipsdo", "IPSubjectName", "ООО Заявитель")
        addr = _child(party, structure, "ccdo", "SubjectAddressDetails")
        _child(addr, structure, "csdo", "AddressKindCode", "2")
        _child(addr, structure, "csdo", "UnifiedCountryCode", "RU", attrs={"codeListId": "ВОИС ST.3"})
        _child(addr, structure, "csdo", "CityName", "Москва")
        _child(addr, structure, "csdo", "StreetName", "Тверская")
        _child(addr, structure, "csdo", "BuildingNumberId", "1")
        comm = _child(party, structure, "ccdo", "CommunicationDetails")
        _child(comm, structure, "csdo", "CommunicationChannelCode", "EM")
        _child(comm, structure, "csdo", "CommunicationChannelId", "test@test.ru")

        # GoodsBaseDetails
        goods = _child(records, structure, "ipcdo", "GoodsBaseDetails")
        _child(goods, structure, "ipsdo", "GoodsClassCode", "09")
        _child(goods, structure, "ipsdo", "GoodsClassName", "Класс 9")
        _child(goods, structure, "ipsdo", "GoodsName", "Программы")
        _child(goods, structure, "ipsdo", "TrademarkDecisionIndicator", "1")
        _child(goods, structure, "ipsdo", "TrademarkApplicationId", "2026/RU-000001")

        # ResourceItemStatusDetails (validity period without EndDateTime)
        resource = _child(records, structure, "ccdo", "ResourceItemStatusDetails")
        period = _child(resource, structure, "ccdo", "ValidityPeriodDetails")
        _child(period, structure, "csdo", "StartDateTime", "2026-09-30T10:00:00+03:00")

        # SignatureDetails
        sig = _child(records, structure, "ipcdo", "SignatureDetails")
        officer = _child(sig, structure, "ipcdo", "OfficerDetails")
        full_name = _child(officer, structure, "ccdo", "FullNameDetails")
        _child(full_name, structure, "csdo", "LastName", "Иванов")
        _child(full_name, structure, "csdo", "FirstName", "Иван")
        _child(officer, structure, "csdo", "PositionName", "Эксперт")

    engine, structure, values, issues = _values_from_xml(build)
    assert not issues, f"Extraction issues: {issues}"

    evaluator = StructuredRuleEvaluator()
    rules = engine.rules[MESSAGE].structured_rules
    for r in rules:
        res = evaluator.evaluate(r, values)
        assert res.status is RuleStatus.PASS, f"Rule {r['rule_id']} failed on valid XML: {res.details}"
