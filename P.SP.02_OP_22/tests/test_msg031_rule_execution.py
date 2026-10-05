from pathlib import Path

import pytest

from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import RuleStatus, StructuredRuleEvaluator


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.031"

APP = "ipcdo:TrademarkApplicationDetails"
APP_STATUS = f"{APP}/ipcdo:IPEntityStatusDetails"
APP_PARTY = f"{APP}/ipcdo:IPPartyDetails"
APP_ADDRESS = f"{APP_PARTY}/ccdo:SubjectAddressDetails"
APP_COMM = f"{APP_PARTY}/ccdo:CommunicationDetails"
APP_AUTH = f"{APP}/ipcdo:PatentAuthorityDetails"
APP_CORR_ADDRESS = f"{APP}/ipcdo:CorrespondenceAddressDetails/ccdo:SubjectAddressDetails"
APP_TM = f"{APP}/ipcdo:TrademarkDetails"
APP_GOODS = f"{APP}/ipcdo:GoodsBaseDetails"
APP_SIG = f"{APP}/ipcdo:SignatureDetails"
APP_OFFICER = f"{APP_SIG}/ipcdo:OfficerDetails"
APP_RESOURCE = "ccdo:ResourceItemStatusDetails"

R007 = "ipcdo:UnifiedRegisterRecordsDetails"
R007_STATUS = f"{R007}/ipcdo:IPEntityStatusDetails"
R007_PARTY = f"{R007}/ipcdo:IPPartyDetails"
R007_ADDRESS = f"{R007_PARTY}/ccdo:SubjectAddressDetails"
R007_COMM = f"{R007_PARTY}/ccdo:CommunicationDetails"
R007_AUTH = f"{R007}/ipcdo:PatentAuthorityDetails"
R007_TM = f"{R007}/ipcdo:TrademarkDetails"
R007_DESC = f"{R007_TM}/ipcdo:TMDescriptionDetails"
R007_GOODS = f"{R007}/ipcdo:GoodsBaseDetails"
R007_RESOURCE = f"{R007}/ccdo:ResourceItemStatusDetails"
R007_SIG = f"{R007}/ipcdo:SignatureDetails"
R007_OFFICER = f"{R007_SIG}/ipcdo:OfficerDetails"


def _engine():
    return EaeuXmlEngine.load_process(PACKAGE)


def _rules(engine, table, code):
    rule_id = f"{MESSAGE}.T{table}.REQ.{code}"
    rules = [rule for rule in engine.rules[MESSAGE].structured_rules if rule["rule_id"] == rule_id]
    assert rules, rule_id
    return rules


def _assert_requirement_fails(engine, table, code, values):
    statuses = [
        StructuredRuleEvaluator().evaluate(rule, values).status
        for rule in _rules(engine, table, code)
    ]
    assert RuleStatus.FAIL in statuses, (table, code, statuses)


T48_INVALID = [
    (1, {APP: [None]}),
    (3, {APP: [None], f"{APP}/ipsdo:IPDocKindCode": "CODE", f"{APP}/ipsdo:IPDocKindName": "NAME"}),
    (4, {APP: [None], f"{APP}/ipsdo:IPDocKindName": "WRONG"}),
    (5, {APP_STATUS: [None], f"{APP_STATUS}/csdo:EventDate": "2026-09-30", f"{APP_STATUS}/csdo:StatusCode": "01"}),
    (6, {APP: [None]}),
    (7, {f"{APP_PARTY}/csdo:UnifiedCountryCode": "RU", f"{APP_PARTY}/csdo:UnifiedCountryCode/@codeListId": "WRONG"}),
    (8, {
        APP_ADDRESS: [None],
        f"{APP_ADDRESS}/csdo:AddressKindCode": "2",
        f"{APP_ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{APP_ADDRESS}/csdo:StreetName": "Street",
        f"{APP_ADDRESS}/csdo:BuildingNumberId": "1",
    }),
    (9, {APP_COMM: [None], f"{APP_COMM}/csdo:CommunicationChannelCode": "EM"}),
    (10, {APP_COMM: [None], f"{APP_COMM}/csdo:CommunicationChannelCode": "XX"}),
    (11, {APP_AUTH: [None]}),
    (12, {APP_AUTH: [None], f"{APP_AUTH}/csdo:UnifiedCountryCode": "RU"}),
    (14, {APP_PARTY: [None], f"{APP_PARTY}/ipsdo:IPPartyKindCode": "RE"}),
    (15, {APP_PARTY: [None], f"{APP_PARTY}/ipsdo:IPPartyKindCode": "AP"}),
    (21, {APP_PARTY: [None], f"{APP_PARTY}/ipsdo:IPPartyKindCode": "PA"}),
    (22, {APP_PARTY: [None], f"{APP_PARTY}/ipsdo:IPPartyKindCode": "RE"}),
    (23, {APP_CORR_ADDRESS: [None], f"{APP_CORR_ADDRESS}/csdo:AddressKindCode": "2"}),
    (24, {APP_CORR_ADDRESS: [None], f"{APP_CORR_ADDRESS}/csdo:UnifiedCountryCode": "US"}),
    (25, {APP: [None]}),
    (27, {APP_TM: [None], f"{APP_TM}/ipsdo:TrademarkKindCode": "140"}),
    (28, {APP_TM: [None], f"{APP_TM}/ipsdo:CollectiveMarkIndicator": "2"}),
    (29, {APP: [None]}),
    (31, {APP: [None]}),
    (33, {APP_RESOURCE: [None]}),
    (34, {APP: [None]}),
    (35, {APP_SIG: [None], f"{APP_SIG}/ccdo:FullNameDetails": [""], f"{APP_SIG}/ipcdo:OfficerDetails": [""]}),
    (36, {APP_OFFICER: [None]}),
]

