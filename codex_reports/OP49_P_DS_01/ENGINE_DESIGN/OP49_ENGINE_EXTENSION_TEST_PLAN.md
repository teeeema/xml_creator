# OP49 / P.DS.01 — Engine Extension Test Plan

Generated: 2026-10-07. Design-only plan; tests listed here were not added or executed by this audit.

## Acceptance strategy

Test the generic engine primitive first in `eaeu_xml/tests`, then add OP49 production-rule regressions only after source/QName blockers are resolved. The engine tests must prove behavior independent of OP49 field names.

## 1. Calendar-month relation

Target layers: validator grammar + evaluator temporal helper/comparison.

- next month with different days: `2026-02-01` vs `2026-01-31` => PASS for offset `+1`;
- same month => FAIL;
- skipped month => FAIL;
- year rollover `2027-01-*` vs `2026-12-*` => PASS;
- leap-year dates do not change month identity;
- date and supported datetime lexical forms normalize consistently;
- missing/invalid date => FAIL, never guessed;
- negative month offset works for the shared relative-selector helper;
- validator rejects unsupported temporal offset shapes/types.

OP49 proof after normative mapping: MSG.002 REQ.006 positive/negative XML cases.

## 2. Existing-engine ALL_EQUAL composition

No new primitive. Regression should prove the proposed composition before reclassifying production mapping:

- three repeated parents with equal field values => PASS;
- one differing value => FAIL;
- reordered parents => same verdict;
- selected reference owner is exactly one instance (`position: 1`);
- missing value is caught by the companion presence requirement, not converted to a default;
- typed DATETIME equality is used only if the resolved normative datatype supports it.

OP49 mapping remains blocked until `ModificationDate` vs `ModificationDateTime` is resolved.

## 3. Existing-engine MAX reclassification

No MAX primitive. Prove the scope/cardinality reduction:

- two repeated report parents, each with its own scalar `ReportDate` and modification date;
- each modification date equal to its own report date => PASS;
- later modification date => PASS;
- one parent with modification date earlier than its own report date => FAIL;
- values from the other parent must not affect the verdict;
- structure/load regression confirms `ReportDate max_occurs == 1` for the report field used by the rule.

OP49 mapping remains blocked until the modification-date source conflict is resolved.

## 4. Context-relative previous-instance selector

Target layers: selector validation, selector evaluation with outer `RuleContext`, comparison selected operand.

- reports deliberately stored out of chronological order; selector still binds by EventDate relation;
- current March report binds February even if January is adjacent in XML;
- Dec/Jan rollover works;
- no exact previous month => zero match and REQ.041 scope means dependent assertion is not applied;
- duplicate reports with the same previous-month EventDate => ambiguous/multiple match => FAIL;
- current and previous values stay within the same repeated owner/nested index tree;
- unrelated sibling collection with matching date cannot be selected;
- ordinary static selectors/`position` keep existing behavior.

### DECIMAL comparison

- `10 >= 2` => PASS and `2 >= 10` => FAIL, proving numeric rather than lexical ordering;
- decimal fractions and negative values where schema permits;
- invalid decimal => FAIL;
- validator accepts `DECIMAL` only on supported comparison forms;
- existing DATETIME and untyped comparisons remain unchanged.

OP49 proof: one parameterized test covering REQ.042-054 field paths after exact QName/path confirmation, plus a dedicated REQ.041 selector-scope test.

## 5. Context-scoped aggregate comparison

Target layers: `FOR_EACH_ASSERTION_KINDS`, validator aggregate shape, evaluator `_assertion_passes`, context-aware aggregation, application path discovery/generator compatibility.

Core cases:

- two parents where global total equals global SUM but parent A is wrong and parent B compensates => FAIL (detects document-scope leakage);
- both parents locally correct => PASS;
- reverse parent order => same result;
- total selector (`VALUE`) selects zero rows => FAIL;
- total selector selects two rows => FAIL;
- parts selector empty: confirm existing SUM-zero semantics intentionally, with companion cardinality rules enforcing required detail count where normative rules require it;
- nested repeated parent/child indexes retain alignment when one sibling is sparse/missing;
- decimal conversion failure => FAIL;
- document-scope `aggregate_comparison` tests remain bit-for-bit semantically unchanged.

Generator/form-path compatibility:

- `_structured_rule_paths` discovers selectors/value fields nested inside `for_each` aggregate assertions;
- generated test data does not flatten children across parents;
- validation-only aggregate behavior must not invent missing normative values.

OP49 proof after QName confirmation: parameterize the six requirements MSG.005 023/029/036 and MSG.006 019/025/032 with one positive and one cross-parent-leak negative case per duty-detail collection.

## 6. Regression gates

Suggested order when implementation begins:

1. targeted new engine tests;
2. `eaeu_xml/tests/test_structured_rules.py`;
3. `eaeu_xml/tests/test_process_package_validator.py`;
4. `eaeu_xml/tests/test_repeatable_xml_alignment.py`;
5. `eaeu_xml/tests/test_required_form_data.py` if generator/path extraction changes;
6. OP49 package tests;
7. shared-process regressions for OP22, OP23, OP26, OP32 where the same engine primitives are loaded.

Do not claim normative closure from green engine tests. Production OP49 tests may be added only after each row's source/QName dependencies are resolved according to the Knowledge Base policy.
