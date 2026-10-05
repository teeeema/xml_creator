# MSG032 Independent Final Review

## STATUS

STATUS = COMPLETE

## VERDICT

VERDICT = READY

## EXECUTIVE_SUMMARY

Independent read-only review completed for `P.SP.02.MSG.032`. The implementation report is substantively confirmed against the repository StructureDefinition, message YAML, mapping audit, production XML tests, and the requested normative page references.

No MSG032 production defect was found. The implementation keeps unsupported or externally dependent semantics unmapped and does not strengthen Table 44 REQ26 from OR to AND.

## NORMATIVE_RECHECK

Primary source: `/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf`.

Table 50 is the MSG032 table on physical pages 741–743. MSG032 inherits Table 44 REQ6–29. The repository mapping contains a complete expanded inventory for requirements 1–32.

Table 44 REQ26 is an OR requirement: `TrademarkKindCode` OR `TrademarkKindName`. MSG032 leaves it unmapped because the evaluator cannot express the exact per-parent disjunction without requiring both fields.

Table 44 REQ27 is same-parent: the triggering code/name and the required `TrademarkPicture` and `TrademarkColourName` are evaluated within the same `TrademarkDetails` instance.

Table 50 REQ30 is conditional on existing `AccompanyingDocumentsDetails` instances. It does not require at least one document instance. The implementation correctly uses vacuous PASS when the optional collection is absent and checks six required children for every existing instance.

## TRANSACTION_CONTEXT

Confirmed:

- message: `P.SP.02.MSG.032`
- transaction: `P.SP.02.TRN.027`
- procedure: `P.SP.02.PRC.006`
- initiating operation: `P.SP.02.OPR.022`
- responding operation: `P.SP.02.OPR.023`
- initiating participant: `P.SP.02.ACT.002`
- responding participant: `P.SP.02.ACT.001`
- response message: `P.SP.02.MSG.002`
- structure: `R.IP.SP.02.002` version `1.0.0`
- root QName: `{urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0}TrademarkRegistrationDetails`

## EXPANDED_INVENTORY

Expanded count: **32**, with every requirement code 1–32 present exactly once in `mapping_audit.inventory`.

Classification:

- `FULLY_MAPPABLE`: 1, 5–12, 14–15, 21–25, 27–32
- `SAFE_PARTIAL`: 2–4
- `AMBIGUOUS`: 13
- `ENGINE_UNSUPPORTED`: 16–20, 26
- `EXTERNAL`: none as primary classification
- `SOURCE_CONFLICT`: none

The implementation’s inventory and classification summary match the YAML assertions and tests.

## CLASSIFICATION_COMPARISON

The implementation report classifications are confirmed.

REQ2 and REQ3 contain only local necessary implications. Classifier membership and classifier absence are explicitly retained as external/unmapped remainder; they are not simulated.

REQ4 requires only the direct application `TrademarkApplicationId` locally. External resource existence, external status, external end date, and equality with the external record remain unmapped.

REQ13 remains ambiguous because a global AP requirement would conflict with the explicit PA/RE party branches.

REQ16–20 remain unmapped because the current evaluator lacks the required exact nested repeated correlation/filter semantics.

## REQ1_5_REVIEW

- REQ1: exact cardinality 1..1 for direct `ipcdo:TrademarkApplicationDetails`; correct.
- REQ2: direct `ipsdo:IPDocKindCode` present implies same-parent `ipsdo:IPDocKindName` forbidden; safe partial.
- REQ3: when direct code is absent, exact normative fallback name is required; classifier absence remains unmapped; safe partial.
- REQ4: direct `ipsdo:TrademarkApplicationId` required; external lookup/equality remains unmapped.
- REQ5: direct `ipcdo:ComplaintDetails` required; exact owner is used.

## TABLE44_REVIEW

Inherited REQ6–29 use dual provenance for Table 50 inheritance and original Table 44 rows. The mapped subset is limited to evaluator-safe assertions. REQ13 and REQ16–20 are not approximated.

## REQ26_REVIEW

PASS. REQ26 is classified `ENGINE_UNSUPPORTED` and has no structured rule. No pair-consistency rule and no simultaneous Code-and-Name requirement were introduced. The normative OR semantics are preserved by leaving the exact assertion unmapped.

## REQ27_REVIEW

PASS. The rule is scoped to `ipcdo:TrademarkApplicationDetails/ipcdo:TrademarkDetails` and uses an `any` condition over the same parent’s `ipsdo:TrademarkKindCode` and `ipsdo:TrademarkKindName`. The required `ipsdo:TrademarkPicture` and `ipsdo:TrademarkColourName` are evaluated in that same parent.

Production tests cover good+good, bad+good, and good+bad repeated trademark instances and verify no cross-parent satisfaction.

## REQ30_REVIEW

PASS. The selector is the direct collection:

