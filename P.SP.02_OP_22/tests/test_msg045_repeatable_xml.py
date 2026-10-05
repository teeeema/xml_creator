from pathlib import Path

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.045"
APP = "ipcdo:TrademarkApplicationDetails"
SIGNATURE = f"{APP}/ipcdo:SignatureDetails"
TRADEMARK = f"{APP}/ipcdo:TrademarkDetails"
RESOURCE = "ccdo:ResourceItemStatusDetails"
STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
PARTY = f"{APP}/ipcdo:IPPartyDetails"
GOODS = f"{APP}/ipcdo:GoodsBaseDetails"


def rule(code, suffix=""):
    engine = EaeuXmlEngine.load_process(PACKAGE)
    rule_id = f"{MESSAGE}.T63.REQ.{code}{suffix}"
    return next(item for item in engine.rules[MESSAGE].structured_rules if item["rule_id"] == rule_id)


def test_req1_exactly_one_application():
    evaluator = StructuredRuleEvaluator()
    r = rule(1)
    assert evaluator.evaluate(r, {APP: []}).status is RuleStatus.FAIL
    assert evaluator.evaluate(r, {APP: [{}]}).status is RuleStatus.PASS
    assert evaluator.evaluate(r, {APP: [{}, {}]}).status is RuleStatus.FAIL


def test_req3_root_resource_end_datetime_forbidden():
    evaluator = StructuredRuleEvaluator()
    r = rule(3)
    path = RESOURCE

    # Absent EndDateTime -> PASS
    valid = {path: [{}]}
    assert evaluator.evaluate(r, valid).status is RuleStatus.PASS

    # Present EndDateTime -> FAIL
    invalid = {
        path: [{}],
        f"{path}/ccdo:ValidityPeriodDetails/csdo:EndDateTime": "2026-10-01T14:00:00+03:00",
    }
    assert evaluator.evaluate(r, invalid).status is RuleStatus.FAIL

    # Application entity status date present does not fail root REQ3
    app_status_date = {
        path: [{}],
        f"{STATUS}/csdo:EventDate": "2026-10-01",
    }
    assert evaluator.evaluate(r, app_status_date).status is RuleStatus.PASS


