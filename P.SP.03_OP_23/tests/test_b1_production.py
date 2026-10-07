from copy import deepcopy
import base64
from pathlib import Path
import re
from xml.etree import ElementTree as ET

import pytest

from eaeu_xml.application import EaeuXmlApplication
from eaeu_xml.presentation.controller import GuiController
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.engine import EaeuXmlEngine


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "P.SP.03_OP_23"
MESSAGES = tuple(f"P.SP.03.MSG.{number:03}" for number in (1, 3, 5, 9, 10, 12))
FORBIDDEN = {
    41: ("ipcdo", "ApellationOfOriginNationalRegistrationDetails"),
    42: ("ipcdo", "AccompanyingDocumentsDetails"),
    43: ("ipsdo", "ConsentToDataProcessingIndicator"),
    44: ("ipcdo", "SignatureDetails"),
}
CASES = [(message, 41) for message in MESSAGES] + [
    (message, req) for message in MESSAGES[:3] for req in (42, 43, 44)
]


def _validate_xml(message: str, xml: str):
    engine = EaeuXmlEngine.load_process(PACKAGE)
    envelope = ET.fromstring(xml)
    body = next(child for child in envelope if child.tag.endswith("}Body"))
    document = next(iter(body))
    structure = engine.get_structure(message, mode=GenerationMode.TEST)
    values, extraction_issues = engine.body_provider._values_from_element(structure, document)
    assert not extraction_issues
    return engine.validate_body(message, values, mode=GenerationMode.TEST)


def _validate_document(message: str, document: ET.Element):
    engine = EaeuXmlEngine.load_process(PACKAGE)
    structure = engine.get_structure(message, mode=GenerationMode.TEST)
    values, extraction_issues = engine.body_provider._values_from_element(structure, document)
    assert not extraction_issues
    return engine.validate_body(message, values, mode=GenerationMode.TEST)


def _raw_generated_document(message: str):
    application = EaeuXmlApplication(ROOT)
    engine = EaeuXmlEngine.load_process(PACKAGE)
    transaction_code = next(
        transaction.transaction_code
        for transaction in application.list_transactions("P.SP.03")
        if any(
            item.message_code == message
            for item in application.list_messages("P.SP.03", transaction.transaction_code)
        )
    )
    values = application.generate_test_data("P.SP.03", transaction_code, message, seed=2303)
    body = engine.build_body(message, values, mode=GenerationMode.TEST)
    return ET.fromstring(ET.tostring(body.serialize_xml_element()))


def _generated_document(message: str):
    document = _raw_generated_document(message)
    validation = _validate_document(message, document)
    assert validation.is_valid, [(issue.code, issue.rule_id) for issue in validation.issues]
    return document


def _positive_document(message: str):
    if message in {
        "P.SP.03.MSG.001",
        "P.SP.03.MSG.003",
        "P.SP.03.MSG.005",
        "P.SP.03.MSG.009",
        "P.SP.03.MSG.010",
        "P.SP.03.MSG.012",
    }:
        envelope = ET.fromstring(_positive_xml(message))
        body = next(element for element in envelope if element.tag.endswith("}Body"))
        return deepcopy(next(iter(body)))
    return _generated_document(message)


def _direct_child(parent: ET.Element, local_name: str):
    return next((element for element in parent if element.tag.endswith("}" + local_name)), None)


def _ensure_child(parent: ET.Element, namespace: str, local_name: str, text: str | None = None):
    child = _direct_child(parent, local_name)
    if child is None:
        child = ET.SubElement(parent, f"{{{namespace}}}{local_name}")
    if text is not None:
        child.text = text
    return child


def _normalise_address(address: ET.Element, namespaces, kind: str | None = None):
    if kind is not None:
        _ensure_child(address, namespaces["csdo"], "AddressKindCode", kind)
    else:
        address_kind = _direct_child(address, "AddressKindCode")
        if address_kind is None:
            _ensure_child(address, namespaces["csdo"], "AddressKindCode", "2")
    country = _ensure_child(address, namespaces["csdo"], "UnifiedCountryCode", "RU")
    country.set("codeListId", "ВОИС ST.3")
    _ensure_child(address, namespaces["csdo"], "CityName", "Москва")
    _ensure_child(address, namespaces["csdo"], "StreetName", "Тестовая")
    _ensure_child(address, namespaces["csdo"], "BuildingNumberId", "1")


def _normalise_communication(communication: ET.Element, namespaces):
    for child in list(communication):
        if child.tag.endswith("}CommunicationChannelName"):
            communication.remove(child)
    _ensure_child(communication, namespaces["csdo"], "CommunicationChannelCode", "TE")
    _ensure_child(communication, namespaces["csdo"], "CommunicationChannelId", "+70000000000")


def _normalise_application_for_common_rules(application: ET.Element, namespaces):
    authority = _direct_child(application, "PatentAuthorityDetails")
    if authority is not None:
        country = _ensure_child(authority, namespaces["csdo"], "UnifiedCountryCode", "RU")
        country.set("codeListId", "ВОИС ST.3")
        _ensure_child(authority, namespaces["csdo"], "AuthorityName", "Роспатент")
        _ensure_child(authority, namespaces["ipsdo"], "OriginOfficeIndicator", "1")
        address = _direct_child(authority, "SubjectAddressDetails")
        if address is None:
            address = ET.SubElement(authority, f"{{{namespaces['ccdo']}}}SubjectAddressDetails")
        _normalise_address(address, namespaces, "2")

    parties = [element for element in application if element.tag.endswith("}IPPartyDetails")]
    if parties:
        party = parties[0]
        for extra in parties[1:]:
            application.remove(extra)
        _ensure_child(party, namespaces["ipsdo"], "IPPartyKindCode", "AP")
        country = _ensure_child(party, namespaces["csdo"], "UnifiedCountryCode", "RU")
        country.set("codeListId", "ВОИС ST.3")
        names = [element for element in party if element.tag.endswith("}IPSubjectName")]
        if names:
            subject = names[0]
            for extra in names[1:]:
                party.remove(extra)
        else:
            subject = ET.SubElement(party, f"{{{namespaces['ipsdo']}}}IPSubjectName")
        subject.text = "Заявитель"
        subject.set("nameRepresentationKindCode", "OR")
        subject.set("languageCode", "RU")
        addresses = [element for element in party if element.tag.endswith("}SubjectAddressDetails")]
        if addresses:
            address = addresses[0]
            for extra in addresses[1:]:
                party.remove(extra)
        else:
            address = ET.SubElement(party, f"{{{namespaces['ccdo']}}}SubjectAddressDetails")
        _normalise_address(address, namespaces, "2")
        communications = [element for element in party if element.tag.endswith("}CommunicationDetails")]
        if communications:
            communication = communications[0]
            for extra in communications[1:]:
                party.remove(extra)
        else:
            communication = ET.SubElement(party, f"{{{namespaces['ccdo']}}}CommunicationDetails")
        _normalise_communication(communication, namespaces)

    correspondence = _direct_child(application, "CorrespondenceAddressDetails")
    if correspondence is not None:
        _ensure_child(correspondence, namespaces["csdo"], "SubjectName", "Заявитель")
        addresses = [element for element in correspondence if element.tag.endswith("}SubjectAddressDetails")]
        if addresses:
            address = addresses[0]
            for extra in addresses[1:]:
                correspondence.remove(extra)
        else:
            address = ET.SubElement(correspondence, f"{{{namespaces['ccdo']}}}SubjectAddressDetails")
        _normalise_address(address, namespaces, "3")
        communications = [element for element in correspondence if element.tag.endswith("}CommunicationDetails")]
        if communications:
            communication = communications[0]
            for extra in communications[1:]:
                correspondence.remove(extra)
        else:
            communication = ET.SubElement(correspondence, f"{{{namespaces['ccdo']}}}CommunicationDetails")
        _normalise_communication(communication, namespaces)

    for origin in [element for element in application if element.tag.endswith("}ApellationOfOriginDetails")]:
        application.remove(origin)

    for address in [element for element in application.iter() if element.tag.endswith("}SubjectAddressDetails")]:
        _normalise_address(address, namespaces)
    for communication in [element for element in application.iter() if element.tag.endswith("}CommunicationDetails")]:
        _normalise_communication(communication, namespaces)


def _normalise_submission_signature_and_attachment(application: ET.Element, namespaces):
    signatures = [element for element in application if element.tag.endswith("}SignatureDetails")]
    if signatures:
        signature = signatures[0]
        for extra in signatures[1:]:
            application.remove(extra)
    else:
        signature = ET.SubElement(application, f"{{{namespaces['ipcdo']}}}SignatureDetails")
    for officer in [element for element in signature if element.tag.endswith("}OfficerDetails")]:
        signature.remove(officer)
    _ensure_child(signature, namespaces["csdo"], "DocCreationDate", "2026-10-06")
    full_name = _direct_child(signature, "FullNameDetails")
    if full_name is None:
        full_name = ET.SubElement(signature, f"{{{namespaces['ccdo']}}}FullNameDetails")
    _ensure_child(full_name, namespaces["csdo"], "LastName", "Тестов")
    _ensure_child(full_name, namespaces["csdo"], "FirstName", "Тест")

    attachments = [element for element in application if element.tag.endswith("}AccompanyingDocumentsDetails")]
    if attachments:
        attachment = attachments[0]
        for extra in attachments[1:]:
            application.remove(extra)
    else:
        attachment = ET.SubElement(application, f"{{{namespaces['ipcdo']}}}AccompanyingDocumentsDetails")
    for child in list(attachment):
        if child.tag.endswith("}DocBinaryText") or child.tag.endswith("}IPDocKindName"):
            attachment.remove(child)
    _ensure_child(attachment, namespaces["ipsdo"], "IPDocKindCode", "05999")
    _ensure_child(attachment, namespaces["csdo"], "PageQuantity", "1")
    _ensure_child(attachment, namespaces["csdo"], "DocName", "Прилагаемый документ")


def _positive_xml(message):
    controller = GuiController(EaeuXmlApplication(ROOT), test_seed=2303)
    controller.select_process("P.SP.03")
    controller.select_transaction("P.SP.03.TRN.001")
    controller.select_message("P.SP.03.MSG.001")
    controller.apply_test_data()
    generated = controller.generate_xml()
    assert generated.success

    envelope = ET.fromstring(generated.xml)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    applications = [element for element in envelope.iter() if element.tag.endswith("}ApellationOfOriginApplicationDetails")]
    submission_messages = {"P.SP.03.MSG.009", "P.SP.03.MSG.010", "P.SP.03.MSG.012"}
    for application in applications:
        _normalise_application_for_common_rules(application, namespaces)
        if message in submission_messages:
            _normalise_submission_signature_and_attachment(application, namespaces)
            _ensure_child(application, namespaces["ipsdo"], "ConsentToDataProcessingIndicator", "1")
    if message in {
        "P.SP.03.MSG.003",
        "P.SP.03.MSG.005",
        "P.SP.03.MSG.010",
        "P.SP.03.MSG.012",
    }:
        body = next(element for element in envelope if element.tag.endswith("}Body"))
        document = next(iter(body))
        old = next(element for element in document if element.tag.endswith("}ApellationOfOriginApplicationDetails"))
        new = deepcopy(old)
        document.append(new)
        old_period = next(element for element in old.iter() if element.tag.endswith("}ValidityPeriodDetails"))
        old_start = next(element for element in old_period if element.tag.endswith("}StartDateTime"))
        old_start.text = "2026-10-06T10:00:00+03:00"
        ET.SubElement(old_period, f"{{{namespaces['csdo']}}}EndDateTime").text = "2026-10-06T11:00:00+03:00"
        new_start = next(element for element in new.iter() if element.tag.endswith("}StartDateTime"))
        new_start.text = "2026-10-06T12:00:00+03:00"
    envelope_code = next(element for element in envelope.iter() if element.tag.endswith("}InfEnvelopeCode"))
    envelope_code.text = message
    return ET.tostring(envelope, encoding="unicode")


def _msg021_positive_document():
    message = "P.SP.03.MSG.021"
    application = EaeuXmlApplication(ROOT)
    engine = EaeuXmlEngine.load_process(PACKAGE)
    transaction_code = next(
        transaction.transaction_code
        for transaction in application.list_transactions("P.SP.03")
        if any(
            item.message_code == message
            for item in application.list_messages("P.SP.03", transaction.transaction_code)
        )
    )
    values = application.generate_test_data("P.SP.03", transaction_code, message, seed=2303)
    body = engine.build_body(message, values, mode=GenerationMode.TEST)
    document = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    namespaces = engine.get_structure(message, mode=GenerationMode.TEST).imported_namespaces

    authority = ET.SubElement(document, f"{{{namespaces['ipcdo']}}}PatentAuthorityDetails")
    country = ET.SubElement(authority, f"{{{namespaces['csdo']}}}UnifiedCountryCode")
    country.text = "RU"
    country.set("codeListId", "ВОИС ST.3")
    ET.SubElement(authority, f"{{{namespaces['csdo']}}}AuthorityName").text = "Роспатент"
    address = ET.SubElement(authority, f"{{{namespaces['ccdo']}}}SubjectAddressDetails")
    ET.SubElement(address, f"{{{namespaces['csdo']}}}AddressKindCode").text = "2"
    ET.SubElement(authority, f"{{{namespaces['ipsdo']}}}OriginOfficeIndicator").text = "1"
    if not any(element.tag.endswith("}ApellationOfOriginApplicationId") for element in document):
        ET.SubElement(document, f"{{{namespaces['ipsdo']}}}ApellationOfOriginApplicationId").text = "2026/RU-000001"
    return document


def _msg022_positive_document():
    message = "P.SP.03.MSG.022"
    application = EaeuXmlApplication(ROOT)
    engine = EaeuXmlEngine.load_process(PACKAGE)
    transaction_code = next(
        transaction.transaction_code
        for transaction in application.list_transactions("P.SP.03")
        if any(
            item.message_code == message
            for item in application.list_messages("P.SP.03", transaction.transaction_code)
        )
    )
    values = application.generate_test_data("P.SP.03", transaction_code, message, seed=2303)
    body = engine.build_body(message, values, mode=GenerationMode.TEST)
    document = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    namespaces = engine.get_structure(message, mode=GenerationMode.TEST).imported_namespaces

    authority = next((element for element in document if element.tag.endswith("}PatentAuthorityDetails")), None)
    if authority is None:
        authority = ET.SubElement(document, f"{{{namespaces['ipcdo']}}}PatentAuthorityDetails")
    country = next((element for element in authority if element.tag.endswith("}UnifiedCountryCode")), None)
    if country is None:
        country = ET.SubElement(authority, f"{{{namespaces['csdo']}}}UnifiedCountryCode")
    country.text = "RU"
    country.set("codeListId", "ВОИС ST.3")
    if not any(element.tag.endswith("}AuthorityName") for element in authority):
        ET.SubElement(authority, f"{{{namespaces['csdo']}}}AuthorityName").text = "Роспатент"
    address = next((element for element in authority if element.tag.endswith("}SubjectAddressDetails")), None)
    if address is None:
        address = ET.SubElement(authority, f"{{{namespaces['ccdo']}}}SubjectAddressDetails")
    address_kind = next((element for element in address if element.tag.endswith("}AddressKindCode")), None)
    if address_kind is None:
        address_kind = ET.SubElement(address, f"{{{namespaces['csdo']}}}AddressKindCode")
    address_kind.text = "2"
    indicator = next((element for element in authority if element.tag.endswith("}OriginOfficeIndicator")), None)
    if indicator is None:
        indicator = ET.SubElement(authority, f"{{{namespaces['ipsdo']}}}OriginOfficeIndicator")
    indicator.text = "1"
    if not any(element.tag.endswith("}ApellationOfOriginApplicationId") for element in document):
        ET.SubElement(document, f"{{{namespaces['ipsdo']}}}ApellationOfOriginApplicationId").text = "2026/RU-000001"
    return document


def _msg023_positive_document():
    message = "P.SP.03.MSG.023"
    application = EaeuXmlApplication(ROOT)
    engine = EaeuXmlEngine.load_process(PACKAGE)
    transaction_code = next(
        transaction.transaction_code
        for transaction in application.list_transactions("P.SP.03")
        if any(
            item.message_code == message
            for item in application.list_messages("P.SP.03", transaction.transaction_code)
        )
    )
    values = application.generate_test_data("P.SP.03", transaction_code, message, seed=2303)
    body = engine.build_body(message, values, mode=GenerationMode.TEST)
    document = ET.fromstring(ET.tostring(body.serialize_xml_element()))
    namespaces = engine.get_structure(message, mode=GenerationMode.TEST).imported_namespaces

    for element in list(document):
        if element.tag.endswith(("}PatentAuthorityDetails", "}IPPaymentDetails")):
            document.remove(element)
        elif element.tag.endswith(("}TrademarkApplicationId", "}DocId", "}PaymentAmount", "}DutyPaymentIndicator")):
            document.remove(element)

    authority = ET.SubElement(document, f"{{{namespaces['ipcdo']}}}PatentAuthorityDetails")
    country = ET.SubElement(authority, f"{{{namespaces['csdo']}}}UnifiedCountryCode")
    country.text = "RU"
    country.set("codeListId", "ВОИС ST.3")
    ET.SubElement(authority, f"{{{namespaces['csdo']}}}AuthorityName").text = "Роспатент"
    address = ET.SubElement(authority, f"{{{namespaces['ccdo']}}}SubjectAddressDetails")
    ET.SubElement(address, f"{{{namespaces['csdo']}}}AddressKindCode").text = "2"
    ET.SubElement(authority, f"{{{namespaces['ipsdo']}}}OriginOfficeIndicator").text = "1"
    if not any(element.tag.endswith("}ApellationOfOriginApplicationId") for element in document):
        ET.SubElement(document, f"{{{namespaces['ipsdo']}}}ApellationOfOriginApplicationId").text = "2026/RU-000001"

    payment = ET.SubElement(document, f"{{{namespaces['ipcdo']}}}IPPaymentDetails")
    ET.SubElement(payment, f"{{{namespaces['csdo']}}}EventDateTime").text = "2026-10-06T10:00:00+03:00"
    party = ET.SubElement(payment, f"{{{namespaces['ipcdo']}}}IPPartyDetails")
    ET.SubElement(party, f"{{{namespaces['ipsdo']}}}IPPartyKindCode").text = "AP"
    party_country = ET.SubElement(party, f"{{{namespaces['csdo']}}}UnifiedCountryCode")
    party_country.text = "RU"
    party_country.set("codeListId", "ВОИС ST.3")
    subject = ET.SubElement(party, f"{{{namespaces['ipsdo']}}}IPSubjectName")
    subject.text = "Заявитель"
    subject.set("nameRepresentationKindCode", "OR")
    subject.set("languageCode", "RU")

    accompanying = ET.SubElement(payment, f"{{{namespaces['ipcdo']}}}AccompanyingDocumentsDetails")
    ET.SubElement(accompanying, f"{{{namespaces['ipsdo']}}}IPDocKindCode").text = "07015"
    ET.SubElement(accompanying, f"{{{namespaces['csdo']}}}DocId").text = "DOC-023"
    ET.SubElement(accompanying, f"{{{namespaces['csdo']}}}DocCreationDate").text = "2026-10-06"
    binary = ET.SubElement(accompanying, f"{{{namespaces['csdo']}}}DocBinaryText")
    binary.text = base64.b64encode(b"test document").decode("ascii")
    binary.set("mediaTypeCode", "pdf")
    return document


def _msg023_set_party_kind(document, kind):
    party = next(element for element in document.iter() if element.tag.endswith("}IPPartyDetails"))
    kind_element = next(element for element in party if element.tag.endswith("}IPPartyKindCode"))
    kind_element.text = kind
    subject = next(element for element in party if element.tag.endswith("}IPSubjectName"))
    if kind in {"PA", "RE"}:
        subject.attrib.pop("nameRepresentationKindCode", None)
        subject.set("languageCode", "RU")
    return party, subject


def _msg024_positive_document():
    message = "P.SP.03.MSG.024"
    document = deepcopy(_msg023_positive_document())
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    envelope_code = next(element for element in document.iter() if element.tag.endswith("}InfEnvelopeCode"))
    envelope_code.text = message
    for element in list(document):
        if element.tag.endswith(("}DutyPaymentIndicator", "}PaymentAmount")):
            document.remove(element)
    ET.SubElement(document, f"{{{namespaces['ipsdo']}}}DutyPaymentIndicator").text = "true"
    amount = ET.SubElement(document, f"{{{namespaces['csdo']}}}PaymentAmount")
    amount.text = "0.00"
    amount.set("currencyCode", "RUB")
    return document


@pytest.mark.parametrize("message, req", CASES)
def test_forbidden_field_real_xml_positive_and_negative(message, req):
    rule = f"{message}.REQ.{req:03}"
    positive_xml = _positive_xml(message)
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    envelope = ET.fromstring(positive_xml)
    application = next(element for element in envelope.iter() if element.tag.endswith("}ApellationOfOriginApplicationDetails"))
    prefix, local_name = FORBIDDEN[req]
    namespace = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST).imported_namespaces[prefix]
    forbidden = ET.SubElement(application, f"{{{namespace}}}{local_name}")
    if req == 44:
        csdo = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST).imported_namespaces["csdo"]
        ET.SubElement(forbidden, f"{{{csdo}}}DocCreationDate").text = "2026-10-06"
    negatives = [ET.tostring(envelope, encoding="unicode")]
    if req == 43:
        expanded = re.sub(
            r"<(?P<tag>[^<> ]*ConsentToDataProcessingIndicator)\s*/>",
            lambda match: f"<{match['tag']}></{match['tag']}>", negatives[0], count=1,
        )
        assert expanded != negatives[0]
        negatives.append(expanded)
        forbidden.text = "1"
        negatives.append(ET.tostring(envelope, encoding="unicode"))
    for negative_xml in negatives:
        negative = _validate_xml(message, negative_xml)
        assert not negative.is_valid
        assert any(issue.code == "STRUCTURED_RULE_FAILED" and issue.rule_id == rule for issue in negative.issues)
        assert all(issue.rule_id == rule for issue in negative.issues)


