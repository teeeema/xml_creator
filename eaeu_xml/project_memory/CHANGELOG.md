# Changelog

## 2026-08-27 — Universal process registry

- Added explicit-root ProcessRegistry without duplicating package parsing.
- Added version-keyed local/shared resolution and fail-fast ambiguous collisions.
- Preserved ProcessPackageLoader.load(Path) and existing production process data/APIs.
- Added synthetic multi-process/shared/collision and relationship architecture tests.
- Passed the 191-test full macOS suite; introduced no production process hardcodes.

## 2026-08-25 — Guide TreeCtrl selection details

- Replaced unstable `TreeItemId.GetID()` / `sip.voidptr` mapping with TreeCtrl item data carrying a value-stable message/path key.
- Added one details formatter for leaf fields, attributes and structural groups, including QName, filling policy, example and source trace.
- Made message rebuild clear details and made search/context-field opening populate details immediately.
- Passed real macOS wx selection smoke for leaf, group, nested field, message switch, search and context open.

## 2026-08-25 — Conservative conditional smart form

- Added explicit source-traced ConditionalFieldRule compilation without NLP/XML-name heuristics.
- Added shared TRUE/FALSE/UNKNOWN evaluation, five effects, dependency indexing and partial reevaluation.
- Applied condition projection before display filters/search and shared conditional-required validation with Application Facade.
- Preserved hidden conditional values/repeatable instances and draft roundtrips; added diagnostic reveal and hidden-search guide access.
- Added conditional summary counts, `[Условно]` markers and Guide automatic-check metadata.
- Audited P.MM.01 at 133 unresolved textual usages and zero machine-evaluable rules; no normative data or conflicts were changed.

## 2026-08-24 — Large form filtering

- Added generic `FormDisplayMode`, immutable `FormPresentation` and hierarchy-preserving `FieldVisibilityFilter`.
- Added ALL, required, user-facing, validation-error and filled-only modes plus debounced five-metadata search.
- Kept hidden-by-filter values and repeatable items in complete BodyValues; validation still processes the complete form state.
- Added facade-provided message summary, a primary user-fields toggle, classifier/external/unresolved markers, collapsible groups and reveal/scroll/focus error navigation.
- Added matching filters to the structured Guide reader without changing its shared DTO counts.
- Verified MSG.001 at 401 ALL, 168 REQUIRED and 398 USER_FIELDS nodes and passed real macOS wx smoke.

## 2026-08-24 — Source-traced common-process addressing

- Added generic participant definitions and a component-based CP logical
  address builder.
- Removed facade derivation of participant codes from `EEC`/`RU` segments.
- Added transaction endpoint validation while keeping all concrete participant
  codes in external process packages.

## 2026-08-24 — Clipboard result and placeholder guidance

- Made wx clipboard success depend on `SetData`, with `Flush` retained only as
  best effort for platform persistence.
- Made the Copy XML action use the XML currently displayed in the preview.
- Replaced the terse TEST comment with definitions of `Y.Y.Y` and `X.X.X` and
  the supplied reference to paragraph 2 of Decision No. 122 of 25 October 2016.

## 2026-08-24 — Placeholder comment and clipboard reliability

- Added a neutral TEST-only XML comment listing only placeholder tokens actually
  used by the generated message.
- Fixed the wx clipboard lifecycle with checked Open/SetData and guaranteed
  Close; preview, copy and save now explicitly use the same XML text.
- Verified real macOS clipboard roundtrip and preview/file equality.

## 2026-08-24 — TEST-only normative version placeholders

- Added explicit per-structure placeholder resolution for TEST without changing
  nullable active versions or substituting guessed semantic versions.
- STRICT now rejects placeholders in root or imported namespaces; generation
  metadata exposes unresolved structures and literal placeholder tokens.
- Added grouped one-namespace-per-line Envelope formatting shared by preview
  and saved XML, plus GUI TEST warnings and mode-dependent process issues.
- Reclassified all 43 P.MM.01 branches and refreshed reference artifacts.

## 2026-08-24 — Typed process/message diagnostics

- Added generic ProcessIssueView and facade aggregation for unresolved versions,
  normative conflicts, unavailable classifiers and delegated external sources.
