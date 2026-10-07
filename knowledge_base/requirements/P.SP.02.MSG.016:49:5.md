---
id: "P.SP.02.MSG.016:49:5"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.016"
requirement: "5"
structure: "R.IP.SP.02.007"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 562
source_table: "Table 49, item 5"
source_item: "REQ 5 (Table 49)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.016:49:5

## Нормативное требование

При отсутствии такого вида документа ipsdo:IPDocKindCode не заполняется, ipsdo:IPDocKindName заполняется нормативным наименованием.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.024 → P.SP.02.TRN.014 → P.SP.02.MSG.016 → P.SP.02.MSG.016:49:5

## XML

- Structure: R.IP.SP.02.007
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 562
- Printed page: 150
- Table/item: Table 49, item 5
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_562]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: P.SP.02.MSG.016.REQ.5
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 49", "page": 562, "source_id": "22OP-RULE-P.SP.02.MSG.016-T49-5", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 49", "page": 562, "source_id": "22OP-RULE-P.SP.02.MSG.016-T49-5", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg016_019_end_to_end.py; P.SP.02_OP_22/tests/test_msg016_019_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg016_019_safe_mapping.py

## Gap

- Reason: OTHER_OPEN
- Missing information: Only SAFE_PARTIAL/partial production fragments exist; whole requirement is not certified. No extra normative interpretation performed.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
