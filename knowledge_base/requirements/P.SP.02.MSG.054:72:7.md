---
id: "P.SP.02.MSG.054:72:7"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.054"
requirement: "7"
structure: "R.IP.SP.03.003"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 803
source_table: "Table 72, item 7"
source_item: "REQ 7 (Table 72)"
qname_status: "UNRESOLVED"
implementation_status: "CURRENT_EXECUTABLE_COVERAGE"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.054:72:7

## Нормативное требование

реквизиты «Регистрационный номер заявки на НМПТ Союза» (ipsdo:ApellationOfOriginApplicationId), «Номер документа» (csdo:DocId), «Сведения о пошлине за осуществление юридически значимых действий» (ipcdo:IPPaymentDetails), «Признак подтверждения уплаты пошлины» (ipsdo:DutyPaymentIndicator), «Сумма платежа» (csdo:PaymentAmount) не заполняются

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.033 → P.SP.02.TRN.049 → P.SP.02.MSG.054 → P.SP.02.MSG.054:72:7

## XML

- Structure: R.IP.SP.03.003
- QName: MISSING / UNRESOLVED
- Namespace: MISSING / UNRESOLVED
- Path: MISSING / UNRESOLVED

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 803
- Printed page: 224
- Table/item: Table 72, item 7
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_803]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "7", "location": "Таблица 72", "page": 803, "source_id": "22OP-RULE-P.SP.02.MSG.054-T72-7", "status": "CONFIRMED", "table": "72", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "7", "location": "Таблица 72", "page": 803, "source_id": "22OP-RULE-P.SP.02.MSG.054-T72-7", "status": "CONFIRMED", "table": "72", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["72"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: MISSING

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