def test_req6_12_inherited_table44_application_descendants():
    evaluator = StructuredRuleEvaluator()

    # REQ 6: ApplicationReceiptDate required
    r6 = rule(6)
    assert evaluator.evaluate(r6, {APP: [{}]}).status is RuleStatus.FAIL
    assert evaluator.evaluate(r6, {APP: [{}], f"{APP}/ipsdo:ApplicationReceiptDate": "2026-09-30"}).status is RuleStatus.PASS

    # REQ 7: UnifiedCountryCode/@codeListId must be "ВОИС ST.3"
    r7 = rule(7)
    valid_country = {APP: [{}], f"{APP}/csdo:UnifiedCountryCode": ["RU"], f"{APP}/csdo:UnifiedCountryCode/@codeListId": ["ВОИС ST.3"]}
    assert evaluator.evaluate(r7, valid_country).status is RuleStatus.PASS
    invalid_country = {APP: [{}], f"{APP}/csdo:UnifiedCountryCode": ["RU"], f"{APP}/csdo:UnifiedCountryCode/@codeListId": ["OTHER"]}
    assert evaluator.evaluate(r7, invalid_country).status is RuleStatus.FAIL

    # REQ 8: SubjectAddressDetails required fields
    r8 = rule(8)
    addr = f"{APP}/ccdo:SubjectAddressDetails"
    valid_addr = {
        APP: [{}],
        addr: [{}],
        f"{addr}/csdo:AddressKindCode": ["2"],
        f"{addr}/csdo:UnifiedCountryCode": ["RU"],
        f"{addr}/csdo:CityName": ["Москва"],
        f"{addr}/csdo:StreetName": ["Ленина"],
        f"{addr}/csdo:BuildingNumberId": ["1"],
    }
    assert evaluator.evaluate(r8, valid_addr).status is RuleStatus.PASS
    missing_city = dict(valid_addr, **{f"{addr}/csdo:CityName": [None]})
    assert evaluator.evaluate(r8, missing_city).status is RuleStatus.FAIL

    # REQ 9: CommunicationDetails channel code and id
    r9 = rule(9)
    comm = f"{APP}/ccdo:CommunicationDetails"
    valid_comm = {APP: [{}], comm: [{}], f"{comm}/csdo:CommunicationChannelCode": ["EM"], f"{comm}/csdo:CommunicationChannelId": ["a@b.ru"]}
    assert evaluator.evaluate(r9, valid_comm).status is RuleStatus.PASS
    missing_comm_id = {APP: [{}], comm: [{}], f"{comm}/csdo:CommunicationChannelCode": ["EM"]}
    assert evaluator.evaluate(r9, missing_comm_id).status is RuleStatus.FAIL

    # REQ 10: CommunicationDetails channel code in {TE, EM, FX}
    r10 = rule(10)
    assert evaluator.evaluate(r10, valid_comm).status is RuleStatus.PASS
    comm_invalid_code = dict(valid_comm, **{f"{comm}/csdo:CommunicationChannelCode": ["XX"]})
    assert evaluator.evaluate(r10, comm_invalid_code).status is RuleStatus.FAIL

    # REQ 11: PatentAuthorityDetails required fields
    r11 = rule(11)
    pa = f"{APP}/ipcdo:PatentAuthorityDetails"
    valid_pa = {APP: [{}], pa: [{}], f"{pa}/csdo:UnifiedCountryCode": ["RU"]}
    assert evaluator.evaluate(r11, valid_pa).status is RuleStatus.PASS
    missing_auth = {APP: [{}], pa: [{}]}
    assert evaluator.evaluate(r11, missing_auth).status is RuleStatus.FAIL

    # REQ 12: PatentAuthorityDetails address completeness
    r12 = rule(12)
    pa_addr = f"{pa}/ccdo:SubjectAddressDetails"
    valid_pa_addr = {
        APP: [{}], pa: [{}], f"{pa}/csdo:UnifiedCountryCode": ["RU"], f"{pa}/csdo:AuthorityName": ["Роспатент"],
        pa_addr: [{}], f"{pa_addr}/csdo:AddressKindCode": ["2"],
    }
    assert evaluator.evaluate(r12, valid_pa_addr).status is RuleStatus.PASS
    missing_addr_kind = dict(valid_pa_addr, **{f"{pa_addr}/csdo:AddressKindCode": [None]})
    assert evaluator.evaluate(r12, missing_addr_kind).status is RuleStatus.FAIL


def test_req14_15_ip_party_ap():
    evaluator = StructuredRuleEvaluator()
    r14 = rule(14)
    r15 = rule(15)

    # 0 AP -> FAIL
    assert evaluator.evaluate(r14, {PARTY: []}).status is RuleStatus.FAIL
    assert evaluator.evaluate(r14, {PARTY: [{}], f"{PARTY}/ipsdo:IPPartyKindCode": ["PA"]}).status is RuleStatus.FAIL

    # 1 AP -> PASS
    valid_ap = {
        PARTY: [{}],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["AP"],
        f"{PARTY}/ipsdo:IPSubjectName": ["ООО Заявитель"],
        f"{PARTY}/csdo:UnifiedCountryCode": ["RU"],
        f"{PARTY}/ccdo:SubjectAddressDetails": [{}],
        f"{PARTY}/ccdo:CommunicationDetails": [{}],
    }
    assert evaluator.evaluate(r14, valid_ap).status is RuleStatus.PASS
    assert evaluator.evaluate(r15, valid_ap).status is RuleStatus.PASS

    # 2 AP -> FAIL
    two_ap = {
        PARTY: [{}, {}],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["AP", "AP"],
    }
    assert evaluator.evaluate(r14, two_ap).status is RuleStatus.FAIL

    # Missing IPSubjectName -> REQ15 FAIL
    missing_name = dict(valid_ap, **{f"{PARTY}/ipsdo:IPSubjectName": [None]})
    assert evaluator.evaluate(r15, missing_name).status is RuleStatus.FAIL


