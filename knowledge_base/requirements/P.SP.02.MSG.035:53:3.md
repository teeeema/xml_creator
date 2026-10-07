---
id: "P.SP.02.MSG.035:53:3"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.035"
requirement: "3"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 569
source_table: "Table 53, item 3"
source_item: "REQ 3 (Table 53)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.035:53:3

## Нормативное требование

Если CancellationStatusIndicator хотя бы для одного GoodsBaseDetails = «1», должен быть второй экземпляр с регистрацией нового ТЗ Союза.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.011 → P.SP.02.TRN.030 → P.SP.02.MSG.035 → P.SP.02.MSG.035:53:3

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:TrademarkApplicationId
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 569
- Printed page: 157
- Table/item: Table 53, item 3
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_569]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: P.SP.02.MSG.035.T53.REQ.3
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 53", "page": 749, "source_id": "22OP-RULE-P.SP.02.MSG.035-T53-3", "status": "CONFIRMED", "table": "53", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 53", "page": 569, "source_id": "22OP-RULE-P.SP.02.MSG.020-T53-3", "status": "CONFIRMED", "table": "53", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["53"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg035_end_to_end.py; P.SP.02_OP_22/tests/test_msg035_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg035_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