- Added success/warning/blocked message presentations, human explanations,
  suggested actions, source/conflict details and explicit generation rules.
- Added message-selector markers and a Process Issues dialog with blocking and
  warning filters.
- Kept user-input validation distinct from system/normative blocks and reserved
  the internal-error dialog for unexpected exceptions.
- Passed a real wx macOS smoke for VERIFIED, NORMATIVE_CONFLICT and the nine-item
  P.MM.01 process issue summary.

## 2026-08-24 — Large-form GUI usability iteration

- Replaced the permanent split preview with Data/XML notebook pages and gave
  the recursive scrolled form the main window area.
- Added full-width selectors, compact status, label-above-input field layout,
  generic examples, tooltips, field information dialogs, validation navigation,
  XML copy/save and a separate settings dialog.
- Separated concise human display names from technical XML QName; for example,
  `Заголовок электронного документа` is visible while `ccdo:EDocHeader` remains
  in help metadata.
- Fixed optional repeatable complex groups so an empty UI does not create a
  phantom instance and false required-child validation.
- Passed real wx 4.3.1 macOS smoke for resolved and blocked P.MM.01 scenarios.

## 2026-08-24 — First wxPython GUI

- Added a presentation-only wx desktop window driven exclusively by
  EaeuXmlApplication and public DTOs.
- Added recursive scrolled forms, scalar/nested/attribute/fixed/forbidden and
  repeatable controls, test-data fill, validation output, XML preview/save and
  in-memory request/response sessions.
- Added a display-independent GuiController with engine-fixture and P.MM.01
  tests for selection, mapping, values, blockers, TEST_ONLY, generation and
  correlation state.
- Added `python -m eaeu_xml.gui`, the `eaeu-xml-gui` console entry point and an
  optional `gui` dependency; core installation remains wx-free.

## 2026-08-24 — Public application facade for future GUI

- Added explicit-root process discovery and stable process, transaction,
  message, form, validation and generation DTOs.
- Added hierarchical StructureDefinition + MessageRules form projection for
  nested/repeatable fields, attributes, required/fixed/forbidden policies and
  classifier metadata.
- Added deterministic seeded TestDataGenerator and high-level TEST SOAP
  generation with typed blockers/warnings instead of routine stack traces.
- Added TransactionSession backed by the existing Decision No. 5
  TransactionInstance, MessageFactory and CorrelationService.
- Recorded that GUI clients must not read YAML, implement Decision No. 5 rules
  or construct XML themselves.

## 2026-08-24 — Explicit normative-conflict boundary

- Added generic validation of normative-conflict metadata.
- Body validation now returns source-traced `NORMATIVE_CONFLICT` issues for an
  affected MessageRule and prevents silent serialization.
- No process-specific identifiers or matching logic were added to the engine.

## 2026-08-24 — Interpretation metadata and arbitrary XML

- Added generic field interpretation status/reason metadata and validation.
- Added direct serialization for normatively declared arbitrary XML children.
- Kept all concrete P.MM.01 interpretation data outside the engine.

## 2026-08-24 — Generic data-driven Body engine

- Added version-specific field definitions and table-coverage metadata to the
  universal ProcessPackage model and loader.
- Added package validation for field hierarchy, ordering, cardinality, sources
  and typed message-rule field references.
- Added aggregate Body validation with STRICT/TEST modes and generic XML
  serialization for nesting, repeatables, attributes, namespaces and fixed values.
- Integrated Body building through `EaeuXmlEngine` without process-specific code.

## 2026-08-20 — Per-structure active versions

- Replaced scalar profile selections with independent nullable
  `{active_version: ...}` entries.
- Added `StructureVersionResolver` and local
  `UNRESOLVED_STRUCTURE_VERSION` behavior.
- Permitted unresolved structures without blocking resolved siblings.
- Added a two-structure, four-version fixture and independence tests.

## 2026-08-20 — Generic operation and catalog metadata

- Added process-agnostic `OperationDefinition` loading and transaction
  cross-reference validation.
- Extended source, message and structure metadata needed by external normative
  catalogs without adding Body logic.

## 0.4.0 — 2026-08-20

