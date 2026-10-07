import json, csv, os, sys
from pathlib import Path

BASE_DIR = Path("/Users/tema/Documents/Work/xml_creator")

with open(BASE_DIR / "codex_reports/OP26_P_MM_01/OP26_SAFE_IMPLEMENTATION_BATCH_MAP.csv") as f:
    batch_rows = list(csv.DictReader(f))

yaml_data = {}
for ypath in sorted((BASE_DIR / "P.MM.01_OP_26/message_rules").glob("P.MM.01.MSG.*.yaml")):
    with open(ypath) as f:
        d = json.load(f)
        yaml_data[d["message_code"]] = (ypath, d)

row_by_prule = {}
for r in batch_rows:
    row_by_prule[(r["MSG"], r["production_rule"])] = r

def get_refs(msg, prule):
    d = yaml_data[msg][1]
    br = next(b for b in d["business_rules"] if b["rule_id"] == prule)
    return br.get("source_refs", [])

rules_map = {}

def reg(msg, prule, rule_body):
    cid = row_by_prule[(msg, prule)]["canonical_requirement_id"]
    rule = {
        "rule_id": cid,
        "production_rule_id": prule,
        "source_refs": get_refs(msg, prule)
    }
    rule.update(rule_body)
    rules_map[(msg, prule)] = rule

APP_KIND = "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/DrugApplicationKindCode"
COUNTRY_KIND = "DrugRegistrationDetails/DrugCountryRegistrationDetails/CountryKindCode"
APP_STATUS = "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode"
REG_STATUS = "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/RegistrationStatusCode"
REG_KIND = "DrugRegistrationDetails/RegistrationKindCode"
REG_NUM = "DrugRegistrationDetails/RegistrationNumberId"
APP_ID = "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationId"

