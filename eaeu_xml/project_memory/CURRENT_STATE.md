# Current state

Version: `0.4.0`, universal engine plus external process-package architecture.

Logical addressing now consumes source-traced participant definitions from
external process packages. Segment (`EEC` or a supplied ISO alpha-2 test/runtime
value) is independent of participant code. No P.MM.01 participant identifier is
embedded in the universal engine or GUI.

Status: `DECISION_5_CORE_VERIFIED_WITH_UNRESOLVED_ITEMS`.

Deployment boundary: self-contained `eaeu_xml/` directory. The normative source is local at `./15kr0005.doc`; there are no runtime imports, reads, symlinks or dependency files pointing to the former parent project.

Process packages are an explicit external input, not an implicit dependency. Implemented: universal definitions, JSON-compatible YAML loader, cross-reference/orphan validation, version-profile selection, engine lookup API, ActionBuilder integration and a BodyProvider protocol.

The BodyProvider now has a generic data-driven implementation. It loads field
trees, validates aggregate issues, cardinality, selected datatypes,
message usage/fixed values and classifier availability, and serializes ordered
nested elements, repeatables and attributes. STRICT and TEST differ only for
missing external classifier datasets. The engine contains no P.MM.01-specific
branches or constants.

Field definitions also carry process-agnostic interpretation status/reason
metadata. Confirmed arbitrary-XML child rows serialize supplied XML elements
directly; package validation enforces their `ANY_XML` representation.

MessageRules may carry fully source-traced `INTERNAL_NORMATIVE_CONFLICT`
metadata. Generic Body validation reports `NORMATIVE_CONFLICT` and prevents
serialization only for the affected message; the engine does not interpret or
repair process-specific conflicts.

The package model now also supports first-class operations, extended source
locations, transaction operation/delivery metadata, message structure versions
and structure table/import metadata. These additions are generic and contain no
P.MM.01 constants.

Version-profile resolution is per structure. Nullable active versions remain
unchanged and valid package state. TEST mode can serialize an explicit
normative placeholder definition without inventing a version; STRICT mode
returns `UNRESOLVED_STRUCTURE_VERSION` for null selections or any remaining
placeholder in root/imported namespaces. Placeholder XML reports
`VERSION_PLACEHOLDER_TEST` and is never production-ready.

The TEST-only XML comment explains the `Y.Y.Y` structure-version placeholder
and the `X.X.X` base-model-version placeholder and directs users to paragraph 2
of EEC Board Decision No. 122 of 25 October 2016. The wx copy action treats a
successful clipboard `SetData` as success; platform-specific `Flush` is best
effort and cannot turn an already completed copy into a reported failure.

A public pre-GUI application layer is available through
`EaeuXmlApplication`. It discovers external packages below an explicit root,
lists transaction/message DTOs, projects StructureDefinition + MessageRules
into hierarchical FormDefinition DTOs, produces reproducible minimal TEST
values, returns validation issues without routine low-level exceptions, and
generates complete SOAP through the existing engine. Application-level
TransactionSession retains the existing TransactionInstance and correlation
services across request/response calls. Normative conflicts remain blockers;
unresolved versions block STRICT but allow typed TEST placeholder XML. Missing
classifier datasets remain warnings and can coexist with placeholder warnings.

The first desktop GUI is implemented under `eaeu_xml.gui`. It provides explicit
process-root selection, process/TRN/message selectors, visible generation
status, a recursive scrolled form, fixed/forbidden/attribute presentation,
repeatable scalar and complex controls, deterministic test-data fill,
validation issue presentation, XML preview/save and an in-memory transaction
session. GUI business behavior is covered through a display-independent
controller. wxPython is optional and was not present in the verification
environment, so real-window smoke launch remains pending an installation with
the `gui` extra.

The usability layout now separates «Заполнение данных» and «XML» in a notebook.
Selectors occupy full rows; the form owns the remaining height; XML preview,
metadata, copy and save occupy the complete result tab. Field labels are above
their controls and use clean human display names, while `ⓘ` help exposes the
official name, XML QName/path, datatype, cardinality, example and other safe DTO
metadata. Validation issues can focus their field, settings are isolated in a
dialog, successful generation switches to XML, and blocked generation stays on
Data. A real wx 4.3.1 macOS smoke passed for TRN.005/MSG.007 and blocked
TRN.004/MSG.005.