@pytest.mark.parametrize("message, req", [("P.SP.03.MSG.001", 46), ("P.SP.03.MSG.009", 52)])
def test_end_datetime_forbidden_real_xml(message, req):
    rule = f"{message}.REQ.{req:03}"
    positive_xml = _positive_xml(message)
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    envelope = ET.fromstring(positive_xml)
    resource = next(element for element in envelope.iter() if element.tag.endswith("}ResourceItemStatusDetails"))
    namespaces = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST).imported_namespaces
    period = next(element for element in resource if element.tag.endswith("}ValidityPeriodDetails"))
    ET.SubElement(period, f"{{{namespaces['csdo']}}}EndDateTime").text = "2026-10-07T10:00:00+03:00"
    negative = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg018_req002_both_forbidden_fields_real_xml():
    message = "P.SP.03.MSG.018"
    controller = GuiController(EaeuXmlApplication(ROOT), test_seed=2303)
    controller.select_process("P.SP.03")
    controller.select_transaction("P.SP.03.TRN.009")
    controller.select_message(message)
    controller.apply_test_data()
    controller.set_values({**controller.values, "csdo:UpdateDateTime": "2026-10-06T10:00:00+03:00"})
    generated = controller.generate_xml()
    assert generated.success

    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    envelope = ET.fromstring(generated.xml)
    body = next(element for element in envelope if element.tag.endswith("}Body"))
    document = next(iter(body))
    positive_xml = ET.tostring(envelope, encoding="unicode")
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    rules = {f"{message}.REQ.001", f"{message}.REQ.002.application_id", f"{message}.REQ.002.accompanying_document"}
    assert {evaluation.rule_id for evaluation in positive.rule_evaluations} == rules
    assert all(evaluation.status.value == "PASS" for evaluation in positive.rule_evaluations)

    missing_date = ET.fromstring(positive_xml)
    missing_body = next(element for element in missing_date if element.tag.endswith("}Body"))
    missing_document = next(iter(missing_body))
    update = next(element for element in missing_document if element.tag.endswith("}UpdateDateTime"))
    missing_document.remove(update)
    missing = _validate_xml(message, ET.tostring(missing_date, encoding="unicode"))
    assert not missing.is_valid
    assert [(issue.code, issue.rule_id) for issue in missing.issues] == [
        ("STRUCTURED_RULE_FAILED", f"{message}.REQ.001")
    ]

    for prefix, local_name, suffix, value in (
        ("ipsdo", "ApellationOfOriginApplicationId", "application_id", "APP-018"),
        ("ipcdo", "AccompanyingDocumentsDetails", "accompanying_document", None),
    ):
        variant = ET.fromstring(positive_xml)
        variant_body = next(element for element in variant if element.tag.endswith("}Body"))
        variant_document = next(iter(variant_body))
        ET.SubElement(variant_document, f"{{{structure.imported_namespaces[prefix]}}}{local_name}").text = value
        negative = _validate_xml(message, ET.tostring(variant, encoding="unicode"))
        assert not negative.is_valid
        assert [(issue.code, issue.rule_id) for issue in negative.issues] == [
            ("STRUCTURED_RULE_FAILED", f"{message}.REQ.002.{suffix}")
        ]


def test_msg025_req001_both_forbidden_fields_real_xml():
    message = "P.SP.03.MSG.025"
    controller = GuiController(EaeuXmlApplication(ROOT), test_seed=2303)
    controller.select_process("P.SP.03")
    controller.select_transaction("P.SP.03.TRN.019")
    controller.select_message(message)
    controller.apply_test_data()
    generated = controller.generate_xml()
    assert generated.success

    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    envelope = ET.fromstring(generated.xml)
    body = next(element for element in envelope if element.tag.endswith("}Body"))
    document = next(iter(body))
    assert any(element.tag.endswith("}AccompanyingDocumentsDetails") for element in document)
    positive_xml = ET.tostring(envelope, encoding="unicode")
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    assert all(evaluation.status.value == "PASS" for evaluation in positive.rule_evaluations)

    for local_name, suffix, value in (
        ("UpdateDateTime", "update_datetime", "2026-10-06T10:00:00+03:00"),
        ("UnifiedCountryCode", "country_code", "RU"),
    ):
        variant = ET.fromstring(positive_xml)
        variant_body = next(element for element in variant if element.tag.endswith("}Body"))
        variant_document = next(iter(variant_body))
        forbidden = ET.SubElement(variant_document, f"{{{structure.imported_namespaces['csdo']}}}{local_name}")
        forbidden.text = value
        if suffix == "country_code":
            forbidden.set("codeListId", "ВОИС ST.3")
        negative = _validate_xml(message, ET.tostring(variant, encoding="unicode"))
        assert not negative.is_valid
        assert [(issue.code, issue.rule_id) for issue in negative.issues] == [
            ("STRUCTURED_RULE_FAILED", f"{message}.REQ.001.{suffix}")
        ]


def test_msg001_req001_exactly_one_application_real_xml():
    message = "P.SP.03.MSG.001"
    rule = f"{message}.REQ.001"
    positive_xml = _positive_xml(message)
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    envelope = ET.fromstring(positive_xml)
    body = next(element for element in envelope if element.tag.endswith("}Body"))
    document = next(iter(body))
    application = next(element for element in document if element.tag.endswith("}ApellationOfOriginApplicationDetails"))
    duplicate = deepcopy(application)
    duplicate_party = next(element for element in duplicate.iter() if element.tag.endswith("}IPPartyDetails"))
    duplicate_kind = next(element for element in duplicate_party if element.tag.endswith("}IPPartyKindCode"))
    duplicate_kind.text = "PA"
    duplicate_address = next(element for element in duplicate_party if element.tag.endswith("}SubjectAddressDetails"))
    next(element for element in duplicate_address if element.tag.endswith("}AddressKindCode")).text = "1"
    duplicate_name = next(element for element in duplicate_party if element.tag.endswith("}IPSubjectName"))
    duplicate_name.attrib.pop("nameRepresentationKindCode", None)
    duplicate_name.set("languageCode", "RU")
    namespaces = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST).imported_namespaces
    ET.SubElement(duplicate_party, f"{{{namespaces['ipsdo']}}}PatentAttorneyId").text = "PA-001"
    document.append(duplicate)
    negative = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
    assert not negative.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [
        (issue.code, issue.rule_id) for issue in negative.issues
    ]


@pytest.mark.parametrize("message", ["P.SP.03.MSG.001", "P.SP.03.MSG.009"])
def test_req009_all_country_code_attributes_real_xml(message):
    rule = f"{message}.REQ.009"
    envelope = ET.fromstring(_positive_xml(message))
    authority = next(element for element in envelope.iter() if element.tag.endswith("}PatentAuthorityDetails"))
    country = next(element for element in authority if element.tag.endswith("}UnifiedCountryCode"))
    country.text = "RU"
    country.set("codeListId", "ВОИС ST.3")
    positive_xml = ET.tostring(envelope, encoding="unicode")
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    country.set("codeListId", "OTHER")
    negative = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


@pytest.mark.parametrize("message, req, local_name", [
    ("P.SP.03.MSG.001", 45, "StartDateTime"),
    ("P.SP.03.MSG.009", 51, "StartDateTime"),
    ("P.SP.03.MSG.009", 42, "ConsentToDataProcessingIndicator"),
])
def test_required_application_field_real_xml(message, req, local_name):
    rule = f"{message}.REQ.{req:03}"
    positive_xml = _positive_xml(message)
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    envelope = ET.fromstring(positive_xml)
    target = next(element for element in envelope.iter() if element.tag.endswith("}" + local_name))
    parent = next(element for element in envelope.iter() if target in element)
    parent.remove(target)
    negative = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


@pytest.mark.parametrize("message", ["P.SP.03.MSG.001", "P.SP.03.MSG.009"])
@pytest.mark.parametrize("req, local_name", [
    (10, "DocId"),
    (11, "IPDocReceiptDate"),
    (12, "ApplicationReceiptDate"),
    (13, "ApellationOfOriginApplicationId"),
])
def test_required_application_identifiers_real_xml(message, req, local_name):
    rule = f"{message}.REQ.{req:03}"
    positive_xml = _positive_xml(message)
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    envelope = ET.fromstring(positive_xml)
    application = next(element for element in envelope.iter() if element.tag.endswith("}ApellationOfOriginApplicationDetails"))
    target = next(element for element in application if element.tag.endswith("}" + local_name))
    application.remove(target)
    negative = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg001_req010_required_doc_id_rejects_empty_element_real_xml():
    message = "P.SP.03.MSG.001"
    rule = f"{message}.REQ.010"
    envelope = ET.fromstring(_positive_xml(message))
    application = next(element for element in envelope.iter() if element.tag.endswith("}ApellationOfOriginApplicationDetails"))
    target = next(element for element in application if element.tag.endswith("}DocId"))
    target.text = None

    negative = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg025_req005_accompanying_document_required_real_xml():
    message = "P.SP.03.MSG.025"
    rule = f"{message}.REQ.005"
    controller = GuiController(EaeuXmlApplication(ROOT), test_seed=2303)
    controller.select_process("P.SP.03")
    controller.select_transaction("P.SP.03.TRN.019")
    controller.select_message(message)
    controller.apply_test_data()
    generated = controller.generate_xml()
    assert generated.success
    positive = _validate_xml(message, generated.xml)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    envelope = ET.fromstring(generated.xml)
    target = next(element for element in envelope.iter() if element.tag.endswith("}AccompanyingDocumentsDetails"))
    parent = next(element for element in envelope.iter() if target in element)
    parent.remove(target)
    negative = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg001_req018_exactly_one_applicant_real_xml():
    message = "P.SP.03.MSG.001"
    rule = f"{message}.REQ.018"
    positive_xml = _positive_xml(message)
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    envelope = ET.fromstring(positive_xml)
    application = next(element for element in envelope.iter() if element.tag.endswith("}ApellationOfOriginApplicationDetails"))
    party = next(element for element in application if element.tag.endswith("}IPPartyDetails"))
    application.append(deepcopy(party))
    negative = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def _msg001_positive_document():
    envelope = ET.fromstring(_positive_xml("P.SP.03.MSG.001"))
    body = next(element for element in envelope if element.tag.endswith("}Body"))
    return deepcopy(next(iter(body)))


def _assert_msg001_rule_passes(document: ET.Element, rule_id: str):
    result = _validate_document("P.SP.03.MSG.001", document)
    assert result.is_valid, [(issue.code, issue.rule_id) for issue in result.issues]
    assert any(
        evaluation.rule_id == rule_id and evaluation.status.value == "PASS"
        for evaluation in result.rule_evaluations
    )


def _assert_msg001_rule_fails(document: ET.Element, rule_id: str):
    result = _validate_document("P.SP.03.MSG.001", document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule_id) in [
        (issue.code, issue.rule_id) for issue in result.issues
    ]


def _append_msg001_representative(document: ET.Element, kind: str):
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure("P.SP.03.MSG.001", mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    application = next(element for element in document if element.tag.endswith("}ApellationOfOriginApplicationDetails"))
    party = ET.SubElement(application, f"{{{namespaces['ipcdo']}}}IPPartyDetails")
    ET.SubElement(party, f"{{{namespaces['ipsdo']}}}IPPartyKindCode").text = kind
    country = ET.SubElement(party, f"{{{namespaces['csdo']}}}UnifiedCountryCode")
    country.text = "RU"
    country.set("codeListId", "ВОИС ST.3")
    subject = ET.SubElement(party, f"{{{namespaces['ipsdo']}}}IPSubjectName")
    subject.text = "Представитель"
    subject.set("languageCode", "RU")
    address = ET.SubElement(party, f"{{{namespaces['ccdo']}}}SubjectAddressDetails")
    _normalise_address(address, namespaces, "1")
    communication = ET.SubElement(party, f"{{{namespaces['ccdo']}}}CommunicationDetails")
    _normalise_communication(communication, namespaces)
    if kind == "PA":
        ET.SubElement(party, f"{{{namespaces['ipsdo']}}}PatentAttorneyId").text = "PA-001"
    return party


@pytest.mark.parametrize("missing", [
    "AddressKindCode",
    "UnifiedCountryCode",
    "CityName",
    "StreetName",
    "BuildingNumberId",
])
def test_msg001_req006_every_address_has_required_fields_real_xml(missing):
    rule = "P.SP.03.MSG.001.REQ.006"
    document = _msg001_positive_document()
    _assert_msg001_rule_passes(document, rule)
    correspondence = next(element for element in document.iter() if element.tag.endswith("}CorrespondenceAddressDetails"))
    address = next(element for element in correspondence if element.tag.endswith("}SubjectAddressDetails"))
    target = next(element for element in address if element.tag.endswith("}" + missing))
    address.remove(target)
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req007_every_communication_has_required_shape_real_xml():
    rule = "P.SP.03.MSG.001.REQ.007"
    document = _msg001_positive_document()
    _assert_msg001_rule_passes(document, rule)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure("P.SP.03.MSG.001", mode=GenerationMode.TEST)
    communication = next(element for element in document.iter() if element.tag.endswith("}CommunicationDetails"))
    ET.SubElement(
        communication,
        f"{{{structure.imported_namespaces['csdo']}}}CommunicationChannelName",
    ).text = "Телефон"
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req008_communication_channel_allowlist_real_xml():
    rule = "P.SP.03.MSG.001.REQ.008"
    document = _msg001_positive_document()
    _assert_msg001_rule_passes(document, rule)
    code = next(element for element in document.iter() if element.tag.endswith("}CommunicationChannelCode"))
    code.text = "XX"
    _assert_msg001_rule_fails(document, rule)


@pytest.mark.parametrize("req, mutation", [
    (14, "authority_name"),
    (15, "origin_indicator"),
    (16, "authority_address_kind"),
])
def test_msg001_req014_016_patent_authority_real_xml(req, mutation):
    rule = f"P.SP.03.MSG.001.REQ.{req:03}"
    document = _msg001_positive_document()
    _assert_msg001_rule_passes(document, rule)
    authority = next(element for element in document.iter() if element.tag.endswith("}PatentAuthorityDetails"))
    if mutation == "authority_name":
        target = next(element for element in authority if element.tag.endswith("}AuthorityName"))
        authority.remove(target)
    elif mutation == "origin_indicator":
        next(element for element in authority if element.tag.endswith("}OriginOfficeIndicator")).text = "0"
    else:
        address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "1"
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req017_party_kind_allowlist_real_xml():
    rule = "P.SP.03.MSG.001.REQ.017"
    document = _msg001_positive_document()
    _assert_msg001_rule_passes(document, rule)
    party = _append_msg001_representative(document, "RE")
    next(element for element in party if element.tag.endswith("}IPPartyKindCode")).text = "XX"
    _assert_msg001_rule_fails(document, rule)


@pytest.mark.parametrize("missing", [
    "UnifiedCountryCode",
    "IPSubjectName",
    "SubjectAddressDetails",
    "CommunicationDetails",
])
def test_msg001_req019_applicant_required_fields_real_xml(missing):
    rule = "P.SP.03.MSG.001.REQ.019"
    document = _msg001_positive_document()
    _assert_msg001_rule_passes(document, rule)
    application = next(element for element in document if element.tag.endswith("}ApellationOfOriginApplicationDetails"))
    party = next(element for element in application if element.tag.endswith("}IPPartyDetails"))
    target = next(element for element in party if element.tag.endswith("}" + missing))
    party.remove(target)
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req020_applicant_name_representation_allowlist_real_xml():
    rule = "P.SP.03.MSG.001.REQ.020"
    document = _msg001_positive_document()
    _assert_msg001_rule_passes(document, rule)
    subject = next(element for element in document.iter() if element.tag.endswith("}IPSubjectName"))
    subject.set("nameRepresentationKindCode", "XX")
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req021_exactly_one_original_name_and_language_real_xml():
    document = _msg001_positive_document()
    cardinality_rule = "P.SP.03.MSG.001.REQ.021.or_cardinality"
    language_rule = "P.SP.03.MSG.001.REQ.021.or_language"
    _assert_msg001_rule_passes(document, cardinality_rule)
    _assert_msg001_rule_passes(document, language_rule)
    subject = next(element for element in document.iter() if element.tag.endswith("}IPSubjectName"))
    subject.attrib.pop("languageCode")
    _assert_msg001_rule_fails(document, language_rule)


def test_msg001_req022_russian_original_forbids_second_name_real_xml():
    rule = "P.SP.03.MSG.001.REQ.022"
    document = _msg001_positive_document()
    _assert_msg001_rule_passes(document, rule)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure("P.SP.03.MSG.001", mode=GenerationMode.TEST)
    party = next(element for element in document.iter() if element.tag.endswith("}IPPartyDetails"))
    second = ET.SubElement(party, f"{{{structure.imported_namespaces['ipsdo']}}}IPSubjectName")
    second.text = "Applicant"
    second.set("nameRepresentationKindCode", "LA")
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req023_non_russian_original_requires_latin_name_real_xml():
    rule = "P.SP.03.MSG.001.REQ.023"
    document = _msg001_positive_document()
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure("P.SP.03.MSG.001", mode=GenerationMode.TEST)
    party = next(element for element in document.iter() if element.tag.endswith("}IPPartyDetails"))
    original = next(element for element in party if element.tag.endswith("}IPSubjectName"))
    original.set("languageCode", "EN")
    latin = ET.SubElement(party, f"{{{structure.imported_namespaces['ipsdo']}}}IPSubjectName")
    latin.text = "Applicant"
    latin.set("nameRepresentationKindCode", "LA")
    _assert_msg001_rule_passes(document, rule)
    party.remove(latin)
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req024_applicant_address_kind_real_xml():
    rule = "P.SP.03.MSG.001.REQ.024"
    document = _msg001_positive_document()
    _assert_msg001_rule_passes(document, rule)
    application = next(element for element in document if element.tag.endswith("}ApellationOfOriginApplicationDetails"))
    party = next(element for element in application if element.tag.endswith("}IPPartyDetails"))
    address = next(element for element in party if element.tag.endswith("}SubjectAddressDetails"))
    next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "1"
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req025_patent_attorney_required_fields_real_xml():
    rule = "P.SP.03.MSG.001.REQ.025"
    document = _msg001_positive_document()
    party = _append_msg001_representative(document, "PA")
    _assert_msg001_rule_passes(document, rule)
    attorney = next(element for element in party if element.tag.endswith("}PatentAttorneyId"))
    party.remove(attorney)
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req026_representative_required_fields_real_xml():
    rule = "P.SP.03.MSG.001.REQ.026"
    document = _msg001_positive_document()
    party = _append_msg001_representative(document, "RE")
    _assert_msg001_rule_passes(document, rule)
    communication = next(element for element in party if element.tag.endswith("}CommunicationDetails"))
    party.remove(communication)
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req027_representative_address_kind_real_xml():
    rule = "P.SP.03.MSG.001.REQ.027"
    document = _msg001_positive_document()
    party = _append_msg001_representative(document, "RE")
    _assert_msg001_rule_passes(document, rule)
    address = next(element for element in party if element.tag.endswith("}SubjectAddressDetails"))
    next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "2"
    _assert_msg001_rule_fails(document, rule)


@pytest.mark.parametrize("scope, rule", [
    ("party", "P.SP.03.MSG.001.REQ.028.party_country"),
    ("address", "P.SP.03.MSG.001.REQ.028.address_country"),
])
def test_msg001_req028_representative_country_allowlist_real_xml(scope, rule):
    document = _msg001_positive_document()
    party = _append_msg001_representative(document, "RE")
    _assert_msg001_rule_passes(document, rule)
    if scope == "party":
        country = next(element for element in party if element.tag.endswith("}UnifiedCountryCode"))
    else:
        address = next(element for element in party if element.tag.endswith("}SubjectAddressDetails"))
        country = next(element for element in address if element.tag.endswith("}UnifiedCountryCode"))
    country.text = "US"
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req029_representative_name_attributes_real_xml():
    rule = "P.SP.03.MSG.001.REQ.029"
    document = _msg001_positive_document()
    party = _append_msg001_representative(document, "RE")
    _assert_msg001_rule_passes(document, rule)
    subject = next(element for element in party if element.tag.endswith("}IPSubjectName"))
    subject.set("nameRepresentationKindCode", "OR")
    _assert_msg001_rule_fails(document, rule)


@pytest.mark.parametrize("req, mutation", [
    (30, "subject_name"),
    (31, "address_kind"),
    (32, "country"),
])
def test_msg001_req030_032_correspondence_address_real_xml(req, mutation):
    rule = f"P.SP.03.MSG.001.REQ.{req:03}"
    document = _msg001_positive_document()
    _assert_msg001_rule_passes(document, rule)
    correspondence = next(element for element in document.iter() if element.tag.endswith("}CorrespondenceAddressDetails"))
    address = next(element for element in correspondence if element.tag.endswith("}SubjectAddressDetails"))
    if mutation == "subject_name":
        target = next(element for element in correspondence if element.tag.endswith("}SubjectName"))
        correspondence.remove(target)
    elif mutation == "address_kind":
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "2"
    else:
        next(element for element in address if element.tag.endswith("}UnifiedCountryCode")).text = "US"
    _assert_msg001_rule_fails(document, rule)


def _append_msg001_origin(document: ET.Element):
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure("P.SP.03.MSG.001", mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    application = next(element for element in document if element.tag.endswith("}ApellationOfOriginApplicationDetails"))
    origin = ET.SubElement(application, f"{{{namespaces['ipcdo']}}}ApellationOfOriginDetails")
    name = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}ApellationOfOriginName")
    name.text = "Тестовое НМПТ"
    name.set("nameRepresentationKindCode", "OR")
    name.set("languageCode", "RU")
    properties = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}GoodsPropertiesDescriptionText")
    properties.text = "Особые свойства товара"
    return origin


def test_msg001_req035_origin_name_representation_allowlist_real_xml():
    rule = "P.SP.03.MSG.001.REQ.035"
    document = _msg001_positive_document()
    origin = _append_msg001_origin(document)
    _assert_msg001_rule_passes(document, rule)
    name = next(element for element in origin if element.tag.endswith("}ApellationOfOriginName"))
    name.set("nameRepresentationKindCode", "LA")
    _assert_msg001_rule_fails(document, rule)


