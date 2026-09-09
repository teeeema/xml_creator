# Architecture

- `core/` — enums, domain errors, centralized namespaces.
- `decision5/models/` — immutable identifiers, addresses, Action, Header, envelope and procedure models; mutable transaction aggregate with typed history.
- `decision5/rules/` — application Header policy, correlation constants and YAML source traceability.
- `decision5/validation/` — separate validators for addresses, identifiers, Action, Header, procedure, correlation and transaction.
- `verification/` — deterministic rule coverage model linking every registry rule to its source, implementation and an existing test.
- `process_packages/` — process-agnostic definitions, explicit-path loader, cross-reference validator, engine facade and Body-provider boundary.
- `application/` — stable GUI-facing facade, discovery, DTO/view models, hierarchical form projection, deterministic test-data generation and transaction sessions.
- `gui/` — optional wxPython presentation layer plus a headless-testable controller; it depends only on the application facade and DTOs.
- `services/` — the only technological UUID generator, Action builder, correlation service, high-level MessageFactory and XML serializer.
- `IntegrationPlatformContext` is the only high-level API that enriches an application message with platform-owned Integration metadata.
- SignalFactory and FaultFactory build separate message branches; neither is modeled as APPLICATION.
- `TransactionStateMachine` owns pattern transitions and correlation-source selection; `TransactionEngine` exposes event/timeout metadata without clocks, network or persistence.
- `RetryService` creates retry records with a new MessageID in the same transaction instance.
- Envelope, Signal, Fault, Integration and Retry validation are separate pipeline stages.
- `DuplicatePolicy` is only a protocol boundary; Decision №5 delegates duplicate detection to common-process data rules.
- `BodyPayload` is a protocol. Decision №5 does not define a concrete P.MM.01 body.

Dependencies point inward: services use Decision 5 models/validators; models use only core. XML serialization and validation do not depend on transport or GUI.

The engine is filesystem-autonomous: its core source, tests, generators, examples and project memory live below the `eaeu_xml/` root. Runtime code performs no implicit parent-directory reads and does not modify `sys.path`. An external process package is read only from a `pathlib.Path` explicitly supplied by the caller.

Common-process normative data is outside the engine. `ProcessPackageLoader` reads required catalog manifests, the active profile, versioned structures and message rules, then `ProcessPackageValidator` rejects broken cross-references, invalid namespaces/source references and orphan definitions. Version profiles contain an independent `active_version` selection for every structure and never create versions. A `null` selection keeps the package valid. STRICT resolution requires concrete root and imported model namespaces; TEST resolution may select one explicit normative placeholder definition and preserves its `Y.Y.Y`/`X.X.X` tokens literally. Placeholder resolution is typed metadata and never creates a semantic version.

Operations are first-class, process-agnostic `OperationDefinition` objects in an
optional `operations.yaml` registry. Transactions reference operation codes;
the universal engine contains no P.MM.01 constants.

Process participants are optional, source-traced `ParticipantDefinition`
objects loaded from `participants.yaml`. Transactions may bind initiating and
responding participant codes. The generic address builder combines an explicit
segment, process code and participant code without deriving process metadata
from `EEC` or a member-state alpha-2 segment.

High-level MessageFactory remains the low-level application builder. Transaction-aware flows use TransactionEngine. Header serialization deterministically mirrors paragraph 29, without claiming that the full order is a schema-level normative sequence.

Interactive clients use `EaeuXmlApplication`; they do not read package YAML,
inspect StructureDefinition/MessageRules internals, invoke Decision No. 5
services directly or serialize XML. `ProcessDiscoveryService` scans only an
explicit caller-supplied root and recognizes packages by their required
manifests. `TransactionSession` owns a real Decision No. 5
`TransactionInstance`, so MessageID, ProcedureID, ConversationID and RelatesTo
remain core responsibilities. `TestDataGenerator` belongs to the application
layer and consumes public FormDefinition DTOs.

The wx GUI renders FormDefinition recursively, collects facade-compatible
values and presents validation/generation DTOs. It may save an already-built
XML string, but it never constructs or serializes XML. wxPython is an optional
dependency, so core and facade imports remain usable without a graphical stack.

FieldView exposes presentation-safe official/display names, XML QName/path,
cardinality and generic example values. Human captions omit trailing technical
QName aliases; full official text and QName remain available through tooltip
and field-help DTO projection. MainFrame uses separate Data/XML notebook pages,
while GuiController owns tab, settings and validation-navigation state without
depending on wx.

Application facade also exposes generic ProcessIssueView records derived from
nullable version selections, source-traced normative-conflict metadata,
classifier availability and delegated external-source rules. GuiController
maps message statuses and related issues into success/warning/blocked
presentations; known statuses never travel through the unexpected-exception
dialog path.

`XmlSerializer` formats the complete facade-produced XML once for preview and
file persistence. Envelope namespace declarations are one per line, with
technology prefixes (`soap`, `wsa`, `int`) separated from generic payload
declarations. The formatter classifies prefixes only; it has no process,
structure or message-specific conditions.
# Field input policy layer (2026-08-24)

`FieldInputPolicyResolver` — отдельный process-agnostic слой между StructureDefinition/MessageRules и Application FormDefinition. Ключ политики: `(message_code, field_path)`. Resolver не выводит источник значения из XML-имени. `StructureDefinition` описывает XML, `MessageRules` — использование, `FieldInputPolicy` — кто/откуда задаёт значение. GUI получает готовые `input_policy`, `value_source`, editable/visible, help и condition через Facade.
# UI input policy layer (2026-08-24)