Typed diagnostic presentation now distinguishes successful generation,
TEST_ONLY warnings, TEST-only placeholder versions and source-confirmed normative blocks.
The application facade aggregates generic process issues across unresolved
structure selections, conflicts, absent classifier datasets and external
sources. The GUI displays text plus cross-platform color cues, message selector
markers, suggested actions and source details. Its Process Issues dialog
supports all/blocking/warning filters. Validation errors caused by user input
remain separate from normative/runtime blockers.

| Mechanism | Implemented | Normative source confirmed | Tests | Known limitations |
|---|---:|---:|---:|---|
| SOAP 1.2 Envelope / UTF-8 | yes | paragraphs 18–29 | yes | Complete Header order is deterministic but not claimed as XSD sequence |
| APPLICATION Header / addresses / identifiers / Action | yes | paragraphs 30–63 | yes | External address membership registries remain external |
| Integration / TrackID / AcceptTime | yes | paragraphs 41–44, table 5 | yes | Platform context models ownership, not a real gateway |
| RCV / PRS / ERR | yes | paragraphs 99, 112–121, appendix 5 | yes | Format-logical codes are process-specific |
| SOAP Fault / RelatesAction / reason / detail | yes | paragraphs 64–76, tables 7–8 | yes | CDATA lexical form is recommended and not preserved |
| Six transaction patterns and state machine | yes | paragraphs 98–139 | yes | No business database rollback or real clock |
| Parameters / timeout decisions / retry | yes | paragraphs 100, 104–110 | yes | Concrete payload reconstruction requires Body model |
| Duplicate-policy boundary | yes | paragraph 101 | yes | Detection requires process-specific rules |
| Rule coverage and report | yes | project audit mechanism | meta-test | 45 unique normative rules audited |
| External ProcessPackage architecture | yes | architectural layer, not normative data | yes | Manifests use JSON-compatible YAML 1.2 |

Verification results:

- baseline: 29 tests;
- normative-audit suite: 37 tests;
- self-contained final suite: 41 tests;
- process-package suite: 60 tests;
- rules: 45 total, 45 verified;
- missing tests: 0;
- remaining implementation mismatches: 0;
- reference XML: 10/10 well-formed.

Autonomy verification also passed from a temporary copy containing only `eaeu_xml/`, under an empty environment with `PYTHONPATH=src`.

See `DECISION_5_VERIFICATION_REPORT.md` for the rule table, transition summary, corrected mismatches and delegated items.

TEST XML with version placeholders includes a neutral data-driven XML comment
between the Envelope opening tag and Header. GUI preview, clipboard copy and
file save consume the same already-generated XML string.
## Local drafts

- GUI поддерживает ручные JSON-черновики, dirty-state, debounce autosave и recovery.
- При загрузке значения сопоставляются с текущей формой и валидируются заново;
  неизвестные поля не подставляются в XML и возвращаются как unmapped.
- Черновик сообщения с unresolved version допустим: TEST использует только
  нормативные placeholders, STRICT остаётся заблокирован. Другие blockers не обходятся.

P.MM.01 E2E reclassification: before = 14 VERIFIED_SOAP, 9 TEST_ONLY,
17 UNRESOLVED_STRUCTURE_VERSION, 3 NORMATIVE_CONFLICT. After = 37
VERSION_PLACEHOLDER_TEST, 3 NORMATIVE_CONFLICT and 3 INITIAL_MESSAGE_BLOCKED
responses whose initiating messages are those conflicts.
# Field input policy (2026-08-24)

Generic model/resolver, DTO, Facade summary и GUI presentation реализованы. Полный P.MM.01 audit: 2960 field usages; непроверенные источники остаются unresolved. Нормативные конфликты и version profile не изменялись.
# UI input policy (2026-08-24)