def test_msg001_req036_exactly_one_original_origin_name_real_xml():
    cardinality_rule = "P.SP.03.MSG.001.REQ.036.or_cardinality"
    language_rule = "P.SP.03.MSG.001.REQ.036.or_language"
    document = _msg001_positive_document()
    origin = _append_msg001_origin(document)
    _assert_msg001_rule_passes(document, cardinality_rule)
    _assert_msg001_rule_passes(document, language_rule)
    name = next(element for element in origin if element.tag.endswith("}ApellationOfOriginName"))
    name.attrib.pop("languageCode")
    _assert_msg001_rule_fails(document, language_rule)


def test_msg001_req037_additional_origin_names_have_no_language_real_xml():
    rule = "P.SP.03.MSG.001.REQ.037"
    document = _msg001_positive_document()
    origin = _append_msg001_origin(document)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure("P.SP.03.MSG.001", mode=GenerationMode.TEST)
    additional = ET.SubElement(origin, f"{{{structure.imported_namespaces['ipsdo']}}}ApellationOfOriginName")
    additional.text = "ТЕСТОВОЕ НМПТ"
    additional.set("nameRepresentationKindCode", "CY")
    _assert_msg001_rule_passes(document, rule)
    additional.set("languageCode", "RU")
    _assert_msg001_rule_fails(document, rule)


@pytest.mark.parametrize("attribute", ["featureKindCode", "featureName"])
def test_msg001_req038_goods_properties_attributes_forbidden_real_xml(attribute):
    rule = "P.SP.03.MSG.001.REQ.038"
    document = _msg001_positive_document()
    origin = _append_msg001_origin(document)
    _assert_msg001_rule_passes(document, rule)
    properties = next(element for element in origin if element.tag.endswith("}GoodsPropertiesDescriptionText"))
    properties.set(attribute, "TEST")
    _assert_msg001_rule_fails(document, rule)


@pytest.mark.parametrize("local_name", ["UnifiedCountryCode", "RegistrationDate", "PublicationDate"])
def test_msg001_req040_origin_fields_forbidden_real_xml(local_name):
    rule = "P.SP.03.MSG.001.REQ.040"
    document = _msg001_positive_document()
    origin = _append_msg001_origin(document)
    _assert_msg001_rule_passes(document, rule)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure("P.SP.03.MSG.001", mode=GenerationMode.TEST)
    namespace = structure.imported_namespaces["csdo" if local_name == "UnifiedCountryCode" else "ipsdo"]
    target = ET.SubElement(origin, f"{{{namespace}}}{local_name}")
    target.text = "RU" if local_name == "UnifiedCountryCode" else "2026-10-06"
    if local_name == "UnifiedCountryCode":
        target.set("codeListId", "ВОИС ST.3")
    _assert_msg001_rule_fails(document, rule)


INHERITED_APPLICATION_MESSAGES = ("P.SP.03.MSG.003", "P.SP.03.MSG.005")
TABLE18_CHANGE_MESSAGES = ("P.SP.03.MSG.010", "P.SP.03.MSG.012")
TWO_APPLICATION_MESSAGES = INHERITED_APPLICATION_MESSAGES + TABLE18_CHANGE_MESSAGES


def _inherited_application_document(message: str):
    envelope = ET.fromstring(_positive_xml(message))
    body = next(element for element in envelope if element.tag.endswith("}Body"))
    return deepcopy(next(iter(body)))


def _application_instances(document: ET.Element):
    return [
        element
        for element in document
        if element.tag.endswith("}ApellationOfOriginApplicationDetails")
    ]


def _assert_rule_passes(message: str, document: ET.Element, rule_id: str):
    result = _validate_document(message, document)
    assert result.is_valid, [(issue.code, issue.rule_id) for issue in result.issues]
    assert any(
        evaluation.rule_id == rule_id and evaluation.status.value == "PASS"
        for evaluation in result.rule_evaluations
    )


def _assert_rule_fails(message: str, document: ET.Element, rule_id: str):
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule_id) in [
        (issue.code, issue.rule_id) for issue in result.issues
    ]


def _append_representative(message: str, application: ET.Element, kind: str):
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    party = ET.SubElement(application, f"{{{namespaces['ipcdo']}}}IPPartyDetails")
    ET.SubElement(party, f"{{{namespaces['ipsdo']}}}IPPartyKindCode").text = kind
    country = ET.SubElement(party, f"{{{namespaces['csdo']}}}UnifiedCountryCode")
    country.text = "RU"
    country.set("codeListId", "ВОИС ST.3")
    subject = ET.SubElement(party, f"{{{namespaces['ipsdo']}}}IPSubjectName")
    subject.text = "Представитель"
    subject.set("languageCode", "RU")
    address = ET.SubElement(party, f"{{{namespaces['ccdo']}}}SubjectAddressDetails")
    _normalise_address(address, namespaces, "1")
    communication = ET.SubElement(party, f"{{{namespaces['ccdo']}}}CommunicationDetails")
    _normalise_communication(communication, namespaces)
    if kind == "PA":
        ET.SubElement(party, f"{{{namespaces['ipsdo']}}}PatentAttorneyId").text = "PA-001"
    return party


def _append_origin(message: str, application: ET.Element):
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    origin = ET.SubElement(application, f"{{{namespaces['ipcdo']}}}ApellationOfOriginDetails")
    name = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}ApellationOfOriginName")
    name.text = "Тестовое НМПТ"
    name.set("nameRepresentationKindCode", "OR")
    name.set("languageCode", "RU")
    properties = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}GoodsPropertiesDescriptionText")
    properties.text = "Особые свойства товара"
    return origin


def _msg011_document():
    message = "P.SP.03.MSG.011"
    document = _raw_generated_document(message)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    item = next(element for element in document if element.tag.endswith("}ApellationOfOriginRegisterItemDetails"))
    authority = _ensure_child(item, namespaces["ipcdo"], "PatentAuthorityDetails")
    country = _ensure_child(authority, namespaces["csdo"], "UnifiedCountryCode", "RU")
    country.set("codeListId", "ВОИС ST.3")
    _ensure_child(authority, namespaces["csdo"], "AuthorityName", "Роспатент")
    _ensure_child(authority, namespaces["ipsdo"], "OriginOfficeIndicator", "1")
    address = _ensure_child(authority, namespaces["ccdo"], "SubjectAddressDetails")
    _normalise_address(address, namespaces, "2")
    resource = _ensure_child(item, namespaces["ccdo"], "ResourceItemStatusDetails")
    period = _ensure_child(resource, namespaces["ccdo"], "ValidityPeriodDetails")
    _ensure_child(period, namespaces["csdo"], "StartDateTime", "2026-10-06T10:00:00+03:00")
    end = _direct_child(period, "EndDateTime")
    if end is not None:
        period.remove(end)
    return document


def _msg011_parts(document: ET.Element):
    item = next(element for element in document if element.tag.endswith("}ApellationOfOriginRegisterItemDetails"))
    authority = next(element for element in item if element.tag.endswith("}PatentAuthorityDetails"))
    resource = next(element for element in item if element.tag.endswith("}ResourceItemStatusDetails"))
    return item, authority, resource


def _append_msg011_attachment(item: ET.Element):
    message = "P.SP.03.MSG.011"
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    attachment = ET.SubElement(item, f"{{{namespaces['ipcdo']}}}AccompanyingDocumentsDetails")
    _ensure_child(attachment, namespaces["ipsdo"], "IPDocKindCode", "05999")
    _ensure_child(attachment, namespaces["csdo"], "DocName", "Документ")
    _ensure_child(attachment, namespaces["csdo"], "PageQuantity", "1")
    return attachment


def _append_msg011_communication(item: ET.Element):
    message = "P.SP.03.MSG.011"
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    correspondence = ET.SubElement(item, f"{{{namespaces['ipcdo']}}}CorrespondenceAddressDetails")
    communication = ET.SubElement(correspondence, f"{{{namespaces['ccdo']}}}CommunicationDetails")
    _normalise_communication(communication, namespaces)
    return communication


def _register_rule_document(message: str, *, require_attachment: bool = False):
    if message == "P.SP.03.MSG.013":
        return _two_register_document(message)
    document = _raw_generated_document(message)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    item = next(element for element in document if element.tag.endswith("}ApellationOfOriginRegisterItemDetails"))
    authority = _ensure_child(item, namespaces["ipcdo"], "PatentAuthorityDetails")
    country = _ensure_child(authority, namespaces["csdo"], "UnifiedCountryCode", "RU")
    country.set("codeListId", "ВОИС ST.3")
    _ensure_child(authority, namespaces["csdo"], "AuthorityName", "Роспатент")
    _ensure_child(authority, namespaces["ipsdo"], "OriginOfficeIndicator", "1")
    address = _ensure_child(authority, namespaces["ccdo"], "SubjectAddressDetails")
    _normalise_address(address, namespaces, "2")
    resource = _ensure_child(item, namespaces["ccdo"], "ResourceItemStatusDetails")
    period = _ensure_child(resource, namespaces["ccdo"], "ValidityPeriodDetails")
    _ensure_child(period, namespaces["csdo"], "StartDateTime", "2026-10-06T10:00:00+03:00")
    end = _direct_child(period, "EndDateTime")
    if end is not None:
        period.remove(end)
    for attachment in [element for element in item if element.tag.endswith("}AccompanyingDocumentsDetails")]:
        item.remove(attachment)
    if require_attachment:
        _append_register_attachment(message, item)
    return document


def _append_register_attachment(message: str, item: ET.Element):
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    attachment = ET.SubElement(item, f"{{{namespaces['ipcdo']}}}AccompanyingDocumentsDetails")
    _ensure_child(attachment, namespaces["ipsdo"], "IPDocKindCode", "05999")
    _ensure_child(attachment, namespaces["csdo"], "DocName", "Документ")
    _ensure_child(attachment, namespaces["csdo"], "PageQuantity", "1")
    return attachment


def _append_register_communication(message: str, item: ET.Element):
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    correspondence = ET.SubElement(item, f"{{{namespaces['ipcdo']}}}CorrespondenceAddressDetails")
    communication = ET.SubElement(correspondence, f"{{{namespaces['ccdo']}}}CommunicationDetails")
    _normalise_communication(communication, namespaces)
    return communication


def test_msg011_req038_goods_properties_attributes_forbidden_real_xml():
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.038"
    document = _msg011_document()
    item, _, _ = _msg011_parts(document)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    origin = ET.SubElement(item, f"{{{structure.imported_namespaces['ipcdo']}}}ApellationOfOriginDetails")
    properties = ET.SubElement(origin, f"{{{structure.imported_namespaces['ipsdo']}}}GoodsPropertiesDescriptionText")
    properties.text = "Особые свойства товара"
    _assert_rule_passes(message, document, rule)
    properties.set("featureKindCode", "TEST")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("mutation", ["authority_name", "address_kind"])
def test_msg011_req039_authority_fields_and_physical_address_real_xml(mutation):
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.039"
    document = _msg011_document()
    _, authority, _ = _msg011_parts(document)
    _assert_rule_passes(message, document, rule)
    if mutation == "authority_name":
        target = next(element for element in authority if element.tag.endswith("}AuthorityName"))
        authority.remove(target)
    else:
        address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "1"
    _assert_rule_fails(message, document, rule)


def test_msg011_req040_origin_office_indicator_real_xml():
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.040"
    document = _msg011_document()
    _, authority, _ = _msg011_parts(document)
    _assert_rule_passes(message, document, rule)
    next(element for element in authority if element.tag.endswith("}OriginOfficeIndicator")).text = "0"
    _assert_rule_fails(message, document, rule)


def test_msg011_req041_address_required_members_real_xml():
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.041"
    document = _msg011_document()
    _, authority, _ = _msg011_parts(document)
    address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
    _assert_rule_passes(message, document, rule)
    target = next(element for element in address if element.tag.endswith("}CityName"))
    address.remove(target)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("mutation", ["channel_name", "channel_code"])
def test_msg011_req042_043_communication_rules_real_xml(mutation):
    message = "P.SP.03.MSG.011"
    req = 42 if mutation == "channel_name" else 43
    rule = f"{message}.REQ.{req:03}"
    document = _msg011_document()
    item, _, _ = _msg011_parts(document)
    communication = _append_msg011_communication(item)
    _assert_rule_passes(message, document, rule)
    if mutation == "channel_name":
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        ET.SubElement(
            communication,
            f"{{{structure.imported_namespaces['csdo']}}}CommunicationChannelName",
        ).text = "Телефон"
    else:
        next(element for element in communication if element.tag.endswith("}CommunicationChannelCode")).text = "XX"
    _assert_rule_fails(message, document, rule)


def test_msg011_req044_country_codelist_real_xml():
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.044"
    document = _msg011_document()
    _, authority, _ = _msg011_parts(document)
    country = next(element for element in authority if element.tag.endswith("}UnifiedCountryCode"))
    _assert_rule_passes(message, document, rule)
    country.set("codeListId", "OTHER")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("local_name, namespace_key", [("DocBinaryText", "csdo"), ("IPDocKindName", "ipsdo")])
def test_msg011_req045_attachment_fields_forbidden_real_xml(local_name, namespace_key):
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.045"
    document = _msg011_document()
    item, _, _ = _msg011_parts(document)
    attachment = _append_msg011_attachment(item)
    _assert_rule_passes(message, document, rule)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    ET.SubElement(attachment, f"{{{structure.imported_namespaces[namespace_key]}}}{local_name}").text = "TEST"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("local_name", ["IPDocKindCode", "PageQuantity"])
def test_msg011_req046_attachment_required_fields_real_xml(local_name):
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.046"
    document = _msg011_document()
    item, _, _ = _msg011_parts(document)
    attachment = _append_msg011_attachment(item)
    _assert_rule_passes(message, document, rule)
    target = next(element for element in attachment if element.tag.endswith("}" + local_name))
    attachment.remove(target)
    _assert_rule_fails(message, document, rule)


def test_msg011_req047_named_attachment_codes_require_doc_name_real_xml():
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.047"
    document = _msg011_document()
    item, _, _ = _msg011_parts(document)
    attachment = _append_msg011_attachment(item)
    _assert_rule_passes(message, document, rule)
    name = next(element for element in attachment if element.tag.endswith("}DocName"))
    attachment.remove(name)
    _assert_rule_fails(message, document, rule)


def test_msg011_req048_duplicate_attachment_codes_need_distinguishing_value_real_xml():
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.048"
    document = _msg011_document()
    item, _, _ = _msg011_parts(document)
    attachment = _append_msg011_attachment(item)
    duplicate = deepcopy(attachment)
    first_name = next(element for element in attachment if element.tag.endswith("}DocName"))
    second_name = next(element for element in duplicate if element.tag.endswith("}DocName"))
    first_name.text = "Первый документ"
    second_name.text = "Второй документ"
    item.append(duplicate)
    _assert_rule_passes(message, document, rule)
    second_name.text = first_name.text
    _assert_rule_fails(message, document, rule)


def test_msg011_req049_start_datetime_required_real_xml():
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.049"
    document = _msg011_document()
    _, _, resource = _msg011_parts(document)
    period = next(element for element in resource if element.tag.endswith("}ValidityPeriodDetails"))
    _assert_rule_passes(message, document, rule)
    start = next(element for element in period if element.tag.endswith("}StartDateTime"))
    period.remove(start)
    _assert_rule_fails(message, document, rule)


def test_msg011_req050_end_datetime_forbidden_real_xml():
    message = "P.SP.03.MSG.011"
    rule = f"{message}.REQ.050"
    document = _msg011_document()
    _, _, resource = _msg011_parts(document)
    period = next(element for element in resource if element.tag.endswith("}ValidityPeriodDetails"))
    _assert_rule_passes(message, document, rule)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    ET.SubElement(period, f"{{{structure.imported_namespaces['csdo']}}}EndDateTime").text = "2026-10-07T10:00:00+03:00"
    _assert_rule_fails(message, document, rule)


REGISTER_INHERITED_MESSAGES = ("P.SP.03.MSG.013", "P.SP.03.MSG.014")


@pytest.mark.parametrize("message", REGISTER_INHERITED_MESSAGES)
@pytest.mark.parametrize("req, mutation", [
    (25, "authority_name"),
    (26, "origin_office"),
    (27, "address_city"),
    (28, "communication_name"),
    (29, "communication_code"),
    (30, "country_codelist"),
])
def test_register_common_req025_030_real_xml(message, req, mutation):
    rule = f"{message}.REQ.{req:03}"
    document = _register_rule_document(message, require_attachment=True)
    item = next(element for element in document if element.tag.endswith("}ApellationOfOriginRegisterItemDetails"))
    authority = next(element for element in item if element.tag.endswith("}PatentAuthorityDetails"))
    communication = None
    if mutation.startswith("communication"):
        if message == "P.SP.03.MSG.013":
            communication = next(
                element
                for element in item.iter()
                if element.tag.endswith("}CommunicationDetails")
            )
        else:
            communication = _append_register_communication(message, item)
            if message == "P.SP.03.MSG.014":
                structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
                namespaces = structure.imported_namespaces
                correspondence = next(
                    element
                    for element in item
                    if element.tag.endswith("}CorrespondenceAddressDetails")
                )
                _ensure_child(correspondence, namespaces["csdo"], "SubjectName", "Получатель")
                address = _ensure_child(correspondence, namespaces["ccdo"], "SubjectAddressDetails")
                _normalise_address(address, namespaces, "3")
    _assert_rule_passes(message, document, rule)

    if mutation == "authority_name":
        authority.remove(next(element for element in authority if element.tag.endswith("}AuthorityName")))
    elif mutation == "origin_office":
        next(element for element in authority if element.tag.endswith("}OriginOfficeIndicator")).text = "0"
    elif mutation == "address_city":
        address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
        address.remove(next(element for element in address if element.tag.endswith("}CityName")))
    elif mutation == "communication_name":
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        ET.SubElement(
            communication,
            f"{{{structure.imported_namespaces['csdo']}}}CommunicationChannelName",
        ).text = "Телефон"
    elif mutation == "communication_code":
        next(element for element in communication if element.tag.endswith("}CommunicationChannelCode")).text = "XX"
    else:
        country = next(element for element in authority if element.tag.endswith("}UnifiedCountryCode"))
        country.set("codeListId", "OTHER")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", REGISTER_INHERITED_MESSAGES)
def test_register_req031_attachment_required_real_xml(message):
    rule = f"{message}.REQ.031"
    document = _register_rule_document(message, require_attachment=True)
    item = next(element for element in document if element.tag.endswith("}ApellationOfOriginRegisterItemDetails"))
    _assert_rule_passes(message, document, rule)
    if message == "P.SP.03.MSG.013":
        for register_item in _register_items(document):
            for attachment in [
                element
                for element in register_item
                if element.tag.endswith("}AccompanyingDocumentsDetails")
            ]:
                register_item.remove(attachment)
    else:
        attachment = next(element for element in item if element.tag.endswith("}AccompanyingDocumentsDetails"))
        item.remove(attachment)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", REGISTER_INHERITED_MESSAGES)
@pytest.mark.parametrize("req, mutation", [
    (32, "binary"),
    (33, "page_quantity"),
    (34, "doc_name"),
])
def test_register_req032_034_attachment_rules_real_xml(message, req, mutation):
    rule = f"{message}.REQ.{req:03}"
    document = _register_rule_document(message, require_attachment=True)
    item = next(element for element in document if element.tag.endswith("}ApellationOfOriginRegisterItemDetails"))
    attachment = next(element for element in item if element.tag.endswith("}AccompanyingDocumentsDetails"))
    _assert_rule_passes(message, document, rule)
    if mutation == "binary":
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        ET.SubElement(attachment, f"{{{structure.imported_namespaces['csdo']}}}DocBinaryText").text = "TEST"
    elif mutation == "page_quantity":
        attachment.remove(next(element for element in attachment if element.tag.endswith("}PageQuantity")))
    else:
        attachment.remove(next(element for element in attachment if element.tag.endswith("}DocName")))
    _assert_rule_fails(message, document, rule)


def test_msg013_req039_goods_properties_attributes_forbidden_real_xml():
    message = "P.SP.03.MSG.013"
    rule = f"{message}.REQ.039"
    document = _register_rule_document(message, require_attachment=True)
    item = next(element for element in document if element.tag.endswith("}ApellationOfOriginRegisterItemDetails"))
    origin = _origin_of(item)
    properties = next(
        element
        for element in origin
        if element.tag.endswith("}GoodsPropertiesDescriptionText")
    )
    _assert_rule_passes(message, document, rule)
    properties.set("featureName", "TEST")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("req, mutation", [
    (30, "binary"),
    (31, "page_quantity"),
    (32, "doc_name"),
])
def test_msg015_req030_032_attachment_rules_real_xml(req, mutation):
    message = "P.SP.03.MSG.015"
    rule = f"{message}.REQ.{req:03}"
    document = _register_rule_document(message)
    item = next(element for element in document if element.tag.endswith("}ApellationOfOriginRegisterItemDetails"))
    attachment = _append_register_attachment(message, item)
    _assert_rule_passes(message, document, rule)
    if mutation == "binary":
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        ET.SubElement(attachment, f"{{{structure.imported_namespaces['csdo']}}}DocBinaryText").text = "TEST"
    elif mutation == "page_quantity":
        attachment.remove(next(element for element in attachment if element.tag.endswith("}PageQuantity")))
    else:
        attachment.remove(next(element for element in attachment if element.tag.endswith("}DocName")))
    _assert_rule_fails(message, document, rule)


