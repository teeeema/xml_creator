# Read-only audit, 2026-10-23

No product file was edited during the audit. Existing working-tree changes were preserved. Cases 1/2 retained as instructed.

CV03 reproduced: MSG027 wrong code 99999 and obsolete Name-only fallback accepted; real get_form/resolver has no fixed/forbidden policy. Acceptance test: 2 failed, 3 passed, 5 deselected (-k 027). Root cause: T57 REQ2/3 use presence of XML Code as a proxy for classifier publication; current authoritative 07365 entry is not enforced. Source: OP22 pp578-579, Decision92 p15, Decision148 p4, original PDF text and SHA256 checked.

CV04 selected MSG054/T72 REQ4-5: named legal-action reference payload and publication state remain external; local Code absence cannot certify its absence in the EAEU registry. Real form, resolver, validator and 5 XML scenarios executed. Three Name-branch invalid cases rejected. Arbitrary unverified Code-only is accepted locally: no normative PASS or normative membership failure asserted without payload. SOURCE_BLOCKED is substantive, not an old test-definition gap.

CV05/06/11/12/13: read-only runtime scripts passed, including exact owner paths and [DOCUMENT-1, None]. Original PDFs checked.
CV07/08/14: real forms, resolver, original PDFs and positive/negative XML checks passed.
CV09/10: current OP49 raw XML positive passes R002/R003; duplicated true and forbidden false fail the corresponding rules. Existing shared boolean fix requires no new change.
CV15 selected OP23 MSG001 REQ021.or_language; source OP23 p344, AP + OR requires languageCode. Positive actual XML passes; removing languageCode fails exact contextual rule. It is not projected statically.

Out-of-selected-scope observation retained: MSG004 has source code07320 but missing enforcement. It is not a STILL_EXTERNAL example and is not silently fixed in this continuation.

Next separate correction is limited to OP22 MSG027 mapping/policy and its source-stale fixture. No shared engine or other OP change is necessary.
