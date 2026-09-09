# P.MM.01 — единый локальный аудит оставшихся диагностик

Дата: 2026-08-25. Режим: AUDIT ONLY. Использованы только уже находящиеся в
workspace файлы. `EXTERNAL_WEB_SEARCH_USED = NO`.

## Executive summary

Восемь структурных диагностик делятся на четыре разных класса: пять реальных
противоречий `NORMATIVE_CONFLICT-001…005`; отсутствие конкретной версии R.006;
отсутствие конкретной версии R.007; отсутствие локальных datasets для внешних
классификаторов; и внешняя реестровая проверка `P.MM.01.MSG.014.R2`. Ничего из
этого не исправлялось: программа не выбирает вариант без доказательства.

Первичный местный источник — `normative_sources/err_22042022_68_doc.pdf`,
Решение Коллегии ЕЭК от 19.04.2022 №68 (изменения к Решению №122), 465 страниц,
SHA-256 `a15cc6c946b35145e58304b7e3621ea76241f510e2202bbaf8912b4f8b0715e6`.

## Краткое объяснение для пользователя

| Проблема | Что не сходится или чего нет | Что делает программа | Что требуется локально |
|---|---|---|---|
| Conflicts 001–005 | Правило сообщения называет поле, которого нет в таблице той же структуры | Блокирует конкретное сообщение, не угадывает поле | Официальное исправление/замена таблиц |
| R.006 | В документе только `Y.Y.Y`, не число версии | TEST placeholder; STRICT block | Документ с конкретной версией R.006/base model |
| R.007 | В документе только `Y.Y.Y`, не число версии | TEST placeholder; STRICT block | Документ с конкретной версией R.007/base model |
| Classifier dataset | Кодовые поля есть, списков допустимых значений нет | Предупреждает, не подтверждает допустимость кода | Подтверждённые datasets с кодом, версией и записями |
| MSG.014.R2 | Статус заявления нужен из реестра, не из Body | Не добавляет поле в XML; оставляет warning | Контракт/данные локального реестра для автоматической проверки |

## Сводная таблица

| Problem | Source A / Value A | Source B / Value B | Type | Current implementation | XML / validation impact | Can fix now |
|---|---|---|---|---|---|---|
| `001` | table 19 item 22 p.219: `ChildJuvenileIndicator` | table 10 pp.347–351: `ChildIndicator` + `JuvenileIndicator`, no combined field | REAL_CONFLICT | MSG.002 blocked | Body, validation, generation | NO |
| `002` | table 21 item 4 p.298: `DrugAttributeEnumText` + attributes | table 13 from p.414: no such fields in R.HC.MM.01.002 | REAL_CONFLICT | MSG.023 blocked | Body, validation, generation | NO |
| `003` | table 21 item 5 p.298: same fields, value “Номер документа основания” | table 13 from p.414: no target fields | REAL_CONFLICT | MSG.023 blocked | Body, validation, generation | NO |
| `004` | table 22 item 6 p.300: same three identifiers | table 13 from p.414: no target fields | REAL_CONFLICT | MSG.024 blocked | Body, validation, generation | NO |
| `005` | table 22 item 7 p.300: `AttributeKindCode` / `AttributeKindName` | table 13 from p.414: no attributes | REAL_CONFLICT | MSG.024 blocked | Body, validation, generation | NO |
| R.006 | tables 2/4 pp.308/310: `Y.Y.Y` | N/A | MISSING_EVIDENCE | `active_version: null` | namespace; STRICT blocker | NO |
| R.007 | tables 5/7 pp.314/315: `Y.Y.Y` | N/A | MISSING_EVIDENCE | `active_version: null` | namespace; STRICT blocker | NO |
| classifier | 64 field refs `REFERENCED_NOT_AVAILABLE` | local datasets: none | IDENTITY_UNRESOLVED | warning/test-only | value membership only | NO |
| MSG.014.R2 | table 22 item 2 p.235: statuses 01–08,99 | R.HC.MM.01.004 table 19: no Body path | RULE_SOURCE_INCOMPLETE | external warning | external validation only | NO |

## NORMATIVE_CONFLICT-001

**Что регулируется:** P.MM.01, TRN.002/PRC.002, MSG.002, R.HC.MM.01.001
v1.1.0, rule `P.MM.01.MSG.002.R22`.

**Claim A / provenance:** `message_rules/P.MM.01.MSG.002.yaml` →
`SRC-PMM01-068` → Decision №68, 19.04.2022, section IX, table 19, item 22,
p.219, version context P.MM.01 1.1.0. It says not to fill
`hcsdo:ChildJuvenileIndicator`.

