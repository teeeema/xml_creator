---
id: "P.SP.02.MSG.003:36:32"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.003"
requirement: "32"
structure: "R.010"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 525
source_table: "Table 36, item 32"
source_item: "REQ 32 (Table 36)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.003:36:32

## Нормативное требование

в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails) реквизиты: «Национальная заявка на регистрацию товарного знака» (ipcdo:TrademarkNationalApplicationDetails), «Сведения об изменении заявителя» (ipcdo:ApplicantChangeDetails), «Сведения об обращении заинтересованного лица о несоответствии обозначения, заявленного на регистрацию в качестве товарного знака Союза, требованиям Договора о товарных знаках» (ipcdo:TrademarkClaimDetails), «Жалоба» (ipcdo:ComplaintDetails), «Текст решения о рассмотрении возражения заявителя» (ipsdo:DecisionOnComplaintText), «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) не заполняются

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.002 → P.SP.02.MSG.003 → P.SP.02.MSG.003:36:32

## XML

- Structure: R.010
- QName: ipcdo:TrademarkApplicationDetails; ipcdo:TrademarkNationalApplicationDetails; ipcdo:ApplicantChangeDetails; ipcdo:TrademarkClaimDetails; ipcdo:ComplaintDetails; ipsdo:DecisionOnComplaintText; ipcdo:AccompanyingDocumentsDetails
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 525
- Printed page: 113
- Table/item: Table 36, item 32
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_525]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: P.SP.02.MSG.003.T36.REQ.32; P.SP.02.MSG.003.T36.REQ.32; P.SP.02.MSG.003.T36.REQ.32; P.SP.02.MSG.003.T36.REQ.32; P.SP.02.MSG.003.T36.REQ.32
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 36. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 525, "source_id": "22OP-RULE-P.SP.02.MSG.003-T36-32", "status": "CONFIRMED", "table": "36", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "32", "location": "Таблица 36. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 525, "source_id": "22OP-RULE-P.SP.02.MSG.003-T36-32", "status": "CONFIRMED", "table": "36", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["36"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg003_embedded_one_of.py; P.SP.02_OP_22/tests/test_msg003_repeatable_xml_alignment.py; P.SP.02_OP_22/tests/test_msg003_table36_full_rules.py; P.SP.02_OP_22/tests/test_msg003_table36_safe_partial_inherited.py; P.SP.02_OP_22/tests/test_msg003_table37_safe_mapping.py

## Gap

- Reason: OTHER_OPEN
- Missing information: Only SAFE_PARTIAL/partial production fragments exist; whole requirement is not certified. No extra normative interpretation performed.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
