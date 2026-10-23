# OP26 SAFE52 implementation audit

## Result

- Canonical requirements: **239**.
- Executable canonical rules before wave: **159**.
- Audit SAFE target: **52**.
- Implemented and closed with positive/negative proof: **45**.
- Reclassified as blocked after source/structure verification: **7**.
- Executable canonical coverage after wave: **204/239**.
- Remaining missing mappings: **35** = original 28 blocked + 7 reclassified.
- Shared engine changes: **0**. GUI changes: **0**. Knowledge Base changes: **0**.

## Normative basis

The implementation uses Decision of the EEC Board dated 19.04.2022 No. 68 / `26_ОП.pdf` and the confirmed OP26 structures. Table 10, PDF page 39 confirms `P.CLS.019` as the world-countries classifier based on ISO 3166-1. Only the 11 `codeListId` identity checks are implemented; classifier membership remains blocked because no machine-readable classifier payload is available.

For Table 19 the local executable cluster is mapped from PDF pages 224–230. The incomplete item 84 remains blocked and was not reconstructed. No semantic `DrugRegistrationDocCode = other` value was guessed.

## Implemented canonical requirements by message

- `P.MM.01.MSG.001`: 1
- `P.MM.01.MSG.002`: 34
- `P.MM.01.MSG.003`: 1
- `P.MM.01.MSG.007`: 1
- `P.MM.01.MSG.010`: 1
- `P.MM.01.MSG.016`: 1
- `P.MM.01.MSG.019`: 1
- `P.MM.01.MSG.020`: 1
- `P.MM.01.MSG.021`: 1
- `P.MM.01.MSG.023`: 1
- `P.MM.01.MSG.024`: 1
- `P.MM.01.MSG.028`: 1

## Reclassified blocked

- `OP26.P_MM_01.P.MM.01.MSG.001.REQ.046` — **UNKNOWN / BLOCKED_BY_SOURCE**: Пункт требует реакцию на семантическое значение «другое» для DrugRegistrationDocCode, но доступный нормативный источник не задаёт код этого значения, а payload классификатора отсутствует.
- `OP26.P_MM_01.P.MM.01.MSG.002.REQ.013` — **SOURCE_CONFLICT / BLOCKED_BY_SOURCE**: При CountryKindCode=02 пункт 13 разрешает «только» четыре вложенных реквизита, но R.HC.MM.01.001 v1.1.0 одновременно делает UnifiedCountryCode и CountryKindCode обязательными в том же DrugCountryRegistrationDetails. Нормативного исключения из слова «только» не найдено.
- `OP26.P_MM_01.P.MM.01.MSG.002.REQ.050` — **UNKNOWN / BLOCKED_BY_SOURCE**: Пункт требует реакцию на семантическое значение «другое» для DrugRegistrationDocCode, но числовой код значения не подтверждён доступным источником.
- `OP26.P_MM_01.P.MM.01.MSG.002.REQ.061` — **SOURCE_CONFLICT / BLOCKED_BY_SOURCE**: Нормативный текст ссылается на ccdo:SubjectAddressDetails, которого нет в подтверждённой структуре R.HC.MM.01.001 v1.1.0; подмена на AddressV4Details была бы догадкой.
- `OP26.P_MM_01.P.MM.01.MSG.002.REQ.086` — **SOURCE_CONFLICT / BLOCKED_BY_SOURCE**: Пункт помещает DrugSecondaryPackageKindCode/Name в PackageDetails, а подтверждённая структура R.HC.MM.01.001 v1.1.0 размещает эти поля в PackageFormDetails.
- `OP26.P_MM_01.P.MM.01.MSG.014.REQ.002` — **SOURCE_CONFLICT / BLOCKED_BY_SOURCE**: ApplicationStatusCode отсутствует в R.HC.MM.01.004 v1.1.0 для MSG.014; существующая business-rule запись уже помечена NEEDS_EXTERNAL_SOURCE / EXTERNAL_REGISTRY_FIELD_REFERENCE.
- `OP26.P_MM_01.P.MM.01.MSG.020.REQ.011` — **UNKNOWN / BLOCKED_BY_SOURCE**: Пункт требует реакцию на семантическое значение «другое» для DrugRegistrationDocCode, но числовой код значения не подтверждён доступным источником.

## Verification

- `PYTHONPATH=eaeu_xml/src pytest -q P.MM.01_OP_26/tests/test_safe52_implementation_wave.py` → **99 passed**.
- `PYTHONPATH=eaeu_xml/src pytest -q P.MM.01_OP_26/tests/test_all_transactions_e2e.py P.MM.01_OP_26/tests/test_validation_wave1_regressions.py P.MM.01_OP_26/tests/test_pmm01_catalog.py` → **32 passed, 64 subtests passed**.
- `PYTHONPATH=eaeu_xml/src pytest -q P.MM.01_OP_26/tests` → **192 passed, 83 subtests passed**.
- Preservation proof: all **159** canonical rule IDs from `mapped_structured_rules.json` are still present; current executable canonical IDs = **204**.

## Runtime6

All six former generic-payload failures now PASS. The cause was OP26 test-data generation for `R.HC.MM.01.002`: optional root document fields needed by the message rules were absent or carried a generic invalid code. The shared evaluator was not changed.