`ipcdo:TrademarkApplicationDetails/ipcdo:AccompanyingDocumentsDetails`

Each existing document requires exactly these six children:

- `ipsdo:IPDocKindCode`
- `csdo:DocId`
- `csdo:DocCreationDate`
- `csdo:DescriptionText`
- `csdo:PageQuantity`
- `csdo:DocBinaryText`

The collection remains optional. Production tests cover good+good, bad+good, good+bad, absent collection, wrong namespace, and same-local-name nested documents under another owner.

## REQ31_32_REVIEW

PASS.

- REQ31 requires `ccdo:ResourceItemStatusDetails/ccdo:ValidityPeriodDetails/csdo:StartDateTime`.
- REQ32 forbids the corresponding `csdo:EndDateTime`.

The YAML uses `for_each` over `ccdo:ResourceItemStatusDetails` and exact relative child paths.

## QNAME_OWNER_REVIEW

PASS. Direct and nested owners are distinguished by exact paths and QName-aware extraction.

Verified by repository tests:

- nested complaint `PatentAuthorityDetails` does not satisfy direct authority rules;
- nested `AccompanyingDocumentsDetails` under NamingAbilityProof does not trigger direct REQ30;
- wrong-namespace `IPDocKindCode` does not satisfy the normative field;
- direct application, complaint, party, trademark, goods, resource, and validity owners match the StructureDefinition.

## REPEATABLE_XML_REVIEW

Existing MSG032 production XML tests cover:

- SubjectAddressDetails: good+good, bad+good, good+bad;
- CommunicationDetails: good+good, bad+good, good+bad;
- AP/RE and RE/AP party ordering;
- same-parent TrademarkDetails REQ27;
- GoodsBaseDetails good+good, bad+good, good+bad;
- AccompanyingDocumentsDetails good+good, bad+good, good+bad;
- absent optional documents;
- QName and nested-owner collisions;
- full build → serialize → parse → extract → validate pipeline.

## NEGATIVE_PROOF_MATRIX

| Requirement | Executable rule / proof | Result |
|---|---|---|
| REQ1 | cardinality 0 and 2 | PASS |
| REQ2 | code present with forbidden name | PASS |
| REQ3 | wrong fallback name | PASS |
| REQ4 | missing direct application ID | PASS |
| REQ5 | missing ComplaintDetails | PASS |
| REQ6–12 | independent production XML mutations | PASS |
| REQ14–15 | independent party/address/communication mutations | PASS |
| REQ21–25 | independent party/trademark mutations | PASS |
| REQ27 | bad trademark parent at either index | PASS |
| REQ28–29 | independent indicator/goods mutations | PASS |
| REQ30 | each of six children, both repeated positions | PASS |
| REQ31 | missing StartDateTime | PASS |
| REQ32 | present EndDateTime | PASS |

Unmapped requirements have no executable negative proof by design: REQ13, REQ16–20, and REQ26 remain explicitly unmapped.

## MESSAGE_ISOLATION

PASS for MSG031 and MSG032. Both rule sets are non-empty, message prefixes are correct, sets are disjoint, and MSG032 validation evaluates only MSG032 rule IDs. MSG033 state was ignored as a normative baseline and was not used to assess MSG032 correctness.

## TEST_RESULTS

Executed with `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider`:

```text
P.SP.02_OP_22/tests/test_msg032_*.py
65 passed in 1.61s

P.SP.02_OP_22/tests/test_msg031_*.py
84 passed in 1.69s

eaeu_xml/tests/test_structured_rules.py
eaeu_xml/tests/test_repeatable_xml_alignment.py
35 passed, 5 subtests passed in 0.11s
```

## DEFECTS

None found in MSG032.

## DISAGREEMENTS_WITH_IMPLEMENTATION_REPORT

None material found.

## EXTERNAL_REMAINDERS

Classifier membership/absence and filing-office resource state remain intentionally external and are not simulated by local rules.

## ENGINE_REMAINDERS

Exact AP-scoped nested repeated correlation semantics for REQ16–20 and exact per-parent OR semantics for REQ26 remain unsupported by the evaluator and are correctly left unmapped.

## CONCURRENT_CHANGES_IGNORED

MSG033 concurrent work was excluded from this audit and was not used as a baseline or defect source.

## REPOSITORY_STATE

The repository was already dirty before this review, including the concurrent MSG032 implementation files and unrelated earlier work. This review did not modify YAML, Python, tests, StructureDefinitions, source references, classifiers, process metadata, or AGENTS.md. The only review output written is this report.

## FINAL_VERDICT

READY. The requested acceptance conditions are independently satisfied: complete Table 50 inventory, safe classification, no REQ26 strengthening, same-parent REQ27, optional per-document REQ30, exact REQ31/32 ownership, QName isolation, production XML coverage, negative proof coverage, message isolation, green focused tests, and no production modifications by this review.

Repository modifications: NONE.
