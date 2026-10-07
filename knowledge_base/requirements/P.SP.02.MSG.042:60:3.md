---
id: "P.SP.02.MSG.042:60:3"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.042"
requirement: "3"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 765
source_table: "Table 60, item 3"
source_item: "REQ 3 (Table 60)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.042:60:3

## Нормативное требование

при отсутствии в классификаторе видов документов, сведений и материалов значения, соответствующего виду документа «Ходатайство о преобразовании заявки на регистрацию товарного знака, знака обслуживания Евразийского экономического союза в заявку на регистрацию коллективного знака Евразийского экономического союза», в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails) реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) не заполняется, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) должен быть заполнен, и его значение должно соответствовать значению: «Ходатайство о преобразовании заявки на регистрацию товарного знака, знака обслуживания Евразийского экономического союза в заявку на регистрацию коллективного знака Евразийского экономического союза»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.019 → P.SP.02.TRN.037 → P.SP.02.MSG.042 → P.SP.02.MSG.042:60:3

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:TrademarkApplicationDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 765
- Printed page: 186
- Table/item: Table 60, item 3
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_765]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 60", "page": 765, "source_id": "22OP-RULE-P.SP.02.MSG.042-T60-3", "status": "CONFIRMED", "table": "60", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "3", "location": "Таблица 60", "page": 765, "source_id": "22OP-RULE-P.SP.02.MSG.042-T60-3", "status": "CONFIRMED", "table": "60", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["60"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg042_end_to_end.py; P.SP.02_OP_22/tests/test_msg042_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg042_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