`UiInputPolicyResolver` расположен после нормативного `FieldInputPolicyResolver`. Первый отвечает только за presentation behaviour; второй — за подтверждённый/неразрешённый источник значения. FormDefinition переносит обе оси: `normative_input_policy` и `ui_input_policy`, а также `ui_policy_origin`. Process-specific исключения загружаются из `ui_input_policies.yaml`.
# Structured user guide (2026-08-24)

Пользовательская инструкция строится через generic `GuideService` и immutable DTO `ProcessGuide`, `MessageGuide`, `FieldGuide`. Form, tooltip, wx reader и Markdown получают данные из одной цепочки Application Facade. Markdown является производным артефактом, а не источником GUI. Полные деревья Body сохраняют hierarchy, attributes и repeatability.
# Guide example provenance (2026-08-24)

`ExampleValueResolver` формирует только documentation examples и возвращает `example_origin`/`unavailable_reason`. Приоритет: fixed → allowed → existing explicit example → classifier placeholder → unambiguous datatype → safe project documentation placeholder → unavailable. XML name не используется для вывода UUID или business value.

# Large form presentation (2026-08-24)

`FieldVisibilityFilter` строит отдельный immutable `FormPresentation` из полного `FormDefinition`. Режимы ALL, REQUIRED, USER_FIELDS, ERRORS и FILLED, а также полнотекстовый поиск, удаляют только presentation nodes и сохраняют необходимые parent groups. Исходная форма и `GuiController.values` не урезаются. wx пересоздаёт только видимое дерево controls из полного state; `update_visible_values` сливает видимый ввод обратно, не удаляя скрытые фильтром значения. Validation всегда получает полный state. Complex groups представлены через `wx.CollapsiblePane`; поиск, error navigation и ERRORS mode раскрывают нужную иерархию.

# Conditional presentation engine (2026-08-25)

`ConditionalRuleCompiler` принимает только explicit structured `conditional_rule` metadata с target/source/operator/effect и source traceability. Текст MessageRules не парсится. `ConditionEvaluator` реализует TRUE/FALSE/UNKNOWN, dependency index, partial source reevaluation, conditional projection и conditional-required validation. Один evaluator используется Application validation, Form presentation и Guide metadata. Pipeline: full FormDefinition → condition projection → display filter → search. Condition state не попадает в normative models/XML. Значения скрытых fields/repeatable groups остаются в BodyValues и drafts.
# MessageRules coverage metadata

`MessageDefinition` carries an independent `message_rules_status` and dedicated source references. The package validator cross-checks that status against the physical `message_rules/<MSG>.yaml`: a confirmed separate table requires a file, while a confirmed absence forbids a synthetic/empty file. This mechanism is generic and process data remains external to the engine.
# Assisted editable input (2026-08-25)

`FieldView` carries explicit presentation capabilities (`manual_edit_allowed`, date/time helpers, timezone picker and identifier generator). Capabilities are resolved by the Application Facade from datatype plus UiInputPolicy/value source and optional process-package UI metadata; wx controls never infer behaviour from XML names. Identifier generation crosses the Application Facade and uses `IdentifierService`. Date/time helpers use `zoneinfo` and return ordinary editable values that continue through the existing validation and draft pipelines.

# Generic file input capability

`FieldView.supports_file_picker` получается из datatype metadata. wx отвечает
только за выбор/отображение; `FileInputService` читает bytes, кодирует lexical
base64 value и определяет необязательный MIME hint. Serializer получает обычное
Body value и не знает о локальном пути. Metadata не добавляется в XML.

# Session persistence boundary

Draft persistence и transaction runtime persistence являются разными слоями.
Будущий snapshot — portable versioned JSON DTO вокруг Decision №5 aggregates,
а не сериализация Python objects. Restore проходит через dedicated validator и
Facade; GUI не создаёт `TransactionInstance`. Текущий `session_metadata` с двумя
ID остаётся non-restorable и не используется как correlation history.

Snapshot v1 реализован в отдельном application module: immutable JSON DTO,
strict validator и atomic storage. Runtime `TransactionSession` предоставляет
только явные capture/save hooks. Load не создаёт runtime aggregate; будущий
restore остаётся отдельным Facade service и GUI не включён.

Runtime restore теперь проходит через `TransactionSessionLifecycleService` и
двухфазный `TransactionSessionRestoreService`. Candidate replay использует
current ProcessPackage, TransactionEngine/StateMachine и core validators;
accepted session выдаётся только после exact runtime→snapshot invariant.
Create-new и restore-existing имеют разную ID-семантику. GUI по-прежнему не
содержит restore logic.
# Responsive GUI boundary

MainFrame owns presentation-only resize coordination. Top-level control bars use
wrapping layout; FormPanel remains the generic dynamic-form boundary and owns
two-axis scrolling plus virtual-size recalculation. The responsive layer does
not mutate FormDefinition, values, validation, drafts, session state or XML.
# Interactive session boundary

GUI session files cross the application boundary as `SessionOpenResult`; only
the lifecycle/restore layer can return a usable TransactionSession. Controller
holds a small NEW/RESTORED presentation context but never duplicates runtime
state. Session snapshots remain correlation-only, while Open-as-new obtains Body
values from the independent draft API and creates a fresh lifecycle session.
# Historical message artifact boundary

Session snapshot answers SOAP/runtime history; session bundle artifacts answer
which immutable Body payload was generated for an application attempt. Bundle
restore attaches artifacts only after typed runtime restore. Body correlation
uses package policy and artifact values; SOAP identifiers remain unrelated.
