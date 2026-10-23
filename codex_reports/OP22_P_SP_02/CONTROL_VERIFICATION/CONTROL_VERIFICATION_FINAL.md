# CONTROL_VERIFICATION — 2026-10-23

TOTAL=15
PASS=14
FAIL=0
SOURCE_BLOCKED=1
NOT_EXECUTED=0
ACTUAL_XML_PROOFS=14 confirmed cases (2 retained); 1 partial external case; 28 current + 5 retained unique XML files
TESTS=435 passed
DIFF_CHECK=PASS
STATUS=COMPLETE — control execution complete; the external source dependency in CV-04 remains open.

PASS applies only to the named control/REQ, not whole-message or whole-process normative certification.
CV-01 (MSG005/07360) and CV-02 (MSG001/07220) retain their existing user-confirmed PASS and artifacts. They were not rerun.
Their existing CSV identities are preserved. All 13 continuation controls were actually executed.
SOURCE_BLOCKED in CV-04 is about an identified external reference payload/publication state, not missing old case definitions.

## ROOT_CAUSE

MSG027 T57 REQ2/3 used XML Code presence as a surrogate for classifier availability. This admitted an arbitrary Code and the obsolete Name-only fallback despite confirmed P.CLS.027 entry07365. The read-only audit reproduced this before edits: 2 failed / 3 passed / 5 deselected in the focused acceptance test. See [READ_ONLY_AUDIT.md](runtime_evidence/READ_ONLY_AUDIT.md).

## CHANGED_FILES

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.027.yaml`: current classifier-present scoped rule; forbidden Name; inactive fallback removed from executable rules while its normative source text is retained.
- `P.SP.02_OP_22/message_field_policies/P.SP.02.MSG.027.yaml`: explicit FIXED07365 / FORBIDDEN form and application policy.
- `P.SP.02_OP_22/tests/test_msg027_end_to_end.py`, `test_msg027_safe_mapping.py`, `test_msg027_repeatable_xml.py`: source-correct fixture and regressions, including wrong/missing Code, Code+Name, obsolete fallback and nested collisions.
- `knowledge_base/decisions/CONTROL_VERIFICATION_2026_10_23.md`: source/evidence note.
- This CSV/report and focused scripts/JSON/XML under `runtime_evidence/`: reproducible control proof.
- `graphify-out/`: required AST refresh. graph.json/report updated; HTML remains stale because 5214 communities exceed its 5000-node rendering limit.

## IMPLEMENTATION

Use existing scoped structured rules and explicit message field policies; no new engine abstraction or other OP change. The legacy `fixed_values` map remains empty for MSG027: validation supplies its defaults before rule evaluation and would conceal a missing raw XML Code. Actual value enforcement belongs to the structured rule, while the application policy fixes form input. Current tests prove both sanitization and independent raw XML rejection.

## NORMATIVE_BASIS

CONFIRMED for the selected passing controls, bounded to the listed local authoritative source documents and exact requirements. Original PDF text, physical page numbers and SHA256 were checked in [continuation_sources.json](runtime_evidence/continuation_sources.json); no historical audit is used as normative proof.

CV-04: UNKNOWN / BLOCKED_BY_SOURCE for authoritative publication state and allowed code membership of the named legal-action reference. No code or classifier identifier was invented. Local Name-branch behavior is evidence of implementation only.

| Case | OP / TRN / MSG | Exact REQ | Result |
|---|---|---|---|
| CV-01 | OP22 / P.SP.02.TRN.004 / P.SP.02.MSG.005 | Table 39 REQ.2-3 | PASS |
| CV-02 | OP22 / P.SP.02.TRN.001 / P.SP.02.MSG.001 | Table 34 REQ.4-5; REQ.34 | PASS |
| CV-03 | OP22 / P.SP.02.TRN.022 / P.SP.02.MSG.027 | P.SP.02.MSG.027.T57.REQ.2; REQ.3 inactive in current classifier revision | PASS |
| CV-04 | OP22 / P.SP.02.TRN.049 / P.SP.02.MSG.054 | P.SP.02.MSG.054.T72.REQ.4; REQ.5.PRESENCE; REQ.5.VALUE | SOURCE_BLOCKED |
| CV-05 | OP22 / P.SP.02.TRN.049 / P.SP.02.MSG.054 | P.SP.02.MSG.054.T72.REQ.7.DOC_ID | PASS |
| CV-06 | OP22 / P.SP.02.TRN.050 / P.SP.02.MSG.056 | P.SP.02.MSG.056.T74.REQ.18 | PASS |
| CV-07 | OP26 / P.MM.01.TRN.001 / P.MM.01.MSG.001 | OP26.P_MM_01.P.MM.01.MSG.001.REQ.034 | PASS |
| CV-08 | OP23 / P.SP.03.TRN.001 / P.SP.03.MSG.001 | P.SP.03.MSG.001.REQ.010; REQ.014; REQ.043 | PASS |
| CV-09 | OP49 / P.DS.01.TRN.001 / P.DS.01.MSG.001 | P.DS.01.MSG.001.R002; R003 (T10 REQ2-3) | PASS |
| CV-10 | OP49 / P.DS.01.TRN.001 / P.DS.01.MSG.001 | P.DS.01.MSG.001.R002; R003 (T10 REQ2-3) | PASS |
| CV-11 | OP22 / P.SP.02.TRN.023 / P.SP.02.MSG.028 | P.SP.02.MSG.028.T44.REQ.33 | PASS |
| CV-12 | OP22 / P.SP.02.TRN.050 / P.SP.02.MSG.056 | P.SP.02.MSG.056.T74.REQ.18 | PASS |
| CV-13 | OP22 / P.SP.02.TRN.049 / P.SP.02.MSG.054 | P.SP.02.MSG.054.T72.REQ.7.DOC_ID | PASS |
| CV-14 | OP26 / P.MM.01.TRN.001 / P.MM.01.MSG.001 | OP26.P_MM_01.P.MM.01.MSG.001.REQ.034 | PASS |
| CV-15 | OP23 / P.SP.03.TRN.001 / P.SP.03.MSG.001 | P.SP.03.MSG.001.REQ.021.or_language | PASS |

## VERIFICATION

Final command actually executed (435 passed in 17.75s):

```bash
PYTHONPATH=eaeu_xml/src python3.13 -m pytest -q \
  P.SP.02_OP_22/tests/test_msg0{27,28,29,30}_{end_to_end,safe_mapping,repeatable_xml}.py \
  codex_reports/OP22_P_SP_02/CONTROL_VERIFICATION/runtime_evidence/test_continuation.py --tb=short
