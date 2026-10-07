---
id: "P.SP.02.MSG.031:49:19"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.031"
requirement: "19"
structure: "R.010"
status: "OPEN_CLASSIFIER"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 740
source_table: "Table 49, item 19"
source_item: "REQ 19 (Table 49)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OPEN_CLASSIFIER"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.031:49:19

## Нормативное требование

если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) соответствует значению «1» – «товарный знак является коллективным», то должен быть заполнен экземпляр реквизита «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails) в составе которого должен быть заполнен один из реквизитов «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) или «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) и их значения должны соответствовать коду или наименованию вида документа «Устав (положение) коллективного знака Евразийского экономического союза, содержащий наименование лица, уполномоченного на регистрацию коллективного знака Союза на свое имя, цель регистрации коллективного знака Союза, перечень субъектов, имеющих право на использование коллективного знака Союза, перечень и единые качественные или иные общие характеристики товаров, которые будут обозначаться коллективным знаком Союза, условия его использования, положения о порядке контроля за его использованием, положения об ответственности за нарушение его требований»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OPEN_CLASSIFIER

## Trace

OP22 → P.SP.02.PRC.005 → P.SP.02.TRN.026 → P.SP.02.MSG.031 → P.SP.02.MSG.031:49:19

## XML

- Structure: R.010
- QName: ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindCode; ipcdo:AccompanyingDocumentsDetails/ipsdo:IPDocKindName

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 740
- Printed page: 161
- Table/item: Table 49, item 19
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Source page: [[sources/OP22_P_SP_02/pages/page_740]]

## Project state

- Status: OPEN_CLASSIFIER
- Production rule: MISSING
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "19", "location": "Таблица 49", "page": 740, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-19", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "19", "location": "Таблица 49", "page": 740, "source_id": "22OP-RULE-P.SP.02.MSG.031-T49-19", "status": "CONFIRMED", "table": "49", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["49"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-positive-19-P.SP.02.MSG.031-48]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-positive-19-P.SP.02.MSG.031-48]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-negative-19-P.SP.02.MSG.031-48]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-negative-19-P.SP.02.MSG.031-48]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-negative-19-P.SP.02.MSG.031-48]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[NEW_OLD-positive-19-P.SP.02.MSG.031-48]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-negative-19-P.SP.02.MSG.031-48]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_production_requirement_per_owner[OLD_NEW-positive-19-P.SP.02.MSG.031-48]

## Gap

- Reason: OPEN_CLASSIFIER
- Missing information: Collective charter document-kind code needs a confirmed classifier; no code/name shortcut. Embedded branch of outer R.010 retained.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.