# =========================================================================
# MSG.001 (39 rules: 16 B1, 21 B2, 2 B3)
# =========================================================================
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R1", {
    "kind": "selection_cardinality",
    "selector": {"collection": "DrugRegistrationDetails"},
    "min_occurs": 1, "max_occurs": 1
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R2", {
    "kind": "selection_cardinality",
    "selector": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "min_occurs": 1, "max_occurs": 1
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R3", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R4", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/EndDateTime",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R5", {
    "kind": "for_each",
    "selector": {"collection": APP_KIND},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02", "03", "04", "99"]}]}}]
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R8", {
    "kind": "for_each",
    "selector": {"collection": COUNTRY_KIND},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02"]}]}}]
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R17", {
    "kind": "for_each",
    "selector": {"collection": APP_STATUS},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02", "03", "04", "05", "06", "07", "08", "99"]}]}}]
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R18", {
    "kind": "for_each",
    "selector": {"collection": APP_STATUS},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "EQ", "value": "01"}]}}]
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R21", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/DrugDetails",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R22", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugGeneralCharacteristicDetails",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R23", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugUsageInstructionDetails",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R24", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/ExpertReportDetails",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R25", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/RiskManagementPlanDetails",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R26", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/QualityRegulatoryDocDetails",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R27", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/RegistrationCertificateHolderDetails",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R29", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugUsageInstructionDetails/PdfBinaryText",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R30", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/RegistrationDossierDocDetails/AnyDetails",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R37", {
    "kind": "for_each",
    "selector": {"collection": REG_STATUS},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02", "03", "04", "99"]}]}}]
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R6", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails"},
    "condition": {"field": "DrugCountryRegistrationDetails/DrugApplicationDetails/DrugApplicationKindCode", "operator": "IN", "value": ["01", "04"]},
    "target": {"field": "RegistrationNumberId"},
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R7", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails"},
    "condition": {"field": "DrugCountryRegistrationDetails/DrugApplicationDetails/DrugApplicationKindCode", "operator": "EQ", "value": "02"},
    "target": {"field": "RegistrationNumberId"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R9", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails"},
    "condition": {"field": "DrugCountryRegistrationDetails/CountryKindCode", "operator": "EQ", "value": "01"},
    "target": {"field": "DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationId"},
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R10", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails"},
    "condition": {"field": "DrugCountryRegistrationDetails/CountryKindCode", "operator": "EQ", "value": "02"},
    "target": {"field": "DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationId"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R12", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails"},
    "condition": {"field": "DrugCountryRegistrationDetails/CountryKindCode", "operator": "EQ", "value": "02"},
    "target": {"field": "RegistrationDossierDocDetails"},
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R13", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails"},
    "condition": {"field": "DrugCountryRegistrationDetails/DrugApplicationDetails/DrugApplicationKindCode", "operator": "IN", "value": ["01", "04"]},
    "target": {"field": "DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails"},
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R16", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails"},
    "condition": {"field": "DrugCountryRegistrationDetails/DrugApplicationDetails/DrugApplicationKindCode", "operator": "EQ", "value": "03"},
    "target": {"field": "DrugCountryRegistrationDetails/DrugApplicationChangeDetails"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R19", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails"},
    "condition": {"field": "DrugCountryRegistrationDetails/DrugApplicationDetails/DrugApplicationKindCode", "operator": "EQ", "value": "01"},
    "target": {"field": "RegistrationKindCode"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R20", {
    "kind": "for_each",
    "selector": {"collection": REG_KIND},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02"]}]}}]
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R31", {
    "kind": "conditional_fixed_value",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails"},
    "condition": {
        "all": [
            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0101"},
            {"field": "DrugAttributeEnumText", "operator": "NE", "value": None}
        ]
    },
    "target": {"field": "DrugAttributeEnumText/@DrugAttributeKindEnumCode"},
    "value": "01"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R32", {
    "kind": "conditional_fixed_value",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails"},
    "condition": {
        "all": [
            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0104"},
            {"field": "DrugAttributeEnumText", "operator": "NE", "value": None}
        ]
    },
    "target": {"field": "DrugAttributeEnumText/@DrugAttributeKindEnumCode"},
    "value": "02"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R33", {
    "kind": "conditional_fixed_value",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails"},
    "condition": {
        "all": [
            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0105"},
            {"field": "DrugAttributeEnumText", "operator": "NE", "value": None}
        ]
    },
    "target": {"field": "DrugAttributeEnumText/@DrugAttributeKindEnumCode"},
    "value": "01"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R36", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails"},
    "condition": {"field": "DrugApplicationKindCode", "operator": "EQ", "value": "99"},
    "target": {"field": "DrugApplicationKindName"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R38", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails"},
    "condition": {"field": "RegistrationStatusCode", "operator": "EQ", "value": "99"},
    "target": {"field": "RegistrationStatusName"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R39", {
    "kind": "for_each",
    "selector": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/DrugRegistrationSpecialConditionDetails/DrugUsageRestrictionKindCode"},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02", "03", "04", "05"]}]}}]
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R40", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/DrugRegistrationSpecialConditionDetails"},
    "condition": {"field": "DrugUsageRestrictionKindCode", "operator": "EQ", "value": "05"},
    "target": {"field": "DrugUsageRestrictionKindName"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R41", {
    "kind": "for_each",
    "selector": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationChangeDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "ChangeTypeCode", "operator": "NE", "value": None}, {"field": "ChangeTypeName", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R42", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/DrugApplicationChangedDetails"},
    "condition": {"field": "ChangeTypeCode", "operator": "EQ", "value": "99"},
    "target": {"field": "ChangeName"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R43", {
    "kind": "for_each",
    "selector": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "@AttributeKindCode", "operator": "NE", "value": None}, {"field": "@DrugAttributeKindEnumCode", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R44", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "condition": {"field": "@AttributeKindCode", "operator": "EQ", "value": "99"},
    "target": {"field": "@DrugAttributeKindEnumCode"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.001", "P.MM.01.MSG.001.R45", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails"},
    "condition": {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0199"},
    "target": {"field": "DrugRegistrationFileName"},
    "state": "REQUIRED"
})

