# Unexpected Acceptances — Negative Validation QA

This report contains only confirmed cases where a canonical requirement proves that the modified XML/value should be rejected and the current local validation path accepts it.

## UA-01 — OP22 empty required UpdateDateTime

- Canonical requirement: `P.SP.02.MSG.024:56:1`
- Source: `ОП_22.pdf`, p.577, Table 56 item 1
- Original valid condition: `csdo:UpdateDateTime` is populated
- Modified test XML: `<csdo:UpdateDateTime/>`
- EXPECTED: REJECT
- ACTUAL: ACCEPT
- Rule expected to catch it: `P.SP.02.MSG.024.T56.REQ.1`
- Why it escaped: required presence checks path membership; extracted empty scalar is `None` but the path remains present
- Severity: HIGH

## UA-02 — OP23 empty required DocId

- Canonical requirement: `P.SP.03.MSG.001.REQ.010`
- Source: `ОП_23.pdf`, p.342, Table 16 item 10
- Original valid condition: application `csdo:DocId` is populated
- Modified test XML: `<csdo:DocId/>`
- EXPECTED: REJECT
- ACTUAL: ACCEPT
- Rule expected to catch it: `P.SP.03.MSG.001.REQ.010`
- Why it escaped: same shared REQUIRED-presence implementation defect
- Severity: HIGH

## UA-03 — OP26 empty required StartDateTime

- Canonical requirement: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.003`
- Source: Decision No. 68, p.208, Table 18 item 3
- Original valid condition: `csdo:StartDateTime` is populated
- Modified test XML: `<csdo:StartDateTime/>`
- EXPECTED: REJECT
- ACTUAL: ACCEPT
- Rule expected to catch it: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.003`
- Why it escaped: same shared REQUIRED-presence implementation defect
- Severity: HIGH

## UA-04 — OP26 DrugApplicationKindCode TEST

- Canonical requirement: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.005`
- Source: Decision No. 68, p.208, Table 18 item 5
- Original valid condition: value is one of `01`, `02`, `03`, `04`, `99`
- Modified test XML/value: `DrugApplicationKindCode=TEST`
- EXPECTED: REJECT
- ACTUAL: ACCEPT in TEST validation mode
- Rule expected to catch it: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.005`
- Why it escaped: runtime rule has an explicit `#text == TEST` alternative that is not present in the canonical requirement
- Severity: HIGH

## UA-05 — OP26 CountryKindCode TEST

- Canonical requirement: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.008`
- Source: Decision No. 68, p.209, Table 18 item 8
- Original valid condition: value is `01` or `02`
- Modified test XML/value: `CountryKindCode=TEST`
- EXPECTED: REJECT
- ACTUAL: ACCEPT in TEST validation mode
- Rule expected to catch it: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.008`
- Why it escaped: runtime rule has an explicit `#text == TEST` alternative not supported by the canonical requirement
- Severity: HIGH

## UA-06 — GUI validates stale form state instead of edited XML body

- Canonical requirement used for reproduction: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.003`
- Source: Decision No. 68, p.208, Table 18 item 3
- Original valid condition: generated XML and controller values both contain populated StartDateTime
- Modified test XML: edit only the XML to empty StartDateTime; controller value remains populated
- EXPECTED: REJECT
- ACTUAL: GUI summary `Проверка пройдена`
- Rule expected to catch it: `OP26.P_MM_01.P.MM.01.MSG.001.REQ.003`
- Why it escaped: `XmlValidationService` stops at envelope/header/root checks and `controller.validate()` validates stale form values rather than re-extracted edited XML body values
- Severity: CRITICAL

## Root-defect grouping

The six confirmed cases reduce to three root defects:

1. Shared REQUIRED presence semantics: UA-01, UA-02, UA-03.
2. OP26 non-normative `TEST` allowlist branches: UA-04, UA-05.
3. GUI edited-XML validation path split: UA-06.

No remediation was applied in this task.

