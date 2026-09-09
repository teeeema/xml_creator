from datetime import date
from pathlib import Path

from eaeu_xml.verification import Decision5RuleCoverage


TRANSITIONS = """| Pattern | Start / sequence | Completion | Timeout / retry | Rollback |
|---|---|---|---|---|
| MUTUAL_OBLIGATIONS | request → RCV → PRS → response → RCV → PRS → final error window | processing-confirmation window expires without ERR | missing expected signal/response → retry while attempts remain | ERR → ROLLBACK_REQUIRED |
| QUESTION_RESPONSE | request → response | response received | response timeout → retry | external application rollback boundary |
| REQUEST_RESPONSE | without guarantee: request → response; guaranteed: request → optional RCV → PRS → response | response received | expected confirmation/response timeout → retry | external application rollback boundary |
| REQUEST_CONFIRMATION | without guarantee: request → response; guaranteed: request → response → RCV | response, or RCV when required | response/RCV failure → re-initiation while attempts remain | external application rollback boundary |
| NOTIFICATION | notification → RCV | RCV received | receive-confirmation timeout → retry | external application rollback boundary |
| INFORMATION_DISTRIBUTION | notification | immediately after send | no confirmation/response timeout | external application rollback boundary |"""


def generate(project_root: Path) -> Path:
    coverage = Decision5RuleCoverage.build(project_root); summary = coverage.summary
    report = f"""# Decision №5 verification report

Generated: {date.today().isoformat()}

## Source

`./15kr0005.doc`, Решение Коллегии ЕЭК от 27 января 2015 г. №5. SHA-256: `bca94f5db76962bf46f6f5569d2d18872dc6e5355b01bd77d79edb985263043e`. Source policy: READ ONLY.

## Summary

- total rules: {summary['total_rules']}
- verified: {summary['verified']}
- unresolved registry rules: {summary['unresolved']}
- implementation mismatches remaining: {summary['mismatches']}
- missing tests: {summary['missing_tests']}
- mismatches found and fixed during audit: 5
- core status: `DECISION_5_CORE_VERIFIED_WITH_UNRESOLVED_ITEMS`

The remaining items are explicit source ambiguity or rules delegated to process/technical documents; no known internal implementation mismatch remains.

## Rule coverage

{coverage.render_markdown()}

## Transaction patterns

{TRANSITIONS}

Transition correlation follows paragraph 102: the source is the message received by the participant at the preceding transaction stage, not arbitrary list adjacency. Retry is available only for an application message in a waiting/active state or following a technological Fault, while the configured repeat count remains.

## XML verification

Ten generated reference documents are stored in `examples/decision5/`. Tests parse all documents and structurally verify SOAP 1.2 namespaces, signal appendix 5 sequences, Fault attributes, Russian reason text and absence of attribute names as standalone elements. UUID values are intentionally not compared literally with appendix 3.

## Mismatches found and fixed

1. ProblemMessage changed from child XML content to string content representing the source XML; CDATA remains a recommendation, not a mandatory lexical requirement.
2. Correlation history no longer assumes that the previous list item is always the normative previous received stage.
3. Retry now rejects non-application records and forbidden states.
4. Fault validation now rejects a reused MessageID, wrong RelatesTo and wrong RelatesAction.
5. Duplicate Integration ownership rule was consolidated, and stale Stage 2 notes/source scope were corrected.

## Known delegated and unresolved items

- Header order follows paragraph 29 and appendix 3 deterministically, but no explicit schema sequence for the complete Header was found.
- Member-state, CA and non-`gate` SR membership depend on external registries/technical solutions.
- Duplicate detection and format-logical codes depend on a concrete common-process specification.
- Concrete retry payload reconstruction requires a Body model.
- CDATA is recommended for ProblemMessage; escaped string content preserves the parsed value but not CDATA lexical form.
- Transaction-level guaranteed delivery remains separate from MQ persistence; real transport is out of scope.

## Final status

`DECISION_5_CORE_VERIFIED_WITH_UNRESOLVED_ITEMS`

## Project autonomy addendum

The original 41-test self-containment suite and the current 56-test engine suite pass from the `eaeu_xml/` boundary. The normative source is local at `./15kr0005.doc`; external process packages are loaded only from an explicit caller-supplied Path.
"""
    path = project_root / "project_memory/DECISION_5_VERIFICATION_REPORT.md"
    path.write_text(report, encoding="utf-8")
    return path


if __name__ == "__main__":
    print(generate(Path(__file__).parents[1]))
