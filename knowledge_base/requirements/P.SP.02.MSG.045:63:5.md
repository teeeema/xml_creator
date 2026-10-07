---
id: "P.SP.02.MSG.045:63:5"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.045"
requirement: "5"
structure: "R.IP.SP.02.002"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 775
source_table: "Table 63, item 5"
source_item: "REQ 5 (Table 63)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.045:63:5

## Нормативное требование

при отсутствии в классификаторе видов документов, сведений и материалов значений, соответствующих видам документов: «Ходатайство о внесении изменений в заявку на регистрацию товарного знака, знака обслуживания Евразийского экономического союза в отношении заявленного обозначения, перечня товаров, адреса для ведения переписки, сведений о представителе заявителя, а также исправлений технического характера»; «Ходатайство о внесении изменений в заявку на регистрацию коллективного знака Евразийского экономического союза в отношении заявленного обозначения, перечня товаров, адреса для ведения переписки, сведений о представителе заявителя, устава (положения) коллективного знака Евразийского экономического союза, а также исправлений технического характера»; «Ходатайство о внесении в заявку на регистрацию товарного знака, знака обслуживания Евразийского экономического союза изменений, касающихся сведений о заявителе и связанных с передачей или переходом права на заявку на регистрацию товарного знака, знака обслуживания Евразийского экономического союза»; «Ходатайство о внесении изменения сведений о заявителе в заявку на регистрацию коллективного знака Евразийского экономического союза вследствие изменения наименования (фамилии, имени, отчества (при наличии)) или места нахождения (места жительства)» реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) не заполняется, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) должен быть заполнен, и его значение должно соответствовать значению указанных видов документов

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.022 → P.SP.02.TRN.040 → P.SP.02.MSG.045 → P.SP.02.MSG.045:63:5

## XML

- Structure: R.IP.SP.02.002
- QName: ipsdo:IPDocKindCode
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipsdo:IPDocKindCode

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 775
- Printed page: 196
- Table/item: Table 63, item 5
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_775]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 63", "page": 775, "source_id": "22OP-RULE-P.SP.02.MSG.045-T63-5", "status": "CONFIRMED", "table": "63", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "5", "location": "Таблица 63", "page": 775, "source_id": "22OP-RULE-P.SP.02.MSG.045-T63-5", "status": "CONFIRMED", "table": "63", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["63"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg045_end_to_end.py; P.SP.02_OP_22/tests/test_msg045_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg045_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