def test_req21_22_pa_re_parties():
    evaluator = StructuredRuleEvaluator()
    r21 = rule(21)
    r22 = rule(22)

    # PA party valid
    valid_pa = {
        PARTY: [{}],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["PA"],
        f"{PARTY}/ipsdo:IPSubjectName": ["Патентный поверенный"],
        f"{PARTY}/csdo:UnifiedCountryCode": ["RU"],
        f"{PARTY}/ccdo:SubjectAddressDetails": [{}],
        f"{PARTY}/ccdo:CommunicationDetails": [{}],
        f"{PARTY}/ipsdo:PatentAttorneyId": ["12345"],
    }
    assert evaluator.evaluate(r21, valid_pa).status is RuleStatus.PASS
    missing_pa_country = dict(valid_pa, **{f"{PARTY}/csdo:UnifiedCountryCode": [None]})
    assert evaluator.evaluate(r21, missing_pa_country).status is RuleStatus.FAIL

    # RE party valid
    valid_re = {
        PARTY: [{}],
        f"{PARTY}/ipsdo:IPPartyKindCode": ["RE"],
        f"{PARTY}/ipsdo:IPSubjectName": ["Представитель"],
        f"{PARTY}/csdo:UnifiedCountryCode": ["RU"],
        f"{PARTY}/ccdo:SubjectAddressDetails": [{}],
        f"{PARTY}/ccdo:CommunicationDetails": [{}],
    }
    assert evaluator.evaluate(r22, valid_re).status is RuleStatus.PASS
    missing_re_addr = dict(valid_re, **{f"{PARTY}/ccdo:SubjectAddressDetails": []})
    assert evaluator.evaluate(r22, missing_re_addr).status is RuleStatus.FAIL


def test_req23_25_correspondence_and_trademark():
    evaluator = StructuredRuleEvaluator()
    r23 = rule(23)
    r24 = rule(24)
    r25_card = rule(25, ".CARDINALITY")
    r25_fields = rule(25, ".FIELDS")

    corr = f"{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:SubjectAddressDetails"
    valid_corr = {
        corr: [{}],
        f"{corr}/csdo:AddressKindCode": ["3"],
        f"{corr}/csdo:UnifiedCountryCode": ["RU"],
        f"{corr}/csdo:CityName": ["Москва"],
        f"{corr}/csdo:StreetName": ["Тверская"],
        f"{corr}/csdo:BuildingNumberId": ["1"],
    }
    assert evaluator.evaluate(r23, valid_corr).status is RuleStatus.PASS
    assert evaluator.evaluate(r24, valid_corr).status is RuleStatus.PASS

    wrong_kind = dict(valid_corr, **{f"{corr}/csdo:AddressKindCode": ["1"]})
    assert evaluator.evaluate(r23, wrong_kind).status is RuleStatus.FAIL

    # REQ 25
    assert evaluator.evaluate(r25_card, {TRADEMARK: []}).status is RuleStatus.FAIL
    valid_tm = {
        TRADEMARK: [{}],
        f"{TRADEMARK}/ipcdo:TMDescriptionDetails": [{}],
        f"{TRADEMARK}/ipcdo:TMDescriptionDetails/csdo:DescriptionText": ["Текстовое описание"],
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": ["110"],
        f"{TRADEMARK}/ipsdo:TrademarkKindName": ["Словесный знак"],
        f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": ["1"],
    }
    assert evaluator.evaluate(r25_card, valid_tm).status is RuleStatus.PASS
    assert evaluator.evaluate(r25_fields, valid_tm).status is RuleStatus.PASS
    missing_desc = dict(valid_tm, **{f"{TRADEMARK}/ipcdo:TMDescriptionDetails": []})
    assert evaluator.evaluate(r25_fields, missing_desc).status is RuleStatus.FAIL