```

The expanded 12 test paths were supplied explicitly in the executed command; brace expansion above denotes the identical file set. 435 includes 13 acceptance gates; one gate verifies an executed, evidence-backed SOURCE_BLOCKED result, so green tests do not turn CV-04 into PASS. All XML is serialized, reparsed, extracted and validated by the real package validator. The manifest includes actual QName, size and SHA256 in [continuation_final_summary.json](runtime_evidence/continuation_final_summary.json).

Body generation uses GenerationMode.TEST and local version placeholders where applicable. These are actual XML body proofs, not official XSD validation, complete integration-envelope proof, external-registry validation or production certification. OP49 selected rules pass even though message validation is_complete=False for unrelated unimplemented rules. OP26 fixed codeListId proof does not certify the missing full classifier payload.

`git diff --check`: exit0. Untracked new text files checked separately. Diff reviewed against session baseline; 538 product-file hashes show only four existing MSG027 files changed, plus the new MSG027 policy. Other OP packages and shared engine unchanged: [continuation_scope_check.json](runtime_evidence/continuation_scope_check.json). No commit or push.

`graphify update .`: exit0; AST graph/report refreshed. HTML rendering limitation above remains. Full regression: NOT RUN, because correction is confined to MSG027; nearest MSG027–030 regression and the selected cross-OP controls were executed.

## Controls 3–15

### CV-03 — OP22 confirmed Code/Name branch

P.SP.02.PRC.034 / P.SP.02.TRN.022 / P.SP.02.MSG.027

REQ: `P.SP.02.MSG.027.T57.REQ.2; REQ.3 inactive in current classifier revision`. Source: ОП_22.pdf pp.578-579 T57 REQ2-3; 92 решение.pdf p.15 / 148 решение.pdf p.4: 07365.

Form / resolver: Code FIXED07365 readonly; Name FORBIDDEN; explicit policy and scoped structured rule; no legacy fixed_values default.

Validator / positive-negative: positive PASS; wrong/missing Code, both and legacy Name-only FAIL exact T57.REQ.2; application sanitization checked.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [continuation_case03.json](runtime_evidence/continuation_case03.json); XML: [cv03_positive.xml](runtime_evidence/cv03_positive.xml), [cv03_wrong_code.xml](runtime_evidence/cv03_wrong_code.xml), [cv03_both.xml](runtime_evidence/cv03_both.xml), [cv03_missing_code.xml](runtime_evidence/cv03_missing_code.xml), [cv03_legacy_name_only.xml](runtime_evidence/cv03_legacy_name_only.xml).

### CV-04 — OP22 STILL_EXTERNAL legal-action classifier branch

P.SP.02.PRC.033 / P.SP.02.TRN.049 / P.SP.02.MSG.054

REQ: `P.SP.02.MSG.054.T72.REQ.4; REQ.5.PRESENCE; REQ.5.VALUE`. Source: ОП_22.pdf pp.801-802 T72 REQ4-5; authoritative publication state and code payload not identified locally.

Form / resolver: Code/Name have no unconditional resolver policy; no invented fixed code.

Validator / positive-negative: real form/resolver/validator executed; Name branch valid; bad/missing Name and both rejected; unverified Code-only locally accepted.

Result: **SOURCE_BLOCKED**. T72 REQ4/5 depend on publication and payload of the named legal-action reference. No authoritative payload/publication-state artifact is identified in the local source registry or normative_classifier_data. Code absence is not proof of reference absence. Name-branch tests are implementation evidence only; code membership cannot be certified.

Evidence: [continuation_case04_case15.json](runtime_evidence/continuation_case04_case15.json); XML: [cv04_name_branch.xml](runtime_evidence/cv04_name_branch.xml), [cv04_bad_name.xml](runtime_evidence/cv04_bad_name.xml), [cv04_missing_name.xml](runtime_evidence/cv04_missing_name.xml), [cv04_both.xml](runtime_evidence/cv04_both.xml), [cv04_unverified_code_only.xml](runtime_evidence/cv04_unverified_code_only.xml).

### CV-05 — OP22 MSG054 root-level DocId

P.SP.02.PRC.033 / P.SP.02.TRN.049 / P.SP.02.MSG.054

REQ: `P.SP.02.MSG.054.T72.REQ.7.DOC_ID`. Source: ОП_22.pdf p.803 T72 REQ7.

Form / resolver: root csdo:DocId FORBIDDEN/hidden; nested paths not forbidden by this root rule.

Validator / positive-negative: positive valid; adding exact-QName root DocId fails T72.REQ.7.DOC_ID.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [op22_cases_05_06_11_12_13_15.json](runtime_evidence/op22_cases_05_06_11_12_13_15.json); XML: [cv05_msg054_positive.xml](runtime_evidence/cv05_msg054_positive.xml), [cv05_msg054_forbidden_root.xml](runtime_evidence/cv05_msg054_forbidden_root.xml).

### CV-06 — OP22 MSG056 nested DocId

P.SP.02.PRC.035 / P.SP.02.TRN.050 / P.SP.02.MSG.056

REQ: `P.SP.02.MSG.056.T74.REQ.18`. Source: ОП_22.pdf p.807 T74 REQ18.

Form / resolver: IPPaymentDetails/AccompanyingDocumentsDetails/csdo:DocId REQUIRED; root DocId FORBIDDEN.

Validator / positive-negative: positive valid; remove attached document DocId: exact REQ18 fails.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [op22_cases_05_06_11_12_13_15.json](runtime_evidence/op22_cases_05_06_11_12_13_15.json); XML: [cv06_msg056_positive.xml](runtime_evidence/cv06_msg056_positive.xml), [cv06_msg056_missing_nested_id.xml](runtime_evidence/cv06_msg056_missing_nested_id.xml).

### CV-07 — OP26 fixed classifier ID

P.MM.01.PRC.001 / P.MM.01.TRN.001 / P.MM.01.MSG.001

REQ: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.034`. Source: 26_ОП.pdf p.213 REQ34; p.39 P.CLS.019.