Добавлен независимый process-agnostic UI policy layer. Normative unresolved остаётся 1831. UI по 2960 usages: USER_INPUT 2184, READ_ONLY 95, EXTERNAL_SYSTEM 1, GROUP 539, HIDDEN 9, UNRESOLVED_UI_POLICY 132. Facade summary и GUI используют UI policy; tooltip сохраняет обе классификации.
# Messages guide (2026-08-24)

Реализованы structured guide API, полнотекстовый поиск, wx reader с контекстным открытием MSG/field и генерация Markdown. Coverage P.MM.01: 28/28 MSG, 2960/2960 usages. После точечного UI bugfix MSG.005: USER_INPUT 2183, HIDDEN 10; normative unresolved остаётся 1831.
# Guide quality audit (2026-08-24)

Examples улучшены с 2202 до 2393; без примера осталось 567. Все examples имеют origin. 132 UNRESOLVED_UI_POLICY проаудированы и сохранены: 41 CONDITIONAL_SOURCE_UNKNOWN, 91 NORMATIVE_CONFLICT. UI/normative policies не менялись.

# Large form filters (2026-08-24)

Добавлены presentation-only режимы ALL / REQUIRED / USER_FIELDS / ERRORS / FILLED, совместный поиск по пяти полям метаданных с debounce 225 ms, сохранение parent hierarchy, session-level mode, facade summary и error navigation с reveal/scroll/focus. Значения и repeatable items остаются в полном `BodyValues`; validation не зависит от видимости controls. Complex groups сворачиваются, обязательные и найденные/ошибочные группы раскрываются. «Сводка» получила фильтры реквизитов поверх прежнего поиска. P.MM.01 MSG.001: ALL 401, REQUIRED 168, USER_FIELDS 398; manual summary 307. Реальный macOS wx smoke: `WX_LARGE_FORM_FILTER_SMOKE_OK`.

# Conditional smart form (2026-08-25)

Добавлены generic ConditionalFieldRule/compiler/evaluator, TRUE/FALSE/UNKNOWN, effects SHOW/HIDE/REQUIRE/ENABLE/DISABLE, dependency index и 225 ms TextCtrl debounce. Search не активирует скрытое условием поле; diagnostic error navigation может временно раскрыть его. Conditional required validation использует тот же evaluator. Values и repeatable items не удаляются, drafts сохраняют полный state. P.MM.01 audit: 133 conditional usages, 0 machine-evaluable, 133 unresolved; поэтому никакой реальной динамики P.MM.01 не придумано, все поля остаются видимыми с marker `[Условно]`. wx smoke: `WX_CONDITIONAL_FORM_SMOKE_OK`.

# Guide tree selection bugfix (2026-08-25)

Исправлено сопоставление wx TreeCtrl selection с FieldGuide: `sip.voidptr` из `TreeItemId.GetID()` больше не используется как Python mapping key. Каждый item хранит immutable `GuideNodeKey(message_code, field_path)` через SetItemData/GetItemData. Leaf, attribute и group используют единый formatter карточки; context open/search сразу показывают details, смена MSG очищает selection. wx smoke: `WX_GUIDE_FIELD_SELECTION_SMOKE_OK`.
# MessageRules audit support

The generic loader, validator, Application Facade and Guide expose source-backed message-rules coverage. File/status consistency is fail-fast; `NEEDS_VERIFICATION` and `NORMATIVE_CONFLICT` block package validation.
# Assisted identifier and temporal controls

Generic wx controls support editable identifier generation through `IdentifierService`, DATE manual/Today/calendar input, and TIME/DATETIME Now input with System, UTC or searchable IANA timezone. The default timezone is stored with wx.Config. P.MM.01 EDocId is explicitly AUTO_ASSISTED_EDITABLE in package UI metadata; fixed envelope/document codes and correlation identifiers remain read-only. MSG.006 UpdateDateTime remains EXTERNAL_SYSTEM with no Now button.
# GUI user acceptance (2026-08-25)

Five real wx P.MM.01 scenarios pass: TRN.004 request/response, TRN.005 both response branches, TRN.011 notification, TRN.008 mutual obligations and the large MSG.001 form. Acceptance found and fixed two generic GUI data bugs: enum Choice values no longer collapse to `None`, and valid manual ANY_XML text is parsed into an XML Element before the unchanged validation pipeline. No normative or XML serialization changes were made.