def test_req27_same_trademark_parent_trigger_and_fields():
    evaluator = StructuredRuleEvaluator()
    r27 = rule(27)

    # Valid: trigger 140 with picture and colour in the same parent
    valid = {
        TRADEMARK: [{}, {}],
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": ["110", "140"],
        f"{TRADEMARK}/ipsdo:TrademarkPicture": [None, "pic_data"],
        f"{TRADEMARK}/ipsdo:TrademarkColourName": [None, "синий"],
    }
    assert evaluator.evaluate(r27, valid).status is RuleStatus.PASS

    # Trigger 140 missing picture -> FAIL
    missing_pic = {
        TRADEMARK: [{}],
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": ["140"],
        f"{TRADEMARK}/ipsdo:TrademarkColourName": ["синий"],
    }
    assert evaluator.evaluate(r27, missing_pic).status is RuleStatus.FAIL

    # Cross-parent mismatch: picture in parent 0, trigger in parent 1 -> FAIL
    cross_parent = {
        TRADEMARK: [{}, {}],
        f"{TRADEMARK}/ipsdo:TrademarkKindCode": ["110", "140"],
        f"{TRADEMARK}/ipsdo:TrademarkPicture": ["pic_data", None],
        f"{TRADEMARK}/ipsdo:TrademarkColourName": [None, "синий"],
    }
    assert evaluator.evaluate(r27, cross_parent).status is RuleStatus.FAIL


def test_req28_collective_mark_indicator():
    evaluator = StructuredRuleEvaluator()
    r28 = rule(28)

    assert evaluator.evaluate(r28, {TRADEMARK: [{}], f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "0"}).status is RuleStatus.PASS
    assert evaluator.evaluate(r28, {TRADEMARK: [{}], f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "1"}).status is RuleStatus.PASS
    assert evaluator.evaluate(r28, {TRADEMARK: [{}], f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "2"}).status is RuleStatus.FAIL
    assert evaluator.evaluate(r28, {TRADEMARK: [{}], f"{TRADEMARK}/ipsdo:CollectiveMarkIndicator": "yes"}).status is RuleStatus.FAIL


def test_req29_per_goods_base_details():
    evaluator = StructuredRuleEvaluator()
    r29_card = rule(29, ".CARDINALITY")
    r29_fields = rule(29, ".FIELDS")

    # 0 goods -> FAIL
    assert evaluator.evaluate(r29_card, {GOODS: []}).status is RuleStatus.FAIL

    # Two valid goods -> PASS
    valid_goods = {
        GOODS: [{}, {}],
        f"{GOODS}/ipsdo:GoodsClassCode": ["01", "02"],
        f"{GOODS}/ipsdo:GoodsClassName": ["Класс 01", "Класс 02"],
        f"{GOODS}/ipsdo:GoodsName": ["Товар 1", "Товар 2"],
    }
    assert evaluator.evaluate(r29_card, valid_goods).status is RuleStatus.PASS
    assert evaluator.evaluate(r29_fields, valid_goods).status is RuleStatus.PASS

    # One good, one bad -> FAIL
    bad_goods = {
        GOODS: [{}, {}],
        f"{GOODS}/ipsdo:GoodsClassCode": ["01", None],
        f"{GOODS}/ipsdo:GoodsClassName": ["Класс 01", "Класс 02"],
        f"{GOODS}/ipsdo:GoodsName": ["Товар 1", "Товар 2"],
    }
    assert evaluator.evaluate(r29_fields, bad_goods).status is RuleStatus.FAIL


def test_req31_application_entity_status():
    evaluator = StructuredRuleEvaluator()
    r31 = rule(31)

    # Valid status
    valid = {
        APP: [{}],
        STATUS: [{}],
        f"{STATUS}/csdo:StatusCode": "02",
    }
    assert evaluator.evaluate(r31, valid).status is RuleStatus.PASS

    # Missing status -> FAIL
    assert evaluator.evaluate(r31, {APP: [{}]}).status is RuleStatus.FAIL

    # StatusCode != 02 (e.g. 30, 01) -> FAIL
    assert evaluator.evaluate(r31, dict(valid, **{f"{STATUS}/csdo:StatusCode": "30"})).status is RuleStatus.FAIL
    assert evaluator.evaluate(r31, dict(valid, **{f"{STATUS}/csdo:StatusCode": "01"})).status is RuleStatus.FAIL

    # codeListId present -> FAIL
    with_codelist = dict(valid, **{f"{STATUS}/csdo:StatusCode/@codeListId": "some_list"})
    assert evaluator.evaluate(r31, with_codelist).status is RuleStatus.FAIL

    # Wrong owner status does not satisfy REQ31
    wrong_owner = {
        APP: [{}],
        "other:IPEntityStatusDetails": [{}],
        "other:IPEntityStatusDetails/csdo:StatusCode": "02",
    }
    assert evaluator.evaluate(r31, wrong_owner).status is RuleStatus.FAIL