- Added process-agnostic ProcessPackage, Process/Procedure/Transaction/Message/Structure definitions, MessageRules, VersionProfile and SourceReference.
- Added explicit-Path ProcessPackageLoader and cross-reference/orphan ProcessPackageValidator.
- Added EaeuXmlEngine accessors and integration with the verified Decision №5 ActionBuilder.
- Added ProcessBodyProvider and explicit NotImplementedProcessBodyProvider without concrete Body logic.
- Added the synthetic `tests/fixtures/P.TEST.01` package with two isolated structure versions.
- Created external `P.MM.01/` skeleton with zero normative definitions and `NEEDS_NORMATIVE_SOURCES`.
- Preserved the dependency-free core by using JSON-compatible YAML 1.2 manifests.

## 0.3.1 — 2026-08-20

- Audited the complete project for parent-directory, legacy-module, absolute-path, requirements and runtime filesystem dependencies.
- Localized all normative-source references to `./15kr0005.doc`; no copy was needed because the verified file was already present.
- Added automated self-containment tests for source hash/location, forbidden paths/imports and symlinks.
- Updated package metadata and README to the verified 0.3 core state.
- Confirmed 41 tests and imports from a temporary standalone copy with no adjacent legacy project.

## 0.3.0 — 2026-08-20

- Completed the full normative audit of the implemented Decision №5 core.
- Consolidated the duplicate Integration ownership rule; final registry contains 45 unique rules.
- Added automatic Decision5RuleCoverage and a meta-test: 45 verified, zero missing tests or remaining mismatches.
- Corrected ProblemMessage string semantics, stage-aware history validation, retry state restrictions and strict Fault correlation validation.
- Completed mutual-obligations final error window and explicit request-confirmation/notification transitions.
- Added Envelope and Retry validators plus the process-specific DuplicatePolicy boundary.
- Generated and parsed ten reference XML files in `examples/decision5/`.
- Added `DECISION_5_VERIFICATION_REPORT.md`; final suite contains 37 tests.

## 0.2.0 — 2026-08-20

- Added platform-owned IntegrationMetadata, TrackId, AcceptTime and enrichment context.
- Added typed RCV, PRS and ERR signal messages with appendix 5 Body structures.
- Added separate SOAP Fault branch, typed codes, Russian localized reasons, RelatesAction/xml:lang attributes and safe ProblemMessage subtree.
- Added all six Decision №5 transaction patterns, state machine, typed parameters, timeout outcomes and retry records.
- Made CorrelationService state-machine-aware while preserving the Stage 2 API fallback.
- Expanded the source registry from 21 to 46 rules and test suite from 17 to 29 tests, including ten well-formed reference XML scenarios.

## 0.1.0 — 2026-08-20

- Created independent src-layout project and project memory.
- Read and registered `15kr0005.doc` as the primary read-only source.
- Added 21 source-traced Decision №5 rules.
- Implemented namespaces, addresses, identifiers, Action, Header policy, procedure/transaction state, correlation, message factory and SOAP serializer.
- Added positive and negative Stage 2 tests.
- Recorded two prompt/source conflicts and unresolved external-source questions.
## 2026-08-24

- Добавлен универсальный application-сервис атомарных JSON-черновиков.
- GUI получил open/save/save-as, dirty confirmation, autosave и crash recovery.
- Добавлены generic и P.MM.01 integration/regression tests для черновиков.
# 2026-08-24

- Добавлены FieldInputPolicyDefinition/Resolver и validation process metadata.
- FormDefinition/FieldView расширены policy/value source/help/condition; добавлен `get_message_input_summary`.
- GUI использует готовую policy, показывает external/unresolved/conditional notices и не создаёт scalar control для structural containers.
- Добавлены generic regression tests input-policy resolver.
# 2026-08-24 — UI policy separation

- Добавлены `UiInputPolicyDefinition`, loader/validator и generic `UiInputPolicyResolver`.
- `FieldView` теперь отдельно переносит normative/UI policy и policy origin.
- GUI controls и message input summary переведены на UI policy.
- Добавлены GROUP presentation, classifier TEST fallback, external/read-only presentation и generic tests.
# 2026-08-24 — P.MM.01 user guide

