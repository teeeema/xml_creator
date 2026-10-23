# CONTROL_VERIFICATION: MSG.027 classifier branch

Date: 2026-10-23. Layer: KNOWLEDGE / implementation verification, not a new normative source.

Confirmed source evidence: original `ОП_22.pdf`, PDF pp.578–579, Table57 REQ2–3;
original `92 решение.pdf`, PDF p.15, entry07365; original `148 решение.pdf`, PDF p.4, entry07365.
The current classifier-present branch requires Code07365 and omits Name. Absence of Code
in user XML is not absence of the entry in the authoritative classifier.

Implementation: MSG.027 structured REQ2 enforces exact Code and forbidden Name;
message field policy exposes FIXED07365 / FORBIDDEN through real get_form().
The obsolete Name-only branch is no longer executable in the current classifier revision.
`fixed_values` remains empty: that legacy mechanism supplies defaults during validation,
which would conceal a missing Code in raw XML. The structured rule checks actual input;
the explicit message policy supplies the form/application fixed value.

Runtime/source proof and source hashes:
`codex_reports/OP22_P_SP_02/CONTROL_VERIFICATION/runtime_evidence/continuation_sources.json`,
`continuation_case03.json`, `READ_ONLY_AUDIT.md`.

Separate external dependency: MSG.054/T72 REQ4–5 names a legal-action reference.
Its authoritative publication state and code payload were not identified in the local source set.
Local Code/Name branch tests do not certify that publication state or code membership.
This control remains SOURCE_BLOCKED / STILL_EXTERNAL; no classifier ID or code was invented.