def test_msg015_req033_duplicate_attachment_codes_need_distinguishing_value_real_xml():
    message = "P.SP.03.MSG.015"
    rule = f"{message}.REQ.033"
    document = _register_rule_document(message)
    item = next(element for element in document if element.tag.endswith("}ApellationOfOriginRegisterItemDetails"))
    attachment = _append_register_attachment(message, item)
    duplicate = deepcopy(attachment)
    first_name = next(element for element in attachment if element.tag.endswith("}DocName"))
    second_name = next(element for element in duplicate if element.tag.endswith("}DocName"))
    first_name.text = "Первый документ"
    second_name.text = "Второй документ"
    item.append(duplicate)
    _assert_rule_passes(message, document, rule)
    second_name.text = first_name.text
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("req, mutation", [
    (38, "goods_attribute"),
    (39, "authority_name"),
    (40, "address_city"),
    (41, "communication_name"),
    (42, "communication_code"),
    (43, "country_codelist"),
    (44, "attachment_present"),
    (45, "origin_office"),
    (46, "start_missing"),
    (47, "end_present"),
])
def test_msg004_req038_047_common_register_rules_real_xml(req, mutation):
    message = "P.SP.03.MSG.004"
    rule = f"{message}.REQ.{req:03}"
    document = _register_rule_document(message)
    item = next(element for element in document if element.tag.endswith("}ApellationOfOriginRegisterItemDetails"))
    authority = next(element for element in item if element.tag.endswith("}PatentAuthorityDetails"))
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces

    properties = None
    communication = None
    if mutation == "goods_attribute":
        origin = ET.SubElement(item, f"{{{namespaces['ipcdo']}}}ApellationOfOriginDetails")
        properties = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}GoodsPropertiesDescriptionText")
        properties.text = "Особые свойства товара"
    elif mutation.startswith("communication"):
        communication = _append_register_communication(message, item)

    _assert_rule_passes(message, document, rule)

    if mutation == "goods_attribute":
        properties.set("featureKindCode", "TEST")
    elif mutation == "authority_name":
        authority.remove(next(element for element in authority if element.tag.endswith("}AuthorityName")))
    elif mutation == "address_city":
        address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
        address.remove(next(element for element in address if element.tag.endswith("}CityName")))
    elif mutation == "communication_name":
        ET.SubElement(communication, f"{{{namespaces['csdo']}}}CommunicationChannelName").text = "Телефон"
    elif mutation == "communication_code":
        next(element for element in communication if element.tag.endswith("}CommunicationChannelCode")).text = "XX"
    elif mutation == "country_codelist":
        next(element for element in authority if element.tag.endswith("}UnifiedCountryCode")).set("codeListId", "OTHER")
    elif mutation == "attachment_present":
        _append_register_attachment(message, item)
    elif mutation == "origin_office":
        next(element for element in authority if element.tag.endswith("}OriginOfficeIndicator")).text = "0"
    else:
        resource = next(element for element in item if element.tag.endswith("}ResourceItemStatusDetails"))
        period = next(element for element in resource if element.tag.endswith("}ValidityPeriodDetails"))
        if mutation == "start_missing":
            period.remove(next(element for element in period if element.tag.endswith("}StartDateTime")))
        else:
            ET.SubElement(period, f"{{{namespaces['csdo']}}}EndDateTime").text = "2026-10-07T10:00:00+03:00"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
def test_req001_exactly_two_application_instances_real_xml(message):
    rule = f"{message}.REQ.001.cardinality"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    document.remove(_application_instances(document)[1])
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
@pytest.mark.parametrize("suffix, local_name, replacement", [
    ("doc_id", "DocId", "DIFFERENT-DOC"),
    ("receipt_date", "IPDocReceiptDate", "2026-10-05"),
    ("application_date", "ApplicationReceiptDate", "2026-10-05"),
    ("application_id", "ApellationOfOriginApplicationId", "DIFFERENT-APP"),
])
def test_req001_required_application_values_equal_real_xml(message, suffix, local_name, replacement):
    rule = f"{message}.REQ.001.{suffix}"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    target = next(element for element in second if element.tag.endswith("}" + local_name))
    target.text = replacement
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
def test_req001_authority_country_equal_real_xml(message):
    rule = f"{message}.REQ.001.authority_country"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    authority = next(element for element in second if element.tag.endswith("}PatentAuthorityDetails"))
    country = next(element for element in authority if element.tag.endswith("}UnifiedCountryCode"))
    country.text = "AM"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
def test_req001_optional_document_name_equal_when_present_real_xml(message):
    rule = f"{message}.REQ.001.ip_doc_kind_name"
    document = _inherited_application_document(message)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    applications = _application_instances(document)
    for application in applications:
        name = _direct_child(application, "IPDocKindName")
        if name is None:
            name = ET.SubElement(application, f"{{{structure.imported_namespaces['ipsdo']}}}IPDocKindName")
        name.text = "Заявка на НМПТ Союза"
    _assert_rule_passes(message, document, rule)
    _direct_child(applications[1], "IPDocKindName").text = "Иное наименование документа"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
@pytest.mark.parametrize("suffix, local_name", [
    ("origin_name", "ApellationOfOriginName"),
    ("origin_id", "ApellationOfOriginEAEUId"),
])
def test_req001_optional_origin_values_equal_when_present_real_xml(message, suffix, local_name):
    rule = f"{message}.REQ.001.{suffix}"
    document = _inherited_application_document(message)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    applications = _application_instances(document)
    origins = [_append_origin(message, application) for application in applications]
    if local_name == "ApellationOfOriginEAEUId":
        for origin in origins:
            _ensure_child(origin, structure.imported_namespaces["ipsdo"], local_name, "AO-001")
    _assert_rule_passes(message, document, rule)
    target = next(element for element in origins[1] if element.tag.endswith("}" + local_name))
    target.text = "DIFFERENT"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
def test_req001_optional_doc_kind_code_allows_both_missing_real_xml(message):
    rule = f"{message}.REQ.001.ip_doc_kind_code"
    document = _inherited_application_document(message)
    for application in _application_instances(document):
        code = _direct_child(application, "IPDocKindCode")
        if code is not None:
            application.remove(code)
    _assert_rule_passes(message, document, rule)


def _msg009_document():
    return _inherited_application_document("P.SP.03.MSG.009")


def test_msg009_req001_exactly_one_application_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.001"
    document = _msg009_document()
    _assert_rule_passes(message, document, rule)
    application = _application_instances(document)[0]
    document.append(deepcopy(application))
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("req, mutation", [
    (6, "address_city"),
    (7, "communication_name"),
    (8, "communication_code"),
])
def test_msg009_req006_008_common_nested_rules_real_xml(req, mutation):
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.{req:03}"
    document = _msg009_document()
    _assert_rule_passes(message, document, rule)
    application = _application_instances(document)[0]
    if mutation == "address_city":
        address = next(element for element in application.iter() if element.tag.endswith("}SubjectAddressDetails"))
        target = next(element for element in address if element.tag.endswith("}CityName"))
        address.remove(target)
    elif mutation == "communication_name":
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        communication = next(element for element in application.iter() if element.tag.endswith("}CommunicationDetails"))
        ET.SubElement(communication, f"{{{structure.imported_namespaces['csdo']}}}CommunicationChannelName").text = "Телефон"
    else:
        code = next(element for element in application.iter() if element.tag.endswith("}CommunicationChannelCode"))
        code.text = "XX"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("req, mutation", [
    (14, "authority_name"),
    (15, "origin_indicator"),
    (16, "authority_address_kind"),
    (17, "party_kind"),
])
def test_msg009_req014_017_real_xml(req, mutation):
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.{req:03}"
    document = _msg009_document()
    _assert_rule_passes(message, document, rule)
    application = _application_instances(document)[0]
    authority = next(element for element in application if element.tag.endswith("}PatentAuthorityDetails"))
    party = next(element for element in application if element.tag.endswith("}IPPartyDetails"))
    if mutation == "authority_name":
        target = next(element for element in authority if element.tag.endswith("}AuthorityName"))
        authority.remove(target)
    elif mutation == "origin_indicator":
        next(element for element in authority if element.tag.endswith("}OriginOfficeIndicator")).text = "0"
    elif mutation == "authority_address_kind":
        address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "1"
    else:
        next(element for element in party if element.tag.endswith("}IPPartyKindCode")).text = "XX"
    _assert_rule_fails(message, document, rule)


def test_msg009_req018_exactly_one_applicant_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.018"
    document = _msg009_document()
    _assert_rule_passes(message, document, rule)
    application = _application_instances(document)[0]
    applicant = next(element for element in application if element.tag.endswith("}IPPartyDetails"))
    application.append(deepcopy(applicant))
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("req, mutation, suffix", [
    (19, "applicant_communication", ""),
    (20, "applicant_name_representation", ""),
    (21, "applicant_original_language", ".or_language"),
    (22, "applicant_second_name", ""),
    (24, "applicant_address_kind", ""),
])
def test_msg009_req019_024_applicant_rules_real_xml(req, mutation, suffix):
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.{req:03}{suffix}"
    document = _msg009_document()
    _assert_rule_passes(message, document, rule)
    application = _application_instances(document)[0]
    party = next(element for element in application if element.tag.endswith("}IPPartyDetails"))
    subject = next(element for element in party if element.tag.endswith("}IPSubjectName"))
    if mutation == "applicant_communication":
        target = next(element for element in party if element.tag.endswith("}CommunicationDetails"))
        party.remove(target)
    elif mutation == "applicant_name_representation":
        subject.set("nameRepresentationKindCode", "XX")
    elif mutation == "applicant_original_language":
        subject.attrib.pop("languageCode")
    elif mutation == "applicant_second_name":
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        second_name = ET.SubElement(party, f"{{{structure.imported_namespaces['ipsdo']}}}IPSubjectName")
        second_name.text = "Applicant"
        second_name.set("nameRepresentationKindCode", "LA")
    else:
        address = next(element for element in party if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "1"
    _assert_rule_fails(message, document, rule)


def test_msg009_req021_original_name_cardinality_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.021.or_cardinality"
    document = _msg009_document()
    _assert_rule_passes(message, document, rule)
    party = next(element for element in _application_instances(document)[0] if element.tag.endswith("}IPPartyDetails"))
    subject = next(element for element in party if element.tag.endswith("}IPSubjectName"))
    subject.set("nameRepresentationKindCode", "LA")
    _assert_rule_fails(message, document, rule)


def test_msg009_req023_non_russian_original_requires_latin_name_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.023"
    document = _msg009_document()
    application = _application_instances(document)[0]
    party = next(element for element in application if element.tag.endswith("}IPPartyDetails"))
    subject = next(element for element in party if element.tag.endswith("}IPSubjectName"))
    subject.set("languageCode", "EN")
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    latin = ET.SubElement(party, f"{{{structure.imported_namespaces['ipsdo']}}}IPSubjectName")
    latin.text = "Applicant"
    latin.set("nameRepresentationKindCode", "LA")
    _assert_rule_passes(message, document, rule)
    party.remove(latin)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("req, kind, mutation", [
    (25, "PA", "patent_attorney"),
    (26, "RE", "representative_communication"),
    (27, "RE", "representative_address_kind"),
    (29, "RE", "representative_name_representation"),
])
def test_msg009_req025_029_representative_rules_real_xml(req, kind, mutation):
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.{req:03}"
    document = _msg009_document()
    application = _application_instances(document)[0]
    party = _append_representative(message, application, kind)
    _assert_rule_passes(message, document, rule)
    if mutation == "patent_attorney":
        target = next(element for element in party if element.tag.endswith("}PatentAttorneyId"))
        party.remove(target)
    elif mutation == "representative_communication":
        target = next(element for element in party if element.tag.endswith("}CommunicationDetails"))
        party.remove(target)
    elif mutation == "representative_address_kind":
        address = next(element for element in party if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "2"
    else:
        subject = next(element for element in party if element.tag.endswith("}IPSubjectName"))
        subject.set("nameRepresentationKindCode", "OR")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("scope, suffix", [("party", ".party_country"), ("address", ".address_country")])
def test_msg009_req028_representative_country_allowlist_real_xml(scope, suffix):
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.028{suffix}"
    document = _msg009_document()
    application = _application_instances(document)[0]
    party = _append_representative(message, application, "RE")
    _assert_rule_passes(message, document, rule)
    if scope == "party":
        country = next(element for element in party if element.tag.endswith("}UnifiedCountryCode"))
    else:
        address = next(element for element in party if element.tag.endswith("}SubjectAddressDetails"))
        country = next(element for element in address if element.tag.endswith("}UnifiedCountryCode"))
    country.text = "US"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("req, mutation", [(30, "subject_name"), (31, "address_kind"), (32, "country")])
def test_msg009_req030_032_correspondence_real_xml(req, mutation):
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.{req:03}"
    document = _msg009_document()
    correspondence = next(element for element in document.iter() if element.tag.endswith("}CorrespondenceAddressDetails"))
    address = next(element for element in correspondence if element.tag.endswith("}SubjectAddressDetails"))
    _assert_rule_passes(message, document, rule)
    if mutation == "subject_name":
        target = next(element for element in correspondence if element.tag.endswith("}SubjectName"))
        correspondence.remove(target)
    elif mutation == "address_kind":
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "2"
    else:
        next(element for element in address if element.tag.endswith("}UnifiedCountryCode")).text = "US"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("req, mutation, suffix", [
    (35, "name_representation", ""),
    (36, "original_language", ".or_language"),
    (37, "additional_language", ""),
    (38, "feature_attribute", ""),
    (40, "forbidden_country", ""),
])
def test_msg009_req035_040_origin_rules_real_xml(req, mutation, suffix):
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.{req:03}{suffix}"
    document = _msg009_document()
    application = _application_instances(document)[0]
    origin = _append_origin(message, application)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    if mutation == "additional_language":
        additional = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}ApellationOfOriginName")
        additional.text = "ТЕСТОВОЕ НМПТ"
        additional.set("nameRepresentationKindCode", "CY")
    _assert_rule_passes(message, document, rule)
    name = next(element for element in origin if element.tag.endswith("}ApellationOfOriginName"))
    if mutation == "name_representation":
        name.set("nameRepresentationKindCode", "LA")
    elif mutation == "original_language":
        name.attrib.pop("languageCode")
    elif mutation == "additional_language":
        additional.set("languageCode", "RU")
    elif mutation == "feature_attribute":
        properties = next(element for element in origin if element.tag.endswith("}GoodsPropertiesDescriptionText"))
        properties.set("featureKindCode", "TEST")
    else:
        country = ET.SubElement(origin, f"{{{namespaces['csdo']}}}UnifiedCountryCode")
        country.text = "RU"
        country.set("codeListId", "ВОИС ST.3")
    _assert_rule_fails(message, document, rule)


def test_msg009_req036_origin_name_cardinality_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.036.or_cardinality"
    document = _msg009_document()
    origin = _append_origin(message, _application_instances(document)[0])
    _assert_rule_passes(message, document, rule)
    name = next(element for element in origin if element.tag.endswith("}ApellationOfOriginName"))
    name.set("nameRepresentationKindCode", "CY")
    _assert_rule_fails(message, document, rule)


def _msg009_signature_and_attachment(document: ET.Element):
    application = _application_instances(document)[0]
    signature = next(element for element in application if element.tag.endswith("}SignatureDetails"))
    attachment = next(element for element in application if element.tag.endswith("}AccompanyingDocumentsDetails"))
    return application, signature, attachment


def test_msg009_req043_signature_required_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.043.signature_required"
    document = _msg009_document()
    _assert_rule_passes(message, document, rule)
    application, signature, _ = _msg009_signature_and_attachment(document)
    application.remove(signature)
    _assert_rule_fails(message, document, rule)


def _replace_signature_with_officer(message: str, signature: ET.Element):
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    for full_name in [element for element in signature if element.tag.endswith("}FullNameDetails")]:
        signature.remove(full_name)
    officer = ET.SubElement(signature, f"{{{namespaces['ipcdo']}}}OfficerDetails")
    officer_name = ET.SubElement(officer, f"{{{namespaces['ccdo']}}}FullNameDetails")
    _ensure_child(officer_name, namespaces["csdo"], "LastName", "Тестов")
    _ensure_child(officer_name, namespaces["csdo"], "FirstName", "Тест")
    _ensure_child(officer, namespaces["csdo"], "PositionName", "Эксперт")
    return officer


def test_msg009_req043_officer_excludes_direct_full_name_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.043.officer_excludes_direct_name"
    document = _msg009_document()
    _, signature, _ = _msg009_signature_and_attachment(document)
    _replace_signature_with_officer(message, signature)
    _assert_rule_passes(message, document, rule)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    direct_name = ET.SubElement(signature, f"{{{structure.imported_namespaces['ccdo']}}}FullNameDetails")
    _ensure_child(direct_name, structure.imported_namespaces["csdo"], "LastName", "Тестов")
    _assert_rule_fails(message, document, rule)


def test_msg009_req044_direct_full_name_excludes_officer_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.044"
    document = _msg009_document()
    _, signature, _ = _msg009_signature_and_attachment(document)
    _assert_rule_passes(message, document, rule)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    officer = ET.SubElement(signature, f"{{{structure.imported_namespaces['ipcdo']}}}OfficerDetails")
    officer_name = ET.SubElement(officer, f"{{{structure.imported_namespaces['ccdo']}}}FullNameDetails")
    _ensure_child(officer_name, structure.imported_namespaces["csdo"], "LastName", "Тестов")
    _assert_rule_fails(message, document, rule)


def test_msg009_req045_at_least_one_attachment_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.045"
    document = _msg009_document()
    _assert_rule_passes(message, document, rule)
    application, _, attachment = _msg009_signature_and_attachment(document)
    application.remove(attachment)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("mutation", ["position", "communication"])
def test_msg009_req046_officer_required_fields_and_no_communication_real_xml(mutation):
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.046"
    document = _msg009_document()
    _, signature, _ = _msg009_signature_and_attachment(document)
    officer = _replace_signature_with_officer(message, signature)
    _assert_rule_passes(message, document, rule)
    if mutation == "position":
        position = next(element for element in officer if element.tag.endswith("}PositionName"))
        officer.remove(position)
    else:
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        communication = ET.SubElement(officer, f"{{{structure.imported_namespaces['ccdo']}}}CommunicationDetails")
        _normalise_communication(communication, structure.imported_namespaces)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("local_name, namespace_key", [("DocBinaryText", "csdo"), ("IPDocKindName", "ipsdo")])
def test_msg009_req047_attachment_fields_forbidden_real_xml(local_name, namespace_key):
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.047"
    document = _msg009_document()
    _, _, attachment = _msg009_signature_and_attachment(document)
    _assert_rule_passes(message, document, rule)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    ET.SubElement(attachment, f"{{{structure.imported_namespaces[namespace_key]}}}{local_name}").text = "TEST"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("local_name", ["IPDocKindCode", "PageQuantity"])
def test_msg009_req048_attachment_required_fields_real_xml(local_name):
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.048"
    document = _msg009_document()
    _, _, attachment = _msg009_signature_and_attachment(document)
    _assert_rule_passes(message, document, rule)
    target = next(element for element in attachment if element.tag.endswith("}" + local_name))
    attachment.remove(target)
    _assert_rule_fails(message, document, rule)


def test_msg009_req049_named_codes_require_doc_name_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.049"
    document = _msg009_document()
    _, _, attachment = _msg009_signature_and_attachment(document)
    _assert_rule_passes(message, document, rule)
    name = next(element for element in attachment if element.tag.endswith("}DocName"))
    attachment.remove(name)
    _assert_rule_fails(message, document, rule)


def test_msg009_req050_duplicate_attachment_codes_need_distinguishing_value_real_xml():
    message = "P.SP.03.MSG.009"
    rule = f"{message}.REQ.050"
    document = _msg009_document()
    application, _, attachment = _msg009_signature_and_attachment(document)
    _assert_rule_passes(message, document, rule)
    duplicate = deepcopy(attachment)
    first_name = next(element for element in attachment if element.tag.endswith("}DocName"))
    second_name = next(element for element in duplicate if element.tag.endswith("}DocName"))
    first_name.text = "Первый документ"
    second_name.text = "Второй документ"
    application.append(duplicate)
    _assert_rule_passes(message, document, rule)
    second_name.text = first_name.text
    _assert_rule_fails(message, document, rule)


def _submission_parts(document: ET.Element, application_index: int = 1):
    application = _application_instances(document)[application_index]
    signature = next(element for element in application if element.tag.endswith("}SignatureDetails"))
    attachment = next(element for element in application if element.tag.endswith("}AccompanyingDocumentsDetails"))
    return application, signature, attachment


@pytest.mark.parametrize("message", TABLE18_CHANGE_MESSAGES)
def test_table18_req041_forbidden_on_second_application_real_xml(message):
    rule = f"{message}.REQ.041"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    ET.SubElement(
        second,
        f"{{{structure.imported_namespaces['ipcdo']}}}ApellationOfOriginNationalRegistrationDetails",
    )
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TABLE18_CHANGE_MESSAGES)
def test_table18_req042_consent_required_on_each_application_real_xml(message):
    rule = f"{message}.REQ.042"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    consent = next(element for element in second if element.tag.endswith("}ConsentToDataProcessingIndicator"))
    second.remove(consent)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TABLE18_CHANGE_MESSAGES)
def test_table18_req043_signature_required_on_each_application_real_xml(message):
    rule = f"{message}.REQ.043.signature_required"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second, signature, _ = _submission_parts(document)
    second.remove(signature)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TABLE18_CHANGE_MESSAGES)
def test_table18_req044_direct_full_name_excludes_officer_real_xml(message):
    rule = f"{message}.REQ.044"
    document = _inherited_application_document(message)
    _, signature, _ = _submission_parts(document)
    _assert_rule_passes(message, document, rule)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    officer = ET.SubElement(signature, f"{{{structure.imported_namespaces['ipcdo']}}}OfficerDetails")
    officer_name = ET.SubElement(officer, f"{{{structure.imported_namespaces['ccdo']}}}FullNameDetails")
    _ensure_child(officer_name, structure.imported_namespaces["csdo"], "LastName", "Тестов")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TABLE18_CHANGE_MESSAGES)
def test_table18_req045_attachment_required_on_each_application_real_xml(message):
    rule = f"{message}.REQ.045"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second, _, attachment = _submission_parts(document)
    second.remove(attachment)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("mutation", ["position", "communication"])
