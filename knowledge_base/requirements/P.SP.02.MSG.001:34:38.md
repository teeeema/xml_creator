---
id: "P.SP.02.MSG.001:34:38"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.001"
requirement: "38"
structure: "R.IP.SP.02.002"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 522
source_table: "Table 34, item 38"
source_item: "REQ 38 (Table 34)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.001:34:38

## Нормативное требование

в составе реквизита «Технологические характеристики записи общего ресурса» (ccdo:ResourceItemStatusDetails) реквизит «Начальная дата и время» (csdo:StartDateTime) заполняется обязательно и соответствует дате и времени включения сведений в национальный раздел Единого реестра ТЗ Союза

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.001 → P.SP.02.TRN.001 → P.SP.02.MSG.001 → P.SP.02.MSG.001:34:38

## XML

- Structure: R.IP.SP.02.002
- QName: ccdo:ResourceItemStatusDetails; csdo:StartDateTime
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 522
- Printed page: 110
- Table/item: Table 34, item 38
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_522]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: P.SP.02.MSG.001.REQ.038
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "38", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 522, "source_id": "22OP-RULE-P.SP.02.MSG.001-38", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "38", "location": "Таблица 34. Требования к электронному документу (сведениям) P.SP.02.MSG.001", "page": 522, "source_id": "22OP-RULE-P.SP.02.MSG.001-38", "status": "CONFIRMED", "table": "34", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["34"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg001_structured_rules.py

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Full source condition includes external resource/registry state; only local fragments, if any, execute.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