T49_INVALID = [
    (1, {R007: [None]}),
    (2, {R007: [None]}),
    (3, {R007: [None]}),
    (4, {R007: [None], f"{R007}/ipsdo:IPDocKindCode": "CODE", f"{R007}/ipsdo:IPDocKindName": "NAME"}),
    (5, {R007: [None]}),
    (6, {f"{R007_PARTY}/csdo:UnifiedCountryCode": "RU", f"{R007_PARTY}/csdo:UnifiedCountryCode/@codeListId": "WRONG"}),
    (7, {
        R007_ADDRESS: [None],
        f"{R007_ADDRESS}/csdo:AddressKindCode": "2",
        f"{R007_ADDRESS}/csdo:UnifiedCountryCode": "RU",
        f"{R007_ADDRESS}/csdo:StreetName": "Street",
        f"{R007_ADDRESS}/csdo:BuildingNumberId": "1",
    }),
    (8, {R007_COMM: [None], f"{R007_COMM}/csdo:CommunicationChannelCode": "EM"}),
    (9, {R007_COMM: [None], f"{R007_COMM}/csdo:CommunicationChannelCode": "XX"}),
    (10, {
        R007_AUTH: [None],
        f"{R007_AUTH}/csdo:UnifiedCountryCode": "RU",
        f"{R007_AUTH}/csdo:AuthorityName": "Office",
    }),
    (11, {R007_PARTY: [None], f"{R007_PARTY}/ipsdo:IPPartyKindCode": "UE"}),
    (12, {
        R007_PARTY: [None],
        f"{R007_PARTY}/csdo:UnifiedCountryCode": "RU",
        f"{R007_PARTY}/ipsdo:IPSubjectName": "Holder",
        f"{R007_PARTY}/ccdo:SubjectAddressDetails": [None],
    }),
    (13, {R007_ADDRESS: [None], f"{R007_ADDRESS}/csdo:AddressKindCode": "3"}),
    (14, {R007_TM: [None], f"{R007_TM}/ipsdo:TrademarkPicture": "QUJD"}),
    (15, {R007_DESC: [None], f"{R007_DESC}/csdo:DescriptionText": "Description"}),
    (16, {R007: [None]}),
    (17, {R007_GOODS: [None], f"{R007_GOODS}/ipsdo:TrademarkId": "TM-1"}),
    (20, {R007_STATUS: [None], f"{R007_STATUS}/csdo:EventDate": "2026-09-30", f"{R007_STATUS}/csdo:StatusCode": "20"}),
    (21, {R007_RESOURCE: [None]}),
    (22, {R007: [None]}),
    (23, {R007_SIG: [None], f"{R007_SIG}/ccdo:FullNameDetails": [""], f"{R007_SIG}/ipcdo:OfficerDetails": [""]}),
    (24, {R007_OFFICER: [None]}),
]


@pytest.mark.parametrize(("code", "values"), T48_INVALID, ids=lambda value: str(value) if isinstance(value, int) else None)
def test_each_executable_table48_requirement_has_an_independent_negative_proof(code, values):
    _assert_requirement_fails(_engine(), 48, code, values)


@pytest.mark.parametrize(("code", "values"), T49_INVALID, ids=lambda value: str(value) if isinstance(value, int) else None)
def test_each_executable_table49_requirement_has_an_independent_negative_proof(code, values):
    _assert_requirement_fails(_engine(), 49, code, values)
