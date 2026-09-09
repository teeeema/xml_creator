# Architecture decisions

## Explicit registry and local/shared structure source

Discovery, registry indexing, package loading and structure resolution remain separate.
A shared catalog is parsed by the canonical loader and keyed by `(structure_id,
version)`. An identical local/shared key requires `source: local` or `source: shared`
in the active profile; silent shadowing is forbidden. Versions are never inferred
from process or model versions.

## D-001 — Independent src-layout package

The new core lives in `eaeu_xml/` and does not reuse the adjacent legacy application.

## D-002 — Typed technological identifiers

MessageID, ProcedureID and ConversationID are separate value objects. Only IdentifierService creates new UUID values.

## D-003 — Stateful correlation

TransactionInstance stores typed MessageRecord history. CorrelationService derives follow-up RelatesTo from the immediately preceding stage, per Decision №5 paragraph 102.

## D-004 — Body is a protocol

The technological envelope accepts BodyPayload. Concrete common-process bodies remain external.

## D-005 — Examples do not independently create normative requirements

Examples may clarify serialization when supported by normative paragraphs, but cannot establish element cardinality alone. Unclear points are recorded in UNRESOLVED_RULES.md.

## D-006 — Separate ownership and message branches

Integration is platform-owned. APPLICATION, SIGNAL and TECHNICAL_FAULT are distinct types with separate factories and policies.

## D-007 — Declarative transaction timing

Timeouts and retry limits are typed metadata/events. Stage 3 contains no clocks, transport or MQ implementation.

## D-008 — Safe ProblemMessage representation

ProblemMessage accepts a well-formed XML element and serializes the complete source XML as string content. Decision №5 recommends CDATA, but lexical CDATA preservation is not mandatory and is not claimed by the ElementTree serializer.

## D-009 — Auditable rule coverage

Decision5RuleCoverage derives the registry inventory, maps every rule to implementation and test evidence, verifies referenced test names through Python AST, and reports unresolved/mismatch/missing-test totals.

## D-010 — Transition-specific correlation

History validation permits correlation to a known earlier message and does not equate list adjacency with the message received on the previous normative transaction stage. Factories/state transitions select the concrete source.

## D-011 — Self-contained project boundary

`eaeu_xml/` is the complete project boundary. The read-only normative source is stored as `./15kr0005.doc`; code, tests and tools may not import or read the adjacent legacy project.

## D-012 — Common processes are external normative packages

The `eaeu_xml` engine contains no process-specific normative data. P.MM.01 and every other common process live in external `ProcessPackage` directories with their own sources and memory.

## D-013 — Explicit package location

ProcessPackage location is always supplied as an explicit `pathlib.Path`. The loader does not inspect the current parent directory, environment variables or conventional sibling names.

## D-014 — Dependency-free manifest subset

Package manifests use JSON syntax, which is a valid YAML 1.2 subset. This keeps the engine free of third-party runtime dependencies while retaining `.yaml` catalog files.

## D-015 — Operations are first-class package definitions

Common-process operations live in an optional `operations.yaml` registry and
are referenced by transactions. This preserves OPR traceability without
hardcoding a concrete process in the engine.

## D-016 — Active structure versions are independent

Each structure entry in a version profile owns its nullable `active_version`.
Validation permits `null` when at least one definition exists. Resolution fails
locally with `UNRESOLVED_STRUCTURE_VERSION` and does not block other structures.

## D-017 — GUI depends only on the application facade

GUI and other interactive clients use `EaeuXmlApplication` DTOs and sessions.
They do not read YAML, inspect StructureDefinition or MessageRules internals,
implement Decision No. 5 rules, build Header/Action/correlation, or serialize
XML. Process discovery is an application concern with an explicit root;
TestDataGenerator is a separate application service. This keeps the GUI dumb
and the normative/runtime decisions in the engine and external package.

## D-018 — wxPython is an optional presentation dependency

The desktop UI lives in `eaeu_xml.gui`. Its controller is display-independent
and unit tested without wx; concrete windows import wx only when GUI modules are
launched. The core installation remains dependency-free, while the `gui`
optional extra installs wxPython. GUI code can persist a facade-produced XML
string but cannot build SOAP, Action, identifiers or correlation itself.

## D-019 — Human field captions are distinct from technical XML identity

FormDefinition retains the complete official name, XML QName and path, while
its display name is a concise human caption. GUI headings use the display name;
QName, datatype, cardinality, example, classifier, fixed value and sources are
shown through tooltip/field-help. This presentation transformation is generic
and never changes normative XML names or serialization.

## D-020 — Typed diagnostics cross the facade boundary

Process/package problems reach presentation clients as generic ProcessIssueView
DTOs with severity, category, affected definitions, safe source text and a
suggested action. GUI does not infer issues from YAML and does not treat known
unresolved, conflict or TEST_ONLY statuses as internal exceptions. User-input
validation remains a separate presentation channel from system/normative
blocks.

## D-021 — Normative version placeholders are explicit TEST-only resolution

An independent structure with no `active_version` may be resolved in TEST mode
only when the package contains exactly one definition carrying explicit
normative placeholder tokens. Root and imported namespaces are serialized
unchanged; `Y.Y.Y` and `X.X.X` are not semantic versions and are never replaced
with guessed values. STRICT resolution rejects any remaining placeholder,
including one in an imported model namespace. Generation reports
`VERSION_PLACEHOLDER_TEST`, unresolved structures and the literal tokens.

## D-022 — Process participants are source-traced package data

The universal engine models a participant code independently from its logical
address segment. `LogicalAddressBuilder` receives segment, process code and
participant code; it never derives one from another. Concrete participants and
transaction endpoint assignments live in external process-package manifests.
Fixed Commission segments and test/runtime national segments are explicit
policies rather than process hardcodes in the engine or GUI.
# 2026-08-24 — conservative field input policy

