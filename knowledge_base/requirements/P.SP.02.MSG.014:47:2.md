---
id: "P.SP.02.MSG.014:47:2"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.014"
requirement: "2"
structure: "R.IP.SP.02.002"
status: "OPEN_EXTERNAL_REGISTRY"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 555
source_table: "Table 47, item 2"
source_item: "REQ 2 (Table 47)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_EXTERNAL_REGISTRY"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.014:47:2

## Нормативное требование

в ресурсах Комиссии должна существовать активная запись заявки со статусом «01» или «02», у которой совокупность TrademarkApplicationId, StatusCode и StartDateTime совпадает с изменяемыми сведениями

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_EXTERNAL_REGISTRY

## Trace

OP22 → P.SP.02.PRC.022 → P.SP.02.TRN.012 → P.SP.02.MSG.014 → P.SP.02.MSG.014:47:2

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:TrademarkApplicationId; ipcdo:IPEntityStatusDetails/csdo:StatusCode; ipcdo:IPEntityStatusDetails/csdo:StartDateTime
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipsdo:TrademarkApplicationId; ipcdo:TrademarkApplicationDetails/ipcdo:IPEntityStatusDetails/csdo:StatusCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 555
- Printed page: 143
- Table/item: Table 47, item 2
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_555]]

## Project state

- Status: OPEN_EXTERNAL_REGISTRY
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 47. Требования к электронному документу (сведениям) P.SP.02.MSG.014", "page": 555, "source_id": "22OP-RULE-P.SP.02.MSG.014-T47-2", "status": "CONFIRMED", "table": "47", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "2", "location": "Таблица 47. Требования к электронному документу (сведениям) P.SP.02.MSG.014", "page": 555, "source_id": "22OP-RULE-P.SP.02.MSG.014-T47-2", "status": "CONFIRMED", "table": "47", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["47"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OPEN_EXTERNAL_REGISTRY
- Missing information: Required Commission/resource state is not available from local message XML.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.