def test_msg010_req046_officer_required_fields_and_no_communication_real_xml(mutation):
    message = "P.SP.03.MSG.010"
    rule = f"{message}.REQ.046"
    document = _inherited_application_document(message)
    _, signature, _ = _submission_parts(document)
    officer = _replace_signature_with_officer(message, signature)
    _assert_rule_passes(message, document, rule)
    if mutation == "position":
        position = next(element for element in officer if element.tag.endswith("}PositionName"))
        officer.remove(position)
    else:
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        communication = ET.SubElement(officer, f"{{{structure.imported_namespaces['ccdo']}}}CommunicationDetails")
        _normalise_communication(communication, structure.imported_namespaces)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize(
    "message, req, local_name, namespace_key",
    [
        ("P.SP.03.MSG.010", 47, "DocBinaryText", "csdo"),
        ("P.SP.03.MSG.010", 47, "IPDocKindName", "ipsdo"),
        ("P.SP.03.MSG.012", 46, "DocBinaryText", "csdo"),
        ("P.SP.03.MSG.012", 46, "IPDocKindName", "ipsdo"),
    ],
)
def test_change_message_attachment_fields_forbidden_real_xml(message, req, local_name, namespace_key):
    rule = f"{message}.REQ.{req:03}"
    document = _inherited_application_document(message)
    _, _, attachment = _submission_parts(document)
    _assert_rule_passes(message, document, rule)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    ET.SubElement(attachment, f"{{{structure.imported_namespaces[namespace_key]}}}{local_name}").text = "TEST"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize(
    "message, req, local_name",
    [
        ("P.SP.03.MSG.010", 48, "IPDocKindCode"),
        ("P.SP.03.MSG.010", 48, "PageQuantity"),
        ("P.SP.03.MSG.012", 47, "IPDocKindCode"),
        ("P.SP.03.MSG.012", 47, "PageQuantity"),
    ],
)
def test_change_message_attachment_required_fields_real_xml(message, req, local_name):
    rule = f"{message}.REQ.{req:03}"
    document = _inherited_application_document(message)
    _, _, attachment = _submission_parts(document)
    _assert_rule_passes(message, document, rule)
    target = next(element for element in attachment if element.tag.endswith("}" + local_name))
    attachment.remove(target)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize(
    "message, req",
    [("P.SP.03.MSG.010", 49), ("P.SP.03.MSG.012", 48)],
)
def test_change_message_named_attachment_codes_require_doc_name_real_xml(message, req):
    rule = f"{message}.REQ.{req:03}"
    document = _inherited_application_document(message)
    _, _, attachment = _submission_parts(document)
    _assert_rule_passes(message, document, rule)
    name = next(element for element in attachment if element.tag.endswith("}DocName"))
    attachment.remove(name)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize(
    "message, req",
    [("P.SP.03.MSG.010", 50), ("P.SP.03.MSG.012", 49)],
)
def test_change_message_duplicate_attachment_codes_are_scoped_per_application_real_xml(message, req):
    rule = f"{message}.REQ.{req:03}"
    document = _inherited_application_document(message)
    second, _, attachment = _submission_parts(document)

    # Both applications intentionally start with the same attachment code/name.
    # The rule must scope duplicate detection to each owning application.
    _assert_rule_passes(message, document, rule)

    duplicate = deepcopy(attachment)
    first_name = next(element for element in attachment if element.tag.endswith("}DocName"))
    second_name = next(element for element in duplicate if element.tag.endswith("}DocName"))
    first_name.text = "Первый документ"
    second_name.text = "Второй документ"
    second.append(duplicate)
    _assert_rule_passes(message, document, rule)
    second_name.text = first_name.text
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize(
    "message, req",
    [("P.SP.03.MSG.010", 51), ("P.SP.03.MSG.012", 50)],
)
def test_change_message_changed_application_end_datetime_forbidden_real_xml(message, req):
    rule = f"{message}.REQ.{req:03}"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    period = next(element for element in second.iter() if element.tag.endswith("}ValidityPeriodDetails"))
    ET.SubElement(period, f"{{{structure.imported_namespaces['csdo']}}}EndDateTime").text = "2026-10-06T13:00:00+03:00"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
@pytest.mark.parametrize("req, mutation", [
    (6, "address_city"),
    (7, "communication_name"),
    (8, "communication_code"),
    (9, "country_codelist"),
])
def test_inherited_req006_009_global_nested_rules_real_xml(message, req, mutation):
    rule = f"{message}.REQ.{req:03}"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    if mutation == "address_city":
        address = next(element for element in second.iter() if element.tag.endswith("}SubjectAddressDetails"))
        target = next(element for element in address if element.tag.endswith("}CityName"))
        address.remove(target)
    elif mutation == "communication_name":
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        communication = next(element for element in second.iter() if element.tag.endswith("}CommunicationDetails"))
        ET.SubElement(communication, f"{{{structure.imported_namespaces['csdo']}}}CommunicationChannelName").text = "Телефон"
    elif mutation == "communication_code":
        code = next(element for element in second.iter() if element.tag.endswith("}CommunicationChannelCode"))
        code.text = "XX"
    else:
        country = next(element for element in second.iter() if element.tag.endswith("}UnifiedCountryCode"))
        country.set("codeListId", "OTHER")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
@pytest.mark.parametrize("req, local_name", [
    (10, "DocId"),
    (11, "IPDocReceiptDate"),
    (12, "ApplicationReceiptDate"),
    (13, "ApellationOfOriginApplicationId"),
])
def test_inherited_req010_013_required_on_each_application_real_xml(message, req, local_name):
    rule = f"{message}.REQ.{req:03}"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    target = next(element for element in second if element.tag.endswith("}" + local_name))
    second.remove(target)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
@pytest.mark.parametrize("req, mutation", [
    (14, "authority_name"),
    (15, "origin_indicator"),
    (16, "authority_address_kind"),
    (17, "party_kind"),
])
def test_inherited_req014_017_each_application_real_xml(message, req, mutation):
    rule = f"{message}.REQ.{req:03}"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    authority = next(element for element in second if element.tag.endswith("}PatentAuthorityDetails"))
    party = next(element for element in second if element.tag.endswith("}IPPartyDetails"))
    if mutation == "authority_name":
        target = next(element for element in authority if element.tag.endswith("}AuthorityName"))
        authority.remove(target)
    elif mutation == "origin_indicator":
        next(element for element in authority if element.tag.endswith("}OriginOfficeIndicator")).text = "0"
    elif mutation == "authority_address_kind":
        address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "1"
    else:
        next(element for element in party if element.tag.endswith("}IPPartyKindCode")).text = "XX"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
def test_inherited_req018_exactly_one_applicant_per_application_real_xml(message):
    rule = f"{message}.REQ.018"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    applicant = next(element for element in second if element.tag.endswith("}IPPartyDetails"))
    second.append(deepcopy(applicant))
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
@pytest.mark.parametrize("req, mutation", [
    (19, "applicant_communication"),
    (20, "applicant_name_representation"),
    (21, "applicant_original_language"),
    (22, "applicant_second_name"),
    (24, "applicant_address_kind"),
])
def test_inherited_req019_024_applicant_rules_real_xml(message, req, mutation):
    suffix = ".or_language" if req == 21 else ""
    rule = f"{message}.REQ.{req:03}{suffix}"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    party = next(element for element in second if element.tag.endswith("}IPPartyDetails"))
    subject = next(element for element in party if element.tag.endswith("}IPSubjectName"))
    if mutation == "applicant_communication":
        target = next(element for element in party if element.tag.endswith("}CommunicationDetails"))
        party.remove(target)
    elif mutation == "applicant_name_representation":
        subject.set("nameRepresentationKindCode", "XX")
    elif mutation == "applicant_original_language":
        subject.attrib.pop("languageCode")
    elif mutation == "applicant_second_name":
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        second_name = ET.SubElement(party, f"{{{structure.imported_namespaces['ipsdo']}}}IPSubjectName")
        second_name.text = "Applicant"
        second_name.set("nameRepresentationKindCode", "LA")
    else:
        address = next(element for element in party if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "1"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
def test_inherited_req021_original_name_cardinality_real_xml(message):
    rule = f"{message}.REQ.021.or_cardinality"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    party = next(element for element in second if element.tag.endswith("}IPPartyDetails"))
    subject = next(element for element in party if element.tag.endswith("}IPSubjectName"))
    subject.set("nameRepresentationKindCode", "LA")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
def test_inherited_req023_non_russian_original_requires_latin_name_real_xml(message):
    rule = f"{message}.REQ.023"
    document = _inherited_application_document(message)
    second = _application_instances(document)[1]
    party = next(element for element in second if element.tag.endswith("}IPPartyDetails"))
    subject = next(element for element in party if element.tag.endswith("}IPSubjectName"))
    subject.set("languageCode", "EN")
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    latin = ET.SubElement(party, f"{{{structure.imported_namespaces['ipsdo']}}}IPSubjectName")
    latin.text = "Applicant"
    latin.set("nameRepresentationKindCode", "LA")
    _assert_rule_passes(message, document, rule)
    party.remove(latin)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
@pytest.mark.parametrize("req, kind, mutation", [
    (25, "PA", "patent_attorney"),
    (26, "RE", "representative_communication"),
    (27, "RE", "representative_address_kind"),
    (29, "RE", "representative_name_representation"),
])
def test_inherited_req025_029_representative_rules_real_xml(message, req, kind, mutation):
    rule = f"{message}.REQ.{req:03}"
    document = _inherited_application_document(message)
    second = _application_instances(document)[1]
    party = _append_representative(message, second, kind)
    _assert_rule_passes(message, document, rule)
    if mutation == "patent_attorney":
        target = next(element for element in party if element.tag.endswith("}PatentAttorneyId"))
        party.remove(target)
    elif mutation == "representative_communication":
        target = next(element for element in party if element.tag.endswith("}CommunicationDetails"))
        party.remove(target)
    elif mutation == "representative_address_kind":
        address = next(element for element in party if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "2"
    else:
        subject = next(element for element in party if element.tag.endswith("}IPSubjectName"))
        subject.set("nameRepresentationKindCode", "OR")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
@pytest.mark.parametrize("scope, suffix", [
    ("party", ".party_country"),
    ("address", ".address_country"),
])
def test_inherited_req028_representative_country_allowlist_real_xml(message, scope, suffix):
    rule = f"{message}.REQ.028{suffix}"
    document = _inherited_application_document(message)
    second = _application_instances(document)[1]
    party = _append_representative(message, second, "RE")
    _assert_rule_passes(message, document, rule)
    if scope == "party":
        country = next(element for element in party if element.tag.endswith("}UnifiedCountryCode"))
    else:
        address = next(element for element in party if element.tag.endswith("}SubjectAddressDetails"))
        country = next(element for element in address if element.tag.endswith("}UnifiedCountryCode"))
    country.text = "US"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
@pytest.mark.parametrize("req, mutation", [
    (30, "subject_name"),
    (31, "address_kind"),
    (32, "country"),
])
def test_inherited_req030_032_correspondence_real_xml(message, req, mutation):
    rule = f"{message}.REQ.{req:03}"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    correspondence = next(element for element in second if element.tag.endswith("}CorrespondenceAddressDetails"))
    address = next(element for element in correspondence if element.tag.endswith("}SubjectAddressDetails"))
    if mutation == "subject_name":
        target = next(element for element in correspondence if element.tag.endswith("}SubjectName"))
        correspondence.remove(target)
    elif mutation == "address_kind":
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "2"
    else:
        next(element for element in address if element.tag.endswith("}UnifiedCountryCode")).text = "US"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
@pytest.mark.parametrize("req, mutation, suffix", [
    (35, "name_representation", ""),
    (36, "original_language", ".or_language"),
    (37, "additional_language", ""),
    (38, "feature_attribute", ""),
    (40, "forbidden_country", ""),
])
def test_inherited_req035_040_origin_rules_real_xml(message, req, mutation, suffix):
    rule = f"{message}.REQ.{req:03}{suffix}"
    document = _inherited_application_document(message)
    applications = _application_instances(document)
    first_origin = _append_origin(message, applications[0])
    origin = _append_origin(message, applications[1])
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    if mutation == "additional_language":
        first_additional = ET.SubElement(first_origin, f"{{{namespaces['ipsdo']}}}ApellationOfOriginName")
        first_additional.text = "ТЕСТОВОЕ НМПТ"
        first_additional.set("nameRepresentationKindCode", "CY")
        additional = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}ApellationOfOriginName")
        additional.text = "ТЕСТОВОЕ НМПТ"
        additional.set("nameRepresentationKindCode", "CY")
    _assert_rule_passes(message, document, rule)
    name = next(element for element in origin if element.tag.endswith("}ApellationOfOriginName"))
    if mutation == "name_representation":
        name.set("nameRepresentationKindCode", "LA")
    elif mutation == "original_language":
        name.attrib.pop("languageCode")
    elif mutation == "additional_language":
        additional.set("languageCode", "RU")
    elif mutation == "feature_attribute":
        properties = next(element for element in origin if element.tag.endswith("}GoodsPropertiesDescriptionText"))
        properties.set("featureKindCode", "TEST")
    else:
        country = ET.SubElement(origin, f"{{{namespaces['csdo']}}}UnifiedCountryCode")
        country.text = "RU"
        country.set("codeListId", "ВОИС ST.3")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
def test_inherited_req036_original_name_cardinality_real_xml(message):
    rule = f"{message}.REQ.036.or_cardinality"
    document = _inherited_application_document(message)
    applications = _application_instances(document)
    _append_origin(message, applications[0])
    origin = _append_origin(message, applications[1])
    _assert_rule_passes(message, document, rule)
    name = next(element for element in origin if element.tag.endswith("}ApellationOfOriginName"))
    name.set("nameRepresentationKindCode", "CY")
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", INHERITED_APPLICATION_MESSAGES)
def test_inherited_req045_start_datetime_required_on_each_application_real_xml(message):
    rule = f"{message}.REQ.045"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    period = next(element for element in second.iter() if element.tag.endswith("}ValidityPeriodDetails"))
    start = next(element for element in period if element.tag.endswith("}StartDateTime"))
    period.remove(start)
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", INHERITED_APPLICATION_MESSAGES)
def test_req046_changed_application_end_datetime_forbidden_real_xml(message):
    rule = f"{message}.REQ.046"
    document = _inherited_application_document(message)
    _assert_rule_passes(message, document, rule)
    second = _application_instances(document)[1]
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    period = next(element for element in second.iter() if element.tag.endswith("}ValidityPeriodDetails"))
    ET.SubElement(period, f"{{{structure.imported_namespaces['csdo']}}}EndDateTime").text = "2026-10-06T13:00:00+03:00"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", TWO_APPLICATION_MESSAGES)
def test_req003_ordered_typed_datetime_real_xml(message):
    rule = f"{message}.REQ.003"
    envelope = ET.fromstring(_positive_xml(message))
    applications = [element for element in envelope.iter() if element.tag.endswith("}ApellationOfOriginApplicationDetails")]
    assert len(applications) == 2
    old, _ = applications
    old_period = next(element for element in old.iter() if element.tag.endswith("}ValidityPeriodDetails"))
    old_end = next(element for element in old_period if element.tag.endswith("}EndDateTime"))
    positive_xml = ET.tostring(envelope, encoding="unicode")
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    assert {e.rule_id for e in positive.rule_evaluations if e.rule_id.startswith(rule)} == {
        rule + ".after_old_start", rule + ".before_new_start"
    }

    for bad_end, failed_suffix in (
        ("2026-10-06T09:00:00+03:00", ".after_old_start"),
        ("2026-10-06T13:00:00+03:00", ".before_new_start"),
    ):
        old_end.text = bad_end
        negative = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
        assert not negative.is_valid
        assert [(issue.code, issue.rule_id) for issue in negative.issues] == [
            ("STRUCTURED_RULE_FAILED", rule + failed_suffix)
        ]

    old_period.remove(old_end)
    missing = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
    assert not missing.is_valid
    assert {issue.rule_id for issue in missing.issues} == {
        rule + ".after_old_start", rule + ".before_new_start"
    }


@pytest.mark.parametrize("local_name", ["UnifiedCountryCode", "AuthorityName"])
def test_msg021_req001_authority_fields_required_real_xml(local_name):
    message = "P.SP.03.MSG.021"
    rule = f"{message}.REQ.001"
    document = _msg021_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    authority = next(element for element in document if element.tag.endswith("}PatentAuthorityDetails"))
    target = next(element for element in authority if element.tag.endswith("}" + local_name))
    authority.remove(target)
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg021_req002_origin_office_indicator_real_xml():
    message = "P.SP.03.MSG.021"
    rule = f"{message}.REQ.002"
    document = _msg021_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid

    indicator = next(element for element in document.iter() if element.tag.endswith("}OriginOfficeIndicator"))
    indicator.text = "0"
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


@pytest.mark.parametrize("mutation", ["missing_address", "wrong_address_kind"])
def test_msg021_req003_physical_address_real_xml(mutation):
    message = "P.SP.03.MSG.021"
    rule = f"{message}.REQ.003"
    document = _msg021_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid

    authority = next(element for element in document if element.tag.endswith("}PatentAuthorityDetails"))
    address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
    if mutation == "missing_address":
        authority.remove(address)
    else:
        kind = next(element for element in address if element.tag.endswith("}AddressKindCode"))
        kind.text = "3"
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg021_req006_application_id_required_real_xml():
    message = "P.SP.03.MSG.021"
    rule = f"{message}.REQ.006"
    document = _msg021_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid

    target = next(element for element in document if element.tag.endswith("}ApellationOfOriginApplicationId"))
    document.remove(target)
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


@pytest.mark.parametrize("prefix, local_name, suffix, value", [
    ("ipsdo", "TrademarkApplicationId", "trademark_application_id", "2026/RU-000002"),
    ("csdo", "DocId", "doc_id", "DOC-021"),
    ("ipcdo", "IPPaymentDetails", "payment_details", None),
    ("ipsdo", "DutyPaymentIndicator", "duty_payment_indicator", "1"),
    ("csdo", "PaymentAmount", "payment_amount", "100.00"),
])
def test_msg021_req007_forbidden_fields_real_xml(prefix, local_name, suffix, value):
    message = "P.SP.03.MSG.021"
    rule = f"{message}.REQ.007.{suffix}"
    document = _msg021_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid

    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    target = ET.SubElement(document, f"{{{structure.imported_namespaces[prefix]}}}{local_name}")
    target.text = value
    if local_name == "PaymentAmount":
        target.set("currencyCode", "RUB")
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg025_req007_document_kind_code_required_real_xml():
    message = "P.SP.03.MSG.025"
    rule = f"{message}.REQ.007"
    controller = GuiController(EaeuXmlApplication(ROOT), test_seed=2303)
    controller.select_process("P.SP.03")
    controller.select_transaction("P.SP.03.TRN.019")
    controller.select_message(message)
    controller.apply_test_data()
    generated = controller.generate_xml()
    assert generated.success

    envelope = ET.fromstring(generated.xml)
    accompanying = next(element for element in envelope.iter() if element.tag.endswith("}AccompanyingDocumentsDetails"))
    kind = next((element for element in accompanying if element.tag.endswith("}IPDocKindCode")), None)
    if kind is None:
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        kind = ET.SubElement(accompanying, f"{{{structure.imported_namespaces['ipsdo']}}}IPDocKindCode")
        kind.text = "00001"
    positive_xml = ET.tostring(envelope, encoding="unicode")
    positive = _validate_xml(message, positive_xml)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    accompanying.remove(kind)
    negative = _validate_xml(message, ET.tostring(envelope, encoding="unicode"))
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg025_req002_to_req004_identifier_exclusivity_real_xml():
    message = "P.SP.03.MSG.025"
    controller = GuiController(EaeuXmlApplication(ROOT), test_seed=2303)
    controller.select_process("P.SP.03")
    controller.select_transaction("P.SP.03.TRN.019")
    controller.select_message(message)
    controller.apply_test_data()
    generated = controller.generate_xml()
    assert generated.success

    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    base = ET.fromstring(generated.xml)
    body = next(element for element in base if element.tag.endswith("}Body"))
    document = next(iter(body))
    for element in list(document):
        if element.tag.endswith(("}ApellationOfOriginApplicationId", "}ApellationOfOriginEAEUId", "}ApellationOfOriginEAEUCertificateId")):
            document.remove(element)

    identifiers = {
        "application": ("ApellationOfOriginApplicationId", "2026/RU-000001"),
        "eaeu": ("ApellationOfOriginEAEUId", "2026/RU-000002"),
        "certificate": ("ApellationOfOriginEAEUCertificateId", "2026/RU-000003/01"),
    }

    for name, (local_name, value) in identifiers.items():
        variant = deepcopy(base)
        variant_body = next(element for element in variant if element.tag.endswith("}Body"))
        variant_document = next(iter(variant_body))
        ET.SubElement(variant_document, f"{{{structure.imported_namespaces['ipsdo']}}}{local_name}").text = value
        positive = _validate_xml(message, ET.tostring(variant, encoding="unicode"))
        assert positive.is_valid, (name, [(issue.code, issue.rule_id) for issue in positive.issues])

    cases = [
        (
            ("application", "eaeu"),
            {f"{message}.REQ.002.eaeu_id", f"{message}.REQ.004.application_id"},
        ),
        (
            ("application", "certificate"),
            {f"{message}.REQ.002.certificate_id", f"{message}.REQ.003.application_id"},
        ),
        (
            ("certificate", "eaeu"),
            {f"{message}.REQ.003.eaeu_id", f"{message}.REQ.004.certificate_id"},
        ),
    ]
    for pair, expected_rules in cases:
        variant = deepcopy(base)
        variant_body = next(element for element in variant if element.tag.endswith("}Body"))
        variant_document = next(iter(variant_body))
        for name in pair:
            local_name, value = identifiers[name]
            ET.SubElement(variant_document, f"{{{structure.imported_namespaces['ipsdo']}}}{local_name}").text = value
        negative = _validate_xml(message, ET.tostring(variant, encoding="unicode"))
        assert not negative.is_valid
        assert {issue.rule_id for issue in negative.issues} == expected_rules


@pytest.mark.parametrize("local_name", ["UnifiedCountryCode", "AuthorityName"])
def test_msg022_req001_inherited_authority_fields_real_xml(local_name):
    message = "P.SP.03.MSG.022"
    rule = f"{message}.REQ.001"
    document = _msg022_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid
    assert any(e.rule_id == rule and e.status.value == "PASS" for e in positive.rule_evaluations)

    authority = next(element for element in document if element.tag.endswith("}PatentAuthorityDetails"))
    target = next(element for element in authority if element.tag.endswith("}" + local_name))
    authority.remove(target)
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg022_req002_inherited_origin_office_indicator_real_xml():
    message = "P.SP.03.MSG.022"
    rule = f"{message}.REQ.002"
    document = _msg022_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid

    indicator = next(element for element in document.iter() if element.tag.endswith("}OriginOfficeIndicator"))
    indicator.text = "0"
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


@pytest.mark.parametrize("mutation", ["missing_address", "wrong_address_kind"])
def test_msg022_req003_inherited_physical_address_real_xml(mutation):
    message = "P.SP.03.MSG.022"
    rule = f"{message}.REQ.003"
    document = _msg022_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid

    authority = next(element for element in document if element.tag.endswith("}PatentAuthorityDetails"))
    address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
    if mutation == "missing_address":
        authority.remove(address)
    else:
        kind = next(element for element in address if element.tag.endswith("}AddressKindCode"))
        kind.text = "3"
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg022_req006_inherited_application_id_required_real_xml():
    message = "P.SP.03.MSG.022"
    rule = f"{message}.REQ.006"
    document = _msg022_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid

    target = next(element for element in document if element.tag.endswith("}ApellationOfOriginApplicationId"))
    document.remove(target)
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg022_req007_payment_and_account_required_real_xml():
    message = "P.SP.03.MSG.022"
    document = _msg022_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid
    assert {
        e.rule_id for e in positive.rule_evaluations
        if e.rule_id.startswith(f"{message}.REQ.007")
    } == {f"{message}.REQ.007.payment_details", f"{message}.REQ.007.account"}

    missing_parent = deepcopy(document)
    payment = next(element for element in missing_parent if element.tag.endswith("}IPPaymentDetails"))
    missing_parent.remove(payment)
    result = _validate_document(message, missing_parent)
    assert not result.is_valid
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", f"{message}.REQ.007.payment_details")
    ]

    missing_account = deepcopy(document)
    payment = next(element for element in missing_account if element.tag.endswith("}IPPaymentDetails"))
    for element in list(payment):
        if element.tag.endswith(("}BankAccountDetails", "}PaymentSystemAccountDetails")):
            payment.remove(element)
    result = _validate_document(message, missing_account)
    assert not result.is_valid
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", f"{message}.REQ.007.account")
    ]