def test_req32_status_descendants_required():
    evaluator = StructuredRuleEvaluator()
    r32 = rule(32)

    valid = {
        STATUS: [{}],
        f"{STATUS}/csdo:EventDate": ["2026-09-30"],
        f"{STATUS}/csdo:DocId": ["DOC-123"],
        f"{STATUS}/ipsdo:IPDocReceiptDate": ["2026-09-30"],
        f"{STATUS}/csdo:DescriptionText": ["Внесение изменений"],
    }
    assert evaluator.evaluate(r32, valid).status is RuleStatus.PASS

    # Missing EventDate -> FAIL
    missing_event = dict(valid, **{f"{STATUS}/csdo:EventDate": [None]})
    assert evaluator.evaluate(r32, missing_event).status is RuleStatus.FAIL

    # Missing DocId -> FAIL
    missing_doc = dict(valid, **{f"{STATUS}/csdo:DocId": [None]})
    assert evaluator.evaluate(r32, missing_doc).status is RuleStatus.FAIL

    # Missing IPDocReceiptDate -> FAIL
    missing_receipt = dict(valid, **{f"{STATUS}/ipsdo:IPDocReceiptDate": [None]})
    assert evaluator.evaluate(r32, missing_receipt).status is RuleStatus.FAIL

    # 0 DescriptionText -> FAIL
    zero_desc = dict(valid, **{f"{STATUS}/csdo:DescriptionText": []})
    assert evaluator.evaluate(r32, zero_desc).status is RuleStatus.FAIL


def test_req33_35_signature_branches_and_officer():
    evaluator = StructuredRuleEvaluator()
    r33_pres = rule(33, ".PRESENCE")
    r33_branch = rule(33, ".BRANCH")
    r34 = rule(34)
    r35 = rule(35)

    # 0 signatures -> FAIL
    assert evaluator.evaluate(r33_pres, {SIGNATURE: []}).status is RuleStatus.FAIL

    # Distinct signatures: one officer, one fullname -> PASS
    separate = {
        SIGNATURE: [{}, {}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}, None],
        f"{SIGNATURE}/ccdo:FullNameDetails": [None, {}],
    }
    assert evaluator.evaluate(r33_pres, separate).status is RuleStatus.PASS
    assert evaluator.evaluate(r33_branch, separate).status is RuleStatus.PASS
    assert evaluator.evaluate(r34, separate).status is RuleStatus.PASS

    # Mutual exclusion violation within same signature -> FAIL
    same_conflict = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ccdo:FullNameDetails": [{}],
    }
    assert evaluator.evaluate(r33_branch, same_conflict).status is RuleStatus.FAIL
    assert evaluator.evaluate(r34, same_conflict).status is RuleStatus.FAIL

    # Officer details required fields (REQ 35)
    valid_officer = {
        SIGNATURE: [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails": [{}],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": ["Петров"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": ["Петр"],
        f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": ["Эксперт"],
    }
    assert evaluator.evaluate(r35, valid_officer).status is RuleStatus.PASS

    # Missing LastName -> FAIL
    assert evaluator.evaluate(r35, dict(valid_officer, **{f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:LastName": [None]})).status is RuleStatus.FAIL

    # Missing FirstName -> FAIL
    assert evaluator.evaluate(r35, dict(valid_officer, **{f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:FullNameDetails/csdo:FirstName": [None]})).status is RuleStatus.FAIL

    # Missing PositionName -> FAIL
    assert evaluator.evaluate(r35, dict(valid_officer, **{f"{SIGNATURE}/ipcdo:OfficerDetails/csdo:PositionName": [None]})).status is RuleStatus.FAIL

    # CommunicationDetails forbidden in OfficerDetails -> FAIL
    assert evaluator.evaluate(r35, dict(valid_officer, **{f"{SIGNATURE}/ipcdo:OfficerDetails/ccdo:CommunicationDetails": [{}]})).status is RuleStatus.FAIL
