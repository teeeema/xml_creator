# OP22 / P.SP.02 — Negative Validation QA

Scope: functional QA of the local `xml_creator` validator against canonical requirements Schema v1.0. No production, test, engine, GUI, or KB files were modified.

## Result

- Negative test cases recorded: 15
- EXPECTED_REJECT_AND_REJECTED: 13
- UNEXPECTED_ACCEPTANCE: 1
- CANNOT_TEST_MISSING_EVIDENCE: 1
- ENGINE_NOT_REACHED: 0
- RUNTIME_ERROR: 0

The confirmed unexpected acceptance is systemic rather than message-specific: a `presence` rule in `rules_engine.py` treats a path as present when the dictionary contains the key, even when the extracted XML scalar value is `None`. Therefore an empty required element can pass a REQUIRED rule.

## Confirmed unexpected acceptance

Canonical requirement: `P.SP.02.MSG.024:56:1`.

Normative source: `ОП_22.pdf`, PDF page 577, Table 56 item 1.

Normative requirement: `csdo:UpdateDateTime` must be filled.

Original valid XML condition: `csdo:UpdateDateTime` contains a datetime value.

Modified test XML: the populated element was changed to `<csdo:UpdateDateTime/>`.

EXPECTED: REJECT.

ACTUAL: ACCEPT.

Rule expected to catch it: `P.SP.02.MSG.024.T56.REQ.1`.

Why it escaped: production XML extraction records the path with value `None`; `StructuredRuleEvaluator` uses `(target in values)` for `presence REQUIRED` instead of checking that the extracted value is populated. Relevant implementation: `eaeu_xml/src/eaeu_xml/process_packages/rules_engine.py:54-56`.

Severity: HIGH.

## Successful rejection controls

The validator correctly rejected representative confirmed violations for:

- exact cardinality: one or three application instances where exactly two are required (`P.SP.02.MSG.012:45:1`, p.550);
- forbidden element: `EndDateTime` where it must not be filled (`P.SP.02.MSG.012:45:34`, p.552);
- wrong fixed value: patent-authority `AddressKindCode=3` where value `2` is required (`P.SP.02.MSG.001:34:12`, p.515);
- wrong application status roles (`P.SP.02.MSG.012:45:31`, p.552);
- cross-instance identifier mismatch (`P.SP.02.MSG.012:45:30`, p.551);
- repeated-instance alignment where one repeated address lacks a required child (`P.SP.02.MSG.027:57:8`);
- XOR/one-of embedded structure: neither payload and both payloads (`P.SP.02.MSG.059:77:1`, p.810);
- strict datetime ordering including equal boundary instants (`P.SP.02.MSG.052:70:22`, p.795);
- cross-instance identifier equality (`P.SP.02.MSG.052:70:24`, p.795).

Targeted verification commands produced `15 passed, 16 deselected` and an additional `31 passed` for the fixed-value, one-of, repeated-position, date/equality, and status controls.

## QName limitation

The implementation rejects an embedded root that has the expected local name in the wrong namespace. However canonical requirement `P.SP.02.MSG.059:77:1` currently has `qname_status: UNRESOLVED`. Per audit rules this is recorded as `CANNOT_TEST_MISSING_EVIDENCE` for a normative QName assertion; the implementation behavior is not promoted into normative proof.

## OP22 verdict

Most sampled cardinality, fixed-value, status, equality, date, one-of, and repeatable-instance rules reject invalid XML correctly. Required scalar elements have a confirmed empty-element gap shared with OP23 and OP26.