# =========================================================================
# MSG.002 (44 rules: 8 B1, 33 B2, 3 B3)
# =========================================================================
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R1", {
    "kind": "selection_cardinality",
    "selector": {"collection": "DrugRegistrationDetails"},
    "min_occurs": 1, "max_occurs": 1
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R2", {
    "kind": "selection_cardinality",
    "selector": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "min_occurs": 1, "max_occurs": 1
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R21", {
    "kind": "for_each",
    "selector": {"collection": "DrugRegistrationDetails/DrugDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "DosageFormDetails/DosageFormCode", "operator": "NE", "value": None},
                {"field": "PackageFormDetails/PackageDetails/DosageFormCode", "operator": "NE", "value": None},
                {"field": "DosageFormDetails/DosageFormName", "operator": "NE", "value": None},
                {"field": "PackageFormDetails/PackageDetails/DosageFormName", "operator": "NE", "value": None},
                {"field": "DosageFormDetails/DosageFormAdditionalFeaturesDetails/RawPartMaterialText", "operator": "NE", "value": None},
                {"field": "PackageFormDetails/PackageDetails/DosageFormAdditionalFeaturesDetails/RawPartMaterialText", "operator": "NE", "value": None}
            ]
        }
    }]
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R3", {
    "kind": "for_each",
    "selector": {"collection": COUNTRY_KIND},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02"]}]}}]
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R8", {
    "kind": "for_each",
    "selector": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "ApplicationId", "operator": "NE", "value": None},
                {"field": "DrugRegistrationCertificateDetails/RegistrationCertificateId", "operator": "NE", "value": None}
            ]
        }
    }]
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R25", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R26", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/EndDateTime",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R28", {
    "kind": "for_each",
    "selector": {"collection": REG_KIND},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02"]}]}}]
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R29", {
    "kind": "for_each",
    "selector": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugPackageLayoutDetails/DrugPackageLayoutKindCode"},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02", "03"]}]}}]
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R30", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugDocumentsDetails/DrugUsageInstructionDetails/PdfBinaryText",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R31", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/RegistrationDossierDocDetails/AnyDetails",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R4", {
    "kind": "for_each",
    "selector": {"collection": APP_STATUS},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02", "03", "04", "05", "06", "07", "08", "99"]}]}}]
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R5", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "DrugCountryRegistrationDetails/CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "RegistrationNumberId"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R10", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateDetails/RegistrationNumberId"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R11", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateDetails/RegistrationCertificateId"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R12", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateDetails/RegistrationCertificateIssueDate"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R14", {
    "kind": "conditional_fixed_value",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateDetails/RegistrationStatusCode"},
    "value": "03"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R15", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateDetails/RegistrationCertificateDurationDetails"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R16", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateDetails/DrugRegistrationSpecialConditionDetails"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R17", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugDocumentsDetails/DrugGeneralCharacteristicDetails"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R18", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugDocumentsDetails/DrugUsageInstructionDetails"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R19", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugDocumentsDetails/DrugPackageLayoutDetails"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R20", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugDocumentsDetails/ExpertReportDetails"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R23", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugDocumentsDetails/QualityRegulatoryDocDetails"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R24", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateHolderDetails"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R27", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails"},
    "condition": {"field": "DrugCountryRegistrationDetails/DrugApplicationDetails/DrugApplicationKindCode", "operator": "EQ", "value": "01"},
    "target": {"field": "RegistrationKindCode"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R32", {
    "kind": "conditional_fixed_value",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails"},
    "condition": {
        "all": [
            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0101"},
            {"field": "DrugAttributeEnumText", "operator": "NE", "value": None}
        ]
    },
    "target": {"field": "DrugAttributeEnumText/@DrugAttributeKindEnumCode"},
    "value": "01"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R33", {
    "kind": "conditional_fixed_value",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails"},
    "condition": {
        "all": [
            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0104"},
            {"field": "DrugAttributeEnumText", "operator": "NE", "value": None}
        ]
    },
    "target": {"field": "DrugAttributeEnumText/@DrugAttributeKindEnumCode"},
    "value": "02"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R34", {
    "kind": "conditional_fixed_value",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails"},
    "condition": {
        "all": [
            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0105"},
            {"field": "DrugAttributeEnumText", "operator": "NE", "value": None}
        ]
    },
    "target": {"field": "DrugAttributeEnumText/@DrugAttributeKindEnumCode"},
    "value": "01"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R35", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails"},
    "condition": {"field": "DrugApplicationKindCode", "operator": "EQ", "value": "99"},
    "target": {"field": "DrugApplicationKindName"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R36", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails"},
    "condition": {"field": "RegistrationStatusCode", "operator": "EQ", "value": "99"},
    "target": {"field": "RegistrationStatusName"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R37", {
    "kind": "for_each",
    "selector": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/DrugRegistrationSpecialConditionDetails/DrugUsageRestrictionKindCode"},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02", "03", "04", "05"]}]}}]
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R38", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/DrugRegistrationSpecialConditionDetails"},
    "condition": {"field": "DrugUsageRestrictionKindCode", "operator": "EQ", "value": "05"},
    "target": {"field": "DrugUsageRestrictionKindName"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R39", {
    "kind": "for_each",
    "selector": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationChangeDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "ChangeTypeCode", "operator": "NE", "value": None}, {"field": "ChangeTypeName", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R40", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugRegistrationCertificateDetails/DrugApplicationChangedDetails"},
    "condition": {"field": "ChangeTypeCode", "operator": "EQ", "value": "99"},
    "target": {"field": "ChangeName"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R41", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails/DrugApplicationDetails/ApplicationStatusDetails"},
    "condition": {"field": "ApplicationStatusCode", "operator": "EQ", "value": "99"},
    "target": {"field": "ApplicationStatusName"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R42", {
    "kind": "for_each",
    "selector": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "@AttributeKindCode", "operator": "NE", "value": None}, {"field": "@DrugAttributeKindEnumCode", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R43", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "condition": {"field": "@AttributeKindCode", "operator": "EQ", "value": "99"},
    "target": {"field": "@DrugAttributeKindEnumCode"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R44", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails"},
    "condition": {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0199"},
    "target": {"field": "DrugRegistrationFileName"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R45", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateHolderDetails"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R46", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateDetails/RegistrationCertificateDurationDetails/EndDateTime"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R47", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateDetails/DrugRegistrationSpecialConditionDetails/DrugUsageRestrictionKindCode"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R48", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/DrugCountryRegistrationDetails"},
    "condition": {
        "all": [
            {"field": "CountryKindCode", "operator": "EQ", "value": "01"},
            {"field": "DrugApplicationDetails/ApplicationStatusDetails/ApplicationStatusCode", "operator": "EQ", "value": "06"}
        ]
    },
    "target": {"field": "DrugRegistrationCertificateDetails/DrugRegistrationSpecialConditionDetails/DrugUsageRestrictionText"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.002", "P.MM.01.MSG.002.R49", {
    "kind": "conditional_presence",
    "scope": {"collection": "DrugRegistrationDetails/RegistrationDossierDocDetails"},
    "condition": {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "99"},
    "target": {"field": "DrugRegistrationFileName"},
    "state": "REQUIRED"
})

# =========================================================================
# MSG.003 (6 rules: 5 B1, 1 B3)
# =========================================================================
reg("P.MM.01.MSG.003", "P.MM.01.MSG.003.R1", {
    "kind": "selection_cardinality",
    "selector": {"collection": "DrugRegistrationDetails"},
    "min_occurs": 1, "max_occurs": 1
})
reg("P.MM.01.MSG.003", "P.MM.01.MSG.003.R2", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/StartDateTime",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.003", "P.MM.01.MSG.003.R3", {
    "kind": "presence",
    "target": "DrugRegistrationDetails/ResourceItemStatusDetails/ValidityPeriodDetails/EndDateTime",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.003", "P.MM.01.MSG.003.R4", {
    "kind": "for_each",
    "selector": {"collection": APP_STATUS},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02", "03", "04", "05", "06", "07", "08", "99"]}]}}]
})
reg("P.MM.01.MSG.003", "P.MM.01.MSG.003.R5", {
    "kind": "for_each",
    "selector": {"collection": APP_STATUS},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["07", "08"]}]}}]
})
reg("P.MM.01.MSG.003", "P.MM.01.MSG.003.R6", {
    "kind": "for_each",
    "selector": {"collection": COUNTRY_KIND},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "EQ", "value": "01"}]}}]
})

