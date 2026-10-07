---
id: "P.SP.02.MSG.014:47:30"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.014"
requirement: "30"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 558
source_table: "Table 47, item 30"
source_item: "REQ 30 (Table 47)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.014:47:30

## Нормативное требование

если вид документа соответствует ходатайству об изменениях, связанных с передачей или переходом права на заявку, и IPPartyKindCode = «AS», в AccompanyingDocumentsDetails должна быть хотя бы одна запись о документе передачи (перехода) права

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.022 → P.SP.02.TRN.012 → P.SP.02.MSG.014 → P.SP.02.MSG.014:47:30

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:AccompanyingDocumentsDetails; ipsdo:IPDocKindCode; ipsdo:IPPartyKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindCode; ipcdo:IPPartyDetails/ipsdo:IPPartyKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 558
- Printed page: 146
- Table/item: Table 47, item 30
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_558]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "30", "location": "Таблица 47. Требования к электронному документу (сведениям) P.SP.02.MSG.014", "page": 558, "source_id": "22OP-RULE-P.SP.02.MSG.014-T47-30", "status": "CONFIRMED", "table": "47", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "30", "location": "Таблица 47. Требования к электронному документу (сведениям) P.SP.02.MSG.014", "page": 558, "source_id": "22OP-RULE-P.SP.02.MSG.014-T47-30", "status": "CONFIRMED", "table": "47", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["47"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Required document/priority kind or membership needs confirmed classifier/reference data.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
