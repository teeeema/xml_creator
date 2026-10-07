import json, csv, os, sys
from pathlib import Path
from eaeu_xml.process_packages import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator, RuleStatus

BASE_DIR = Path("/Users/tema/Documents/Work/xml_creator")

with open(BASE_DIR / "codex_reports/OP26_P_MM_01/OP26_SAFE_IMPLEMENTATION_BATCH_MAP.csv") as f:
    batch_rows = list(csv.DictReader(f))

with open(BASE_DIR / "codex_reports/OP26_P_MM_01/mapped_structured_rules.json") as f:
    mapped_rules = json.load(f)

engine = EaeuXmlEngine.load_process(BASE_DIR / "P.MM.01_OP_26")
evaluator = StructuredRuleEvaluator()

def get_base_values(msg):
    if msg == "P.MM.01.MSG.001":
        return {
            "DrugRegistrationDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/CountryKindCode": "01",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/DrugApplicationKindCode": "02",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationStatusDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode": "01",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/RegistrationStatusCode": "01",
            "DrugRegistrationDetails/RegistrationNumberId": "RU/01/2026",
            "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime": "2026-08-24T00:00:00",
            "DrugRegistrationDetails/RegistrationKindCode": "01",
            "DrugRegistrationDetails/RegistrationDossierDocDetails": [None],
            "DrugRegistrationDetails/RegistrationDossierDocDetails/DrugRegistrationFileCode": "0101",
            "DrugRegistrationDetails/RegistrationDossierDocDetails/DrugAttributeEnumText": [None],
            "DrugRegistrationDetails/RegistrationDossierDocDetails/DrugAttributeEnumText/@AttributeKindCode": "01",
            "DrugRegistrationDetails/RegistrationDossierDocDetails/DrugAttributeEnumText/@DrugAttributeKindEnumCode": "01",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugPackageLayoutDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugPackageLayoutDetails/DrugPackageLayoutKindCode": "01",
        }
    if msg == "P.MM.01.MSG.002":
        return {
            "DrugRegistrationDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/CountryKindCode": "01",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/DrugApplicationKindCode": "02",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationStatusDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode": "06",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/RegistrationStatusCode": "03",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/RegistrationNumberId": "REG-001",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/RegistrationCertificateId": "RC-001",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/RegistrationCertificateIssueDate": "2026-08-24",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/RegistrationCertificateDurationDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/RegistrationCertificateDurationDetails/EndDateTime": "2031-08-24T00:00:00",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/DrugRegistrationSpecialConditionDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/DrugRegistrationSpecialConditionDetails/DrugUsageRestrictionKindCode": "01",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/DrugRegistrationSpecialConditionDetails/DrugUsageRestrictionText": "Restriction",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugGeneralCharacteristicDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugUsageInstructionDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/ExpertReportDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/RiskManagementPlanDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/QualityRegulatoryDocDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugPackageLayoutDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugPackageLayoutDetails/DrugPackageLayoutKindCode": "01",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateHolderDetails": [None],
            "DrugRegistrationDetails/RegistrationNumberId": "RU/01/2026",
            "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime": "2026-08-24T00:00:00",
            "DrugRegistrationDetails/RegistrationKindCode": "01",
            "DrugRegistrationDetails/DrugDetails": [None],
            "DrugRegistrationDetails/DrugDetails/DosageFormDetails": [None],
            "DrugRegistrationDetails/DrugDetails/DosageFormDetails/DosageFormCode": "DF-01",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationId": "APP-001",
        }
    if msg == "P.MM.01.MSG.003":
        return {
            "DrugRegistrationDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/CountryKindCode": "01",
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationStatusDetails": [None],
            "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode": "07",
            "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime": "2026-08-24T00:00:00",
            "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/EndDateTime": "2031-08-24T00:00:00",
        }
    if msg in ("P.MM.01.MSG.007", "P.MM.01.MSG.010"):
        return {
            "EDocHeader/EDocCode": "R.HC.MM.01.007",
            "RecordQuantity": 100,
        }
    if msg == "P.MM.01.MSG.012":
        return {
            "ApplicationId": "APP-123",
            "RegistrationKindCode": "01",
            "RegistrationDossierDocDetails": [None],
            "RegistrationDossierDocDetails/DrugRegistrationDocCode": "01001",
            "RegistrationDossierDocDetails/DocCopyBinaryText": "BASE64DATA",
        }
    if msg == "P.MM.01.MSG.014":
        return {
            "ApplicationId": "APP-123",
        }
    if msg == "P.MM.01.MSG.016":
        return {
            "ApplicationId": "APP-123",
            "ApprovalImpossibilityReasonCode": "01",
            "CountryDrugRegistrationDetails/CountryKindCode": "02",
        }
    if msg in ("P.MM.01.MSG.019", "P.MM.01.MSG.020", "P.MM.01.MSG.021"):
        return {
            "EDocHeader/EDocCode": "R.HC.MM.01.003",
            "ApplicationId": "APP-123",
            "RegistrationKindCode": "01",
            "RegistrationDossierDocDetails": [None],
            "RegistrationDossierDocDetails/RegistrationFileIndicator": "0",
            "RegistrationDossierDocDetails/DrugRegistrationFileCode": "0101",
            "RegistrationDossierDocDetails/DocCopyBinaryText": "BASE64DATA",
            "RegistrationDossierDocDetails/PdfBinaryText": "BASE64DATA",
            "RegistrationDossierDocDetails/DrugAttributeEnumText": [None],
            "RegistrationDossierDocDetails/DrugAttributeEnumText/@AttributeKindCode": "01",
            "RegistrationDossierDocDetails/DrugAttributeEnumText/@DrugAttributeKindEnumCode": "01",
        }
    if msg == "P.MM.01.MSG.023":
        return {
            "EDocHeader/EDocCode": "R.HC.MM.01.002",
            "ApplicationId": "APP-123",
            "DocAgreementIndicator": True,
            "DrugRegistrationFileCode": "0401",
            "RegistrationDossierDocDetails": [None],
            "RegistrationDossierDocDetails/RegistrationFileIndicator": "0",
            "RegistrationDossierDocDetails/DrugRegistrationFileCode": "0101",
            "RegistrationDossierDocDetails/DocCopyBinaryText": "BASE64DATA",
        }
    if msg == "P.MM.01.MSG.024":
        return {
            "EDocHeader/EDocCode": "R.HC.MM.01.002",
            "ApplicationId": "APP-123",
            "DrugRegistrationFileCode": "0101",
            "RegistrationDossierDocDetails": [None],
            "RegistrationDossierDocDetails/DocCopyBinaryText": "BASE64DATA",
        }
    if msg == "P.MM.01.MSG.025":
        return {
            "EDocHeader/EDocCode": "R.HC.MM.01.004",
            "ApplicationId": "APP-123",
        }
    if msg in ("P.MM.01.MSG.027", "P.MM.01.MSG.028"):
        return {
            "RegistrationNumberId": "REG-123",
            "RegistrationDossierDocDetails": [None],
            "RegistrationDossierDocDetails/RegistrationFileIndicator": "0",
            "RegistrationDossierDocDetails/DrugRegistrationFileCode": "0401",
            "RegistrationDossierDocDetails/DocCreationDate": "2026-08-24",
            "RegistrationDossierDocDetails/DocName": "Doc Name",
            "RegistrationDossierDocDetails/PdfBinaryText": "BASE64DATA",
        }
    return {}

all_pass = True
for msg, rules in mapped_rules.items():
    vals = get_base_values(msg)
    for r in rules:
        ev = evaluator.evaluate(r, vals)
        if ev.status != RuleStatus.PASS:
            print(f"FAIL base: [{msg}] {r['production_rule_id']} ({r['rule_id']}) -> {ev.message}")
            all_pass = False

print("All base evaluations pass?", all_pass)
