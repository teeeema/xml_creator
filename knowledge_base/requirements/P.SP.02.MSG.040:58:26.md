---
id: "P.SP.02.MSG.040:58:26"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.040"
requirement: "26"
structure: "R.IP.SP.02.002"
status: "IMPLEMENTED_CONFIRMED"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 720
source_table: "Table 44, item 26"
source_item: "REQ 26 (Table 58)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "CLOSED_CONFIRMED"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.040:58:26

## Нормативное требование

в составе реквизита «Заявка на товарный знак Союза (ходатайство, жалоба)» (ipcdo:TrademarkApplicationDetails), в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Код вида товарного знака» (ipsdo:TrademarkKindCode) или реквизита «Наименование вида товарного знака» (ipsdo:TrademarkKindName) должны соответствовать одному из следующих значений: «110» – «Словесный знак»; «120» – «Буквенный знак»; «130» – «Цифровой знак»; «140» – «Изобразительный знак»; «150» – «Объемный знак»; «160» – «Знак, представляющий собой цвет»; «170» – «Знак, представляющий собой сочетание цветов»; «180» – «Комбинированный знак» в соответствии со справочником основных характеристик товарного знака и знака обслуживания Евразийского экономического союза (по виду и приоритету), утвержденным Решением Коллегии Комиссии от 29 ноября 2022 г. № 184

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification.

## Trace

OP22 → P.SP.02.PRC.016 → P.SP.02.TRN.035 → P.SP.02.MSG.040 → P.SP.02.MSG.040:58:26

## XML

- Structure: R.IP.SP.02.002
- QName: ipcdo:TrademarkDetails; ipsdo:TrademarkKindCode; ipsdo:TrademarkKindName
- Namespace: MISSING / UNRESOLVED
- Path: ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkDetails; ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkDetails/ipsdo:TrademarkKindCode; ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkDetails/ipsdo:TrademarkKindName

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 720
- Printed page: 141
- Table/item: Table 44, item 26
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 58 item 26 via range 6-29 (PDF p.760)
- Inherited source chain: 44
- Source page: [[sources/OP22_P_SP_02/pages/page_720]]

## Project state

- Status: IMPLEMENTED_CONFIRMED
- Production rule: P.SP.02.MSG.040.T58.REQ.26
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-29", "location": "Таблица 58", "page": 760, "source_id": "22OP-RULE-P.SP.02.MSG.040-T58-6-29", "status": "CONFIRMED", "table": "58", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "26", "location": "Таблица 44. Требования к заполнению реквизитов P.SP.02.MSG.028", "page": 720, "source_id": "22OP-RULE-P.SP.02.MSG.028-T44-26", "status": "CONFIRMED", "table": "44", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["44"]}
- Positive test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_existing_production_inclusive_or_truth_table[False-True-P.SP.02.MSG.040-58]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_existing_production_inclusive_or_truth_table[True-False-P.SP.02.MSG.040-58]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_existing_production_inclusive_or_truth_table[True-True-P.SP.02.MSG.040-58]
- Negative test: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_existing_production_inclusive_or_truth_table[False-False-P.SP.02.MSG.040-58]
- Runtime proof: P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_existing_production_inclusive_or_truth_table[False-False-P.SP.02.MSG.040-58]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_existing_production_inclusive_or_truth_table[False-True-P.SP.02.MSG.040-58]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_existing_production_inclusive_or_truth_table[True-False-P.SP.02.MSG.040-58]; P.SP.02_OP_22/tests/test_fix_now_code_msg012_xml.py::test_existing_production_inclusive_or_truth_table[True-True-P.SP.02.MSG.040-58]

## Gap

- Reason: Current verified delivery snapshot counts this requirement within executable coverage.
- Missing information: None recorded
- Required action: MISSING
- Closure criterion: Already counted as implemented in the current verified delivery snapshot.