@pytest.mark.parametrize("prefix, local_name, value", [
    ("csdo", "EventDateTime", "2026-10-06T10:00:00+03:00"),
    ("ipcdo", "IPPartyDetails", None),
    ("ipcdo", "AccompanyingDocumentsDetails", None),
])
def test_msg022_req008_payment_children_forbidden_real_xml(prefix, local_name, value):
    message = "P.SP.03.MSG.022"
    rule = f"{message}.REQ.008"
    document = _msg022_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid

    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    payment = next(element for element in document if element.tag.endswith("}IPPaymentDetails"))
    target = ET.SubElement(payment, f"{{{structure.imported_namespaces[prefix]}}}{local_name}")
    target.text = value
    if local_name == "IPPartyDetails":
        ET.SubElement(target, f"{{{structure.imported_namespaces['ipsdo']}}}IPPartyKindCode").text = "AP"
        ET.SubElement(target, f"{{{structure.imported_namespaces['ipsdo']}}}IPSubjectName").text = "Заявитель"
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


@pytest.mark.parametrize("prefix, local_name, suffix, value", [
    ("ipsdo", "TrademarkApplicationId", "trademark_application_id", "2026/RU-000002"),
    ("csdo", "DocId", "doc_id", "DOC-022"),
    ("csdo", "PaymentAmount", "payment_amount", "100.00"),
    ("ipsdo", "DutyPaymentIndicator", "duty_payment_indicator", "1"),
])
def test_msg022_req009_top_level_fields_forbidden_real_xml(prefix, local_name, suffix, value):
    message = "P.SP.03.MSG.022"
    rule = f"{message}.REQ.009.{suffix}"
    document = _msg022_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid

    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    target = ET.SubElement(document, f"{{{structure.imported_namespaces[prefix]}}}{local_name}")
    target.text = value
    if local_name == "PaymentAmount":
        target.set("currencyCode", "RUB")
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert [(issue.code, issue.rule_id) for issue in negative.issues] == [("STRUCTURED_RULE_FAILED", rule)]


@pytest.mark.parametrize("local_name", ["UnifiedCountryCode", "AuthorityName"])
def test_msg023_req001_inherited_authority_fields_real_xml(local_name):
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.001"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    authority = next(element for element in document if element.tag.endswith("}PatentAuthorityDetails"))
    target = next(element for element in authority if element.tag.endswith("}" + local_name))
    authority.remove(target)
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


def test_msg023_req002_inherited_origin_office_indicator_real_xml():
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.002"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    indicator = next(element for element in document.iter() if element.tag.endswith("}OriginOfficeIndicator"))
    indicator.text = "0"
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


@pytest.mark.parametrize("mutation", ["missing_address", "wrong_address_kind"])
def test_msg023_req003_inherited_physical_address_real_xml(mutation):
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.003"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    authority = next(element for element in document if element.tag.endswith("}PatentAuthorityDetails"))
    address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
    if mutation == "missing_address":
        authority.remove(address)
    else:
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "3"
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


def test_msg023_req006_inherited_application_id_required_real_xml():
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.006"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    target = next(element for element in document if element.tag.endswith("}ApellationOfOriginApplicationId"))
    document.remove(target)
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


def test_msg023_req007_payment_required_and_accounts_forbidden_real_xml():
    message = "P.SP.03.MSG.023"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid

    missing = deepcopy(document)
    payment = next(element for element in missing if element.tag.endswith("}IPPaymentDetails"))
    missing.remove(payment)
    result = _validate_document(message, missing)
    assert ("STRUCTURED_RULE_FAILED", f"{message}.REQ.007.payment_details") in [
        (issue.code, issue.rule_id) for issue in result.issues
    ]

    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    for account_kind in ("BankAccountDetails", "PaymentSystemAccountDetails"):
        variant = deepcopy(document)
        payment = next(element for element in variant if element.tag.endswith("}IPPaymentDetails"))
        if account_kind == "PaymentSystemAccountDetails":
            account = ET.SubElement(payment, f"{{{structure.imported_namespaces['ccdo']}}}PaymentSystemAccountDetails")
            ET.SubElement(account, f"{{{structure.imported_namespaces['csdo']}}}PaymentSystemAccountId").text = "ACCOUNT-1"
            ET.SubElement(account, f"{{{structure.imported_namespaces['csdo']}}}PaymentSystemName").text = "Тестовая система"
        else:
            account = ET.SubElement(payment, f"{{{structure.imported_namespaces['ccdo']}}}BankAccountDetails")
            ET.SubElement(account, f"{{{structure.imported_namespaces['csdo']}}}BankAccountId").text = "40702810000000000001"
            bank = ET.SubElement(account, f"{{{structure.imported_namespaces['ccdo']}}}BankDetails")
            ET.SubElement(bank, f"{{{structure.imported_namespaces['csdo']}}}BusinessEntityName").text = "Тестовый банк"
            bank_id = ET.SubElement(bank, f"{{{structure.imported_namespaces['csdo']}}}UnifiedBankId")
            bank_id.text = "044525000"
            bank_id.set("schemeId", "BIC")
        result = _validate_document(message, variant)
        assert not result.is_valid
        assert ("STRUCTURED_RULE_FAILED", f"{message}.REQ.007.accounts_forbidden") in [
            (issue.code, issue.rule_id) for issue in result.issues
        ]


@pytest.mark.parametrize("local_name", ["EventDateTime", "IPPartyDetails", "AccompanyingDocumentsDetails"])
def test_msg023_req008_payment_children_required_real_xml(local_name):
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.008"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    payment = next(element for element in document if element.tag.endswith("}IPPaymentDetails"))
    target = next(element for element in payment if element.tag.endswith("}" + local_name))
    payment.remove(target)
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


def test_msg023_req009_exactly_one_allowed_party_real_xml():
    message = "P.SP.03.MSG.023"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid

    payment = next(element for element in document if element.tag.endswith("}IPPaymentDetails"))
    party = next(element for element in payment if element.tag.endswith("}IPPartyDetails"))
    payment.append(deepcopy(party))
    duplicate = _validate_document(message, document)
    assert ("STRUCTURED_RULE_FAILED", f"{message}.REQ.009.cardinality") in [
        (issue.code, issue.rule_id) for issue in duplicate.issues
    ]

    document = _msg023_positive_document()
    party = next(element for element in document.iter() if element.tag.endswith("}IPPartyDetails"))
    next(element for element in party if element.tag.endswith("}IPPartyKindCode")).text = "XX"
    bad_kind = _validate_document(message, document)
    assert ("STRUCTURED_RULE_FAILED", f"{message}.REQ.009.kind") in [
        (issue.code, issue.rule_id) for issue in bad_kind.issues
    ]


@pytest.mark.parametrize("local_name", ["UnifiedCountryCode", "IPSubjectName"])
def test_msg023_req010_party_fields_required_real_xml(local_name):
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.010"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    party = next(element for element in document.iter() if element.tag.endswith("}IPPartyDetails"))
    target = next(element for element in party if element.tag.endswith("}" + local_name))
    party.remove(target)
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


@pytest.mark.parametrize("attribute, value", [("nameRepresentationKindCode", "TR"), ("languageCode", "EN")])
def test_msg023_req011_applicant_name_attributes_real_xml(attribute, value):
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.011"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    subject = next(element for element in document.iter() if element.tag.endswith("}IPSubjectName"))
    subject.set(attribute, value)
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


def test_msg023_req012_patent_attorney_id_for_pa_real_xml():
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.012"
    document = _msg023_positive_document()
    party, _ = _msg023_set_party_kind(document, "PA")
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    attorney = ET.SubElement(party, f"{{{structure.imported_namespaces['ipsdo']}}}PatentAttorneyId")
    attorney.text = "PA-001"
    assert _validate_document(message, document).is_valid
    party.remove(attorney)
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


def test_msg023_req013_representative_country_real_xml():
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.013"
    document = _msg023_positive_document()
    party, _ = _msg023_set_party_kind(document, "RE")
    assert _validate_document(message, document).is_valid
    country = next(element for element in party if element.tag.endswith("}UnifiedCountryCode"))
    country.text = "US"
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


@pytest.mark.parametrize("mutation", ["name_representation", "language"])
def test_msg023_req014_representative_name_attributes_real_xml(mutation):
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.014"
    document = _msg023_positive_document()
    party, subject = _msg023_set_party_kind(document, "RE")
    assert _validate_document(message, document).is_valid
    if mutation == "name_representation":
        subject.set("nameRepresentationKindCode", "OR")
    else:
        subject.set("languageCode", "EN")
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


def test_msg023_req015_exactly_one_accompanying_document_real_xml():
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.015"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    payment = next(element for element in document if element.tag.endswith("}IPPaymentDetails"))
    accompanying = next(element for element in payment if element.tag.endswith("}AccompanyingDocumentsDetails"))
    payment.append(deepcopy(accompanying))
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


def test_msg023_req016_document_kind_name_forbidden_real_xml():
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.016"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    accompanying = next(element for element in document.iter() if element.tag.endswith("}AccompanyingDocumentsDetails"))
    ET.SubElement(accompanying, f"{{{structure.imported_namespaces['ipsdo']}}}IPDocKindName").text = "Документ"
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


@pytest.mark.parametrize("mutation", ["missing", "wrong"])
def test_msg023_req017_document_kind_code_real_xml(mutation):
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.017"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    accompanying = next(element for element in document.iter() if element.tag.endswith("}AccompanyingDocumentsDetails"))
    kind = next(element for element in accompanying if element.tag.endswith("}IPDocKindCode"))
    if mutation == "missing":
        accompanying.remove(kind)
    else:
        kind.text = "99999"
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


@pytest.mark.parametrize("local_name", ["DocId", "DocCreationDate"])
def test_msg023_req018_document_fields_required_real_xml(local_name):
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.018"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    accompanying = next(element for element in document.iter() if element.tag.endswith("}AccompanyingDocumentsDetails"))
    target = next(element for element in accompanying if element.tag.endswith("}" + local_name))
    accompanying.remove(target)
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


@pytest.mark.parametrize("message", ["P.SP.03.MSG.023", "P.SP.03.MSG.024"])
@pytest.mark.parametrize("mutation", ["missing", "media_type"])
def test_msg023_024_req019_binary_document_real_xml(message, mutation):
    rule = f"{message}.REQ.019"
    document = _msg023_positive_document() if message.endswith("023") else _msg024_positive_document()
    positive = _validate_document(message, document)
    assert positive.is_valid, [(issue.code, issue.rule_id) for issue in positive.issues]

    accompanying = next(element for element in document.iter() if element.tag.endswith("}AccompanyingDocumentsDetails"))
    binary = next(element for element in accompanying if element.tag.endswith("}DocBinaryText"))
    if mutation == "missing":
        accompanying.remove(binary)
    elif mutation == "media_type":
        binary.set("mediaTypeCode", "exe")
    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in negative.issues]


@pytest.mark.parametrize("prefix, local_name, suffix, value", [
    ("ipsdo", "TrademarkApplicationId", "trademark_application_id", "2026/RU-000002"),
    ("csdo", "DocId", "doc_id", "DOC-TOP-023"),
    ("csdo", "PaymentAmount", "payment_amount", "100.00"),
    ("ipsdo", "DutyPaymentIndicator", "duty_payment_indicator", "1"),
])
def test_msg023_req020_top_level_fields_forbidden_real_xml(prefix, local_name, suffix, value):
    message = "P.SP.03.MSG.023"
    rule = f"{message}.REQ.020.{suffix}"
    document = _msg023_positive_document()
    assert _validate_document(message, document).is_valid
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    target = ET.SubElement(document, f"{{{structure.imported_namespaces[prefix]}}}{local_name}")
    target.text = value
    if local_name == "PaymentAmount":
        target.set("currencyCode", "RUB")
    result = _validate_document(message, document)
    assert not result.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in result.issues]


@pytest.mark.parametrize("req, mutation, expected_suffix", [
    (1, "authority_country", ""),
    (1, "authority_name", ""),
    (2, "origin_office", ""),
    (3, "address_missing", ""),
    (3, "address_kind", ""),
    (6, "application_id", ""),
    (7, "payment_missing", ".payment_details"),
    (7, "account_present", ".accounts_forbidden"),
    (8, "event_datetime", ""),
    (8, "party_missing", ""),
    (8, "document_missing", ""),
    (9, "party_count", ".cardinality"),
    (9, "party_kind", ".kind"),
    (10, "party_country", ""),
    (10, "party_name", ""),
    (11, "applicant_name_representation", ""),
    (11, "applicant_language", ""),
    (12, "patent_attorney", ""),
    (13, "representative_country", ""),
    (14, "representative_name_representation", ""),
    (14, "representative_language", ""),
    (15, "document_count", ""),
    (16, "document_kind_name", ""),
    (17, "document_kind_missing", ""),
    (17, "document_kind_wrong", ""),
    (18, "document_id", ""),
    (18, "document_date", ""),
])
def test_msg024_inherited_req001_to_req018_real_xml(req, mutation, expected_suffix):
    message = "P.SP.03.MSG.024"
    rule = f"{message}.REQ.{req:03}{expected_suffix}"
    document = _msg024_positive_document()
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces

    if mutation == "patent_attorney":
        party, _ = _msg023_set_party_kind(document, "PA")
        attorney = ET.SubElement(party, f"{{{namespaces['ipsdo']}}}PatentAttorneyId")
        attorney.text = "PA-001"
    elif mutation in {"representative_country", "representative_name_representation", "representative_language"}:
        party, subject = _msg023_set_party_kind(document, "RE")

    positive = _validate_document(message, document)
    assert positive.is_valid, [(issue.code, issue.rule_id) for issue in positive.issues]

    if mutation in {"authority_country", "authority_name", "origin_office", "address_missing", "address_kind"}:
        authority = next(element for element in document if element.tag.endswith("}PatentAuthorityDetails"))
        if mutation == "authority_country":
            authority.remove(next(element for element in authority if element.tag.endswith("}UnifiedCountryCode")))
        elif mutation == "authority_name":
            authority.remove(next(element for element in authority if element.tag.endswith("}AuthorityName")))
        elif mutation == "origin_office":
            next(element for element in authority if element.tag.endswith("}OriginOfficeIndicator")).text = "0"
        elif mutation == "address_missing":
            authority.remove(next(element for element in authority if element.tag.endswith("}SubjectAddressDetails")))
        else:
            address = next(element for element in authority if element.tag.endswith("}SubjectAddressDetails"))
            next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "3"
    elif mutation == "application_id":
        document.remove(next(element for element in document if element.tag.endswith("}ApellationOfOriginApplicationId")))
    elif mutation == "payment_missing":
        document.remove(next(element for element in document if element.tag.endswith("}IPPaymentDetails")))
    elif mutation == "account_present":
        payment = next(element for element in document if element.tag.endswith("}IPPaymentDetails"))
        account = ET.SubElement(payment, f"{{{namespaces['ccdo']}}}PaymentSystemAccountDetails")
        ET.SubElement(account, f"{{{namespaces['csdo']}}}PaymentSystemAccountId").text = "ACCOUNT-1"
        ET.SubElement(account, f"{{{namespaces['csdo']}}}PaymentSystemName").text = "Тестовая система"
    elif mutation in {"event_datetime", "party_missing", "document_missing"}:
        payment = next(element for element in document if element.tag.endswith("}IPPaymentDetails"))
        local_name = {
            "event_datetime": "EventDateTime",
            "party_missing": "IPPartyDetails",
            "document_missing": "AccompanyingDocumentsDetails",
        }[mutation]
        payment.remove(next(element for element in payment if element.tag.endswith("}" + local_name)))
    elif mutation == "party_count":
        payment = next(element for element in document if element.tag.endswith("}IPPaymentDetails"))
        party = next(element for element in payment if element.tag.endswith("}IPPartyDetails"))
        payment.append(deepcopy(party))
    elif mutation == "party_kind":
        party = next(element for element in document.iter() if element.tag.endswith("}IPPartyDetails"))
        next(element for element in party if element.tag.endswith("}IPPartyKindCode")).text = "XX"
    elif mutation in {"party_country", "party_name"}:
        party = next(element for element in document.iter() if element.tag.endswith("}IPPartyDetails"))
        local_name = "UnifiedCountryCode" if mutation == "party_country" else "IPSubjectName"
        party.remove(next(element for element in party if element.tag.endswith("}" + local_name)))
    elif mutation in {"applicant_name_representation", "applicant_language"}:
        subject = next(element for element in document.iter() if element.tag.endswith("}IPSubjectName"))
        if mutation == "applicant_name_representation":
            subject.set("nameRepresentationKindCode", "TR")
        else:
            subject.set("languageCode", "EN")
    elif mutation == "patent_attorney":
        party.remove(attorney)
    elif mutation == "representative_country":
        country = next(element for element in party if element.tag.endswith("}UnifiedCountryCode"))
        country.text = "US"
    elif mutation == "representative_name_representation":
        subject.set("nameRepresentationKindCode", "OR")
    elif mutation == "representative_language":
        subject.set("languageCode", "EN")
    elif mutation == "document_count":
        payment = next(element for element in document if element.tag.endswith("}IPPaymentDetails"))
        accompanying = next(element for element in payment if element.tag.endswith("}AccompanyingDocumentsDetails"))
        payment.append(deepcopy(accompanying))
    elif mutation == "document_kind_name":
        accompanying = next(element for element in document.iter() if element.tag.endswith("}AccompanyingDocumentsDetails"))
        ET.SubElement(accompanying, f"{{{namespaces['ipsdo']}}}IPDocKindName").text = "Документ"
    elif mutation in {"document_kind_missing", "document_kind_wrong"}:
        accompanying = next(element for element in document.iter() if element.tag.endswith("}AccompanyingDocumentsDetails"))
        kind = next(element for element in accompanying if element.tag.endswith("}IPDocKindCode"))
        if mutation == "document_kind_missing":
            accompanying.remove(kind)
        else:
            kind.text = "99999"
    elif mutation in {"document_id", "document_date"}:
        accompanying = next(element for element in document.iter() if element.tag.endswith("}AccompanyingDocumentsDetails"))
        local_name = "DocId" if mutation == "document_id" else "DocCreationDate"
        accompanying.remove(next(element for element in accompanying if element.tag.endswith("}" + local_name)))

    negative = _validate_document(message, document)
    assert not negative.is_valid
    assert ("STRUCTURED_RULE_FAILED", rule) in [(issue.code, issue.rule_id) for issue in negative.issues]


def test_msg024_req020_duty_payment_indicator_required_real_xml():
    message = "P.SP.03.MSG.024"
    rule = f"{message}.REQ.020"
    document = _msg024_positive_document()
    assert _validate_document(message, document).is_valid
    indicator = next(element for element in document if element.tag.endswith("}DutyPaymentIndicator"))
    document.remove(indicator)
    result = _validate_document(message, document)
    assert not result.is_valid
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [("STRUCTURED_RULE_FAILED", rule)]


def test_msg024_req021_true_requires_zero_amount_real_xml():
    message = "P.SP.03.MSG.024"
    rule = f"{message}.REQ.021"
    document = _msg024_positive_document()
    assert _validate_document(message, document).is_valid
    amount = next(element for element in document if element.tag.endswith("}PaymentAmount"))
    amount.text = "0.01"
    result = _validate_document(message, document)
    assert not result.is_valid
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [("STRUCTURED_RULE_FAILED", rule)]


@pytest.mark.parametrize("bad_amount", ["0", "0.00", "-1.00"])
def test_msg024_req022_false_requires_positive_amount_real_xml(bad_amount):
    message = "P.SP.03.MSG.024"
    rule = f"{message}.REQ.022"
    document = _msg024_positive_document()
    indicator = next(element for element in document if element.tag.endswith("}DutyPaymentIndicator"))
    amount = next(element for element in document if element.tag.endswith("}PaymentAmount"))
    indicator.text = "false"
    amount.text = "1.00"
    assert _validate_document(message, document).is_valid
    amount.text = bad_amount
    result = _validate_document(message, document)
    assert not result.is_valid
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [("STRUCTURED_RULE_FAILED", rule)]