Form / resolver: DrugRegistrationDetails/DrugCountryRegistrationDetails/UnifiedCountryCode/@codeListId FIXED P.CLS.019 readonly.

Validator / positive-negative: positive serialized attribute P.CLS.019; raw XML changed to P.CLS.999 fails REQ034.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [op26_op23_B_case07_case08_case14_evidence.json](runtime_evidence/op26_op23_B_case07_case08_case14_evidence.json); XML: [op26_op23_B_case07_positive.xml](runtime_evidence/op26_op23_B_case07_positive.xml), [op26_op23_B_case14_negative_raw_xml_tamper.xml](runtime_evidence/op26_op23_B_case14_negative_raw_xml_tamper.xml).

### CV-08 — OP23 message-specific REQUIRED/FORBIDDEN

P.SP.03.PRC.001 / P.SP.03.TRN.001 / P.SP.03.MSG.001

REQ: `P.SP.03.MSG.001.REQ.010; REQ.014; REQ.043`. Source: ОП_23.pdf p.342 T16 REQ10/14; p.350 REQ43.

Form / resolver: Application DocId and AuthorityName REQUIRED; ConsentToDataProcessingIndicator FORBIDDEN.

Validator / positive-negative: positive valid; missing DocId/AuthorityName and added Consent fail exact corresponding rules.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [op26_op23_B_case07_case08_case14_evidence.json](runtime_evidence/op26_op23_B_case07_case08_case14_evidence.json); XML: [op26_op23_B_case08_positive.xml](runtime_evidence/op26_op23_B_case08_positive.xml), [op26_op23_B_case08_negative_missing_docid.xml](runtime_evidence/op26_op23_B_case08_negative_missing_docid.xml), [op26_op23_B_case08_negative_missing_authority.xml](runtime_evidence/op26_op23_B_case08_negative_missing_authority.xml), [op26_op23_B_case08_negative_forbidden_consent.xml](runtime_evidence/op26_op23_B_case08_negative_forbidden_consent.xml).

