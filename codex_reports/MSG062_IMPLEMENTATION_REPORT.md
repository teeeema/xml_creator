# P.SP.02.MSG.062 IMPLEMENTATION REPORT

## STATUS
COMPLETE

## VERDICT
READY

## CHANGED_FILES
- `P.SP.02_OP_22/message_rules/P.SP.02.MSG.062.yaml`
- `P.SP.02_OP_22/tests/test_msg062_safe_mapping.py`
- `P.SP.02_OP_22/tests/test_msg062_repeatable_xml.py`
- `P.SP.02_OP_22/tests/test_msg062_end_to_end.py`
- `codex_reports/MSG062_IMPLEMENTATION_REPORT.md`

## NORMATIVE_INVENTORY
- **Authoritative Source**: Decision No. 22 (`ОП_22.pdf`), Section 92, Table 81, physical pages 816–820 (document pages 237–241).
- **Captured Table Rows**: 16 total
  - Row 1: Item 1 (p. 817)
  - Row 2: Item 2 (p. 817)
  - Row 3: Item 3 (p. 818)
  - Row 4: Item 4 (p. 818)
  - Row 5: Item 5 (p. 818)
  - Row 6: Item 6–29 (p. 818, references Table 44 items 6–29)
  - Row 7: Item 30 (p. 819)
  - Row 8: Item 31 (p. 819)
  - Row 9: Item 32 (p. 819)
  - Row 10: Item 33 (p. 819)
  - Row 11: Item 34 (p. 819)
  - Row 12: Item 35 (p. 819)
  - Row 13: Item 36 (p. 819)
  - Row 14: Item 37 (p. 820)
  - Row 15: Item 38 (p. 820)
  - Row 16: Item 39 (p. 820)
- **Expanded Requirements**: 39 distinct requirements (Items 1–39).

## STRUCTURE
- **Structure**: `R.IP.SP.02.002` (version `1.0.0`), namespace `urn:EEC:R:IP:SP:02:TrademarkRegistrationDetails:v1.0.0`, root element `TrademarkRegistrationDetails`.
- **Transaction**: `P.SP.02.TRN.053` ("направление доводов заявителя в отношении обращения заинтересованного лица").
- **Procedure**: `P.SP.02.PRC.009`.
- **Initiating Operation**: `P.SP.02.OPR.194`.
- **Responding Operation**: `P.SP.02.OPR.195`.
- **Initiating Participant**: `P.SP.02.ACT.001`.
- **Responding Participant**: `P.SP.02.ACT.002`.
- **Initiating Message**: `P.SP.02.MSG.062`.
- **Response Message**: `P.SP.02.MSG.002`.
- **Direction**: `REQUEST` (initiating message of `REQUEST_RESPONSE` transaction).

## INHERITANCE
- Full 3-hop inheritance established: `Table 81 (p. 818) -> Table 44 (pp. 715–721) -> Table 34 (pp. 514–520)`.
- Verified directly in `/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf`.
- Each expanded requirement in range 6–29 retains confirmed source references pointing to Table 81, Table 44, and Table 34.

## MAPPING_COUNTS
- **Captured Table Rows**: 16
- **Expanded Requirement Count**: 39
- **Arithmetic Verification**: 33 + 1 + 2 + 1 + 2 + 0 = 39
  - `FULLY_MAPPABLE`: 33
  - `SAFE_PARTIAL`: 1
  - `EXTERNAL`: 2
  - `AMBIGUOUS`: 1
  - `ENGINE_UNSUPPORTED`: 2
  - `SOURCE_CONFLICT`: 0

