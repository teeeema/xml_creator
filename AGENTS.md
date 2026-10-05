## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).


# AGENTS.md

# EAEU XML Creator — Codex Instructions

## 1. Project purpose

This repository implements an offline EAEU XML message generator and validator.

The project contains:
- XML generation logic;
- XML parsing/extraction logic;
- EAEU process definitions;
- transaction/message definitions;
- normative mappings;
- source references;
- validation rules;
- GUI;
- automated tests.

Correctness against normative EAEU documents is more important than
convenience, speculative behavior, or reducing the number of failing tests.


## 2. Core rule

NEVER invent normative behavior.

A test passing is not proof that the implementation is normatively correct.

Before changing normative behavior, determine whether it is supported by:

1. normative source documents;
2. existing confirmed mappings/source_refs;
3. XSD/schema data;
4. classifier/reference data;
5. established project behavior.

Clearly distinguish:

- CONFIRMED — directly supported by a source;
- IMPLEMENTATION — existing project behavior;
- INFERRED — reasonable but not explicitly confirmed;
- UNKNOWN — insufficient source information.

Do not silently convert INFERRED or UNKNOWN information into normative facts.


## 3. Required workflow

For every coding task:

1. Understand the request.
2. Inspect the relevant implementation.
3. Locate related tests.
4. Locate related normative mappings/source references when applicable.
5. Identify the root cause.
6. Determine whether the problem is local or shared.
7. Make the smallest correct change.
8. Add/update regression tests when appropriate.
9. Run targeted tests.
10. Run broader relevant tests when appropriate.
11. Review the final diff.
12. Stop when the requested task is complete.

Do not edit code before understanding the existing implementation.


## 4. Investigate before changing

Before implementing a fix:

- find the relevant class/function;
- inspect its callers;
- inspect related tests;
- search for similar implementations;
- determine the affected processes/messages;
- inspect shared infrastructure before adding local workarounds.

Prefer evidence over assumptions.

When the exact file/symbol is already known, use targeted investigation
instead of exploring the entire repository.


## 5. Root-cause-first debugging

Always fix the root cause when practical.

Bad:

    MSG.003 fails
        ↓
    add MSG.003 special case

Preferred:

    MSG.003 fails
        ↓
    investigate extraction/evaluator
        ↓
    discover shared alignment bug
        ↓
    fix shared implementation
        ↓
    regression-test MSG.003 and related messages

Do not introduce message-specific or process-specific exceptions for a
problem caused by shared infrastructure.


## 6. Minimal changes

Keep changes surgical.

Do not:

- rewrite working modules unnecessarily;
- refactor unrelated code;
- rename unrelated symbols;
- reformat entire files;
- change APIs without need;
- introduce unnecessary dependencies;
- add speculative abstractions;
- modify unrelated tests.

Preserve existing architecture unless the task explicitly requires an
architectural change.


## 7. Normative data protection

Treat the following as sensitive project data:

- normative mappings;
- source_refs;
- process definitions;
- transaction definitions;
- message definitions;
- participant definitions;
- classifier mappings;
- normative identifiers;
- procedure/action mappings.

Do NOT modify them merely to make tests pass.

Any modification must have a clear reason and, when applicable, normative
evidence.

Never fabricate a source_ref.


## 8. Missing normative information

If required information is absent from the available normative sources:

DO NOT guess.

Report it explicitly.

Example:

    STATUS: BLOCKED_BY_SOURCE

    Missing:
    - XSD for ...
    - classifier for ...
    - normative definition of ...

Implementation must not silently compensate for missing normative data.


## 9. XML semantics

Preserve XML semantics exactly.

Pay special attention to:

- namespaces;
- exact QName;
- attributes;
- element ordering;
- optional elements;
- required elements;
- repeatable elements;
- nested repeatable elements;
- parent-child relationships;
- positional alignment.

Do not compare XML elements only by local name when exact QName semantics
are required.


## 10. Repeatable XML structures

Repeated XML parents must preserve positional relationships.

Example:

    Parent[0] -> Type = "G"
    Parent[1] -> Type missing

Correct representation must preserve:

    ["G", None]

and must NOT collapse this into:

    ["G"]

because doing so destroys parent alignment.

Nested repeatables must preserve their corresponding nested structure.

Never broadcast a scalar value across repeated parent contexts unless the
schema/rule explicitly requires that behavior.


## 11. XML extraction

When extraction behavior is incorrect across multiple messages, inspect
shared extraction logic first.

In particular, investigate:

- StructureDefinition;
- element extraction;
- attribute extraction;
- parent indexing;
- packing/indexing;
- QName matching;
- repeatable-parent handling;
- nested repeatables.

Do not implement per-message extraction logic when the underlying issue is
generic.


## 12. Rules engine

Rules must evaluate values in the correct XML context.

Do not:

- leak values between repeated parents;
- broadcast unrelated values;
- silently coerce missing values into valid values;
- ignore namespace differences;
- turn structural extraction errors into evaluator special cases.

If a rule failure originates in extraction, fix extraction rather than
patching the evaluator.


## 13. Missing values

Missing XML data must remain distinguishable from actual values.

Do not replace missing data with fabricated defaults such as:

    ""
    0
    false
    "UNKNOWN"

unless explicitly required by the schema or normative rule.

Use the project's established missing-value representation.


## 14. QName and namespaces

Namespace correctness is mandatory.

Treat:

    {namespace-A}Element

and

    {namespace-B}Element

as different elements when exact QName matching is required.

Do not introduce local-name-only fallback matching unless explicitly
required.


## 15. EAEU integration header