@pytest.mark.parametrize("prefix, local_name, suffix, value", [
    ("csdo", "UpdateDateTime", "update_datetime", "2026-10-06T10:00:00+03:00"),
    ("csdo", "UnifiedCountryCode", "country_code", "RU"),
    ("ipsdo", "ApellationOfOriginEAEUId", "eaeu_id", "EAEU-1"),
    ("ipsdo", "ApellationOfOriginEAEUCertificateId", "certificate_id", "CERT-1"),
    ("ipsdo", "ApellationOfOriginApplicationId", "application_id", "APP-1"),
    ("ipcdo", "AccompanyingDocumentsDetails", "accompanying_document", None),
])
def test_msg016_only_header_allowed_real_xml(prefix, local_name, suffix, value):
    message = "P.SP.03.MSG.016"
    rule = f"{message}.REQ.001.{suffix}"
    document = _generated_document(message)
    positive = _validate_document(message, document)
    assert positive.is_valid
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    target = ET.SubElement(document, f"{{{structure.imported_namespaces[prefix]}}}{local_name}")
    target.text = value
    if local_name == "UnifiedCountryCode":
        target.set("codeListId", "ВОИС ST.3")
    result = _validate_document(message, document)
    assert not result.is_valid
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [("STRUCTURED_RULE_FAILED", rule)]

# OP23 register-message production rules (MSG.006-008).
# Build the XML from the package structure without pre-validating it, then
# normalize it into a positive real-XML fixture before exercising production validation.
def _raw_register_document(message: str):
    application = EaeuXmlApplication(ROOT)
    engine = EaeuXmlEngine.load_process(PACKAGE)
    transaction_code = next(
        transaction.transaction_code
        for transaction in application.list_transactions("P.SP.03")
        if any(
            item.message_code == message
            for item in application.list_messages("P.SP.03", transaction.transaction_code)
        )
    )
    values = application.generate_test_data("P.SP.03", transaction_code, message, seed=2303)
    structure = engine.get_structure(message, mode=GenerationMode.TEST)
    document = engine.body_provider._serialize(structure, engine.body_provider._flatten(values))
    return ET.fromstring(ET.tostring(document))


def _remove_direct_children(parent: ET.Element, local_name: str):
    for child in [item for item in parent if item.tag.endswith("}" + local_name)]:
        parent.remove(child)


def _set_identifier_pair(item: ET.Element, namespaces, pair: str):
    for local_name in ("ApellationOfOriginApplicationId", "ApplicationReceiptDate", "DocId", "IPDocReceiptDate"):
        _remove_direct_children(item, local_name)
    if pair == "application":
        _ensure_child(item, namespaces["ipsdo"], "ApellationOfOriginApplicationId", "APP-001")
        _ensure_child(item, namespaces["ipsdo"], "ApplicationReceiptDate", "2026-10-01")
    else:
        _ensure_child(item, namespaces["csdo"], "DocId", "DOC-001")
        _ensure_child(item, namespaces["ipsdo"], "IPDocReceiptDate", "2026-10-01")


def _normalise_register_item(item: ET.Element, namespaces, kind: str):
    _ensure_child(item, namespaces["ipsdo"], "ResourceItemKindCode", kind)
    _set_identifier_pair(item, namespaces, "application")
    _remove_direct_children(item, "AccompanyingDocumentsDetails")
    _remove_direct_children(item, "ApellationOfOriginNationalRegistrationDetails")

    origin = _ensure_child(item, namespaces["ipcdo"], "ApellationOfOriginDetails")
    _ensure_child(origin, namespaces["ipsdo"], "ApellationOfOriginEAEUId", "AO-001")
    properties = _ensure_child(origin, namespaces["ipsdo"], "GoodsPropertiesDescriptionText", "Особые свойства товара")
    properties.attrib.pop("featureKindCode", None)
    properties.attrib.pop("featureName", None)

    if kind == "RH":
        _ensure_child(origin, namespaces["ipsdo"], "ApellationOfOriginGoodsText", "Товар")
        geographic = _ensure_child(origin, namespaces["ipcdo"], "GeographicRegionDescriptionTextDetails")
        _ensure_child(geographic, namespaces["ipsdo"], "GeographicRegionDescriptionText", "Географический объект")

        right = _ensure_child(item, namespaces["ipcdo"], "ApellationOfOriginEAEURightDetails")
        _ensure_child(right, namespaces["ipsdo"], "ApellationOfOriginEAEUCertificateId", "CERT-001")
        _ensure_child(right, namespaces["csdo"], "DocValidityDate", "2030-01-01")
        parties = [child for child in right if child.tag.endswith("}IPPartyDetails")]
        party = parties[0] if parties else ET.SubElement(right, f"{{{namespaces['ipcdo']}}}IPPartyDetails")
        for extra in parties[1:]:
            right.remove(extra)
        _ensure_child(party, namespaces["ipsdo"], "IPPartyKindCode", "RH")
        country = _ensure_child(party, namespaces["csdo"], "UnifiedCountryCode", "RU")
        country.set("codeListId", "ВОИС ST.3")
        names = [child for child in party if child.tag.endswith("}IPSubjectName")]
        subject = names[0] if names else ET.SubElement(party, f"{{{namespaces['ipsdo']}}}IPSubjectName")
        for extra in names[1:]:
            party.remove(extra)
        subject.text = "Правообладатель"
        subject.set("nameRepresentationKindCode", "OR")
        subject.set("languageCode", "RU")
        address = _ensure_child(party, namespaces["ccdo"], "SubjectAddressDetails")
        _normalise_address(address, namespaces, "2")
        communication = _ensure_child(party, namespaces["ccdo"], "CommunicationDetails")
        _normalise_communication(communication, namespaces)

        correspondence = _ensure_child(item, namespaces["ipcdo"], "CorrespondenceAddressDetails")
        _ensure_child(correspondence, namespaces["csdo"], "SubjectName", "Правообладатель")
        address = _ensure_child(correspondence, namespaces["ccdo"], "SubjectAddressDetails")
        _normalise_address(address, namespaces, "3")
        communication = _ensure_child(correspondence, namespaces["ccdo"], "CommunicationDetails")
        _normalise_communication(communication, namespaces)
    else:
        _remove_direct_children(item, "ApellationOfOriginEAEURightDetails")
        _remove_direct_children(item, "CorrespondenceAddressDetails")
        country = _ensure_child(origin, namespaces["csdo"], "UnifiedCountryCode", "RU")
        country.set("codeListId", "ВОИС ST.3")
        _ensure_child(origin, namespaces["ipsdo"], "RegistrationDate", "2026-10-01")
        _ensure_child(origin, namespaces["ipsdo"], "PublicationDate", "2026-10-02")
        names = [child for child in origin if child.tag.endswith("}ApellationOfOriginName")]
        name = names[0] if names else ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}ApellationOfOriginName")
        for extra in names[1:]:
            origin.remove(extra)
        name.text = "Тестовое НМПТ"
        name.set("nameRepresentationKindCode", "OR")
        name.set("languageCode", "RU")

    authority = _ensure_child(item, namespaces["ipcdo"], "PatentAuthorityDetails")
    country = _ensure_child(authority, namespaces["csdo"], "UnifiedCountryCode", "RU")
    country.set("codeListId", "ВОИС ST.3")
    _ensure_child(authority, namespaces["csdo"], "AuthorityName", "Роспатент")
    _ensure_child(authority, namespaces["ipsdo"], "OriginOfficeIndicator", "1")
    address = _ensure_child(authority, namespaces["ccdo"], "SubjectAddressDetails")
    _normalise_address(address, namespaces, "2")

    resource = _ensure_child(item, namespaces["ccdo"], "ResourceItemStatusDetails")
    period = _ensure_child(resource, namespaces["ccdo"], "ValidityPeriodDetails")
    _ensure_child(period, namespaces["csdo"], "StartDateTime", "2026-10-06T10:00:00+03:00")
    _ensure_child(period, namespaces["csdo"], "EndDateTime", "2026-10-07T10:00:00+03:00")

    for address in [element for element in item.iter() if element.tag.endswith("}SubjectAddressDetails")]:
        _normalise_address(address, namespaces)
    for communication in [element for element in item.iter() if element.tag.endswith("}CommunicationDetails")]:
        _normalise_communication(communication, namespaces)
    for country in [element for element in item.iter() if element.tag.endswith("}UnifiedCountryCode")]:
        country.set("codeListId", "ВОИС ST.3")
    for properties in [element for element in item.iter() if element.tag.endswith("}GoodsPropertiesDescriptionText")]:
        properties.attrib.pop("featureKindCode", None)
        properties.attrib.pop("featureName", None)


def _two_register_document(message: str, *, kind: str = "RH", identifier_pair: str = "application"):
    document = _raw_register_document(message)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    items = [child for child in document if child.tag.endswith("}ApellationOfOriginRegisterItemDetails")]
    if items:
        first = items[0]
        for extra in items[1:]:
            document.remove(extra)
    else:
        first = ET.SubElement(document, f"{{{namespaces['ipcdo']}}}ApellationOfOriginRegisterItemDetails")
    _normalise_register_item(first, namespaces, kind)
    _set_identifier_pair(first, namespaces, identifier_pair)
    if message == "P.SP.03.MSG.013":
        geographic = next(
            element
            for element in first.iter()
            if element.tag.endswith("}GeographicRegionDescriptionTextDetails")
        )
        country = _ensure_child(geographic, namespaces["csdo"], "UnifiedCountryCode", "RU")
        country.set("codeListId", "ВОИС ST.3")
        _append_register_attachment(message, first)
    second = deepcopy(first)
    document.append(second)
    _set_identifier_pair(second, namespaces, identifier_pair)

    first_period = next(element for element in first.iter() if element.tag.endswith("}ValidityPeriodDetails"))
    second_period = next(element for element in second.iter() if element.tag.endswith("}ValidityPeriodDetails"))
    next(element for element in first_period if element.tag.endswith("}StartDateTime")).text = "2026-10-06T10:00:00+03:00"
    next(element for element in first_period if element.tag.endswith("}EndDateTime")).text = "2026-10-07T10:00:00+03:00"
    next(element for element in second_period if element.tag.endswith("}StartDateTime")).text = "2026-10-08T10:00:00+03:00"
    _remove_direct_children(second_period, "EndDateTime")

    status_code = (
        "02"
        if message in {"P.SP.03.MSG.006", "P.SP.03.MSG.013"} and kind == "AO"
        else {
            "P.SP.03.MSG.006": "11",
            "P.SP.03.MSG.007": "12",
            "P.SP.03.MSG.008": "19",
            "P.SP.03.MSG.013": "11",
        }[message]
    )
    second_status = _ensure_child(second, namespaces["ipcdo"], "IPEntityStatusDetails")
    _ensure_child(second_status, namespaces["csdo"], "EventDate", "2026-10-08")
    status = _ensure_child(second_status, namespaces["csdo"], "StatusCode", status_code)
    status.attrib.pop("codeListId", None)
    return document


def _register_items(document: ET.Element):
    return [child for child in document if child.tag.endswith("}ApellationOfOriginRegisterItemDetails")]


def _status_of(item: ET.Element):
    return next(element for element in item if element.tag.endswith("}IPEntityStatusDetails"))


def _right_of(item: ET.Element):
    return next(element for element in item if element.tag.endswith("}ApellationOfOriginEAEURightDetails"))


def _origin_of(item: ET.Element):
    return next(element for element in item if element.tag.endswith("}ApellationOfOriginDetails"))


def _party_of(item: ET.Element):
    return next(element for element in _right_of(item) if element.tag.endswith("}IPPartyDetails"))


def _correspondence_of(item: ET.Element):
    return next(element for element in item if element.tag.endswith("}CorrespondenceAddressDetails"))


@pytest.mark.parametrize("rule_id, mutation", [
    ("P.SP.03.MSG.006.REQ.001.cardinality", "remove_second"),
    ("P.SP.03.MSG.006.REQ.001.resource_kind", "second_kind"),
    ("P.SP.03.MSG.006.REQ.002", "invalid_kind"),
    ("P.SP.03.MSG.006.REQ.003.presence", "remove_start"),
    ("P.SP.03.MSG.006.REQ.003.order", "reverse_start"),
    ("P.SP.03.MSG.006.REQ.004.presence", "remove_old_end"),
    ("P.SP.03.MSG.006.REQ.004.after_old_start", "old_end_before_start"),
    ("P.SP.03.MSG.006.REQ.004.before_new_start", "old_end_after_new_start"),
    ("P.SP.03.MSG.006.REQ.005", "new_end"),
    ("P.SP.03.MSG.006.REQ.006.presence", "remove_origin_id"),
    ("P.SP.03.MSG.006.REQ.006.equality", "change_origin_id"),
    ("P.SP.03.MSG.006.REQ.007.combination", "break_application_pair"),
    ("P.SP.03.MSG.006.REQ.007.application_id", "change_application_id"),
    ("P.SP.03.MSG.006.REQ.007.application_date", "change_application_date"),
    ("P.SP.03.MSG.006.REQ.012", "remove_goods"),
    ("P.SP.03.MSG.006.REQ.014", "remove_certificate"),
    ("P.SP.03.MSG.006.REQ.015", "change_certificate"),
    ("P.SP.03.MSG.006.REQ.017", "party_kind"),
    ("P.SP.03.MSG.006.REQ.018", "party_country"),
    ("P.SP.03.MSG.006.REQ.019", "party_language"),
    ("P.SP.03.MSG.006.REQ.020", "party_address_kind"),
    ("P.SP.03.MSG.006.REQ.021", "correspondence_subject"),
    ("P.SP.03.MSG.006.REQ.022", "correspondence_country"),
    ("P.SP.03.MSG.006.REQ.025", "authority_name"),
    ("P.SP.03.MSG.006.REQ.026", "origin_office"),
    ("P.SP.03.MSG.006.REQ.027", "address_city"),
    ("P.SP.03.MSG.006.REQ.028", "communication_name"),
    ("P.SP.03.MSG.006.REQ.029", "communication_code"),
    ("P.SP.03.MSG.006.REQ.030", "country_codelist"),
    ("P.SP.03.MSG.006.REQ.031", "attachment"),
    ("P.SP.03.MSG.006.REQ.033", "status_11"),
    ("P.SP.03.MSG.006.REQ.036", "goods_attribute"),
])
def test_msg006_safe_production_rules_real_xml(rule_id, mutation):
    message = "P.SP.03.MSG.006"
    document = _two_register_document(message)
    items = _register_items(document)
    _assert_rule_passes(message, document, rule_id)

    if mutation == "remove_second":
        document.remove(items[1])
    elif mutation in {"second_kind", "invalid_kind"}:
        target = items[1] if mutation == "second_kind" else items[0]
        next(element for element in target if element.tag.endswith("}ResourceItemKindCode")).text = "AO" if mutation == "second_kind" else "XX"
    elif mutation in {"remove_start", "reverse_start", "remove_old_end", "old_end_before_start", "old_end_after_new_start", "new_end"}:
        first_period = next(element for element in items[0].iter() if element.tag.endswith("}ValidityPeriodDetails"))
        second_period = next(element for element in items[1].iter() if element.tag.endswith("}ValidityPeriodDetails"))
        if mutation == "remove_start":
            _remove_direct_children(first_period, "StartDateTime")
        elif mutation == "reverse_start":
            next(element for element in second_period if element.tag.endswith("}StartDateTime")).text = "2026-10-05T10:00:00+03:00"
        elif mutation == "remove_old_end":
            _remove_direct_children(first_period, "EndDateTime")
        elif mutation == "old_end_before_start":
            next(element for element in first_period if element.tag.endswith("}EndDateTime")).text = "2026-10-05T10:00:00+03:00"
        elif mutation == "old_end_after_new_start":
            next(element for element in first_period if element.tag.endswith("}EndDateTime")).text = "2026-10-09T10:00:00+03:00"
        else:
            structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
            ET.SubElement(second_period, f"{{{structure.imported_namespaces['csdo']}}}EndDateTime").text = "2026-10-09T10:00:00+03:00"
    elif mutation in {"remove_origin_id", "change_origin_id"}:
        origin = _origin_of(items[0] if mutation == "remove_origin_id" else items[1])
        target = next(element for element in origin if element.tag.endswith("}ApellationOfOriginEAEUId"))
        if mutation == "remove_origin_id":
            origin.remove(target)
        else:
            target.text = "AO-OTHER"
    elif mutation == "break_application_pair":
        _remove_direct_children(items[0], "ApplicationReceiptDate")
    elif mutation == "change_application_id":
        next(element for element in items[1] if element.tag.endswith("}ApellationOfOriginApplicationId")).text = "APP-OTHER"
    elif mutation == "change_application_date":
        next(element for element in items[1] if element.tag.endswith("}ApplicationReceiptDate")).text = "2026-10-02"
    elif mutation == "remove_goods":
        _remove_direct_children(_origin_of(items[0]), "ApellationOfOriginGoodsText")
    elif mutation in {"remove_certificate", "change_certificate"}:
        right = _right_of(items[0] if mutation == "remove_certificate" else items[1])
        target = next(element for element in right if element.tag.endswith("}ApellationOfOriginEAEUCertificateId"))
        if mutation == "remove_certificate":
            right.remove(target)
        else:
            target.text = "CERT-OTHER"
    elif mutation == "party_kind":
        next(element for element in _party_of(items[0]) if element.tag.endswith("}IPPartyKindCode")).text = "AP"
    elif mutation == "party_country":
        party = _party_of(items[0])
        party.remove(next(element for element in party if element.tag.endswith("}UnifiedCountryCode")))
    elif mutation == "party_language":
        next(element for element in _party_of(items[0]) if element.tag.endswith("}IPSubjectName")).set("languageCode", "EN")
    elif mutation == "party_address_kind":
        address = next(element for element in _party_of(items[0]) if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "1"
    elif mutation == "correspondence_subject":
        correspondence = _correspondence_of(items[0])
        correspondence.remove(next(element for element in correspondence if element.tag.endswith("}SubjectName")))
    elif mutation == "correspondence_country":
        address = next(element for element in _correspondence_of(items[0]) if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}UnifiedCountryCode")).text = "US"
    elif mutation in {"authority_name", "origin_office"}:
        authority = next(element for element in items[0] if element.tag.endswith("}PatentAuthorityDetails"))
        if mutation == "authority_name":
            authority.remove(next(element for element in authority if element.tag.endswith("}AuthorityName")))
        else:
            next(element for element in authority if element.tag.endswith("}OriginOfficeIndicator")).text = "0"
    elif mutation == "address_city":
        address = next(element for element in items[0].iter() if element.tag.endswith("}SubjectAddressDetails"))
        address.remove(next(element for element in address if element.tag.endswith("}CityName")))
    elif mutation in {"communication_name", "communication_code"}:
        communication = next(element for element in items[0].iter() if element.tag.endswith("}CommunicationDetails"))
        if mutation == "communication_name":
            structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
            ET.SubElement(communication, f"{{{structure.imported_namespaces['csdo']}}}CommunicationChannelName").text = "Телефон"
        else:
            next(element for element in communication if element.tag.endswith("}CommunicationChannelCode")).text = "XX"
    elif mutation == "country_codelist":
        next(element for element in items[0].iter() if element.tag.endswith("}UnifiedCountryCode")).set("codeListId", "OTHER")
    elif mutation == "attachment":
        structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
        ET.SubElement(items[0], f"{{{structure.imported_namespaces['ipcdo']}}}AccompanyingDocumentsDetails")
    elif mutation == "status_11":
        next(element for element in _status_of(items[1]) if element.tag.endswith("}StatusCode")).text = "12"
    else:
        next(element for element in _origin_of(items[0]) if element.tag.endswith("}GoodsPropertiesDescriptionText")).set("featureKindCode", "TEST")
    _assert_rule_fails(message, document, rule_id)


@pytest.mark.parametrize("rule_id, mutation", [
    ("P.SP.03.MSG.006.REQ.007.doc_id", "doc_id"),
    ("P.SP.03.MSG.006.REQ.007.receipt_date", "receipt_date"),
])
def test_msg006_req007_document_identifier_equality_real_xml(rule_id, mutation):
    message = "P.SP.03.MSG.006"
    document = _two_register_document(message, identifier_pair="document")
    items = _register_items(document)
    _assert_rule_passes(message, document, rule_id)
    local_name = "DocId" if mutation == "doc_id" else "IPDocReceiptDate"
    next(element for element in items[1] if element.tag.endswith("}" + local_name)).text = "DOC-OTHER" if mutation == "doc_id" else "2026-10-02"
    _assert_rule_fails(message, document, rule_id)


@pytest.mark.parametrize("rule_id, mutation", [
    ("P.SP.03.MSG.006.REQ.037", "forbidden_right"),
    ("P.SP.03.MSG.006.REQ.038", "publication"),
    ("P.SP.03.MSG.006.REQ.040.or_cardinality", "second_original"),
    ("P.SP.03.MSG.006.REQ.040.or_language", "original_language"),
    ("P.SP.03.MSG.006.REQ.041", "translated_language"),
    ("P.SP.03.MSG.006.REQ.044", "status_02"),
])
def test_msg006_ao_production_rules_real_xml(rule_id, mutation):
    message = "P.SP.03.MSG.006"
    document = _two_register_document(message, kind="AO")
    items = _register_items(document)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    _assert_rule_passes(message, document, rule_id)
    origin = _origin_of(items[0])
    if mutation == "forbidden_right":
        ET.SubElement(items[0], f"{{{namespaces['ipcdo']}}}ApellationOfOriginEAEURightDetails")
    elif mutation == "publication":
        _remove_direct_children(origin, "PublicationDate")
    elif mutation == "second_original":
        extra = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}ApellationOfOriginName")
        extra.text = "Другое НМПТ"
        extra.set("nameRepresentationKindCode", "OR")
        extra.set("languageCode", "RU")
    elif mutation == "original_language":
        next(element for element in origin if element.tag.endswith("}ApellationOfOriginName")).attrib.pop("languageCode", None)
    elif mutation == "translated_language":
        extra = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}ApellationOfOriginName")
        extra.text = "Перевод"
        extra.set("nameRepresentationKindCode", "TR")
        extra.set("languageCode", "RU")
    else:
        next(element for element in _status_of(items[1]) if element.tag.endswith("}StatusCode")).text = "03"
    _assert_rule_fails(message, document, rule_id)