## FULLY_MAPPABLE (33)
- **Table 81 REQ 1**: Exactly 1 `ipcdo:TrademarkApplicationDetails` instance (`selection_cardinality`, min 1, max 1).
- **Table 81 REQ 5**: `ipcdo:ArgumentDetails` required inside `ipcdo:TrademarkApplicationDetails`.
- **Inherited REQ 6**: `ipsdo:ApplicationReceiptDate` formatted per ISO 8601.
- **Inherited REQ 7**: `csdo:UnifiedCountryCode/@codeListId` == "ВОИС ST.3" wherever `UnifiedCountryCode` is present.
- **Inherited REQ 8**: `ccdo:SubjectAddressDetails` required fields (AddressKindCode, UnifiedCountryCode, CityName, StreetName, BuildingNumberId).
- **Inherited REQ 9**: `ccdo:CommunicationDetails` required fields (CommunicationChannelCode, CommunicationChannelId; CommunicationChannelName forbidden).
- **Inherited REQ 10**: `CommunicationChannelCode` allowed enumeration ("AO", "EM", "FX", "TE", "TF", "TL").
- **Inherited REQ 11**: `ipcdo:PatentAuthorityDetails` required fields (UnifiedCountryCode, AuthorityName, OriginOfficeIndicator).
- **Inherited REQ 12**: `OriginOfficeIndicator` == True.
- **Inherited REQ 14**: Exactly 1 applicant `IPPartyDetails` (IPPartyKindCode == "AP").
- **Inherited REQ 15**: In applicant `IPPartyDetails`: `SubjectAddressDetails` and `IPSubjectName` required.
- **Inherited REQ 16**: In applicant `IPPartyDetails`: `IPSubjectName/@nameRepresentationKindCode` in {"OR", "LA"}.
- **Inherited REQ 17**: In applicant `IPPartyDetails`: exactly 1 `IPSubjectName` with `@nameRepresentationKindCode` == "OR" and languageCode present.
- **Inherited REQ 20**: In applicant `IPPartyDetails`: `SubjectAddressDetails/csdo:AddressKindCode` == "2".
- **Inherited REQ 21**: If `IPPartyKindCode` == "PA": `SubjectAddressDetails` and `IPSubjectName` required.
- **Inherited REQ 22**: If `IPPartyKindCode` == "RE": `SubjectAddressDetails` and `IPSubjectName` required.
- **Inherited REQ 23**: In `ipcdo:CorrespondenceAddressDetails`: `SubjectAddressDetails/csdo:AddressKindCode` == "3".
- **Inherited REQ 24**: In `ipcdo:CorrespondenceAddressDetails`: `ccdo:CommunicationDetails` required.
- **Inherited REQ 25**: Exactly 1 `ipcdo:TrademarkDetails` instance, with `TMDescriptionDetails`, `TrademarkKindCode`, `TrademarkKindName`, `CollectiveMarkIndicator` required.
- **Inherited REQ 26**: `TrademarkKindCode` in 110..180 or `TrademarkKindName` in standard kind names.
- **Inherited REQ 27**: For kinds 140..180: `TrademarkPicture` and `TrademarkColourName` required.
- **Inherited REQ 28**: `CollectiveMarkIndicator` in {"0", "1"}.
- **Inherited REQ 29**: At least 1 `ipcdo:GoodsBaseDetails` instance; `GoodsClassCode`, `GoodsClassName`, `GoodsName` required.
- **Table 81 REQ 30**: In `ipcdo:TrademarkClaimDetails`: `StakeholderDetails`, `RequestId`, `RequestDate` required.
- **Table 81 REQ 31**: In `ipcdo:TrademarkClaimDetails/ipcdo:StakeholderDetails`: `UnifiedCountryCode`, `SubjectName`, `SubjectBriefName`, `SubjectAddressDetails` required.
- **Table 81 REQ 32**: In `ipcdo:TrademarkApplicationDetails/ipcdo:ArgumentDetails`: `DescriptionText`, `EventDate` required.
- **Table 81 REQ 33**: In `ipcdo:TrademarkApplicationDetails`: `TrademarkNationalApplicationDetails`, `ApplicantChangeDetails`, `ComplaintDetails`, `ApplicantComplainResponseDetails` forbidden (0..0).
- **Table 81 REQ 34**: `ipcdo:RefusalDetails` forbidden (0..0).
- **Table 81 REQ 35**: In `ccdo:ResourceItemStatusDetails`: `ValidityPeriodDetails/csdo:StartDateTime` required.
- **Table 81 REQ 36**: In `ccdo:ResourceItemStatusDetails`: `ValidityPeriodDetails/csdo:EndDateTime` forbidden.
- **Table 81 REQ 37**: `ipcdo:SignatureDetails` min_occurs 1; if `OfficerDetails` present -> `FullNameDetails` forbidden.
- **Table 81 REQ 38**: In `ipcdo:SignatureDetails`: if `FullNameDetails` present -> `OfficerDetails` forbidden.
- **Table 81 REQ 39**: In `ipcdo:OfficerDetails`: `FullNameDetails/csdo:LastName`, `FullNameDetails/csdo:FirstName`, `csdo:PositionName` required; `ccdo:CommunicationDetails` forbidden.

