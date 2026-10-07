---
id: "P.SP.02.MSG.003:36:4"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.003"
requirement: "4"
structure: "R.010"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 524
source_table: "Table 36, item 4"
source_item: "REQ 4 (Table 36)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.003:36:4

## Нормативное требование

при отсутствии в классификаторе видов документов, сведений и материалов вида документа «Решение об отказе в регистрации товарного знака, знака обслуживания Евразийского экономического союза», реквизит «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) не заполняется, а реквизит «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) должен быть заполнен, и его значение должно быть «Решение об отказе в регистрации товарного знака, знака обслуживания Евразийского экономического союза»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.002 → P.SP.02.MSG.003 → P.SP.02.MSG.003:36:4

## XML

- Structure: R.010
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipsdo:IPDocKindCode; ipsdo:IPDocKindName

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 524
- Printed page: 112
- Table/item: Table 36, item 4
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_524]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 36. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 524, "source_id": "22OP-RULE-P.SP.02.MSG.003-T36-4", "status": "CONFIRMED", "table": "36", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "4", "location": "Таблица 36. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 524, "source_id": "22OP-RULE-P.SP.02.MSG.003-T36-4", "status": "CONFIRMED", "table": "36", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["36"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg003_embedded_one_of.py; P.SP.02_OP_22/tests/test_msg003_repeatable_xml_alignment.py; P.SP.02_OP_22/tests/test_msg003_table36_full_rules.py; P.SP.02_OP_22/tests/test_msg003_table36_safe_partial_inherited.py; P.SP.02_OP_22/tests/test_msg003_table37_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Existing classifier/reference-data gap retained; local safe fragment does not establish full membership/existence.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
