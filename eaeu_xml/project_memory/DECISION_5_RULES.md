# Decision №5 rules

The machine-readable registry is `src/eaeu_xml/decision5/rules/source_rules.yaml` and contains 45 unique source-traced rules. The former duplicate Integration ownership entry was consolidated into `D5-HDR-INTEGRATION`.

Stage 2 groups remain implemented: namespaces/envelope, application Header, identifiers, Action, logical addresses, correlation and external Body boundary.

Addressing audit clarification: paragraphs 45–53 establish
`EAEU://<segment>/CP/<process-code>/<participant-code>[/<authority-id>]`.
Paragraph 48/table 6 makes `EEC` the Commission segment and national segments
ISO 3166-1 alpha-2 values. Paragraphs 30, 32 and 34 make `wsa:To` the actual
recipient address and `wsa:ReplyTo/wsa:Address` the sender address for the
response. Concrete participant codes remain external process-package data.

Stage 3 groups:

- D5-INTEGRATION-STRUCTURE / TRACK / TIME / OWNER — paragraphs 41–44 and table 5;
- D5-SIGNAL-RCV / PRS / ERR / ACTION / BODY — paragraphs 112–121 and appendix 5 tables 1–5;
- D5-FAULT-TO / CORRELATION / HEADER / ACTION / BODY / CODES / REASON / DETAIL — paragraphs 66–76 and tables 7–8;
- D5-TRN-PARAMETERS / RETRY — paragraphs 100 and 104–110;
- D5-TRN-MUTUAL / QUESTION / REQUEST / CONFIRMATION / NOTIFICATION / DISTRIBUTION — paragraphs 122–139.

`Decision5RuleCoverage` associates every entry with source, implementation and a real test method. Final coverage: 45 VERIFIED, 0 unresolved registry entries, 0 mismatches and 0 missing tests.

`D5-FAULT-DETAIL` verifies the optional Detail and ProblemMessage string value. CDATA is a recommendation in paragraph 76, so lexical CDATA preservation is not treated as a mandatory conformance condition.