## SAFE_PARTIAL (1)
- **Table 81 REQ 4**:
  - *Safe Fragment*: `ipsdo:TrademarkApplicationId` is REQUIRED inside `ipcdo:TrademarkApplicationDetails`.
  - *Unmapped Remainder*: External query against national patent office database for record with `StatusCode` == '02', empty `EndDateTime`, and matching `TrademarkApplicationId`.

## EXTERNAL (2)
- **Table 81 REQ 2**: Classifier 92 inclusion condition for "Доводы заявителя в отношении обращения заинтересованного лица...".
- **Table 81 REQ 3**: Classifier 92 absence condition for "Доводы заявителя в отношении обращения заинтересованного лица...".

## AMBIGUOUS (1)
- **Inherited REQ 13**: `IPPartyKindCode` == "AP" without distinct repeated party scope, conflicting with representative and patent attorney parties.

## ENGINE_UNSUPPORTED (2)
- **Inherited REQ 18**: Conditional secondary `IPSubjectName` language representation rules.
- **Inherited REQ 19**: Conditional address script representation rules.

## SOURCE_CONFLICT (0)
- None identified.

## EXECUTABLE_REQUIREMENTS (40 structured rules)
Covering all 33 FULLY_MAPPABLE and 1 SAFE_PARTIAL requirements:
- REQ 1: Cardinality min 1, max 1
- REQ 4: Application ID presence
- REQ 5: ArgumentDetails presence
- REQ 6: ApplicationReceiptDate presence
- REQ 7: CodeListId == "ВОИС ST.3"
- REQ 8: Address required fields
- REQ 9: Communication details required fields and forbidden name
- REQ 10: Communication channel codes
- REQ 11: Patent authority required fields
- REQ 12: OriginOfficeIndicator == True
- REQ 14: Exactly 1 AP party
- REQ 15: AP party name and address presence
- REQ 16: AP party name representation kind code in {OR, LA}
- REQ 17: Exactly 1 primary AP name with languageCode
- REQ 20: AP address kind code == "2"
- REQ 21: PA party name and address presence
- REQ 22: RE party name and address presence
- REQ 23: Correspondence address kind code == "3"
- REQ 24: Correspondence communication details presence
- REQ 25: Trademark details cardinality and required fields (2 rules)
- REQ 26: Trademark kind code or name condition
- REQ 27: Trademark picture and colour conditional presence
- REQ 28: Collective mark indicator values
- REQ 29: Goods base details cardinality and required fields (2 rules)
- REQ 30: Trademark claim details required fields
- REQ 31: Stakeholder details required fields
- REQ 32: ArgumentDetails DescriptionText and EventDate presence
- REQ 33: Forbidden details (4 cardinality rules)
- REQ 34: RefusalDetails forbidden (cardinality 0..0)
- REQ 35: Resource status StartDateTime required
- REQ 36: Resource status EndDateTime forbidden
- REQ 37: Signature presence and officer-branch mutual exclusion (2 rules)
- REQ 38: Signature fullname-branch mutual exclusion
- REQ 39: Officer details required fields and forbidden communication details