def _apply_rh_register_mutation(message: str, document: ET.Element, mutation: str):
    items = _register_items(document)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    if mutation == "remove_second":
        document.remove(items[1])
    elif mutation == "resource_kind":
        next(element for element in items[0] if element.tag.endswith("}ResourceItemKindCode")).text = "AO"
    elif mutation in {"remove_start", "reverse_start", "remove_old_end", "old_end_before_start", "old_end_after_new_start", "new_end"}:
        first_period = next(element for element in items[0].iter() if element.tag.endswith("}ValidityPeriodDetails"))
        second_period = next(element for element in items[1].iter() if element.tag.endswith("}ValidityPeriodDetails"))
        if mutation == "remove_start":
            _remove_direct_children(first_period, "StartDateTime")
        elif mutation == "reverse_start":
            next(element for element in second_period if element.tag.endswith("}StartDateTime")).text = "2026-10-05T10:00:00+03:00"
        elif mutation == "remove_old_end":
            _remove_direct_children(first_period, "EndDateTime")
        elif mutation == "old_end_before_start":
            next(element for element in first_period if element.tag.endswith("}EndDateTime")).text = "2026-10-05T10:00:00+03:00"
        elif mutation == "old_end_after_new_start":
            next(element for element in first_period if element.tag.endswith("}EndDateTime")).text = "2026-10-09T10:00:00+03:00"
        else:
            ET.SubElement(second_period, f"{{{namespaces['csdo']}}}EndDateTime").text = "2026-10-09T10:00:00+03:00"
    elif mutation in {"remove_origin_id", "change_origin_id"}:
        origin = _origin_of(items[0] if mutation == "remove_origin_id" else items[1])
        target = next(element for element in origin if element.tag.endswith("}ApellationOfOriginEAEUId"))
        if mutation == "remove_origin_id":
            origin.remove(target)
        else:
            target.text = "AO-OTHER"
    elif mutation == "break_identifier_pair":
        _remove_direct_children(items[0], "ApplicationReceiptDate")
    elif mutation == "application_id":
        next(element for element in items[1] if element.tag.endswith("}ApellationOfOriginApplicationId")).text = "APP-OTHER"
    elif mutation == "application_date":
        next(element for element in items[1] if element.tag.endswith("}ApplicationReceiptDate")).text = "2026-10-02"
    elif mutation == "doc_id":
        next(element for element in items[1] if element.tag.endswith("}DocId")).text = "DOC-OTHER"
    elif mutation == "receipt_date":
        next(element for element in items[1] if element.tag.endswith("}IPDocReceiptDate")).text = "2026-10-02"
    elif mutation == "remove_goods":
        _remove_direct_children(_origin_of(items[0]), "ApellationOfOriginGoodsText")
    elif mutation in {"remove_certificate", "change_certificate"}:
        right = _right_of(items[0] if mutation == "remove_certificate" else items[1])
        target = next(element for element in right if element.tag.endswith("}ApellationOfOriginEAEUCertificateId"))
        if mutation == "remove_certificate":
            right.remove(target)
        else:
            target.text = "CERT-OTHER"
    elif mutation == "party_kind":
        next(element for element in _party_of(items[0]) if element.tag.endswith("}IPPartyKindCode")).text = "AP"
    elif mutation == "party_country":
        party = _party_of(items[0])
        party.remove(next(element for element in party if element.tag.endswith("}UnifiedCountryCode")))
    elif mutation == "party_language":
        next(element for element in _party_of(items[0]) if element.tag.endswith("}IPSubjectName")).set("languageCode", "EN")
    elif mutation == "party_address_kind":
        address = next(element for element in _party_of(items[0]) if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}AddressKindCode")).text = "1"
    elif mutation == "correspondence_subject":
        correspondence = _correspondence_of(items[0])
        correspondence.remove(next(element for element in correspondence if element.tag.endswith("}SubjectName")))
    elif mutation == "correspondence_country":
        address = next(element for element in _correspondence_of(items[0]) if element.tag.endswith("}SubjectAddressDetails"))
        next(element for element in address if element.tag.endswith("}UnifiedCountryCode")).text = "US"
    elif mutation in {"authority_name", "origin_office"}:
        authority = next(element for element in items[0] if element.tag.endswith("}PatentAuthorityDetails"))
        if mutation == "authority_name":
            authority.remove(next(element for element in authority if element.tag.endswith("}AuthorityName")))
        else:
            next(element for element in authority if element.tag.endswith("}OriginOfficeIndicator")).text = "0"
    elif mutation == "address_city":
        address = next(element for element in items[0].iter() if element.tag.endswith("}SubjectAddressDetails"))
        address.remove(next(element for element in address if element.tag.endswith("}CityName")))
    elif mutation in {"communication_name", "communication_code"}:
        communication = next(element for element in items[0].iter() if element.tag.endswith("}CommunicationDetails"))
        if mutation == "communication_name":
            ET.SubElement(communication, f"{{{namespaces['csdo']}}}CommunicationChannelName").text = "Телефон"
        else:
            next(element for element in communication if element.tag.endswith("}CommunicationChannelCode")).text = "XX"
    elif mutation == "country_codelist":
        next(element for element in items[0].iter() if element.tag.endswith("}UnifiedCountryCode")).set("codeListId", "OTHER")
    elif mutation == "attachment":
        ET.SubElement(items[0], f"{{{namespaces['ipcdo']}}}AccompanyingDocumentsDetails")
    elif mutation == "status":
        next(element for element in _status_of(items[1]) if element.tag.endswith("}StatusCode")).text = "XX"
    elif mutation == "doc_validity":
        next(
            element
            for element in _right_of(items[1])
            if element.tag.endswith("}DocValidityDate")
        ).text = "2031-01-01"
    else:
        raise AssertionError(f"Unknown mutation: {mutation}")


MSG007_RULE_CASES = [
    ("P.SP.03.MSG.007.REQ.001", "remove_second", "application"),
    ("P.SP.03.MSG.007.REQ.002", "resource_kind", "application"),
    ("P.SP.03.MSG.007.REQ.003.presence", "remove_start", "application"),
    ("P.SP.03.MSG.007.REQ.003.order", "reverse_start", "application"),
    ("P.SP.03.MSG.007.REQ.004.presence", "remove_old_end", "application"),
    ("P.SP.03.MSG.007.REQ.004.after_old_start", "old_end_before_start", "application"),
    ("P.SP.03.MSG.007.REQ.004.before_new_start", "old_end_after_new_start", "application"),
    ("P.SP.03.MSG.007.REQ.005", "new_end", "application"),
    ("P.SP.03.MSG.007.REQ.006.presence", "remove_origin_id", "application"),
    ("P.SP.03.MSG.007.REQ.006.equality", "change_origin_id", "application"),
    ("P.SP.03.MSG.007.REQ.007.combination", "break_identifier_pair", "application"),
    ("P.SP.03.MSG.007.REQ.007.application_id", "application_id", "application"),
    ("P.SP.03.MSG.007.REQ.007.application_date", "application_date", "application"),
    ("P.SP.03.MSG.007.REQ.007.doc_id", "doc_id", "document"),
    ("P.SP.03.MSG.007.REQ.007.receipt_date", "receipt_date", "document"),
    ("P.SP.03.MSG.007.REQ.012", "remove_goods", "application"),
    ("P.SP.03.MSG.007.REQ.014", "remove_certificate", "application"),
    ("P.SP.03.MSG.007.REQ.015", "change_certificate", "application"),
    ("P.SP.03.MSG.007.REQ.017", "party_kind", "application"),
    ("P.SP.03.MSG.007.REQ.018", "party_country", "application"),
    ("P.SP.03.MSG.007.REQ.019", "party_language", "application"),
    ("P.SP.03.MSG.007.REQ.020", "party_address_kind", "application"),
    ("P.SP.03.MSG.007.REQ.021", "correspondence_subject", "application"),
    ("P.SP.03.MSG.007.REQ.022", "correspondence_country", "application"),
    ("P.SP.03.MSG.007.REQ.025", "authority_name", "application"),
    ("P.SP.03.MSG.007.REQ.026", "origin_office", "application"),
    ("P.SP.03.MSG.007.REQ.027", "address_city", "application"),
    ("P.SP.03.MSG.007.REQ.028", "communication_name", "application"),
    ("P.SP.03.MSG.007.REQ.029", "communication_code", "application"),
    ("P.SP.03.MSG.007.REQ.030", "country_codelist", "application"),
    ("P.SP.03.MSG.007.REQ.031", "attachment", "application"),
    ("P.SP.03.MSG.007.REQ.033", "status", "application"),
]


@pytest.mark.parametrize("rule_id, mutation, identifier_pair", MSG007_RULE_CASES)
def test_msg007_safe_production_rules_real_xml(rule_id, mutation, identifier_pair):
    message = "P.SP.03.MSG.007"
    document = _two_register_document(message, identifier_pair=identifier_pair)
    _assert_rule_passes(message, document, rule_id)
    _apply_rh_register_mutation(message, document, mutation)
    _assert_rule_fails(message, document, rule_id)


MSG008_RULE_CASES = [
    (rule_id.replace("P.SP.03.MSG.007.", "P.SP.03.MSG.008."), mutation, identifier_pair)
    for rule_id, mutation, identifier_pair in MSG007_RULE_CASES
] + [("P.SP.03.MSG.008.REQ.034", "doc_validity", "application")]


@pytest.mark.parametrize("rule_id, mutation, identifier_pair", MSG008_RULE_CASES)
def test_msg008_safe_production_rules_real_xml(rule_id, mutation, identifier_pair):
    message = "P.SP.03.MSG.008"
    document = _two_register_document(message, identifier_pair=identifier_pair)
    _assert_rule_passes(message, document, rule_id)
    _apply_rh_register_mutation(message, document, mutation)
    _assert_rule_fails(message, document, rule_id)


@pytest.mark.parametrize("message", ["P.SP.03.MSG.013", "P.SP.03.MSG.014"])
def test_register_changed_item_end_datetime_forbidden_real_xml(message):
    rule = f"{message}.REQ.005"
    document = _register_rule_document(message, require_attachment=True)
    if message == "P.SP.03.MSG.013":
        first, second = _register_items(document)
    else:
        first = next(
            element
            for element in document
            if element.tag.endswith("}ApellationOfOriginRegisterItemDetails")
        )
        second = deepcopy(first)
        document.append(second)
    _assert_rule_passes(message, document, rule)

    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    period = next(element for element in second.iter() if element.tag.endswith("}ValidityPeriodDetails"))
    ET.SubElement(
        period,
        f"{{{structure.imported_namespaces['csdo']}}}EndDateTime",
    ).text = "2026-10-07T10:00:00+03:00"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", ["P.SP.03.MSG.014", "P.SP.03.MSG.015"])
def test_register_resource_item_kind_rh_real_xml(message):
    rule = f"{message}.REQ.002"
    document = _register_rule_document(
        message,
        require_attachment=(message == "P.SP.03.MSG.014"),
    )
    item = next(
        element
        for element in document
        if element.tag.endswith("}ApellationOfOriginRegisterItemDetails")
    )
    kind = next(element for element in item if element.tag.endswith("}ResourceItemKindCode"))
    kind.text = "RH"
    _assert_rule_passes(message, document, rule)
    kind.text = "AO"
    _assert_rule_fails(message, document, rule)


@pytest.mark.parametrize("message", ["P.SP.03.MSG.013", "P.SP.03.MSG.014"])
@pytest.mark.parametrize(
    "req,mutation",
    [
        (17, "party_kind"),
        (20, "party_address_kind"),
        (22, "correspondence_country"),
    ],
)
def test_msg013_014_rh_conditional_rules_real_xml(message, req, mutation):
    rule = f"{message}.REQ.{req:03d}"
    document = _register_rule_document(message)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    item = next(
        element
        for element in document
        if element.tag.endswith("}ApellationOfOriginRegisterItemDetails")
    )
    _normalise_register_item(item, namespaces, "RH")
    geographic = next(
        element
        for element in item.iter()
        if element.tag.endswith("}GeographicRegionDescriptionTextDetails")
    )
    country = _ensure_child(geographic, namespaces["csdo"], "UnifiedCountryCode", "RU")
    country.set("codeListId", "ВОИС ST.3")
    _append_register_attachment(message, item)

    _assert_rule_passes(message, document, rule)
    _apply_rh_register_mutation(message, document, mutation)
    result = _validate_document(message, document)
    assert not result.is_valid
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", rule)
    ]


@pytest.mark.parametrize(
    "req,mutation",
    [
        (12, "remove_goods"),
        (14, "remove_certificate"),
        (18, "party_country"),
        (19, "party_language"),
        (21, "correspondence_subject"),
    ],
)
@pytest.mark.parametrize("message", ["P.SP.03.MSG.013", "P.SP.03.MSG.014"])
def test_msg013_014_rh_inherited_shape_rules_real_xml(req, mutation, message):
    rule = f"{message}.REQ.{req:03d}"
    document = _register_rule_document(message)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    item = next(
        element
        for element in document
        if element.tag.endswith("}ApellationOfOriginRegisterItemDetails")
    )
    _normalise_register_item(item, namespaces, "RH")
    geographic = next(
        element
        for element in item.iter()
        if element.tag.endswith("}GeographicRegionDescriptionTextDetails")
    )
    country = _ensure_child(geographic, namespaces["csdo"], "UnifiedCountryCode", "RU")
    country.set("codeListId", "ВОИС ST.3")
    _append_register_attachment(message, item)

    _assert_rule_passes(message, document, rule)
    if message == "P.SP.03.MSG.013" and req == 14:
        for register_item in _register_items(document):
            right = _right_of(register_item)
            right.remove(
                next(
                    element
                    for element in right
                    if element.tag.endswith("}ApellationOfOriginEAEUCertificateId")
                )
            )
    else:
        _apply_rh_register_mutation(message, document, mutation)
    result = _validate_document(message, document)
    assert not result.is_valid
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", rule)
    ]


@pytest.mark.parametrize(
    "rule_id,mutation,identifier_pair",
    [
        ("P.SP.03.MSG.013.REQ.003.presence", "remove_start", "application"),
        ("P.SP.03.MSG.013.REQ.003.order", "reverse_start", "application"),
        ("P.SP.03.MSG.013.REQ.004.presence", "remove_old_end", "application"),
        ("P.SP.03.MSG.013.REQ.004.after_old_start", "old_end_before_start", "application"),
        ("P.SP.03.MSG.013.REQ.004.before_new_start", "old_end_after_new_start", "application"),
        ("P.SP.03.MSG.013.REQ.006.presence", "remove_origin_id", "application"),
        ("P.SP.03.MSG.013.REQ.006.equality", "change_origin_id", "application"),
        ("P.SP.03.MSG.013.REQ.007.combination", "break_identifier_pair", "application"),
        ("P.SP.03.MSG.013.REQ.007.application_id", "application_id", "application"),
        ("P.SP.03.MSG.013.REQ.007.application_date", "application_date", "application"),
        ("P.SP.03.MSG.013.REQ.007.doc_id", "doc_id", "document"),
        ("P.SP.03.MSG.013.REQ.007.receipt_date", "receipt_date", "document"),
        ("P.SP.03.MSG.013.REQ.015", "change_certificate", "application"),
        ("P.SP.03.MSG.013.REQ.036", "status", "application"),
    ],
)
def test_msg013_change_pair_rules_real_xml(rule_id, mutation, identifier_pair):
    message = "P.SP.03.MSG.013"
    document = _two_register_document(message, identifier_pair=identifier_pair)
    _assert_rule_passes(message, document, rule_id)
    _apply_rh_register_mutation(message, document, mutation)
    _assert_rule_fails(message, document, rule_id)


@pytest.mark.parametrize(
    "rule_id,mutation",
    [
        ("P.SP.03.MSG.013.REQ.041", "publication"),
        ("P.SP.03.MSG.013.REQ.043.or_cardinality", "second_original"),
        ("P.SP.03.MSG.013.REQ.043.or_language", "original_language"),
        ("P.SP.03.MSG.013.REQ.047", "status_02"),
    ],
)
def test_msg013_ao_change_rules_real_xml(rule_id, mutation):
    message = "P.SP.03.MSG.013"
    document = _two_register_document(message, kind="AO")
    items = _register_items(document)
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    _assert_rule_passes(message, document, rule_id)
    origin = _origin_of(items[0])
    if mutation == "publication":
        _remove_direct_children(origin, "PublicationDate")
    elif mutation == "second_original":
        extra = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}ApellationOfOriginName")
        extra.text = "Другое НМПТ"
        extra.set("nameRepresentationKindCode", "OR")
        extra.set("languageCode", "RU")
    elif mutation == "original_language":
        next(element for element in origin if element.tag.endswith("}ApellationOfOriginName")).attrib.pop("languageCode", None)
    else:
        next(element for element in _status_of(items[1]) if element.tag.endswith("}StatusCode")).text = "03"
    _assert_rule_fails(message, document, rule_id)


def _msg013_ao_document():
    message = "P.SP.03.MSG.013"
    document = _two_register_document(message, kind="AO")
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    item = next(
        element
        for element in document
        if element.tag.endswith("}ApellationOfOriginRegisterItemDetails")
    )
    return document, item, namespaces


def test_msg013_req002_resource_item_kind_allowlist_real_xml():
    message = "P.SP.03.MSG.013"
    rule = f"{message}.REQ.002"
    document, item, _ = _msg013_ao_document()
    _assert_rule_passes(message, document, rule)
    for register_item in _register_items(document):
        next(
            element
            for element in register_item
            if element.tag.endswith("}ResourceItemKindCode")
        ).text = "XX"
    result = _validate_document(message, document)
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", rule)
    ]


@pytest.mark.parametrize("forbidden_local_name", ["ApellationOfOriginEAEURightDetails", "CorrespondenceAddressDetails"])
def test_msg013_req040_ao_forbidden_fields_real_xml(forbidden_local_name):
    message = "P.SP.03.MSG.013"
    rule = f"{message}.REQ.040"
    document, item, _ = _msg013_ao_document()
    _assert_rule_passes(message, document, rule)

    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    ET.SubElement(
        item,
        f"{{{structure.imported_namespaces['ipcdo']}}}{forbidden_local_name}",
    )

    result = _validate_document(message, document)
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", rule)
    ]


@pytest.mark.parametrize("mutation", ["representation", "language"])
def test_msg013_req044_additional_origin_name_attributes_real_xml(mutation):
    message = "P.SP.03.MSG.013"
    rule = f"{message}.REQ.044"
    document, item, namespaces = _msg013_ao_document()
    origin = _origin_of(item)
    additional = ET.SubElement(origin, f"{{{namespaces['ipsdo']}}}ApellationOfOriginName")
    additional.text = "ТЕСТОВОЕ НМПТ"
    additional.set("nameRepresentationKindCode", "CY")
    _assert_rule_passes(message, document, rule)

    if mutation == "representation":
        additional.set("nameRepresentationKindCode", "LA")
    else:
        additional.set("languageCode", "RU")
    result = _validate_document(message, document)
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", rule)
    ]


def _append_msg013_national_registration(
    item: ET.Element,
    namespaces,
    country_code: str,
    national_id: str,
    *,
    include_right: bool = False,
):
    registration = ET.SubElement(
        item,
        f"{{{namespaces['ipcdo']}}}ApellationOfOriginNationalRegistrationDetails",
    )
    country = ET.SubElement(registration, f"{{{namespaces['csdo']}}}UnifiedCountryCode")
    country.text = country_code
    country.set("codeListId", "ВОИС ST.3")
    ET.SubElement(
        registration,
        f"{{{namespaces['ipsdo']}}}ApellationOfOriginNationalId",
    ).text = national_id
    if include_right:
        ET.SubElement(registration, f"{{{namespaces['ipcdo']}}}IPRightDetails")
    return registration


def test_msg013_req023_national_registration_shape_real_xml():
    message = "P.SP.03.MSG.013"
    rule = f"{message}.REQ.023.shape"
    document = _two_register_document(message)
    item = _register_items(document)[0]
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    registration = _append_msg013_national_registration(
        item,
        namespaces,
        "RU",
        "NAT-001",
        include_right=True,
    )
    _assert_rule_passes(message, document, rule)

    right = next(element for element in registration if element.tag.endswith("}IPRightDetails"))
    registration.remove(right)
    result = _validate_document(message, document)
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", rule)
    ]


def test_msg013_req023_national_registration_country_unique_real_xml():
    message = "P.SP.03.MSG.013"
    rule = f"{message}.REQ.023.unique_country"
    document = _two_register_document(message)
    item = _register_items(document)[0]
    structure = EaeuXmlEngine.load_process(PACKAGE).get_structure(message, mode=GenerationMode.TEST)
    namespaces = structure.imported_namespaces
    _append_msg013_national_registration(item, namespaces, "RU", "NAT-001", include_right=True)
    _assert_rule_passes(message, document, rule)

    _append_msg013_national_registration(item, namespaces, "RU", "NAT-002", include_right=True)
    result = _validate_document(message, document)
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", rule)
    ]


def test_msg013_req045_national_registration_shape_real_xml():
    message = "P.SP.03.MSG.013"
    rule = f"{message}.REQ.045.shape"
    document, item, namespaces = _msg013_ao_document()
    registration = _append_msg013_national_registration(item, namespaces, "RU", "NAT-001")
    _assert_rule_passes(message, document, rule)

    ET.SubElement(
        registration,
        f"{{{namespaces['ipsdo']}}}RegistrationDate",
    ).text = "2026-10-01"
    result = _validate_document(message, document)
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", rule)
    ]


def test_msg013_req045_national_registration_country_unique_real_xml():
    message = "P.SP.03.MSG.013"
    rule = f"{message}.REQ.045.unique_country"
    document, item, namespaces = _msg013_ao_document()
    _append_msg013_national_registration(item, namespaces, "RU", "NAT-001")
    _assert_rule_passes(message, document, rule)

    _append_msg013_national_registration(item, namespaces, "RU", "NAT-002")
    result = _validate_document(message, document)
    assert [(issue.code, issue.rule_id) for issue in result.issues] == [
        ("STRUCTURED_RULE_FAILED", rule)
    ]