- Неизвестный источник значения получает `UNRESOLVED_INPUT_POLICY`, а не предполагаемый USER_INPUT/AUTO_*.
- `required/optional/forbidden` остаётся независимым измерением от input policy.
- Добавлен обоснованный тип `STRUCTURAL_CONTAINER`: группа без отдельного пользовательского scalar control.
- Явные policies хранятся в process package; generic resolver не содержит P.MM.01-specific веток.
# 2026-08-24 — Normative value source ≠ UI input policy

Normative value source and UI input policy are separate concepts. UI may require user input where the normative model does not specify a provider. Такое поведение имеет origin `PROJECT_UI_DEFAULT` и является проектным UX-решением, а не утверждением о требованиях Решения №68.

Приоритет UI resolution: forbidden safety → explicit manual override → confirmed automatic source → classifier/enum → structural container → external system → conditional → project default USER_INPUT → unresolved. Внешний classifier без dataset использует существующий TEST fallback USER_INPUT; нормативная policy при этом остаётся CLASSIFIER.
# 2026-08-24 — guide is a presentation projection

Сводка не является новой нормативной моделью. Она объединяет существующие ProcessPackage definitions, normative/UI policies, examples и SourceReference. GUI читает structured guide API, а standalone Markdown генерируется из него. Конфликтные сообщения показывают несоответствие и не получают обходной Body example.
# 2026-08-24 — examples are instructional, not normative

Example value не объявляет допустимое нормативное значение. UUID применяется только при явно UUID datatype/policy. Business identifiers и codes получают нейтральные помеченные placeholders; classifier без dataset не получает выдуманный код. Отсутствие безопасного примера сохраняется с reason code.

# 2026-08-24 — form filtering is presentation-only

Фильтр большой формы никогда не изменяет `FormDefinition`, normative models или XML mapping. Hidden-by-filter fields остаются в `GuiController.values`; изменение видимых controls сливается в полный state. Repeatable instance markers и значения сохраняются между режимами. Validation и generation работают по полному state, а error navigation может временно раскрыть конкретный path без смены выбранного режима. Summary основной формы и «Сводки» использует Facade DTO, а не повторный подсчёт нормативных правил в GUI.

# 2026-08-25 — conditional rendering requires structured traceable rules

Dynamic SHOW/HIDE/REQUIRE/ENABLE/DISABLE разрешены только для explicit machine-readable MessageRules metadata с source traceability. Русский текст условия, QName, XML name и business intuition не компилируются. UNKNOWN сохраняет поле видимым и annotated. FALSE visibility не удаляет existing BodyValues. `ConditionEvaluator` является единственным engine для presentation, validation и guide; condition results являются session presentation state и никогда не сериализуются.
# Decision: explicit message-specific rules coverage

Use `HAS_SEPARATE_RULE_TABLE`, `NO_SEPARATE_RULE_TABLE`, `NEEDS_VERIFICATION`, or `NORMATIVE_CONFLICT` on every loaded `MessageDefinition`. Absence of a message-rules YAML is valid only when explicitly confirmed by source metadata; it is no longer treated as implicit incompleteness.
# Decision: generated does not imply locked

A program-generated value does not automatically mean manual editing is forbidden. `AUTO_ONLY` and `AUTO_ASSISTED_EDITABLE` are presentation classifications, not normative FieldInputPolicy values. Helper controls are UI actions and never change normative value-source semantics. AUTO_FIXED remains read-only; CORRELATION remains read-only unless an explicit process UI rule permits otherwise; EXTERNAL_SYSTEM never receives a misleading Now helper.

# Decision: binary draft payload is embedded

Binary Body values сохраняются в draft v1 как подготовленная base64-строка.
Это сохраняет backward compatibility и независимость от исходного пути.
Filename/MIME — presentation metadata. 20 MiB threshold — только UX warning.

# Decision: draft is not a transaction session

`DraftDocument` сохраняет пользовательские Body values и form context. Даже
наличие legacy `session_metadata` не доказывает существование продолжимой
транзакции. Persistable runtime state требует отдельной versioned
`TransactionSessionSnapshot`, полной проверяемой history и явного выбора
Continue. До появления этих данных действует `SESSION_RESTART_REQUIRED`.

Рекомендуемое хранение — отдельный atomic `*.eaeusession.json` и optional
immutable snapshot reference в draft. Open-as-new переносит Body values, но
создаёт новые ProcedureID, ConversationID и MessageID и не переносит RelatesTo.

# Decision: snapshot validity is computed, never trusted

`session_restorable` не является входом безопасности. Snapshot v1 считается
структурно пригодным только после typed identifier/Action, history graph,
attempt, direction, state, process-version и timing validation. Unknown schema
versions и любые повреждения блокируются без repair. Storage отделён от restore;
успешный round-trip сам по себе не разрешает GUI Continue.

# Decision: restore is current-package replay, not deserialization

Snapshot превращается в runtime aggregate только через current ProcessPackage
compatibility, semantic Action/message checks, state-machine replay, core
correlation validation и exact round-trip. Historical IDs не регенерируются.
Unsupported direction/timing fail closed. Candidate session не выходит за
restore service до final acceptance.
# Decision: GUI Continue consumes a typed pending restore result

Opening a session does not immediately replace the active runtime. The Facade
returns a typed pending `SessionOpenResult`; GUI enables Continue only when its
restore result is RESTORABLE and continue_ready. Continue adopts that exact
TransactionSession. Since snapshot v1 excludes Body values, Open-as-new requires
an explicit Body draft and invokes create_new; no implicit snapshot/draft link
is introduced.