**Claim B / provenance:** `structures/R.HC.MM.01.001/1.1.0.yaml` → same PDF,
table 10: item 2.4.2.3.2 p.347 `ChildIndicator`, item 2.4.2.3.3 p.348
`JuvenileIndicator` (also the pair on p.351). Structure identity: table 8,
item R.HC.MM.01.001, p.319. No combined QName, alias, replacement or version
transition is locally recorded.

**Concrete conflict:** A = one `ChildJuvenileIndicator`; B = two independent
`ChildIndicator` and `JuvenileIndicator`. They cannot both be satisfied without
inventing a target. Current implementation follows **blocked/neither**:
empty `field_paths`, `INTERNAL_NORMATIVE_CONFLICT`, error `NORMATIVE_CONFLICT`.
It affects Body and XML generation of MSG.002, not SOAP header or TRN mapping.

**Conclusion:** `REAL_NORMATIVE_CONFLICT`. Required evidence is a local
corrigendum/amendment or replacement table that explicitly maps the name.
`SAFE_TO_FIX = NO`; blocker remains.

## NORMATIVE_CONFLICT-002 and -003

**What they regulate:** TRN.016/PRC.016, MSG.023, R.HC.MM.01.002 v1.1.0;
rules R4 and R5 in `message_rules/P.MM.01.MSG.023.yaml`.

**Claim A:** local `SRC-PMM01-068`, Decision №68, IX, table 21 p.298:
item 4 requires `hcsdo:DrugAttributeEnumText` to contain `AttributeKindCode`
or `AttributeKindName`; item 5 constrains one of those values to
«Номер документа основания».

**Claim B:** `structures/R.HC.MM.01.002/1.1.0.yaml` traces the same PDF:
structure table 11 item R.HC.MM.01.002 p.413 and complete requisite table 13
from p.414 (rows p.415 onward). None of the element or attributes exists there.

**Concrete conflicts:** 002: A = required element/attributes, B = no matching
path. 003: A = value constraint on the same attributes, B = no attributes on
which to apply it. Program follows **blocked/neither**, never imports similarly
named fields from another structure. MSG.023 Body/XML and validation are
blocked; mapping/header are unchanged.

**Conclusion:** both `REAL_NORMATIVE_CONFLICT`; need local correction of table
13 or table 21 items 4–5 with exact parent/path. Both `SAFE_TO_FIX = NO`.

## NORMATIVE_CONFLICT-004 and -005

**What they regulate:** TRN.015/PRC.015, MSG.024, R.HC.MM.01.002 v1.1.0;
rules R6 and R7 in `message_rules/P.MM.01.MSG.024.yaml`.

**Claim A:** same local PDF, IX, table 22 p.300. Item 6 requires a populated
`DrugAttributeEnumText` to contain `AttributeKindCode` or `AttributeKindName`.
Item 7 says `AttributeKindCode = «другое»` requires `AttributeKindName`.

**Claim B:** same active structure/table-13 evidence as 002/003: the element
and attributes are absent.

**Concrete conflicts:** 004: A = required choice of two attributes, B = no
element/attributes. 005: A = conditional attribute pair, B = no pair. Current
program follows **blocked/neither**; MSG.024 Body/XML generation and validation
are blocked but transaction mapping/header are unchanged.

**Conclusion:** both `REAL_NORMATIVE_CONFLICT`; need local correction linked to
table 22 items 6–7 or table 13. Both `SAFE_TO_FIX = NO`.

## R.006 audit

**Normative evidence:** `structures/R.006/Y.Y.Y.yaml` has direct
SourceReference to Decision №68, table 2 item R.006 p.308 and field table 4
from p.310. Literal values are `version = Y.Y.Y`, namespace
`urn:EEC:R:ProcessingResultDetails:vY.Y.Y`, ccdo/csdo imports `vX.X.X`.
This is DIRECT_NORMATIVE evidence of a placeholder, not of a numeric version.

**Current implementation:** `version_profiles/current.yaml` stores
`R.006.active_version = null`; generic resolver issues
`UNRESOLVED_STRUCTURE_VERSION` in STRICT and uses placeholder only in TEST.
Affected messages: MSG.004, MSG.009, MSG.018; affected transactions:
TRN.001/002/003/005/006/008/009/010/012/014/015/016/017/018/019.

**Impact:** structure YES; header NO; Body namespace YES; mapping NO;
validation YES; provenance-only NO; production-ready YES. `R006_PROBLEM_TYPE`
is `MISSING_EVIDENCE`: no conflicting numeric local version exists. A local
document must prove the concrete R.006 and base-model version applicable to
P.MM.01 1.1.0. `SAFE_TO_SET_R006_VERSION = NO`.

## R.007 audit

**Normative evidence:** `structures/R.007/Y.Y.Y.yaml` traces to Decision №68,
table 5 item R.007 p.314 and field table 7 from p.315. Literal values are
`version = Y.Y.Y`, namespace `urn:EEC:R:ResourceStatusDetails:vY.Y.Y`, imports
`vX.X.X`. This is DIRECT_NORMATIVE evidence only for placeholders.