# =========================================================================
# MSG.007 (2 rules: 1 B1, 1 B4)
# =========================================================================
reg("P.MM.01.MSG.007", "P.MM.01.MSG.007.R1", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "RecordQuantity", "operator": "EQ", "value": None},
                {"field": "RecordQuantity", "operator": "LE", "value": 5000}
            ]
        }
    }]
})
reg("P.MM.01.MSG.007", "P.MM.01.MSG.007.R2", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [
        {"kind": "presence", "target": {"field": "StartDateTime"}, "state": "FORBIDDEN"},
        {"kind": "presence", "target": {"field": "EndDateTime"}, "state": "FORBIDDEN"}
    ]
})

# =========================================================================
# MSG.010 (1 rule: 1 B4)
# =========================================================================
reg("P.MM.01.MSG.010", "P.MM.01.MSG.010.R1", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "RecordQuantity", "operator": "EQ", "value": None},
                {"field": "RecordQuantity", "operator": "LE", "value": 5000}
            ]
        }
    }]
})

# =========================================================================
# MSG.012 (5 rules: 5 B1)
# =========================================================================
reg("P.MM.01.MSG.012", "P.MM.01.MSG.012.R1", {
    "kind": "presence",
    "target": "ApplicationId",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.012", "P.MM.01.MSG.012.R2", {
    "kind": "presence",
    "target": "RegistrationNumberId",
    "state": "FORBIDDEN"
})
reg("P.MM.01.MSG.012", "P.MM.01.MSG.012.R3", {
    "kind": "presence",
    "target": "RegistrationKindCode",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.012", "P.MM.01.MSG.012.R4", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "DrugRegistrationDocCode", "operator": "EQ", "value": "01001"},
                {"field": "DrugRegistrationDocName", "operator": "NE", "value": None}
            ]
        }
    }]
})
reg("P.MM.01.MSG.012", "P.MM.01.MSG.012.R5", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "DocCopyBinaryText", "operator": "NE", "value": None},
                {"field": "AnyDetails", "operator": "NE", "value": None}
            ]
        }
    }]
})