## UNMAPPED_REQUIREMENTS
- REQ 2 (classifier 92 inclusion)
- REQ 3 (classifier 92 absence)
- REQ 4 (remainder: national patent office database lookup)
- REQ 13 (ambiguous party kind scope)
- REQ 18 (unsupported secondary language code constraints)
- REQ 19 (unsupported address script constraints)

## IMPLEMENTATION
1. `P.SP.02_OP_22/message_rules/P.SP.02.MSG.062.yaml`:
   - Expanded 39 declarative business rules with 3-hop source references for inherited requirements 6–29.
   - Added 40 structured rules covering 34 requirements.
   - Added full `mapping_audit` metadata with `captured_row_count: 16`, `expanded_requirement_count: 39`, classification counts, summary, partial remainders, and 39-item inventory.
2. Test Suites:
   - `P.SP.02_OP_22/tests/test_msg062_safe_mapping.py`: 16 test functions validating inventory integrity, classification arithmetic, 3-hop source references, unmapped requirement safety, and individual structured rule evaluations.
   - `P.SP.02_OP_22/tests/test_msg062_repeatable_xml.py`: 13 test functions verifying XML extraction, element-tree construction, namespace correctness, cardinality constraints, repeatable contexts, and isolation.
   - `P.SP.02_OP_22/tests/test_msg062_end_to_end.py`: 8 test functions validating transaction metadata binding (`P.SP.02.TRN.053`), round-trip build-serialize-parse-extract-validate pipeline, and failure modes on invalid or missing fields.

## OWNER_QNAME_SAFETY
- Every target path uses exact qualified names with confirmed namespace prefixes (`ipcdo:`, `ipsdo:`, `csdo:`, `ccdo:`).
- `ArgumentDetails` and `TrademarkClaimDetails` are evaluated strictly inside `ipcdo:TrademarkApplicationDetails`.
- `RefusalDetails` is evaluated strictly at the root structure level.

## REPEATABLE_RECORD_SAFETY
- Exactly 1 `ipcdo:TrademarkApplicationDetails` instance is enforced via `selection_cardinality`.
- AP-party rules are scoped via `selector.parent` to `IPPartyDetails[IPPartyKindCode='AP']`.
- Repeatable goods and signature items enforce constraints across each child instance independently.

## MESSAGE_ISOLATION
- All rules are strictly scoped by `rule_id` prefix `P.SP.02.MSG.062.` and `applies_to_structure: "R.IP.SP.02.002"`.
- Transaction `P.SP.02.TRN.053` binds exclusively to `P.SP.02.MSG.062` (request) and `P.SP.02.MSG.002` (response).

## NORMATIVE_BASIS
- CONFIRMED — Decision No. 22 (`ОП_22.pdf`), Section 92, Table 81, physical pages 816–820; Table 44, physical pages 715–721; Table 34, physical pages 514–520.

## MSG062_TESTS
- `pytest P.SP.02_OP_22/tests/test_msg062_*.py`:
  - 37 passed in 0.77s

## ENGINE_VALIDATOR_REGRESSION
- `pytest eaeu_xml/tests/test_structured_rules.py eaeu_xml/tests/test_process_package_validator.py`:
  - 40 passed, 5 subtests passed in 0.09s

## FULL_OP22_REGRESSION
- `pytest P.SP.02_OP_22/tests`:
  - 2348 passed, 0 failed, 0 errors in 96.38s

## GIT_DIFF_CHECK
- Confirmed strictly task-owned changes:
  - `P.SP.02_OP_22/message_rules/P.SP.02.MSG.062.yaml`
  - `P.SP.02_OP_22/tests/test_msg062_safe_mapping.py`
  - `P.SP.02_OP_22/tests/test_msg062_repeatable_xml.py`
  - `P.SP.02_OP_22/tests/test_msg062_end_to_end.py`
  - `codex_reports/MSG062_IMPLEMENTATION_REPORT.md`
- No foreign files, no core Python infrastructure, and no MSG063 files were modified.

## REMAINING_ISSUES
None