**Current implementation:** profile stores `R.007.active_version = null`;
generic resolver makes TEST placeholder output and blocks STRICT. The only
other numerical fixture found is P.VERSION.01 test data and is not normative.
Affected messages: MSG.005, MSG.006; transaction: TRN.004/PRC.007.

**Impact:** structure YES; header NO; Body namespace YES; mapping NO;
validation YES; provenance-only NO; production-ready YES.
`R007_PROBLEM_TYPE = MISSING_EVIDENCE`: разногласий локальных документов нет,
но нет достаточного доказательства числа. Need a local R.007/base-model
version document. `SAFE_TO_SET_R007_VERSION = NO`.

## CLASSIFIER_DATASET_NOT_AVAILABLE audit

**Diagnostic source:** `body.py` emits this for a present `classifier_ref`
(ERROR in STRICT, WARNING in TEST). `facade.py` emits one aggregate warning if
an active structure has classifier fields and `classifiers_available` is false.
Loader defines availability as any non-hidden file in `P.MM.01/classifiers/`.

**Local evidence:** 64 fields are explicitly `REFERENCED_NOT_AVAILABLE` /
`EXTERNAL_CLASSIFIER_DATASET`, across all eight structures and therefore all
28 messages. Examples: R.006 `ProcessingResultV2Code`, datatype
`csdo:ProcessingResultCodeV2Type`, table 4 p.313; R.007 `UnifiedCountryCode`,
`csdo:UnifiedCountryCodeType`, table 7 p.318; R.HC.MM.01.001 has 52 such
fields (table 10 pp.323–410). Counts in other structures: .002=2, .003=3,
.004=1, .006=3, .007=1.

**Dataset search:** local directory `P.MM.01/classifiers/` is empty. No CSV,
XLS/XLSX, database, code-list XML/JSON, dictionary or XSD enumeration dataset
was found. Examples are not datasets. Field datatype names partly identify a
kind of list, but no stable universal classifier code, version and complete
entries are locally given. Therefore `CLASSIFIER_PROBLEM_TYPE =
IDENTITY_UNRESOLVED` (operationally also `MISSING_DATASET`), not conflict.

**Impact:** structure NO; header NO; Body YES for entered code values; mapping
NO; validation YES; provenance-only NO; production-ready YES. XML hierarchy
can be made, but membership of codes cannot be locally confirmed. Need local,
authoritative datasets identifying code, version and values. No integration is
safe now.

## P.MM.01.MSG.014.R2 audit

**What it regulates:** business/value constraint, not cardinality, mapping or
classifier. It lists `ApplicationStatusCode` values 01–08 and 99.

**Local Source A:** `message_rules/P.MM.01.MSG.014.yaml` → `SRC-PMM01-068` →
Decision №68, 19.04.2022, IX, table 22 item 2 p.235, P.MM.01 1.1.0. It proves
the list of registry-side application-stage values.

**Local Source B:** `structures/R.HC.MM.01.004/1.1.0.yaml` → same Decision,
table 18 item R.HC.MM.01.004 p.436 and table 19 from p.437. There is no
`ApplicationStatusCode` Body path. This is not a contradiction: Source A
addresses registry context, not an XML field of the request.

**Current implementation:** R2 has empty `field_paths`,
`NEEDS_EXTERNAL_SOURCE`, reason `EXTERNAL_REGISTRY_FIELD_REFERENCE`; facade
shows external warning. Affected: MSG.014/TRN.007/PRC.010. It follows neither
invented Body field nor guessed registry data.

**Impact:** structure NO; header NO; Body NO; mapping NO; validation YES only
for external registry lookup; provenance-only NO; production-ready YES.
`MSG014_R2_PROBLEM_TYPE = RULE_SOURCE_INCOMPLETE`. The rule text is local, but
an executable verification needs a local registry-data contract/dataset.

## Current implementation, XML impact, and missing evidence

Conflicts 001–005 are `VALIDATION_BLOCKER + XML_GENERATION_BLOCKER` for
MSG.002/023/024. R.006/R.007 are STRICT blockers but have literal normative
placeholder TEST serialization. Classifier and R2 do not alter Body hierarchy,
SOAP header or transaction mapping, but prevent complete production validation.
Every item contributes to `P.MM.01_PRODUCTION_READY = NO`; independently,
`XSD_VALIDATION = NOT_AVAILABLE` remains unmodified and unresearched.

| Problem | Missing local proof |
|---|---|
| 001 | whether combined indicator maps to one/both fields or another path |
| 002–005 | exact R.HC.MM.01.002 parent/path/attributes for rules 4–7 |
| R.006 | concrete structure and base-model version for P.MM.01 1.1.0 |
| R.007 | concrete structure and base-model version for P.MM.01 1.1.0 |
| classifier | authoritative dataset identity, version, records and coverage |
| MSG.014.R2 | local registry lookup contract/data for automatic validation |