# =========================================================================
# MSG.014 (1 rule: 1 B1)
# =========================================================================
reg("P.MM.01.MSG.014", "P.MM.01.MSG.014.R1", {
    "kind": "presence",
    "target": "RegistrationNumberId",
    "state": "FORBIDDEN"
})

# =========================================================================
# MSG.016 (3 rules: 3 B1)
# =========================================================================
reg("P.MM.01.MSG.016", "P.MM.01.MSG.016.R3", {
    "kind": "for_each",
    "selector": {"collection": "ApprovalImpossibilityReasonCode"},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["01", "02", "03", "04", "99"]}]}}]
})
reg("P.MM.01.MSG.016", "P.MM.01.MSG.016.R4", {
    "kind": "for_each",
    "selector": {"collection": "CountryDrugRegistrationDetails/CountryKindCode"},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "EQ", "value": "02"}]}}]
})
reg("P.MM.01.MSG.016", "P.MM.01.MSG.016.R5", {
    "kind": "presence",
    "target": "ApplicationId",
    "state": "REQUIRED"
})

# =========================================================================
# MSG.019 (11 rules: 4 B1, 7 B2)
# =========================================================================
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R1", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "ApplicationId", "operator": "NE", "value": None}, {"field": "RegistrationNumberId", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R2", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{"kind": "presence", "target": {"field": "PdfBinaryText"}, "state": "FORBIDDEN"}]
})
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R3", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{"kind": "presence", "target": {"field": "AnyDetails"}, "state": "FORBIDDEN"}]
})
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R6", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "@AttributeKindCode", "operator": "NE", "value": None}, {"field": "@DrugAttributeKindEnumCode", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R7", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "@AttributeKindCode", "operator": "EQ", "value": "99"},
        "target": {"field": "@DrugAttributeKindEnumCode"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R8", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "RegistrationFileIndicator", "operator": "NOT_IN", "value": ["0", False]},
                {"field": "DrugRegistrationFileCode", "operator": "NE", "value": None},
                {"field": "DrugRegistrationFileName", "operator": "NE", "value": None}
            ]
        }
    }]
})
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R9", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "99"},
        "target": {"field": "DrugRegistrationFileName"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R10", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "RegistrationFileIndicator", "operator": "NOT_IN", "value": ["1", True]},
                {"field": "DrugRegistrationDocCode", "operator": "NE", "value": None},
                {"field": "DrugRegistrationDocName", "operator": "NE", "value": None}
            ]
        }
    }]
})
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R11", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "DrugRegistrationDocCode", "operator": "EQ", "value": "99"},
        "target": {"field": "DrugRegistrationDocName"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R12", {
    "kind": "conditional_presence",
    "scope": {"collection": "EDocHeader/EDocCode"},
    "condition": {"field": "RegistrationNumberId", "operator": "NE", "value": None},
    "target": {"field": "ApplicationId"},
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.019", "P.MM.01.MSG.019.R13", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "@DrugAttributeKindEnumCode", "operator": "EQ", "value": "TEST"},
                {"field": "@DrugAttributeKindEnumCode", "operator": "IN", "value": ["01", "02", "03", "04", "05", "06", "99"]}
            ]
        }
    }]
})

