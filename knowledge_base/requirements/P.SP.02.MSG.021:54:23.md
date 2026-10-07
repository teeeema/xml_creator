---
id: "P.SP.02.MSG.021:54:23"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.021"
requirement: "23"
structure: "R.IP.SP.02.007"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 576
source_table: "Table 54, item 23"
source_item: "REQ 23 (Table 54)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.021:54:23

## Нормативное требование

Новое DocValidityDate должно быть больше остальных DocValidityDate в сообщении.

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.030 → P.SP.02.TRN.019 → P.SP.02.MSG.021 → P.SP.02.MSG.021:54:23

## XML

- Structure: R.IP.SP.02.007
- QName: csdo:DocValidityDate
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:IPDocumentDetails/csdo:DocValidityDate

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 576
- Printed page: 164
- Table/item: Table 54, item 23
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_576]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "23", "location": "Таблица 54", "page": 576, "source_id": "22OP-RULE-P.SP.02.MSG.021-T54-23", "status": "CONFIRMED", "table": "54", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "23", "location": "Таблица 54", "page": 576, "source_id": "22OP-RULE-P.SP.02.MSG.021-T54-23", "status": "CONFIRMED", "table": "54", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["54"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg021_end_to_end.py; P.SP.02_OP_22/tests/test_msg021_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg021_safe_mapping.py

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Date/set relationship needs previous union resource state; current XML cannot supply that state.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
