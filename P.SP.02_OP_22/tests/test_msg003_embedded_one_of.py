from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


PACKAGE = Path(__file__).resolve().parents[1]
MESSAGE = "P.SP.02.MSG.003"


def _sample_value(field):
    datatype = (field.datatype or "").lower()
    if "indicatortype" in datatype:
        return True
    if "datetimetype" in datatype:
        return "2026-09-18T12:00:00+03:00"
    if datatype.endswith("datetype"):
        return "2026-09-18"
    if "quantity" in datatype or "integer" in datatype:
        return 1
    return "TEST"


def _minimal_values(structure):
    fields_by_id = {field.field_id: field for field in structure.fields}
    included: set[str] = set()
    children = {field.parent for field in structure.fields if field.parent}
    values = {}
    for field in sorted(structure.fields, key=lambda item: item.order):
        if not field.min_occurs:
            continue
        if field.parent and field.parent not in included:
            continue
        included.add(field.field_id)
        if field.kind == "ATTRIBUTE" or field.field_id not in children:
            values[field.path] = _sample_value(field)
        else:
            values[field.path] = None
    return values


def _embedded_values(structure_id, structure):
    values = _minimal_values(structure)
    if structure_id == "R.IP.SP.02.002":
        app = "ipcdo:TrademarkApplicationDetails"
        trademark = f"{app}/ipcdo:TrademarkDetails"
        goods = f"{app}/ipcdo:GoodsBaseDetails"
        values[trademark] = None
        values[f"{trademark}/ipcdo:TMDescriptionDetails"] = None
        values[f"{trademark}/ipcdo:TMDescriptionDetails/csdo:DescriptionText"] = "TEST"
        values[f"{trademark}/ipsdo:TrademarkKindCode"] = "110"
        values[f"{trademark}/ipsdo:TrademarkKindName"] = "TEST"
        values[f"{trademark}/ipsdo:CollectiveMarkIndicator"] = "1"
        values[goods] = None
        values[f"{goods}/ipsdo:GoodsClassCode"] = "01"
        values[f"{goods}/ipsdo:GoodsClassName"] = "TEST"
        values[f"{goods}/ipsdo:GoodsName"] = "TEST"
        values[f"{goods}/ipsdo:TrademarkApplicationId"] = "APP-001"
        values[f"{goods}/ipsdo:TrademarkRegRefusalReasonText"] = "TEST"
        values["ipcdo:RefusalDetails"] = None
        values["ipcdo:RefusalDetails/csdo:EventDate"] = "2026-09-18"
        values["ipcdo:RefusalDetails/csdo:DescriptionText"] = "TEST"
        values["ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails"] = None
        values[
            "ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:EndDateTime"
        ] = "2026-09-18T12:00:00+03:00"
    elif structure_id == "R.IP.SP.02.007":
        root = "ipcdo:UnifiedRegisterRecordsDetails"
        party = f"{root}/ipcdo:IPPartyDetails"
        address = f"{party}/ccdo:SubjectAddressDetails"
        communication = f"{party}/ccdo:CommunicationDetails"
        goods = f"{root}/ipcdo:GoodsBaseDetails"
        validity = f"{root}/ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails"
        values.update({
            f"{root}/ipsdo:RegistrationDate": "2026-09-18",
            f"{root}/csdo:DocValidityDate": "2027-09-18",
            f"{root}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
            f"{root}/ipsdo:TrademarkId": "2026/RU-000001",
            party: None,
            f"{party}/ipsdo:IPPartyKindCode": "RH",
            f"{party}/csdo:UnifiedCountryCode": "RU",
            f"{party}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{party}/ipsdo:IPSubjectName": "Правообладатель",
            address: None,
            f"{address}/csdo:AddressKindCode": "2",
            f"{address}/csdo:UnifiedCountryCode": "RU",
            f"{address}/csdo:UnifiedCountryCode/@codeListId": "ВОИС ST.3",
            f"{address}/csdo:CityName": "Москва",
            f"{address}/csdo:StreetName": "Тестовая",
            f"{address}/csdo:BuildingNumberId": "1",
            communication: None,
            f"{communication}/csdo:CommunicationChannelCode": "EM",
            f"{communication}/csdo:CommunicationChannelId": "test@example.test",
            goods: None,
            f"{goods}/ipsdo:GoodsClassName": "Класс 01",
            f"{goods}/ipsdo:GoodsName": "Товар",
            f"{goods}/ipsdo:TrademarkDecisionIndicator": True,
            f"{goods}/ipsdo:TrademarkApplicationId": "2026/RU-000001",
            validity: None,
            f"{validity}/csdo:StartDateTime": "2026-09-18T12:00:00+03:00",
        })
    return values


@pytest.mark.parametrize("embedded_structure_id", ["R.IP.SP.02.002", "R.IP.SP.02.007"])
def test_msg003_build_serialize_validate_for_each_embedded_variant(embedded_structure_id):
    engine = EaeuXmlEngine.load_process(PACKAGE)
    container = engine.get_structure(MESSAGE, mode=GenerationMode.TEST)
    embedded = engine.resolve_structure(embedded_structure_id, mode=GenerationMode.TEST).definition
    body = engine.build_body(
        MESSAGE,
        _minimal_values(container),
        mode=GenerationMode.TEST,
        embedded_structure_id=embedded_structure_id,
        embedded_values=_embedded_values(embedded_structure_id, embedded),
    )
    serialized = ET.tostring(body.serialize_xml_element(), encoding="utf-8")
    root = ET.fromstring(serialized)
    payload = list(root)[-1]
    assert payload.tag == f"{{{embedded.namespace}}}{embedded.root_element}"

    values = _minimal_values(container)
    values["*"] = payload
    result = engine.validate_body(MESSAGE, values, mode=GenerationMode.TEST)
    assert result.is_valid, [(issue.code, issue.field_path, issue.message) for issue in result.issues]
