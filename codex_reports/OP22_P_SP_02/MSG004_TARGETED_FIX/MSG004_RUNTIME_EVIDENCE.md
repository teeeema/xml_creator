# MSG004 runtime evidence — 2026-10-23

Expected/actual valid refers to the selected classifier rule. Negative XML is well-formed and passed through namespace-aware parse/extract before validation. REQ2 applies only under ipcdo:TrademarkApplicationDetails; nested accompanying-document Name remains valid (T38 REQ30).

| Case | Expected valid | Before valid | After valid | Rule / serializer rejection | Verdict |
|---|---|---|---|---|---|
| positive | True | True | True | {'P.SP.02.MSG.004.REQ.2': 'PASS'} | PASS |
| missing | False | True | False | {'P.SP.02.MSG.004.REQ.2': 'FAIL'} | PASS |
| forbidden | False | True | False | {'P.SP.02.MSG.004.REQ.2': 'FAIL'} | PASS |
| wrong_code | False | True | False | {'P.SP.02.MSG.004.REQ.2': 'FAIL'} | PASS |
| both | False | True | False | {'P.SP.02.MSG.004.REQ.2': 'FAIL'} | PASS |
| form_tamper | True | True | True | {'P.SP.02.MSG.004.REQ.2': 'PASS'} | PASS |
| serializer_tamper | False | True | False | [{'rule_id': 'P.SP.02.MSG.004.REQ.2', 'code': 'STRUCTURED_RULE_FAILED'}] | PASS |

## GUI and resolver

before.json and after.json contain real get_form(), EffectiveMessageFieldPolicy and GuiController control states. Code: before editable/no policy; after FIXED07320, editable=False. Direct Name: before editable/no policy; after FORBIDDEN, editable=False and hidden. Scoped source rules for required EventDate/fixed StatusCode remain derived visual policies, not newly application-enforced contextual fields.

gui_probe.py instantiated the actual PySide6 GuiViewModel with QGuiApplication (offscreen), selected OP22/TRN003/MSG004, attempted both forbidden edits via setFieldValue(), and called generateXml(). GUI_GENERATED.xml contains07320 and no direct Name; gui_evidence.json records fields and generation status. This is executable Qt model/controller proof, not manual desktop visual inspection. The application also sanitizes malicious/stale values before body generation; direct low-level serializer rejects the invalid input with BodyValidationError/REQ2 rather than emitting invalid XML.

The generated integration XML reports VERSION_PLACEHOLDER_TEST. It is not production-XSD proof. Body XML files and GUI_GENERATED.xml are actual serialized artifacts. Raw XML tampering is checked independently of application sanitization. sources.json preserves original PDF/RTF extracts and source hashes. before/after JSON preserve exact rejection IDs.