### CV-09 — OP49 structured selection cardinality

P.DS.01.PRC.001 / P.DS.01.TRN.001 / P.DS.01.MSG.001

REQ: `P.DS.01.MSG.001.R002; R003 (T10 REQ2-3)`. Source: 49_ОП.pdf p.79 T10 REQ2-3.

Form / resolver: where DailyInfoIndicator scopes cardinality; owner and indicator have no unconditional resolver entry.

Validator / positive-negative: one true passes; duplicate true fails R002; true+false fails R003; false-only fails R002/R003; real form/resolver checked.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [op49_case09_case10_evidence.json](runtime_evidence/op49_case09_case10_evidence.json); XML: [op49_case09_generated_positive.xml](runtime_evidence/op49_case09_generated_positive.xml), [op49_case09_duplicate_true.xml](runtime_evidence/op49_case09_duplicate_true.xml), [op49_case09_add_forbidden_false.xml](runtime_evidence/op49_case09_add_forbidden_false.xml), [op49_case09_replace_daily_with_false.xml](runtime_evidence/op49_case09_replace_daily_with_false.xml).

### CV-10 — Contextual rule not statically projected

P.DS.01.PRC.001 / P.DS.01.TRN.001 / P.DS.01.MSG.001

REQ: `P.DS.01.MSG.001.R002; R003 (T10 REQ2-3)`. Source: 49_ОП.pdf p.79 T10 REQ2-3.

Form / resolver: where DailyInfoIndicator scopes cardinality; owner and indicator have no unconditional resolver entry.

Validator / positive-negative: one true passes; duplicate true fails R002; true+false fails R003; false-only fails R002/R003; real form/resolver checked.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [op49_case09_case10_evidence.json](runtime_evidence/op49_case09_case10_evidence.json); XML: [op49_case09_generated_positive.xml](runtime_evidence/op49_case09_generated_positive.xml), [op49_case09_duplicate_true.xml](runtime_evidence/op49_case09_duplicate_true.xml), [op49_case09_add_forbidden_false.xml](runtime_evidence/op49_case09_add_forbidden_false.xml), [op49_case09_replace_daily_with_false.xml](runtime_evidence/op49_case09_replace_daily_with_false.xml).

### CV-11 — Repeatable owner and exact XML path

P.SP.02.PRC.002 / P.SP.02.TRN.023 / P.SP.02.MSG.028

REQ: `P.SP.02.MSG.028.T44.REQ.33`. Source: ОП_22.pdf p.722 T44 REQ33; p.879 T10 row2.16.4.

Form / resolver: ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails/csdo:DocId REQUIRED per owner.

Validator / positive-negative: two XML owners extract [DOCUMENT-1,DOCUMENT-2]; missing second child extracts [DOCUMENT-1,None] and fails exact REQ33.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [op22_cases_05_06_11_12_13_15.json](runtime_evidence/op22_cases_05_06_11_12_13_15.json); XML: [cv11_msg028_two_documents.xml](runtime_evidence/cv11_msg028_two_documents.xml), [cv11_msg028_second_document_missing_id.xml](runtime_evidence/cv11_msg028_second_document_missing_id.xml).

