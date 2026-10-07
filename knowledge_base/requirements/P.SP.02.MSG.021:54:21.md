---
id: "P.SP.02.MSG.021:54:21"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.021"
requirement: "21"
structure: "R.IP.SP.02.007"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 575
source_table: "Table 54, item 21"
source_item: "REQ 21 (Table 54)"
qname_status: "UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.021:54:21

## Нормативное требование

В существующей записи количество DocValidityDate должно быть на один меньше, чем в сообщении.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.030 → P.SP.02.TRN.019 → P.SP.02.MSG.021 → P.SP.02.MSG.021:54:21

## XML

- Structure: R.IP.SP.02.007
- QName: UNRESOLVED: see canonical source row
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 575
- Printed page: 163
- Table/item: Table 54, item 21
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_575]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: P.SP.02.MSG.021.T54.REQ.21
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "21", "location": "Таблица 54", "page": 575, "source_id": "22OP-RULE-P.SP.02.MSG.021-T54-21", "status": "CONFIRMED", "table": "54", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "21", "location": "Таблица 54", "page": 575, "source_id": "22OP-RULE-P.SP.02.MSG.021-T54-21", "status": "CONFIRMED", "table": "54", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["54"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg021_end_to_end.py; P.SP.02_OP_22/tests/test_msg021_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg021_safe_mapping.py

## Gap

- Reason: OTHER_OPEN
- Missing information: Only SAFE_PARTIAL/partial production fragments exist; whole requirement is not certified. No extra normative interpretation performed.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