## Recommended next fix order

`SAFE_TO_FIX_NOW: none.` Wait for local evidence in this order: (1) official
corrections for conflicts 001–005; (2) independently sourced version evidence
for R.006 and R.007; (3) classifier datasets; (4) MSG.014 registry contract.
No external search is proposed.

## Tests/checks and changed-files audit

- Baseline full suite: 273 tests / 905 subtests — OK.
- Final full suite: 273 tests / 905 subtests — OK.
- Full suite includes engine, engine GUI, P.MM.01 and P.MM.01 GUI tests.
- Compile check and import check: OK. wx smoke: NOT_REQUIRED (GUI unchanged).
- Only process-memory documentation was changed. No Decision №5 core,
  TransactionEngine, ProcessPackage, serializer, structure, rule, profile,
  session, artifact, GUI, Body schema or classifier production code changed.

## Final statuses

```text
NORMATIVE_CONFLICT_001_CLASSIFIED = YES
NORMATIVE_CONFLICT_002_CLASSIFIED = YES
NORMATIVE_CONFLICT_003_CLASSIFIED = YES
NORMATIVE_CONFLICT_004_CLASSIFIED = YES
NORMATIVE_CONFLICT_005_CLASSIFIED = YES
NORMATIVE_CONFLICT_001_TYPE = REAL_NORMATIVE_CONFLICT
NORMATIVE_CONFLICT_002_TYPE = REAL_NORMATIVE_CONFLICT
NORMATIVE_CONFLICT_003_TYPE = REAL_NORMATIVE_CONFLICT
NORMATIVE_CONFLICT_004_TYPE = REAL_NORMATIVE_CONFLICT
NORMATIVE_CONFLICT_005_TYPE = REAL_NORMATIVE_CONFLICT
SAFE_TO_FIX_CONFLICT_001 = NO
SAFE_TO_FIX_CONFLICT_002 = NO
SAFE_TO_FIX_CONFLICT_003 = NO
SAFE_TO_FIX_CONFLICT_004 = NO
SAFE_TO_FIX_CONFLICT_005 = NO
R006_VERSION_AUDITED = YES
R007_VERSION_AUDITED = YES
R006_PROBLEM_TYPE = MISSING_EVIDENCE
R007_PROBLEM_TYPE = MISSING_EVIDENCE
R006_VERSION_CONFIRMED_LOCAL = NO
R007_VERSION_CONFIRMED_LOCAL = NO
SAFE_TO_SET_R006_VERSION = NO
SAFE_TO_SET_R007_VERSION = NO
SAFE_TO_REMOVE_R006_WARNING = NO
SAFE_TO_REMOVE_R007_WARNING = NO
CLASSIFIER_REQUIREMENT_AUDITED = YES
CLASSIFIER_PROBLEM_TYPE = IDENTITY_UNRESOLVED
CLASSIFIER_IDENTITY_CONFIRMED = NO
CLASSIFIER_DATASET_FOUND_LOCALLY = NO
CLASSIFIER_VERSION_CONFIRMED = NO
SAFE_TO_INTEGRATE_CLASSIFIER_DATASET = NO
SAFE_TO_REMOVE_CLASSIFIER_WARNING = NO
MSG014_R2_AUDITED = YES
MSG014_R2_PROBLEM_TYPE = RULE_SOURCE_INCOMPLETE
MSG014_R2_LOCAL_EVIDENCE_SUFFICIENT = NO
SAFE_TO_FIX_MSG014_R2 = NO
SAFE_TO_REMOVE_MSG014_R2_WARNING = NO
ALL_NORMATIVE_CONFLICTS_EXPLAINED_IN_PLAIN_LANGUAGE = YES
ALL_CONFLICTING_VALUES_EXPLICITLY_LISTED = YES
CURRENT_IMPLEMENTATION_BEHAVIOR_DOCUMENTED = YES
XML_IMPACT_DOCUMENTED_FOR_ALL_DIAGNOSTICS = YES
VALIDATION_IMPACT_DOCUMENTED_FOR_ALL_DIAGNOSTICS = YES
MISSING_EVIDENCE_EXPLICITLY_LISTED = YES
ALL_LOCAL_SOURCE_PROVENANCE_AUDITED = YES
SAFE_TO_REMOVE_ANY_NORMATIVE_CONFLICT_BLOCKER = NO
SAFE_TO_REMOVE_ANY_REMAINING_WARNING = NO
EXTERNAL_WEB_SEARCH_USED = NO
XSD_VALIDATION = NOT_AVAILABLE
P.MM.01_PRODUCTION_READY = NO
```