- Добавлены ProcessGuide/MessageGuide/FieldGuide, guide search и четыре Facade methods.
- Добавлен wx reader «Сводка» с сообщениями, поиском, деревом Body и карточкой поля.
- Info controls формы открывают guide на текущем field path; tooltip сокращён.
- Добавлены generators полного Markdown guide и quality report, а также guide regression tests.
# 2026-08-24 — safe guide examples

- Добавлен generic `ExampleValueResolver` и provenance metadata в FieldView/FieldGuide.
- Удалена documentation-эвристика `*Id → UUID`; добавлены safe identifier/code/classifier placeholders.
- Guide instruction text приведён к официальным формулировкам «Укажите…/Выберите…/Значение формируется…».
- Добавлены example/unresolved audits и regression tests.
# 2026-08-25 — explicit MessageRules coverage

- Added source-backed per-message rule-table statuses.
- Added validator consistency checks and human-readable Facade/Guide projections.
- Added regression tests for missing confirmed rule files and unresolved audit status.
# 2026-08-25 — assisted editable identifiers and date/time controls

- Added generic presentation capabilities without changing normative policies.
- Added IdentifierService-backed generation, date calendar/Today and zoneinfo-backed Now controls.
- Added System/UTC/IANA selection, timezone search aliases and persisted default timezone.
- Preserved validation, form filters and draft value handling.
# 2026-08-25 — GUI user acceptance bugfixes

- Fixed enum `wx.Choice` value collection and restoration independently of boolean controls.
- Fixed manual ANY_XML input conversion while preserving validation errors for malformed XML.
- Completed five real macOS wx acceptance scenarios without redesigning the application.

# 2026-08-25 — binary and boolean UX

- Added datatype-driven file picker capability and application-level file/base64 service.
- Added filename/size/MIME presentation, clear action and large-file confirmation.
- Embedded binary values in existing draft v1 without storing local paths.
- Changed boolean display to Да/Нет while preserving typed bool/XML semantics.

# 2026-08-25 — transaction session persistence audit

- Separated Body draft data from persisted Decision №5 transaction runtime state.
- Defined snapshot contents, strict validation, Continue and Open-as-new semantics.
- Recorded current blockers for notification, mutual obligations, retry and transport event status.
- Kept automatic restore disabled and preserved `SESSION_RESTART_REQUIRED`.

# 2026-08-25 — transaction session snapshot v1

- Added versioned portable session/history DTOs and deterministic JSON codec.
- Added strict typed correlation, retry, signal/fault, state/version and stale-timing validation.
- Added fsync + atomic replace storage that preserves the previous snapshot on failure.
- Added explicit TransactionSession capture/save hooks without GUI restore or legacy-draft conversion.

# 2026-08-25 — unified transaction lifecycle and restore

- Added typed two-phase ProcessPackage-aware session restore results.
- Unified new-session and restored-session runtime state transitions through TransactionEngine.
- Added exact ID/history/state replay and runtime-to-snapshot acceptance invariant.
- Proved next response/retry/signal/fault behavior while leaving GUI and legacy drafts unchanged.
# 2026-08-25 — responsive wx layout

- Added horizontal fallback scrolling to the form while preserving vertical scrolling.
- Made filter, data-action and XML-action bars wrap at narrow widths.
- Rewrapped long status/summary text and refreshed form virtual size after resize.
- Added a real-wx narrow/grow regression without changing application or XML logic.
# 2026-08-25 — GUI transaction session controls

- Added distinct Open/Continue/Save Session controls backed by typed lifecycle restore results.
- Added explicit Body-draft Open-as-new flow with fresh session identifiers and no old history.
- Preserved strict invalid/version/timing/state/correlation blocking and RECEIVED limitation.
- Added real-wx restart, correlation, invalid-file and four-size regressions.
# 2026-08-25 — restored-session final XML audit

- Added parser-based continuous-vs-restored response XML and fresh-restart tests.
- Verified response, signal, Fault, notification, invalid restore and identity separation.
- Recorded missing restored Body correlation state and retry XML payload as production blockers.
- Made no production runtime, snapshot-schema, serializer or normative changes.
# 2026-08-25 — message artifact persistence

- Added atomic versioned session bundle and immutable integrity-checked Body artifacts.
- Added source-traced previous-Body correlation and payload-backed retry XML.
- Preserved snapshot v1/SOAP restore separation and legacy draft restrictions.
