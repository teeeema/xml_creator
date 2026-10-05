# MSG028 remediation report

## STATUS

COMPLETE

## VERDICT

READY

## CHANGED_FILES

- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.028.yaml` — replaced the over-strict REQ26 rules and added exact REQ16, REQ17, and REQ20 mappings.
- `P.SP.02_OP_22/tests/test_msg028_safe_mapping.py` — updates mapping boundaries and checks the inclusive-OR REQ26 declaration.
- `P.SP.02_OP_22/tests/test_msg028_repeatable_xml.py` — adds production extraction coverage for AP-parent-scoped REQ16, REQ17, and REQ20.
- `P.SP.02_OP_22/tests/test_msg028_end_to_end.py` — adds the REQ26 production-extraction truth table and updates the valid fixture.
- `codex_reports/MSG028_REMEDIATION_REPORT.md` — this report.

## PREVIOUS_STATE

Historical mapping had 34 executable requirement codes, including REQ26 represented by one rule requiring both fields to be members of their value sets and eight code-to-name `conditional_fixed_value` rules. That required a matched code/name pair. Table 44 REQ26 instead uses the inclusive conjunction `TrademarkKindCode or TrademarkKindName`.

## NORMATIVE_INVENTORY

Table 44 has 41 numbered normative requirements. The historical expanded rule representation had 50 structured-rule objects because REQ26 was expanded into nine objects. The Table 44 source text and existing provenance were used; no broad OP_22 re-audit was performed.

## REQ26_NORMATIVE_ANALYSIS

REQ26 states that the value of `ipsdo:TrademarkKindCode` **or** `ipsdo:TrademarkKindName` must correspond to one of the eight listed trademark types. The operator is inclusive OR:

| Code valid | Name valid | Normative result |
| --- | --- | --- |
| true | true | PASS |
| true | false | PASS |
| false | true | PASS |
| false | false | FAIL |

Missing/missing also fails.

## REQ26_PREVIOUS_IMPLEMENTATION

The prior `for_each` member checks were conjunctive, and the eight conditional fixed-value rules additionally enforced a paired correspondence. Therefore TF and FT were rejected although the normative OR permits them. This was stronger than Table 44.

## REQ26_FINAL_IMPLEMENTATION

REQ26 is now one `for_each` rule over each same-parent `ipcdo:TrademarkDetails`. Its sole assertion is `kind: condition` with `condition.any`: one member check for code and one for name. It has the original Table 44 REQ26 source reference. No classifier inference, positional assumption, XOR, or AND pairing remains.

## OLD_UNMAPPED_REASSESSMENT

| REQ | Previous | A selector.parent | B condition all/any/not | C cross-instance | Final | Executable |
| --- | --- | --- | --- | --- | --- | --- |
| 13 | AMBIGUOUS | Does not resolve normative owner ambiguity | No | No | AMBIGUOUS | No |
| 16 | ENGINE_UNSUPPORTED | Scopes each `IPSubjectName` to its AP parent | Not required | Not required | FULLY_MAPPABLE | Yes |
| 17 | ENGINE_UNSUPPORTED | Scopes candidate names to the one AP parent | Exact `all` filter for OR representation and language presence | Not required | FULLY_MAPPABLE | Yes |
| 18 | ENGINE_UNSUPPORTED | Parent scope alone cannot express normative second-instance conditional absence | No conditional cardinality/ordinal operator | No | ENGINE_UNSUPPORTED | No |
| 19 | ENGINE_UNSUPPORTED | Parent scope alone cannot express normative second-instance LA semantics | No ordinal operator | No | ENGINE_UNSUPPORTED | No |
| 20 | ENGINE_UNSUPPORTED | Scopes each address to its AP parent | Not required | Not required | FULLY_MAPPABLE | Yes |
| 32 | EXTERNAL | No | No | No | EXTERNAL | No |

REQ32 still requires authoritative priority-characteristic classifier data. REQ18 and REQ19 refer to an ordinal “second instance”; A/B/C do not supply a normatively safe ordinal/cardinality conditional expression. REQ13 remains ambiguous because global enforcement would conflict with the separately specified PA/RE party rows.

## FINAL_MAPPING_COUNTS

| Classification | Count |
| --- | ---: |
| FULLY_MAPPABLE | 33 |
| SAFE_PARTIAL | 4 |
| AMBIGUOUS | 1 |
| ENGINE_UNSUPPORTED | 2 |
| EXTERNAL | 1 |
| Unique normative requirement codes | 41 |
| Historical expanded rule objects | 50 |
| Executable requirement codes | 37 |
| Structured-rule objects | 45 |

Arithmetic: `33 + 4 + 1 + 2 + 1 = 41` classified requirement codes. The executable set includes the 33 full and four safe-partial requirement codes.

## EXECUTABLE_REQUIREMENTS

`{1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37,38,39,40,41}`

## UNMAPPED_REQUIREMENTS

`{13,18,19,32}`

## PRODUCTION_TESTS

REQ26 truth-table coverage uses production build → serialize → parse → extract values before evaluation:

- TT PASS
- TF PASS
- FT PASS
- FF FAIL
- missing/missing FAIL

The new REQ16/17/20 tests also construct XML, extract production values, and prove AP-parent ownership for valid and invalid representation, language, and address-kind cases.

## MSG028_TESTS

```text
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests/test_msg028_*.py -p no:cacheprovider
119 passed in 3.91s
```

## ENGINE_VALIDATOR_REGRESSION

```text
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py -p no:cacheprovider
40 passed, 5 subtests passed in 0.10s
```

## FULL_OP22_REGRESSION

```text
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests -p no:cacheprovider
2115 passed in 81.61s
```

## GIT_DIFF_CHECK

`git diff --check` produced no output for the MSG028 scope and the worktree.

## REMAINING_ISSUES

REQ13, REQ18, REQ19, and REQ32 remain intentionally unmapped for the reasons recorded above. No shared engine or concurrent Gemini MSG043 change was modified.
