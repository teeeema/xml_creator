---
id: "P.SP.02.MSG.010:43:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.010"
requirement: "4"
structure: "R.IP.SP.02.002"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 547
source_table: "Table 43, item 4"
source_item: "REQ 4 (Table 43)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.010:43:4

## Нормативное требование

ipsdo:TrademarkApplicationId должен быть заполнен; должна существовать активная запись заявки со статусом «01» или «02» и совпадающим номером

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.018 → P.SP.02.TRN.008 → P.SP.02.MSG.010 → P.SP.02.MSG.010:43:4

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:TrademarkApplicationId
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 547
- Printed page: 135
- Table/item: Table 43, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_547]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: P.SP.02.MSG.010.REQ.4
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 43. Требования к электронному документу (сведениям) P.SP.02.MSG.010", "page": 547, "source_id": "22OP-RULE-P.SP.02.MSG.010-T43-4", "status": "CONFIRMED", "table": "43", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 43. Требования к электронному документу (сведениям) P.SP.02.MSG.010", "page": 547, "source_id": "22OP-RULE-P.SP.02.MSG.010-T43-4", "status": "CONFIRMED", "table": "43", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["43"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OTHER_OPEN
- Missing information: Only SAFE_PARTIAL/partial production fragments exist; whole requirement is not certified. No extra normative interpretation performed.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
