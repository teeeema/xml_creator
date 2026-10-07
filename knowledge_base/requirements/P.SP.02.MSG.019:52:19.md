---
id: "P.SP.02.MSG.019:52:19"
op: "OP22"
process: "P.SP.02"
message: "P.SP.02.MSG.019"
requirement: "19"
structure: "R.IP.SP.02.007"
status: "OPEN_PRODUCTION_MAPPING"
evidence_level: "CONFIRMED_PDF_SOURCE_REF"
source_document: "ОП_22.pdf"
source_pages: 530
source_table: "Table 37, item 19"
source_item: "REQ 19 (Table 52)"
qname_status: "PREFIXED_NAMESPACE_UNRESOLVED"
implementation_status: "OTHER_OPEN"
generated_by: "knowledge_base/tools/build_kb.py"
---

# P.SP.02.MSG.019:52:19

## Нормативное требование

если в составе реквизита «Товарный знак Союза» (ipcdo:TrademarkDetails) значение реквизита «Признак коллективного знака» (ipsdo:CollectiveMarkIndicator) соответствует значению «1» – «товарный знак является коллективным», то должен быть заполнен экземпляр реквизита «Прилагаемый документ» (ipcdo:AccompanyingDocumentsDetails), в составе которого должен быть заполнен один из реквизитов «Код вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindCode) или «Наименование вида документа, используемого в сфере интеллектуальной собственности» (ipsdo:IPDocKindName) и их значения должны соответствовать коду или наименованию вида документа «Выписка из устава (положения) коллективного знака Евразийского экономического союза о единых качественных или иных общих характеристиках товаров, в отношении которых этот товарный знак зарегистрирован»

## Простыми словами

**AUDIT_DERIVED_EXPLANATION**

OTHER_OPEN

## Trace

OP22 → P.SP.02.PRC.027 → P.SP.02.TRN.017 → P.SP.02.MSG.019 → P.SP.02.MSG.019:52:19

## XML

- Structure: R.IP.SP.02.007
- QName: ipcdo:TrademarkDetails; ipsdo:CollectiveMarkIndicator; ipcdo:AccompanyingDocumentsDetails; ipsdo:IPDocKindCode; ipsdo:IPDocKindName
- Namespace: MISSING / UNRESOLVED
- Path: UNRESOLVED: no certified exact-owner production mapping; canonical source row and refs supplied.

## Source

- Document: ОП_22.pdf
- SHA256: see [[02_SOURCE_REGISTRY]]
- PDF page: 530
- Printed page: 118
- Table/item: Table 37, item 19
- Evidence level: CONFIRMED_PDF_SOURCE_REF
- Applied by current table: Table 52 item 19 via range 6-19 (PDF p.568)
- Inherited source chain: 37
- Source page: [[sources/OP22_P_SP_02/pages/page_530]]

## Project state

- Status: OPEN_PRODUCTION_MAPPING
- Production rule: P.SP.02.MSG.019.T52.REQ.6_19
- Wiring: {"current": {"document": "ОП_22.pdf", "item": "6-19", "location": "Таблица 52", "page": 568, "source_id": "22OP-RULE-P.SP.02.MSG.019-T52-6-19", "status": "CONFIRMED", "table": "52", "version_context": "P.SP.02 1.0.0"}, "leaf": {"document": "ОП_22.pdf", "item": "19", "location": "Таблица 37. Требования к заполнению реквизитов P.SP.02.MSG.003", "page": 530, "source_id": "22OP-RULE-P.SP.02.MSG.003-T37-19", "status": "CONFIRMED", "table": "37", "version_context": "P.SP.02 1.0.0"}, "range_chain": ["37"]}
- Positive test: MISSING
- Negative test: MISSING
- Runtime proof: NO_DIRECT_TEST: canonical normative row supplied; gap remains open.

## Gap

- Reason: OTHER_OPEN
- Missing information: Only SAFE_PARTIAL/partial production fragments exist; whole requirement is not certified. No extra normative interpretation performed.
- Required action: Preserve open remainder; no code correction is authorized in this report-only task.
- Closure criterion: The confirmed normative mapping is wired in production and covered by regression evidence.