# =========================================================================
# MSG.020 (7 rules: 2 B1, 5 B2)
# =========================================================================
reg("P.MM.01.MSG.020", "P.MM.01.MSG.020.R1", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "ApplicationId", "operator": "NE", "value": None}, {"field": "RegistrationNumberId", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.020", "P.MM.01.MSG.020.R3", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "PdfBinaryText", "operator": "NE", "value": None}, {"field": "AnyDetails", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.020", "P.MM.01.MSG.020.R6", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "@AttributeKindCode", "operator": "NE", "value": None}, {"field": "@DrugAttributeKindEnumCode", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.020", "P.MM.01.MSG.020.R7", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "@AttributeKindCode", "operator": "EQ", "value": "99"},
        "target": {"field": "@DrugAttributeKindEnumCode"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.020", "P.MM.01.MSG.020.R8", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "RegistrationFileIndicator", "operator": "NOT_IN", "value": ["0", False]},
                {"field": "DrugRegistrationFileCode", "operator": "NE", "value": None},
                {"field": "DrugRegistrationFileName", "operator": "NE", "value": None}
            ]
        }
    }]
})
reg("P.MM.01.MSG.020", "P.MM.01.MSG.020.R9", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "99"},
        "target": {"field": "DrugRegistrationFileName"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.020", "P.MM.01.MSG.020.R10", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "RegistrationFileIndicator", "operator": "NOT_IN", "value": ["1", True]},
                {"field": "DrugRegistrationDocCode", "operator": "NE", "value": None},
                {"field": "DrugRegistrationDocName", "operator": "NE", "value": None}
            ]
        }
    }]
})

# =========================================================================
# MSG.021 (14 rules: 2 B1, 11 B2, 1 B3)
# =========================================================================
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R1", {
    "kind": "presence",
    "target": "RegistrationKindCode",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R2", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "RegistrationKindCode", "operator": "EQ", "value": "02"},
        "target": {"field": "DrugRegistrationDocCode"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R3", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "RegistrationKindCode", "operator": "EQ", "value": "02"},
        "target": {"field": "DrugRegistrationFileCode"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R4", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "RegistrationKindCode", "operator": "EQ", "value": "01"},
        "target": {"field": "DrugRegistrationFileCode"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R5", {
    "kind": "conditional_fixed_value",
    "scope": {"collection": "RegistrationDossierDocDetails"},
    "condition": {
        "all": [
            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0101"},
            {"field": "DrugAttributeEnumText", "operator": "NE", "value": None}
        ]
    },
    "target": {"field": "DrugAttributeEnumText/@AttributeKindCode"},
    "value": "01"
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R6", {
    "kind": "conditional_fixed_value",
    "scope": {"collection": "RegistrationDossierDocDetails"},
    "condition": {
        "all": [
            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0104"},
            {"field": "DrugAttributeEnumText", "operator": "NE", "value": None}
        ]
    },
    "target": {"field": "DrugAttributeEnumText/@AttributeKindCode"},
    "value": "02"
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R7", {
    "kind": "conditional_fixed_value",
    "scope": {"collection": "RegistrationDossierDocDetails"},
    "condition": {
        "all": [
            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0105"},
            {"field": "DrugAttributeEnumText", "operator": "NE", "value": None}
        ]
    },
    "target": {"field": "DrugAttributeEnumText/@AttributeKindCode"},
    "value": "01"
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R8", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "DocCopyBinaryText", "operator": "NE", "value": None}, {"field": "AnyDetails", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R11", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "@AttributeKindCode", "operator": "NE", "value": None}, {"field": "@AttributeKindName", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R12", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugAttributeEnumText"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "@AttributeKindCode", "operator": "EQ", "value": "99"},
        "target": {"field": "@AttributeKindName"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R13", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "RegistrationFileIndicator", "operator": "NOT_IN", "value": ["0", False]},
                {"field": "DrugRegistrationFileCode", "operator": "NE", "value": None},
                {"field": "DrugRegistrationFileName", "operator": "NE", "value": None}
            ]
        }
    }]
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R14", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "99"},
        "target": {"field": "DrugRegistrationFileName"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R15", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "RegistrationFileIndicator", "operator": "NOT_IN", "value": ["1", True]},
                {"field": "DrugRegistrationDocCode", "operator": "NE", "value": None},
                {"field": "DrugRegistrationDocName", "operator": "NE", "value": None}
            ]
        }
    }]
})
reg("P.MM.01.MSG.021", "P.MM.01.MSG.021.R16", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "DrugRegistrationDocCode", "operator": "EQ", "value": "99"},
        "target": {"field": "DrugRegistrationDocName"},
        "state": "REQUIRED"
    }]
})