# Binary file input and boolean UX (2026-08-25)

Generic `supports_file_picker` определяется по datatype metadata. Application
service формирует base64 Body value и presentation-only filename/size/MIME;
путь не попадает в XML или draft. Draft v1 сохраняет embedded base64. Boolean
Choice показывает Да/Нет при сохранении typed bool и XML true/false.
TransactionSession recovery не изменялся.

# Transaction session persistence audit (2026-08-25)

Аудит подтвердил возможность отдельного versioned snapshot, но текущие drafts
не содержат достаточной history/state для безопасного restore. Автоматическое
восстановление не реализовано; `SESSION_RESTART_REQUIRED` сохранён. Перед MVP
application session должна использовать полный TransactionDefinition/Engine,
а history — фиксировать direction, message subtype, faults и event status.

# Session snapshot v1 storage (2026-08-25)

Реализованы отдельные `TransactionSessionSnapshot`, strict validator и atomic
`*.eaeusession.json` storage. Runtime session имеет explicit capture/save hooks;
legacy drafts не конвертируются. Snapshot v1 покрывает application, retry,
signal/fault correlation и corruption cases. GUI Continue/restore не включены:
на завершении storage-only этапа статус был `SAFE_TO_ENABLE_GUI_CONTINUE = NO`;
он пересмотрен последующим restore этапом ниже.

# Unified lifecycle and runtime restore (2026-08-25)

Application new/restore paths объединены через lifecycle service. Restore
повторно проверяет current package, replay state/history, retry/signal/fault и
core correlation, сохраняет IDs и доказывает exact snapshot round-trip.
TRN.004 next response и TRN.008 next signal доказаны. GUI не изменён;
`SAFE_TO_ENABLE_GUI_CONTINUE = YES` только для typed RESTORABLE result.
# Responsive wx layout (2026-08-25)

MainFrame имеет разумный minimum `700x560`; filter/action bars переносят
controls через `wx.WrapSizer`. FormPanel поддерживает обе оси прокрутки и
пересчитывает virtual size после resize, длинные summary texts оборачиваются по
текущей ширине. Real macOS wx resize regression проходит. Core, Facade, drafts,
session lifecycle, XML и normative semantics не менялись.
# GUI transaction session controls (2026-08-25)

GUI now opens `*.eaeusession.json` through lifecycle restore, enables Continue
only from typed RESTORABLE/continue_ready, adopts the restored TransactionSession
without regenerating correlation, and saves active sessions through application
API. Open-as-new explicitly loads a Body draft and calls create_new because the
session snapshot contains no Body values. Real macOS wx restart/correlation and
responsive smokes pass. Legacy draft session restore remains forbidden.
# Restored-session final XML audit (2026-08-25)

Fresh restart → restored TransactionSession → response/signal/fault → parsed
final XML proves Header IDs, Action, correlation, namespaces and serializer
ownership. Production continuation remains blocked: snapshot v1 has no previous
Body values required for P.MM.01 EDocRefId correlation, and retry has no
payload-backed XML generation API. Core/schema/serializer were not changed.
# Message artifact persistence (2026-08-25)

Session bundle v1 atomically stores immutable Body artifacts beside unchanged
snapshot v1. Artifacts are history-linked, integrity-checked and restore
EDoc-style Body correlation only through package policy. Payload-backed retry
creates a fresh Decision №5 Header with original Body, never raw XML. This proves
session-continuation persistence; it does not lift unrelated P.MM.01 normative,
classifier, XSD or structure-version blockers.

# Universal process registry (2026-08-27)

Stage C adds an explicit-root `ProcessRegistry` above the existing loader and an
explicit-version `StructureResolver`. Shared structure catalogs are infrastructure
only; local/shared collisions require `source: local|shared` in the existing version
profile selection. No P.MM.01 data, XML, GUI, SOAP, session or retry behavior changed.
See `UNIVERSAL_REGISTRY_REFACTOR_REPORT.md`.