### CV-12 — Structure OPTIONAL / Message REQUIRED

P.SP.02.PRC.035 / P.SP.02.TRN.050 / P.SP.02.MSG.056

REQ: `P.SP.02.MSG.056.T74.REQ.18`. Source: ОП_23.pdf p.565 T13 row8.10.4: 0..1; ОП_22.pdf p.807 T74 REQ18.

Form / resolver: nested DocId structure min0; form/resolver REQUIRED within accompanying-document owner.

Validator / positive-negative: positive valid; missing nested DocId fails REQ18.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [op22_cases_05_06_11_12_13_15.json](runtime_evidence/op22_cases_05_06_11_12_13_15.json); XML: [cv06_msg056_positive.xml](runtime_evidence/cv06_msg056_positive.xml), [cv06_msg056_missing_nested_id.xml](runtime_evidence/cv06_msg056_missing_nested_id.xml).

### CV-13 — Structure ALLOWED / Message FORBIDDEN

P.SP.02.PRC.033 / P.SP.02.TRN.049 / P.SP.02.MSG.054

REQ: `P.SP.02.MSG.054.T72.REQ.7.DOC_ID`. Source: ОП_23.pdf p.542 T13 row7: 0..1; ОП_22.pdf p.803 T72 REQ7.

Form / resolver: root DocId permitted by structure min0; form/resolver FORBIDDEN in message.

Validator / positive-negative: positive absent root valid; adding root fails exact message REQ7.DOC_ID.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [op22_cases_05_06_11_12_13_15.json](runtime_evidence/op22_cases_05_06_11_12_13_15.json); XML: [cv05_msg054_positive.xml](runtime_evidence/cv05_msg054_positive.xml), [cv05_msg054_forbidden_root.xml](runtime_evidence/cv05_msg054_forbidden_root.xml).

### CV-14 — FIXED value protected against raw XML tampering

P.MM.01.PRC.001 / P.MM.01.TRN.001 / P.MM.01.MSG.001

REQ: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.034`. Source: 26_ОП.pdf p.213 REQ34; p.39 P.CLS.019.

Form / resolver: DrugRegistrationDetails/DrugCountryRegistrationDetails/UnifiedCountryCode/@codeListId FIXED P.CLS.019 readonly.

Validator / positive-negative: positive serialized attribute P.CLS.019; raw XML changed to P.CLS.999 fails REQ034.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [op26_op23_B_case07_case08_case14_evidence.json](runtime_evidence/op26_op23_B_case07_case08_case14_evidence.json); XML: [op26_op23_B_case07_positive.xml](runtime_evidence/op26_op23_B_case07_positive.xml), [op26_op23_B_case14_negative_raw_xml_tamper.xml](runtime_evidence/op26_op23_B_case14_negative_raw_xml_tamper.xml).

### CV-15 — Additional contextual rule from OP23

P.SP.03.PRC.001 / P.SP.03.TRN.001 / P.SP.03.MSG.001

REQ: `P.SP.03.MSG.001.REQ.021.or_language`. Source: ОП_23.pdf p.344 T16 REQ21.

Form / resolver: IPPartyKindCode AP + IPSubjectName representation OR requires languageCode; contextual rule absent from static req IDs.

Validator / positive-negative: positive actual XML PASS; deleting languageCode from AP/OR name fails REQ021.or_language.

Result: **PASS**. Source, real get_form/resolver and positive/negative raw XML validation agree for the selected requirement.

Evidence: [continuation_case04_case15.json](runtime_evidence/continuation_case04_case15.json); XML: [cv15_op23_positive.xml](runtime_evidence/cv15_op23_positive.xml), [cv15_op23_missing_language.xml](runtime_evidence/cv15_op23_missing_language.xml).

## REMAINING_ISSUES

- CV-04: obtain an authoritative legal-action reference payload and its publication state for the applicable revision to close membership/branch selection. Local XML probes are complete; normative closure is blocked.
- Historical MSG004/07320 finding from this control run was subsequently corrected in the separate 2026-10-23 targeted task; see ../MSG004_TARGETED_FIX/MSG004_FINAL.md. Original baseline evidence and the 14 PASS / 1 SOURCE_BLOCKED control history are preserved; MSG004 is not added to those 15 controls.
- Existing unrelated working-tree modifications are preserved. No whole-repository or production PASS is claimed.
