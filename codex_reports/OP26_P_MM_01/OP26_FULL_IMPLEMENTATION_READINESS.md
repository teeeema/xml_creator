# OP26 / P.MM.01 — full implementation readiness

## 1. What is already sufficient

- 201/201 current canonical requirement records were reviewed.
- The primary PDF is present and the 16 filling-rule tables are available.
- Current workspace contains 201 business-rule records and **159 executable structured rules**.
- The current engine has the local primitives needed for the discovered local rules; no confirmed generic `ENGINE_CAPABILITY_MISSING` was found.
- P.CLS.019 identity is normatively confirmed at PDF 39 / printed 38 / Table 10.

## 2. What can be implemented now without new normative data

**52 missing atomic business rules** can be mapped from the existing normative text: 11 `codeListId=P.CLS.019` rules, 4 rules historically misclassified as classifier/registry, 36 local source rows from MSG.002 Table 19 items 50–83 and 85–86, and the first MSG.028 Table 21 item 5. These are production tasks, but final QName/schema closure still depends on model versions/XSD.

## 3. What requires only production work

The current canonical files show 42 unmapped records, but the normative source expands those to **80 unmapped atomic requirements** because MSG.002 REQ.050 contains 38 source rows and MSG.028 REQ.005 merges two source rows. Of the 80, 52 are locally implementable now and 28 are blocked by missing/contradictory external information.

## 4. What requires engine work

No confirmed local semantic primitive is missing. The engine already supports presence, fixed/conditional rules, comparisons including `IN`, repeated-context rules, cardinality and an explicit external-not-evaluated status. A real external-registry adapter may be needed later, but its correct interface cannot be specified until the registry contract is obtained; this is currently an external-contract blocker, not a proven engine-design defect.

## 5. What requires classifiers

There are **22 atomic P.CLS.019-dependent rules**: 11 only need the classifier identifier and are safe to map because Table 10 identifies it as `P.CLS.019`; 11 need actual country-code membership and are blocked because no authoritative payload/version/effective date is available. Historical `MSG.014.REQ.002` is not a classifier dependency: PDF 235/Table 22/item 2 enumerates values 01–08 and 99 directly.

## 6. What requires external registry

The corrected count is **11 atomic registry dependencies**, not 14. Historical MSG.001 REQ.046, MSG.002 REQ.013 and MSG.020 REQ.011 are local rules. The 11 real dependencies need an authoritative contract for existence/absence checks, equality checks, active-record semantics, two time-aware StartDateTime comparisons, status/reference-state checks and document-presence checks.

## 7. What requires XSD/common models

Eight structure XSDs are declared and **0 bytes were found** after recursive search of `/Users/tema/Documents/Work/Документы_xml` for XSD/XML/ZIP/RAR/7z and schema-related filenames. In addition, current model imports remain `X.X.X`. Consequently **196 canonical requirement field QNames are prefix-only/unresolved**, while the five remaining canonical requirements are source conflicts. R.006/R.007 also have `Y.Y.Y` structure versions and unresolved concrete root QNames.

## 8. What contains source conflict

Five requirements remain blocked: MSG.002/REQ.022, MSG.023/REQ.004-.005 and MSG.024/REQ.006-.007. See `OP26_SOURCE_CONFLICTS_DETAILED.md`.

## 9. What requires normative clarification

MSG.002 Table 19 item 84 is truncated in the source at PDF 230 / printed 229. Its missing tail cannot be inferred. Source numbering anomalies also exist in MSG.020 Table 26 (no item 2) and MSG.024 Table 22 (starts at item 2), but those numbering gaps alone are not evidence of missing requirements.

## 10. What is implemented but insufficiently tested

All 159 current structured rules lack dedicated requirement-level negative regression proof. Live audit executed all 159 in TEST mode: 153 PASS, 6 FAIL on generic generated values. The six are MSG.023 REQ.001/.006/.009 and MSG.024 REQ.003/.008/.010; because those messages already contain normative conflicts, the branch-level E2E classification does not expose these local-rule failures as separate test failures.

## 11. What is tested but lacks strict runtime proof

The OP26 test suite passes, but the strict 43-branch runtime matrix has **0 `VERIFIED_SOAP` branches**: 37 are `VERSION_PLACEHOLDER_TEST`, 3 `NORMATIVE_CONFLICT`, and 3 `INITIAL_MESSAGE_BLOCKED`. Thus TEST-mode rule invocation exists, but strict normative runtime proof remains missing for all 159 mapped rules until versions/QNames/XSD/conflicts are resolved.

## 12. Minimum material package for 100% closure

1. Official bytes of all eight declared OP26 structure XSDs, including their imported schema set.
2. Concrete versions for R.006 and R.007.
3. Concrete base-model and healthcare-model versions used for `ccdo/csdo/hccdo/hcsdo` imports (current `X.X.X`).
4. Official machine-readable P.CLS.019 country classifier payload with applicable version/effective date.
5. Official unified-registry contract/API/schema or authoritative offline snapshot specification covering the 11 lookup semantics.
6. Official clarification/corrigendum for the five source conflicts.
7. Official corrected text for MSG.002 Table 19 item 84.

Once these materials are available, the remaining production mapping, requirement-level tests, real XSD validation and strict E2E proof can be completed without inventing normative behavior.
