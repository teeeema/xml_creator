---
id: "P.SP.02.MSG.061:80:31"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.061"
requirement: "31"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 815
source_table: "Table 80, item 31"
source_item: "REQ 31 (Table 80)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.061:80:31

## Нормативное требование

в составе реквизита «Сведения об обращении заинтересованного лица о несоответствии обозначения, заявленного на регистрацию в качестве товарного знака Союза, требованиям Договора о товарных знаках» (ipcdo:TrademarkClaimDetails) должны быть заполнены следующие реквизиты: «Заинтересованное лицо» (ipcdo:StakeholderDetails); «Регистрационный номер обращения заинтересованного лица» (ipsdo:RequestId); «Дата обращения заинтересованного лица» (ipsdo:RequestDate); «Описание несоответствия» (ipsdo:InconsistencyText)

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.008 → P.SP.02.TRN.052 → P.SP.02.MSG.061 → P.SP.02.MSG.061:80:31

## XML

- Structure: R.IP.SP.02.002
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 815
- Printed page: 236
- Table/item: Table 80, item 31
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_815]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "31", "location": "Таблица 80", "page": 815, "source_id": "22OP-RULE-P.SP.02.MSG.061-T80-31", "status": "CONFIRMED", "table": "80", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "31", "location": "Таблица 80", "page": 815, "source_id": "22OP-RULE-P.SP.02.MSG.061-T80-31", "status": "CONFIRMED", "table": "80", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["80"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