# =========================================================================
# MSG.023 (6 rules: 4 B1, 2 B2)
# =========================================================================
reg("P.MM.01.MSG.023", "P.MM.01.MSG.023.R1", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "0401"},
                {"field": "DrugRegistrationFileName", "operator": "NE", "value": None}
            ]
        }
    }]
})
reg("P.MM.01.MSG.023", "P.MM.01.MSG.023.R2", {
    "kind": "presence",
    "target": "ApplicationId",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.023", "P.MM.01.MSG.023.R3", {
    "kind": "presence",
    "target": "DocAgreementIndicator",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.023", "P.MM.01.MSG.023.R6", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "PdfBinaryText", "operator": "NE", "value": None}, {"field": "AnyDetails", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.023", "P.MM.01.MSG.023.R9", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "DrugRegistrationFileCode", "operator": "NE", "value": None},
                {"field": "DrugRegistrationFileName", "operator": "NE", "value": None}
            ]
        }
    }]
})
reg("P.MM.01.MSG.023", "P.MM.01.MSG.023.R10", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "99"},
        "target": {"field": "DrugRegistrationFileName"},
        "state": "REQUIRED"
    }]
})

# =========================================================================
# MSG.024 (5 rules: 4 B1, 1 B2)
# =========================================================================
reg("P.MM.01.MSG.024", "P.MM.01.MSG.024.R2", {
    "kind": "presence",
    "target": "ApplicationId",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.024", "P.MM.01.MSG.024.R3", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "PdfBinaryText", "operator": "NE", "value": None}, {"field": "AnyDetails", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.024", "P.MM.01.MSG.024.R8", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "DrugRegistrationFileCode", "operator": "NE", "value": None}, {"field": "DrugRegistrationFileName", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.024", "P.MM.01.MSG.024.R9", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "conditional_presence",
        "condition": {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "99"},
        "target": {"field": "DrugRegistrationFileName"},
        "state": "REQUIRED"
    }]
})
reg("P.MM.01.MSG.024", "P.MM.01.MSG.024.R10", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {
            "any": [
                {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": "TEST"},
                {"field": "DrugRegistrationFileCode", "operator": "IN", "value": ["0101", "0102", "0103", "0104", "0105", "0106", "0107", "0199", "0403", "0405", "0406"]}
            ]
        }
    }]
})

# =========================================================================
# MSG.025 (2 rules: 1 B2, 1 B3)
# =========================================================================
reg("P.MM.01.MSG.025", "P.MM.01.MSG.025.R1", {
    "kind": "for_each",
    "selector": {"collection": "EDocHeader/EDocCode"},
    "assertions": [{
        "kind": "condition",
        "condition": {"any": [{"field": "RegistrationNumberId", "operator": "NE", "value": None}, {"field": "ApplicationId", "operator": "NE", "value": None}]}
    }]
})
reg("P.MM.01.MSG.025", "P.MM.01.MSG.025.R2", {
    "kind": "conditional_presence",
    "scope": {"collection": "EDocHeader/EDocCode"},
    "condition": {"field": "RegistrationNumberId", "operator": "NE", "value": None},
    "target": {"field": "DrugRegistrationCertificateDetails/DocCreationDate"},
    "state": "REQUIRED"
})

# =========================================================================
# MSG.027 (7 rules: 1 B1, 4 B2, 2 B3)
# =========================================================================
reg("P.MM.01.MSG.027", "P.MM.01.MSG.027.R1", {
    "kind": "presence",
    "target": "RegistrationNumberId",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.027", "P.MM.01.MSG.027.R2", {
    "kind": "selection_cardinality",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "min_occurs": 1, "max_occurs": 1
})
reg("P.MM.01.MSG.027", "P.MM.01.MSG.027.R3", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [
        {"kind": "presence", "target": {"field": "RegistrationFileIndicator"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "DocCreationDate"}, "state": "REQUIRED"},
        {
            "kind": "condition",
            "condition": {
                "any": [
                    {
                        "all": [
                            {"field": "DrugRegistrationDocCode", "operator": "NE", "value": None},
                            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": None}
                        ]
                    },
                    {
                        "all": [
                            {"field": "DrugRegistrationDocCode", "operator": "EQ", "value": None},
                            {"field": "DrugRegistrationFileCode", "operator": "NE", "value": None}
                        ]
                    }
                ]
            }
        }
    ]
})
reg("P.MM.01.MSG.027", "P.MM.01.MSG.027.R4", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [
        {
            "kind": "conditional_presence",
            "condition": {"field": "RegistrationFileIndicator", "operator": "IN", "value": ["0", False]},
            "target": {"field": "DrugRegistrationFileCode"},
            "state": "REQUIRED"
        },
        {
            "kind": "conditional_presence",
            "condition": {"field": "RegistrationFileIndicator", "operator": "IN", "value": ["0", False]},
            "target": {"field": "DrugRegistrationDocCode"},
            "state": "FORBIDDEN"
        }
    ]
})
reg("P.MM.01.MSG.027", "P.MM.01.MSG.027.R5", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [
        {
            "kind": "conditional_presence",
            "condition": {"field": "RegistrationFileIndicator", "operator": "IN", "value": ["1", True]},
            "target": {"field": "DrugRegistrationDocCode"},
            "state": "REQUIRED"
        },
        {
            "kind": "conditional_presence",
            "condition": {"field": "RegistrationFileIndicator", "operator": "IN", "value": ["1", True]},
            "target": {"field": "DrugRegistrationFileCode"},
            "state": "FORBIDDEN"
        }
    ]
})
reg("P.MM.01.MSG.027", "P.MM.01.MSG.027.R6", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugRegistrationDocCode"},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["02002", "02010", "02005", "02004", "02006", "07004", "13028"]}]}}]
})
reg("P.MM.01.MSG.027", "P.MM.01.MSG.027.R7", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugRegistrationFileCode"},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "EQ", "value": "0401"}]}}]
})