When working with the Decision No. 5 integration header, preserve the
established structure and semantics of fields such as:

- wsa:To
- wsa:ReplyTo
- wsa:From
- wsa:FaultTo
- wsa:Action
- wsa:MessageID
- wsa:RelatesTo
- int:ProcedureID
- int:ConversationID
- int:Integration
- TrackID
- AcceptTime

Do not invent endpoint addresses, procedure IDs, action values, or
integration identifiers.

When constructing Action, follow confirmed project/normative mappings
rather than deriving values speculatively.


## 16. Process isolation

Changes for one EAEU process must not silently affect another process.

After modifying shared infrastructure, consider regression impact on
multiple processes.

Examples may include:

- P.MM.01
- P.MM.06
- P.DS.01
- P.SP.02

Do not assume behavior confirmed for one process automatically applies to
another.


## 17. GUI isolation

GUI code must not contain normative business logic.

Keep separation between:

    GUI
      ↓
    application layer
      ↓
    XML/domain/process logic

When working on GUI migration or PySide6/QML work, do not modify backend,
XML engine, application/process packages, or normative data unless the task
explicitly requires it.

Prefer adapting the GUI to existing backend interfaces.


## 18. Dependencies

Do not add a dependency if the existing stack can reasonably solve the
problem.

Before adding one:

1. explain why it is necessary;
2. verify it does not duplicate existing functionality;
3. keep dependency scope minimal.

Never silently replace core project dependencies.


## 19. Tests

Tests are evidence, not the specification.

When a test fails:

    Test failure
        ↓
    investigate
        ↓
    determine whether implementation OR test is wrong

Do not automatically modify production code to satisfy an incorrect test.

Do not weaken assertions merely to make the suite green.


## 20. Regression tests

For bug fixes, add regression coverage when practical.

A regression test should:

- reproduce the original bug;
- fail before the fix;
- pass after the fix;
- test the actual root cause.

For shared XML infrastructure changes, test more than one relevant shape
when appropriate.

Important cases include:

- single instance;
- repeated parent;
- missing child in first parent;
- missing child in later parent;
- repeated attributes;
- nested repeatables;
- namespace/QName differences.


## 21. Test execution

Run the smallest relevant test set first.

Example:

    targeted test
        ↓
    related module tests
        ↓
    broader regression suite

Do not repeatedly run the entire suite when a targeted test provides the
needed feedback.

Before finishing a shared/core change, run broader relevant tests when
feasible.


## 22. Test reporting

Never claim:

    "all tests pass"

unless they were actually executed.

Report exact results when available.

Example:

    Targeted:
    12 passed

    Related suite:
    273 passed

    Full suite:
    905 passed, 0 failed

If a suite was not run, say:

    NOT RUN

and explain why.


## 23. Existing user changes

Assume existing uncommitted changes may be intentional.

Before modifying files:

- inspect relevant diff/status when appropriate;
- do not overwrite unrelated work;
- do not reset files simply because they differ from HEAD.

Never use destructive Git operations unless explicitly required.


## 24. Git safety

Do not automatically:

- git reset --hard;
- git clean -fd;
- force push;
- rewrite history;
- discard user changes.

Do not create commits unless requested.

When asked to create a commit, keep it scoped to the requested work.


## 25. Context efficiency

Use context carefully.

Prefer:

- targeted symbol search;
- targeted file reads;
- targeted test execution;
- relevant log sections.

Avoid:

- repeatedly reading unchanged files;
- dumping huge generated XML files;
- loading entire logs when only an error section matters;
- reading the whole repository without reason.

Large context does not replace targeted investigation.


## 26. Subagents

Use subagents only when they provide real value.

Good uses:

- independent investigation of separate components;
- parallel test/root-cause investigation;
- clearly separable research tasks.

Do not spawn subagents for simple file reads, searches, or trivial edits.

Verify important subagent conclusions before relying on them.


## 27. Generated XML verification

When changing XML generation:

verify when applicable:

1. root element;
2. namespace declarations;
3. QName;
4. header;
5. body structure;
6. required fields;
7. optional fields;
8. ordering;
9. repeatability;
10. attributes;
11. normative identifiers;
12. validation result.

Do not consider XML correct solely because it is well-formed.


## 28. Security

Never expose or commit:

- passwords;
- API keys;
- access tokens;
- session tokens;
- private credentials.

Do not print secrets in reports or logs.

If credentials are discovered, do not reproduce them unnecessarily.


## 29. Completion criteria

A task is complete when:

- the root cause is understood;
- requested behavior is implemented;
- unrelated behavior was preserved;
- relevant tests were executed;
- the diff was reviewed;
- remaining uncertainty is reported.

Do not continue refactoring after these conditions are satisfied unless
requested.


## 30. Required final response

For substantial coding tasks, finish with:

### ROOT_CAUSE

Explain the actual cause.

### CHANGED_FILES

List changed files and why.

### IMPLEMENTATION

Explain the implemented solution.

### NORMATIVE_BASIS

State one of:

- CONFIRMED — with source/reference;
- NOT_APPLICABLE;
- UNKNOWN / BLOCKED_BY_SOURCE.

Never fabricate a normative source.

### VERIFICATION

List commands/tests actually executed and their results.

### REMAINING_ISSUES

List unresolved issues.

If none:

    None


## 31. Primary principle

Correctness > passing tests.

Normative evidence > assumptions.

Root-cause fix > workaround.

Small verified change > large speculative refactor.

Existing project architecture > unnecessary new abstraction.

When uncertain, investigate and report uncertainty instead of guessing.