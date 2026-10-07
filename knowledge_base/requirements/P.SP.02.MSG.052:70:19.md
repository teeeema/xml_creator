---
id: "P.SP.02.MSG.052:70:19"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.052"
requirement: "19"
structure: "R.IP.SP.02.007"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 740
source_table: "Table 49, item 19"
source_item: "REQ 19 (Table 70)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.052:70:19

## Нормативное требование

если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) соответствует значению «1» – «товарный знак является коллективным», то должен быть заполнен экземпляр реквизита «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) в составе которого должен быть заполнен один из реквизитов «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) или «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) и их значения должны соответствовать коду или наименованию вида документа «Устав (положение) коллективного знака Евразийского экономического союза, содержащий наименование лица, уполномоченного на регистрацию коллективного знака Союза на свое имя, цель регистрации коллективного знака Союза, перечень субъектов, имеющих право на использование коллективного знака Союза, перечень и единые качественные или иные общие характеристики товаров, которые будут обозначаться коллективным знаком Союза, условия его использования, положения о порядке контроля за его использованием, положения об ответственности за нарушение его требований»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.029 → P.SP.02.TRN.047 → P.SP.02.MSG.052 → P.SP.02.MSG.052:70:19

## XML

- Structure: R.IP.SP.02.007
- QName: ipcdo:UnifiedRegisterRecordsDetails
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:UnifiedRegisterRecordsDetails

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 740
- Printed page: 161
- Table/item: Table 49, item 19
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 70 item 19 via range 6-19 (PDF p.794)
- Inherited source chain: 49
- Source page: [[sources/OP22_P_SP_02/pages/page_740]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 70", "page": 794, "source_id": "22OP-RULE-P.SP.02.MSG.052-T70-6-19", "status": "CONFIRMED", "table": "70", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "19", "location": "Таблица 49", "page": 740, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-19", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: P.SP.02_OP_22/tests/test_msg052_end_to_end.py; P.SP.02_OP_22/tests/test_msg052_repeatable_xml.py; P.SP.02_OP_22/tests/test_msg052_safe_mapping.py

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Collective charter document-kind code needs a confirmed classifier; no code/name shortcut.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