# =========================================================================
# MSG.028 (6 rules: 3 B1, 1 B2, 2 B3)
# =========================================================================
reg("P.MM.01.MSG.028", "P.MM.01.MSG.028.R1", {
    "kind": "presence",
    "target": "RegistrationNumberId",
    "state": "REQUIRED"
})
reg("P.MM.01.MSG.028", "P.MM.01.MSG.028.R2", {
    "kind": "selection_cardinality",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "min_occurs": 1, "max_occurs": 1
})
reg("P.MM.01.MSG.028", "P.MM.01.MSG.028.R3", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [
        {"kind": "presence", "target": {"field": "RegistrationFileIndicator"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "DocName"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "DocCreationDate"}, "state": "REQUIRED"},
        {"kind": "presence", "target": {"field": "DocCopyBinaryText"}, "state": "REQUIRED"},
        {
            "kind": "condition",
            "condition": {
                "any": [
                    {
                        "all": [
                            {"field": "DrugRegistrationDocCode", "operator": "NE", "value": None},
                            {"field": "DrugRegistrationFileCode", "operator": "EQ", "value": None}
                        ]
                    },
                    {
                        "all": [
                            {"field": "DrugRegistrationDocCode", "operator": "EQ", "value": None},
                            {"field": "DrugRegistrationFileCode", "operator": "NE", "value": None}
                        ]
                    }
                ]
            }
        }
    ]
})
reg("P.MM.01.MSG.028", "P.MM.01.MSG.028.R4", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails"},
    "assertions": [
        {
            "kind": "conditional_presence",
            "condition": {"field": "RegistrationFileIndicator", "operator": "IN", "value": ["0", False]},
            "target": {"field": "DrugRegistrationFileCode"},
            "state": "REQUIRED"
        },
        {
            "kind": "conditional_presence",
            "condition": {"field": "RegistrationFileIndicator", "operator": "IN", "value": ["0", False]},
            "target": {"field": "DrugRegistrationDocCode"},
            "state": "FORBIDDEN"
        }
    ]
})
reg("P.MM.01.MSG.028", "P.MM.01.MSG.028.R6", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugRegistrationDocCode"},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "IN", "value": ["02002", "02010", "02005", "02004", "02006", "07004", "13028"]}]}}]
})
reg("P.MM.01.MSG.028", "P.MM.01.MSG.028.R7", {
    "kind": "for_each",
    "selector": {"collection": "RegistrationDossierDocDetails/DrugRegistrationFileCode"},
    "assertions": [{"kind": "condition", "condition": {"any": [{"field": "#text", "operator": "EQ", "value": "TEST"}, {"field": "#text", "operator": "EQ", "value": "0401"}]}}]
})

print(f"\nTOTAL ALL RULES MAPPED: {len(rules_map)} of {len(batch_rows)}")
assert len(rules_map) == len(batch_rows) == 159
print("ALL 159 RULES FULLY AND EXACTLY MAPPED!")

# Output mappings grouped by message to a json file
grouped = {}
for (m, prule), rdef in rules_map.items():
    grouped.setdefault(m, []).append(rdef)

with open(BASE_DIR / "codex_reports/OP26_P_MM_01/mapped_structured_rules.json", "w") as f:
    json.dump(grouped, f, ensure_ascii=False, indent=2)

print("Saved mapped structured rules to codex_reports/OP26_P_MM_01/mapped_structured_rules.json")
