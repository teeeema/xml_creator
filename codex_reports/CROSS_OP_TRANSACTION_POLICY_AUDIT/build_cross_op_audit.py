from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = Path("/Users/tema/Documents/Work/Документы_xml")
EAEU_SRC = ROOT / "eaeu_xml" / "src"
if str(EAEU_SRC) not in sys.path:
    sys.path.insert(0, str(EAEU_SRC))

from eaeu_xml.application import EaeuXmlApplication  # noqa: E402


MATRIX_COLUMNS = [
    "OP",
    "PRC",
    "TRN",
    "MSG",
    "structure",
    "field_path",
    "normative_policy",
    "normative_fixed_value",
    "classifier",
    "classifier_status",
    "current_gui_policy",
    "current_default",
    "current_validator_policy",
    "status",
    "priority",
    "policy_origin",
    "source_refs",
    "notes",
]

CLASSIFIER_COLUMNS = [
    "OP",
    "MSG",
    "CLASSIFIER_ID",
    "DOCUMENT_KIND",
    "EXPECTED_CODE",
    "CODE_CONFIRMED",
    "NAME_BRANCH_ALLOWED",
    "SOURCE",
    "VERSION_DATE",
    "STATUS",
    "NOTES",
]

SOURCE_BLOCKER_COLUMNS = [
    "OP",
    "PRC",
    "TRN",
    "MSG",
    "canonical_requirement_id",
    "category",
    "source",
    "source_page",
    "structure",
    "status",
    "notes",
]

MESSAGE_REVIEW_COLUMNS = [
    "OP",
    "PRC",
    "TRN",
    "MSG",
    "structure",
    "review_status",
    "matrix_rows",
    "unique_field_defects",
    "source_blockers",
    "other_blockers",
    "unresolved_structured_rules",
    "notes",
]


DECISION_92_DOCUMENT_KINDS = {
    "07325": "заявка на регистрацию и предоставление права использования наименования места происхождения товара Евразийского экономического союза",
    "07330": "заявка на предоставление права использования зарегистрированного наименования места происхождения товара Евразийского экономического союза",
    "07335": "ходатайство о внесении изменений в заявку на регистрацию и (или) предоставление права использования наименования места происхождения товара Евразийского экономического союза",
    "07340": "ходатайство о выдаче свидетельства о праве использования наименования места происхождения товара Евразийского экономического союза в отношении наименования места происхождения товара, зарегистрированного до вступления в силу Договора о товарных знаках, знаках обслуживания и наименованиях мест происхождения товаров Евразийского экономического союза от 3 февраля 2020 года",
    "07345": "заявление о внесении изменений в сведения Единого реестра наименований мест происхождения товаров Евразийского экономического союза",
    "07350": "заявление о продлении срока действия свидетельства о праве использования наименования места происхождения товара Евразийского экономического союза",
    "07355": "ходатайство о предоставлении 6-месячного срока для подачи заявления о продлении срока действия свидетельства о праве использования наименования места происхождения товара Евразийского экономического союза",
    "09055": "решение о регистрации наименования места происхождения товара Евразийского экономического союза и (или) предоставлении права использования наименования места происхождения товара Евразийского экономического союза",
    "09065": "решение об отказе в регистрации наименования места происхождения товара Евразийского экономического союза и (или) в предоставлении права использования наименования места происхождения товара Евразийского экономического союза",
}


@dataclass
class PolicyEvidence:
    policy: str
    fixed_value: Any = None
    origin: str = "STRUCTURE"
    source_refs: tuple[str, ...] = ()
    notes: str = ""
    conditional: bool = False


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def normalize_text(value: str) -> str:
    value = value.casefold().replace("ё", "е")
    return re.sub(r"[^0-9a-zа-я]+", " ", value).strip()


def decision92_codes_for_requirement(text: str) -> list[str]:
    normalized = normalize_text(text)
    matches = [
        code
        for code, name in DECISION_92_DOCUMENT_KINDS.items()
        if normalize_text(name) in normalized
    ]
    return sorted(matches)


def refs_to_text(refs: Iterable[dict[str, Any]] | None) -> tuple[str, ...]:
    result: list[str] = []
    for ref in refs or ():
        if not isinstance(ref, dict):
            continue
        parts = [str(ref.get("source_id") or "").strip()]
        document = str(ref.get("document") or "").strip()
        page = ref.get("page")
        table = ref.get("table")
        item = ref.get("item")
        if document:
            parts.append(document)
        if page is not None:
            parts.append(f"p.{page}")
        if table:
            parts.append(f"table {table}")
        if item:
            parts.append(f"item {item}")
        text = " | ".join(part for part in parts if part)
        if text:
            result.append(text)
    return tuple(result)


def flatten_fields(fields) -> list[Any]:
    result: list[Any] = []
    stack = list(reversed(tuple(fields)))
    while stack:
        field = stack.pop()
        result.append(field)
        stack.extend(reversed(tuple(field.children)))
    return result


def baseline_policy(field: Any, by_path: dict[str, Any]) -> PolicyEvidence:
    required = (field.min_occurs or 0) > 0
    if not required:
        return PolicyEvidence("OPTIONAL", origin="STRUCTURE")
    parent_path = field.path.rsplit("/", 1)[0] if "/" in field.path else None
    while parent_path:
        parent = by_path.get(parent_path)
        if parent is not None and (parent.min_occurs or 0) == 0:
            return PolicyEvidence(
                "CONDITIONAL",
                origin="STRUCTURE",
                notes="Structurally required only when optional ancestor is present.",
                conditional=True,
            )
        parent_path = parent_path.rsplit("/", 1)[0] if "/" in parent_path else None
    return PolicyEvidence("REQUIRED", origin="STRUCTURE")


def source_ref_text(rule: dict[str, Any]) -> tuple[str, ...]:
    return refs_to_text(rule.get("source_refs"))


def selector_candidates(selector: dict[str, Any], paths: list[str]) -> list[str]:
    if not selector:
        return []
    collection = selector.get("collection") or selector.get("path")
    if isinstance(collection, str):
        exact = [p for p in paths if p == collection]
        if exact:
            return exact
        suffix = [p for p in paths if p.endswith("/" + collection) or p == collection]
        if suffix:
            return suffix
    qname = selector.get("qname")
    if isinstance(qname, str):
        candidates = [p for p in paths if p.split("/")[-1] == qname]
        under = selector.get("under")
        if not isinstance(under, str) or not under:
            return candidates
        return [
            p for p in candidates
            if p == under or p.startswith(under + "/") or p.endswith("/" + under + "/" + qname)
        ]
    return []


def target_candidates(base: str, target: dict[str, Any] | str, paths: list[str]) -> list[str]:
    field = target if isinstance(target, str) else target.get("field") or target.get("path")
    if not isinstance(field, str) or not field:
        return []
    if base:
        if (field == base or field.startswith(base + "/")) and field in paths:
            return [field]
        candidate = f"{base}/{field}"
        if candidate in paths:
            return [candidate]
        return [
            p for p in paths
            if p.startswith(base + "/") and (p == candidate or p.endswith("/" + field))
        ]
    if field in paths:
        return [field]
    suffix = "/" + field
    return [p for p in paths if p == field or p.endswith(suffix)]


def merge_policy(current: PolicyEvidence, new: PolicyEvidence) -> PolicyEvidence:
    rank = {
        "STRUCTURE": 0,
        "FIELD_USAGE": 1,
        "FIXED_VALUES": 2,
        "STRUCTURED_RULE": 3,
        "MESSAGE_FIELD_POLICY": 4,
    }
    if rank.get(new.origin, 0) < rank.get(current.origin, 0):
        return current
    return new


CONTEXTUAL_SELECTOR_KEYS = frozenset({"where", "when", "parent", "position", "relative_to_context"})
CONTEXTUAL_RULE_KINDS = frozenset({"condition", "conditional_presence", "conditional_fixed_value"})


def is_contextual_mapping(value: dict[str, Any] | None) -> bool:
    if not isinstance(value, dict):
        return False
    return any(key in value for key in CONTEXTUAL_SELECTOR_KEYS)


def derive_structured_overlays(
    rules: list[dict[str, Any]], paths: list[str], structure_id: str
) -> tuple[dict[str, PolicyEvidence], list[dict[str, Any]]]:
    overlays: dict[str, PolicyEvidence] = {}
    unresolved: list[dict[str, Any]] = []

    def apply(path: str, policy: str, *, value: Any = None, rule: dict[str, Any], conditional: bool = False, note: str = ""):
        evidence = PolicyEvidence(
            "CONDITIONAL" if conditional and policy not in {"FORBIDDEN", "FIXED"} else policy,
            fixed_value=value,
            origin="STRUCTURED_RULE",
            source_refs=source_ref_text(rule),
            notes=note or ("Context-dependent structured rule." if conditional else "Source-confirmed structured rule."),
            conditional=conditional,
        )
        overlays[path] = merge_policy(overlays.get(path, PolicyEvidence("OPTIONAL")), evidence)

    def handle_rule(rule: dict[str, Any], inherited_conditional: bool = False):
        kind = rule.get("kind")
        selector = rule.get("selector") if isinstance(rule.get("selector"), dict) else {}
        conditional = (
            inherited_conditional
            or kind in CONTEXTUAL_RULE_KINDS
            or any(key in rule for key in ("when", "condition", "scope"))
            or is_contextual_mapping(selector)
        )

        # The effective form policy deliberately projects only context-free
        # structured rules. Anything that depends on a repeatable instance,
        # parent predicate, position, scope, or runtime condition remains a
        # validator/runtime rule and must not be reported as a static GUI defect.
        if conditional:
            unresolved.append(rule)
            return

        if kind == "selection_cardinality":
            candidates = selector_candidates(selector, paths)
            policy = None
            if rule.get("max_occurs") == 0:
                policy = "FORBIDDEN"
            elif (rule.get("min_occurs") or 0) > 0:
                policy = "REQUIRED"
            if policy and candidates:
                for path in candidates:
                    apply(path, policy, rule=rule, conditional=conditional)
            elif policy:
                unresolved.append(rule)
            return

        if kind == "presence":
            raw_target = rule.get("target")
            target = raw_target if isinstance(raw_target, (str, dict)) else {}
            if is_contextual_mapping(target):
                unresolved.append(rule)
                return
            candidates = target_candidates("", target, paths)
            state = str(rule.get("state") or "").upper()
            if state in {"REQUIRED", "FORBIDDEN", "OPTIONAL"} and candidates:
                for path in candidates:
                    apply(path, state, rule=rule, conditional=conditional)
            elif state:
                unresolved.append(rule)
            return

        if kind == "fixed_value":
            raw_target = rule.get("target")
            target = raw_target if isinstance(raw_target, (str, dict)) else {}
            if is_contextual_mapping(target):
                unresolved.append(rule)
                return
            candidates = target_candidates("", target, paths)
            if candidates:
                for path in candidates:
                    apply(path, "FIXED", value=rule.get("value"), rule=rule, conditional=conditional)
            else:
                unresolved.append(rule)
            return

        if kind == "for_each":
            bases = selector_candidates(selector, paths)
            if not bases and isinstance(selector.get("collection"), str):
                raw = selector["collection"]
                bases = [raw]
            assertions = rule.get("assertions") if isinstance(rule.get("assertions"), list) else []
            for assertion in assertions:
                if not isinstance(assertion, dict):
                    continue
                akind = assertion.get("kind")
                raw_target = assertion.get("target")
                target = raw_target if isinstance(raw_target, (str, dict)) else {}
                assertion_contextual = (
                    akind in CONTEXTUAL_RULE_KINDS
                    or any(key in assertion for key in ("when", "condition", "scope"))
                    or is_contextual_mapping(target)
                )
                if assertion_contextual:
                    unresolved.append({
                        "parent_rule": rule.get("rule_id"),
                        "assertion": assertion,
                        "source_refs": rule.get("source_refs", []),
                    })
                    continue
                matched = False
                for base in bases:
                    candidates = target_candidates(base, target, paths)
                    if not candidates:
                        continue
                    matched = True
                    if akind == "presence":
                        state = str(assertion.get("state") or "").upper()
                        if state in {"REQUIRED", "FORBIDDEN", "OPTIONAL"}:
                            for path in candidates:
                                apply(path, state, rule=rule, conditional=conditional)
                    elif akind == "fixed_value":
                        for path in candidates:
                            apply(path, "FIXED", value=assertion.get("value"), rule=rule, conditional=conditional)
                    elif akind in {"conditional_presence", "conditional_fixed_value"}:
                        state = str(assertion.get("state") or "CONDITIONAL").upper()
                        for path in candidates:
                            apply(path, state if state in {"REQUIRED", "FORBIDDEN"} else "CONDITIONAL",
                                  value=assertion.get("value"), rule=rule, conditional=True)
                if akind in {"presence", "fixed_value", "conditional_presence", "conditional_fixed_value"} and not matched:
                    unresolved.append({"parent_rule": rule.get("rule_id"), "assertion": assertion, "source_refs": rule.get("source_refs", [])})
            return

    for rule in rules:
        if not isinstance(rule, dict):
            continue
        applies_to_structure = rule.get("applies_to_structure")
        if applies_to_structure and applies_to_structure != structure_id:
            continue
        handle_rule(rule)
    return overlays, unresolved


def validator_policy(rules: dict[str, Any], path: str, normative: PolicyEvidence) -> str:
    field_usage = rules.get("field_usage") if isinstance(rules.get("field_usage"), dict) else {}
    fixed = rules.get("fixed_values") if isinstance(rules.get("fixed_values"), dict) else {}
    if path in fixed:
        return f"FIXED={fixed[path]!r}"
    if path in field_usage:
        return str(field_usage[path])
    if normative.origin == "MESSAGE_FIELD_POLICY":
        return f"MESSAGE_POLICY:{normative.policy}"
    if normative.origin == "STRUCTURED_RULE":
        return f"STRUCTURED:{normative.policy}"
    return "STRUCTURE"


def gui_policy(field: Any) -> str:
    if field.visibility == "HIDDEN":
        return "FORBIDDEN/HIDDEN"
    if field.fixed_value is not None and not field.editable:
        return "FIXED/READ_ONLY"
    if field.required:
        return "REQUIRED" + ("/READ_ONLY" if not field.editable else "")
    if field.ui_input_policy == "CONDITIONAL":
        return "CONDITIONAL"
    return "OPTIONAL" + ("/READ_ONLY" if not field.editable else "")


def compare_status(normative: PolicyEvidence, field: Any, validator: str) -> tuple[str, str]:
    gui = gui_policy(field)
    if normative.conditional and normative.origin in {"STRUCTURED_RULE", "MESSAGE_FIELD_POLICY"}:
        if field.ui_input_policy != "CONDITIONAL":
            return "GUI_VALIDATOR_DIVERGENCE", "P1"
        return "PASS", ""
    if normative.policy == "FIXED":
        expected = normative.fixed_value
        if field.fixed_value != expected:
            return "DEFAULT_VALUE_DEFECT", "P0"
        if field.editable:
            return "GUI_DEFECT", "P0"
        if not validator.startswith(("FIXED", "STRUCTURED:FIXED", "MESSAGE_POLICY:FIXED")):
            return "VALIDATOR_DEFECT", "P0"
        return "PASS", ""
    if normative.policy == "REQUIRED":
        if not field.required:
            if validator.startswith("STRUCTURED:REQUIRED"):
                return "GUI_VALIDATOR_DIVERGENCE", "P0"
            return "GUI_DEFECT", "P0"
        if validator in {"FORBIDDEN", "NOT_USED"}:
            return "VALIDATOR_DEFECT", "P0"
        return "PASS", ""
    if normative.policy == "FORBIDDEN":
        if field.visibility != "HIDDEN" or field.editable:
            if validator.startswith(("STRUCTURED:FORBIDDEN", "MESSAGE_POLICY:FORBIDDEN")):
                return "GUI_VALIDATOR_DIVERGENCE", "P1"
            return "GUI_DEFECT", "P1"
        if validator not in {"FORBIDDEN", "NOT_USED"} and not validator.startswith(
            ("STRUCTURED:FORBIDDEN", "MESSAGE_POLICY:FORBIDDEN")
        ):
            return "VALIDATOR_DEFECT", "P1"
        return "PASS", ""
    if normative.policy == "CONDITIONAL":
        if field.ui_input_policy != "CONDITIONAL" and normative.origin in {"STRUCTURED_RULE", "MESSAGE_FIELD_POLICY"}:
            return "GUI_VALIDATOR_DIVERGENCE", "P1"
        return "PASS", ""
    return "PASS", ""


def find_classifier_tokens(rule: dict[str, Any]) -> list[str]:
    text = " ".join(
        str(rule.get(key) or "")
        for key in ("source_text", "description", "notes", "rule_id")
    )
    result = set(re.findall(r"P\.CLS\.\d{3}", text))
    for ref in rule.get("classifier_refs") or ():
        if isinstance(ref, str):
            result.add(ref)
        elif isinstance(ref, dict):
            for key in ("classifier_id", "code", "id"):
                if ref.get(key):
                    result.add(str(ref[key]))
    return sorted(result)


def extract_document_kind(text: str) -> str:
    quoted = re.findall(r"«([^»]{8,800})»", text)
    if quoted:
        return max(quoted, key=len).strip()
    return ""


def load_pcls027() -> tuple[dict[str, list[str]], str]:
    files = sorted((ROOT / "P.SP.02_OP_22" / "normative_classifier_data").glob("*"))
    index: dict[str, list[str]] = defaultdict(list)
    source = ""
    for path in files:
        if not path.is_file():
            continue
        source = str(path.relative_to(ROOT))
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        stack = [data]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                name = None
                code = None
                for key in ("name", "title", "document_kind", "label", "value_name"):
                    if isinstance(value.get(key), str):
                        name = value[key].strip()
                        break
                for key in ("code", "value", "id", "value_code"):
                    if value.get(key) is not None and not isinstance(value.get(key), (dict, list)):
                        code = str(value[key]).strip()
                        break
                if name and code:
                    index[name].append(code)
                stack.extend(value.values())
            elif isinstance(value, list):
                stack.extend(value)
    return index, source


def source_corpus_manifest() -> list[dict[str, Any]]:
    rows = []
    for path in sorted(SOURCE_DIR.rglob("*")):
        if path.is_file():
            rows.append({"path": str(path), "suffix": path.suffix.lower(), "size": path.stat().st_size})
    return rows


def join_unique(values: Iterable[Any]) -> str:
    return "; ".join(sorted({str(value).strip() for value in values if str(value).strip()}))


def aggregate_semantic_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse TRN reuse while preserving one row per effective field-policy semantic."""
    grouped: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in rows:
        key = tuple(
            str(row.get(column, ""))
            for column in (
                "OP",
                "MSG",
                "structure",
                "field_path",
                "normative_policy",
                "normative_fixed_value",
                "classifier",
                "classifier_status",
                "current_gui_policy",
                "current_default",
                "current_validator_policy",
                "status",
                "priority",
                "policy_origin",
                "source_refs",
                "notes",
            )
        )
        existing = grouped.get(key)
        if existing is None:
            grouped[key] = dict(row)
            continue
        existing["PRC"] = join_unique((existing.get("PRC", ""), row.get("PRC", "")))
        existing["TRN"] = join_unique((existing.get("TRN", ""), row.get("TRN", "")))
    return list(grouped.values())


def is_source_blocking_status(status: str) -> bool:
    return status in {
        "SOURCE_BLOCKED",
        "SOURCE_AND_ENGINE_BLOCKED",
        "SOURCE_REPORT_ONLY_BLOCKED",
    }


def build_requirement_blockers(
    branches_by_message: dict[tuple[str, str], list[dict[str, str]]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    classifier_rows: list[dict[str, Any]] = []

    def context(op: str, msg: str) -> tuple[str, str, str]:
        branches = branches_by_message.get((op, msg), [])
        return (
            join_unique(branch.get("PRC", "") for branch in branches),
            join_unique(branch.get("TRN", "") for branch in branches),
            join_unique(branch.get("structure", "") for branch in branches),
        )

    op22_path = ROOT / "codex_reports" / "OP22_P_SP_02" / "REVERIFY_2026" / "OP22_BLOCKERS_REVERIFIED.csv"
    for source_row in load_csv(op22_path):
        if source_row.get("current_requirement_result") != "BLOCKED_BY_NORMATIVE_SOURCE":
            continue
        msg = source_row.get("msg", "")
        prc, trn, structure = context("OP22", msg)
        rows.append({
            "OP": "OP22",
            "PRC": prc,
            "TRN": trn,
            "MSG": msg,
            "canonical_requirement_id": source_row.get("canonical_id", ""),
            "category": source_row.get("new_blocker_category") or source_row.get("old_reason", ""),
            "source": str(op22_path.relative_to(ROOT)),
            "source_page": "",
            "structure": structure,
            "status": "SOURCE_BLOCKED",
            "notes": join_unique((source_row.get("evidence", ""), source_row.get("notes", ""))),
        })

    op23_path = ROOT / "codex_reports" / "OP23_P_SP_03" / "PROOF_CLOSURE" / "OP23_PROOF_CLOSURE_MATRIX.csv"
    for source_row in load_csv(op23_path):
        strict = source_row.get("strict_status", "")
        if strict in {"FULL_PROOF", "LINK_ONLY_RESOLVED", "NEW_TEST_ADDED"}:
            continue
        blocker = source_row.get("blocker_code", "")
        req_text = source_row.get("REQ", "")
        decision92_codes = decision92_codes_for_requirement(req_text) if blocker == "CLASSIFIER" else []
        if strict == "BLOCKED_SOURCE" and blocker == "CLASSIFIER" and decision92_codes:
            status = "SOURCE_RESOLVED_RUNTIME_UNIMPLEMENTED"
            category = "CLASSIFIER_DECISION_92_RESOLVED"
            resolution_note = f"Current Decision №92 exact-name matches: {', '.join(decision92_codes)}. Source blocker is resolved; runtime proof/enforcement remains open."
            document_kind = " | ".join(
                f"{code} — {DECISION_92_DOCUMENT_KINDS[code]}" for code in decision92_codes
            )
            classifier_rows.append({
                "OP": "OP23",
                "MSG": source_row.get("MSG", ""),
                "CLASSIFIER_ID": "UNSPECIFIED_CLASSIFIER",
                "DOCUMENT_KIND": document_kind,
                "EXPECTED_CODE": "|".join(decision92_codes),
                "CODE_CONFIRMED": "YES",
                "NAME_BRANCH_ALLOWED": "NO",
                "SOURCE": "/Users/tema/Documents/Work/Документы_xml/92 решение.pdf pp.13-14,17",
                "VERSION_DATE": "Decision №92 от 27.07.2021; current local amended text",
                "STATUS": "RESOLVED_FIXED_CODE" if len(decision92_codes) == 1 else "RESOLVED_CODE_OR_NAME",
                "NOTES": "Exact current Decision №92 name-to-code evidence resolves the historical source blocker; runtime enforcement is not thereby proven.",
            })
        else:
            status = {
                "BLOCKED_SOURCE": "SOURCE_BLOCKED",
                "BLOCKED_ENGINE": "ENGINE_BLOCKED",
                "BLOCKED_MULTIPLE": "SOURCE_AND_ENGINE_BLOCKED",
                "PARTIAL": "PARTIAL_PROOF",
            }.get(strict, "REVIEWED_BLOCKER")
            category = blocker or strict
            resolution_note = ""
        rows.append({
            "OP": "OP23",
            "PRC": source_row.get("PRC", ""),
            "TRN": source_row.get("TRN", ""),
            "MSG": source_row.get("MSG", ""),
            "canonical_requirement_id": source_row.get("canonical_id", ""),
            "category": category,
            "source": join_unique((str(op23_path.relative_to(ROOT)), source_row.get("source_refs", ""))),
            "source_page": source_row.get("source_page", ""),
            "structure": source_row.get("structure", ""),
            "status": status,
            "notes": join_unique((resolution_note, source_row.get("note", ""))),
        })

    op26_path = ROOT / "codex_reports" / "OP26_P_MM_01" / "BLOCKER_RECOVERY_2" / "OP26_BLOCKER35_MATRIX.csv"
    for source_row in load_csv(op26_path):
        msg = source_row.get("message", "")
        prc, trn, structure = context("OP26", msg)
        rows.append({
            "OP": "OP26",
            "PRC": prc,
            "TRN": trn,
            "MSG": msg,
            "canonical_requirement_id": source_row.get("canonical_requirement_id", ""),
            "category": source_row.get("category", ""),
            "source": str(op26_path.relative_to(ROOT)),
            "source_page": source_row.get("pdf_page", ""),
            "structure": structure,
            "status": "SOURCE_BLOCKED",
            "notes": join_unique((source_row.get("summary_problem", ""), source_row.get("current_resolution", ""))),
        })

    op32_path = ROOT / "codex_reports" / "OP32_P_MM_06" / "OP32_REAUDIT_GAPS.csv"
    for source_row in load_csv(op32_path):
        rows.append({
            "OP": "OP32",
            "PRC": source_row.get("procedure", ""),
            "TRN": source_row.get("transaction", ""),
            "MSG": source_row.get("message", ""),
            "canonical_requirement_id": source_row.get("canonical_requirement_id", ""),
            "category": source_row.get("current_state", ""),
            "source": join_unique((str(op32_path.relative_to(ROOT)), source_row.get("trace_source_refs", ""))),
            "source_page": source_row.get("source_page", ""),
            "structure": source_row.get("structure", ""),
            "status": "SOURCE_BLOCKED",
            "notes": join_unique((source_row.get("missing_information", ""), source_row.get("required_material", ""))),
        })

    op49_path = ROOT / "codex_reports" / "OP49_P_DS_01" / "OP49_BLOCKED_REQUIREMENTS.csv"
    for source_row in load_csv(op49_path):
        msg = source_row.get("message", "")
        prc, trn, structure = context("OP49", msg)
        source_dependent = any(
            source_row.get(column) == "YES"
            for column in ("classifier_blocked", "external_registry_blocked", "source_conflict", "xsd_qname_only_primary")
        )
        engine_dependent = source_row.get("engine_capability_gap") == "YES"
        if source_dependent and engine_dependent:
            status = "SOURCE_AND_ENGINE_BLOCKED"
        elif source_dependent:
            status = "SOURCE_BLOCKED"
        elif engine_dependent:
            status = "ENGINE_BLOCKED"
        else:
            status = "REVIEWED_BLOCKER"
        rows.append({
            "OP": "OP49",
            "PRC": prc,
            "TRN": trn,
            "MSG": msg,
            "canonical_requirement_id": source_row.get("canonical_id", ""),
            "category": source_row.get("primary_triage_status", ""),
            "source": str(op49_path.relative_to(ROOT)),
            "source_page": source_row.get("pdf_page", ""),
            "structure": structure,
            "status": status,
            "notes": join_unique((source_row.get("primary_blocker_reason", ""), source_row.get("required_action", ""))),
        })

    op35_path = ROOT / "codex_reports" / "OP35_1_P_TS_01" / "INITIAL_AUDIT" / "13_MESSAGE_IMPLEMENTABILITY.csv"
    for source_row in load_csv(op35_path):
        rows.append({
            "OP": "OP35.1",
            "PRC": "",
            "TRN": "",
            "MSG": source_row.get("message_code", ""),
            "canonical_requirement_id": f"SOURCE_REPORT_ONLY::{source_row.get('message_code', '')}",
            "category": source_row.get("implementability_status", ""),
            "source": str(op35_path.relative_to(ROOT)),
            "source_page": source_row.get("source_pages", ""),
            "structure": source_row.get("structure_id", ""),
            "status": "SOURCE_REPORT_ONLY_BLOCKED",
            "notes": source_row.get("blocking_reason", ""),
        })

    unique: list[dict[str, Any]] = []
    seen: set[tuple[str, ...]] = set()
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in SOURCE_BLOCKER_COLUMNS)
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return unique, classifier_rows


def op_number(root: Path) -> str:
    match = re.search(r"_OP_(\d+)$", root.name)
    return f"OP{match.group(1)}" if match else root.name


def build() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    app = EaeuXmlApplication(ROOT)
    package_roots = {
        load_yaml(path / "process.yaml").get("process_code"): path
        for path in sorted(ROOT.glob("P.*_OP_*"))
        if path.is_dir() and (path / "process.yaml").exists()
    }
    package_roots = {k: v for k, v in package_roots.items() if k}

    pcls027, pcls027_source = load_pcls027()
    matrix: list[dict[str, Any]] = []
    classifier_rows: list[dict[str, Any]] = []
    unresolved_structured: list[dict[str, Any]] = []
    message_seen: set[tuple[str, str]] = set()
    transaction_seen: set[tuple[str, str]] = set()
    unique_field_seen: set[tuple[str, str, str, str]] = set()
    process_counts: dict[str, Counter] = defaultdict(Counter)
    branches: dict[tuple[str, str, str, str, str], dict[str, str]] = {}

    for process in app.list_processes():
        process_code = process.process_code
        root = package_roots[process_code]
        op = op_number(root)
        messages_data = load_yaml(root / "messages.yaml")
        messages_index = {
            row.get("message_code"): row
            for row in messages_data.get("messages", [])
            if isinstance(row, dict)
        }
        transaction_data = load_yaml(root / "transactions.yaml")
        transactions_index = {
            row.get("transaction_code"): row
            for row in transaction_data.get("transactions", [])
            if isinstance(row, dict)
        }

        for transaction in app.list_transactions(process_code):
            transaction_seen.add((process_code, transaction.transaction_code))
            tr_raw = transactions_index.get(transaction.transaction_code, {})
            prc = tr_raw.get("procedure_code") or ""
            for message in app.list_messages(process_code, transaction.transaction_code):
                message_seen.add((process_code, message.message_code))
                raw = messages_index.get(message.message_code, {})
                rules_file = root / "message_rules" / f"{message.message_code}.yaml"
                rules = load_yaml(rules_file)
                form = app.get_form(process_code, transaction.transaction_code, message.message_code)
                branch_key = (op, prc, transaction.transaction_code, message.message_code, form.structure_id)
                branches[branch_key] = {
                    "OP": op,
                    "PRC": prc,
                    "TRN": transaction.transaction_code,
                    "MSG": message.message_code,
                    "structure": form.structure_id,
                }
                fields = flatten_fields(form.fields)
                by_path = {field.path: field for field in fields}
                paths = list(by_path)
                structured = rules.get("structured_rules") if isinstance(rules.get("structured_rules"), list) else []
                structured_overlays, unresolved = derive_structured_overlays(
                    structured, paths, form.structure_id
                )
                for item in unresolved:
                    unresolved_structured.append({
                        "OP": op,
                        "TRN": transaction.transaction_code,
                        "MSG": message.message_code,
                        "rule": json.dumps(item, ensure_ascii=False, default=str),
                    })

                field_usage = rules.get("field_usage") if isinstance(rules.get("field_usage"), dict) else {}
                fixed_values = rules.get("fixed_values") if isinstance(rules.get("fixed_values"), dict) else {}
                engine = app._engine(process_code)
                effective = app._effective_message_field_policies(engine, message.message_code)

                for field in fields:
                    unique_field_seen.add((process_code, message.message_code, form.structure_id, field.path))
                    normative = baseline_policy(field, by_path)
                    usage = field_usage.get(field.path)
                    if usage in {"REQUIRED", "OPTIONAL", "FORBIDDEN", "NOT_USED"}:
                        normalized = "FORBIDDEN" if usage == "NOT_USED" else usage
                        normative = merge_policy(normative, PolicyEvidence(normalized, origin="FIELD_USAGE"))
                    if field.path in fixed_values:
                        normative = merge_policy(normative, PolicyEvidence(
                            "FIXED", fixed_value=fixed_values[field.path], origin="FIXED_VALUES"
                        ))
                    if field.path in structured_overlays:
                        normative = merge_policy(normative, structured_overlays[field.path])
                    if effective and field.path in effective:
                        mp = effective[field.path]
                        normative = merge_policy(normative, PolicyEvidence(
                            mp.policy,
                            fixed_value=mp.fixed_value,
                            origin="MESSAGE_FIELD_POLICY",
                            source_refs=tuple(mp.affected_by_req),
                            notes=mp.notes or mp.condition or "",
                            conditional=mp.policy == "CONDITIONAL",
                        ))

                    validator = validator_policy(rules, field.path, normative)
                    status, priority = compare_status(normative, field, validator)
                    classifier = field.classifier or ""
                    classifier_status = ""
                    if classifier:
                        classifier_status = "STILL_EXTERNAL"
                    row = {
                        "OP": op,
                        "PRC": prc,
                        "TRN": transaction.transaction_code,
                        "MSG": message.message_code,
                        "structure": form.structure_id,
                        "field_path": field.path,
                        "normative_policy": normative.policy,
                        "normative_fixed_value": "" if normative.fixed_value is None else normative.fixed_value,
                        "classifier": classifier,
                        "classifier_status": classifier_status,
                        "current_gui_policy": gui_policy(field),
                        "current_default": "" if field.fixed_value is None else field.fixed_value,
                        "current_validator_policy": validator,
                        "status": status,
                        "priority": priority,
                        "policy_origin": normative.origin,
                        "source_refs": "; ".join(normative.source_refs),
                        "notes": normative.notes,
                    }
                    matrix.append(row)
                    process_counts[op][status] += 1

                # Classifier-dependent business-rule resolution.
                for rule in rules.get("business_rules") or ():
                    if not isinstance(rule, dict):
                        continue
                    text = str(rule.get("source_text") or "")
                    classifier_ids = find_classifier_tokens(rule)
                    if "классификатор" in text.casefold() and not classifier_ids:
                        if process_code == "P.SP.02" and ("IPDocKindCode" in text or "IPDocKindName" in text):
                            classifier_ids = ["P.CLS.027"]
                        else:
                            classifier_ids = ["UNSPECIFIED_CLASSIFIER"]
                    for classifier_id in classifier_ids:
                        document_kind = extract_document_kind(text)
                        expected_code = ""
                        status = "STILL_EXTERNAL"
                        code_confirmed = "NO"
                        name_branch_allowed = "UNKNOWN"
                        source = "; ".join(refs_to_text(rule.get("source_refs")))
                        notes = "No exact local authoritative name-to-code match established by this audit."
                        if classifier_id == "P.CLS.027" and document_kind:
                            matches = sorted(set(pcls027.get(document_kind, [])))
                            if len(matches) == 1:
                                expected_code = matches[0]
                                status = "RESOLVED_FIXED_CODE"
                                code_confirmed = "YES"
                                name_branch_allowed = "NO"
                                source = "; ".join(filter(None, (source, pcls027_source)))
                                notes = "Exact document-kind name match in local P.CLS.027 data."
                            elif len(matches) > 1:
                                status = "AMBIGUOUS"
                                expected_code = "|".join(matches)
                                name_branch_allowed = "UNKNOWN"
                                notes = "Exact name maps to multiple codes."
                            else:
                                status = "STILL_EXTERNAL"
                                name_branch_allowed = "UNKNOWN"
                                notes = "Exact document-kind name is absent from current local P.CLS.027 data; source review is still required."
                        classifier_rows.append({
                            "OP": op,
                            "MSG": message.message_code,
                            "CLASSIFIER_ID": classifier_id,
                            "DOCUMENT_KIND": document_kind,
                            "EXPECTED_CODE": expected_code,
                            "CODE_CONFIRMED": code_confirmed,
                            "NAME_BRANCH_ALLOWED": name_branch_allowed,
                            "SOURCE": source,
                            "VERSION_DATE": "",
                            "STATUS": status,
                            "NOTES": notes,
                        })

    branches_by_message: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for branch in branches.values():
        branches_by_message[(branch["OP"], branch["MSG"])].append(branch)

    requirement_blockers, source_classifier_rows = build_requirement_blockers(branches_by_message)
    classifier_rows.extend(source_classifier_rows)

    # Deduplicate classifier rows repeated through TRN branches and repeated source requirements.
    classifier_unique: list[dict[str, Any]] = []
    seen_classifier = set()
    for row in classifier_rows:
        key = tuple(str(row.get(col, "")) for col in CLASSIFIER_COLUMNS)
        if key not in seen_classifier:
            seen_classifier.add(key)
            classifier_unique.append(row)

    # The full matrix is branch-level. Headline defect counts are semantic and do not multiply
    # the same MSG/structure/field policy merely because a message is reused by several TRNs.
    semantic_matrix = aggregate_semantic_rows(matrix)
    defects = [row for row in semantic_matrix if row["status"] != "PASS"]
    divergences = [
        row for row in semantic_matrix
        if row["status"] in {"GUI_VALIDATOR_DIVERGENCE", "VALIDATOR_DEFECT"}
    ]

    unresolved_unique: list[dict[str, Any]] = []
    unresolved_grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in unresolved_structured:
        key = (row["OP"], row["MSG"], row["rule"])
        existing = unresolved_grouped.get(key)
        if existing is None:
            unresolved_grouped[key] = dict(row)
        else:
            existing["TRN"] = join_unique((existing.get("TRN", ""), row.get("TRN", "")))
    unresolved_unique.extend(unresolved_grouped.values())

    matrix_rows_by_branch = Counter(
        (row["OP"], row["PRC"], row["TRN"], row["MSG"], row["structure"])
        for row in matrix
    )
    defects_by_message_structure = Counter(
        (row["OP"], row["MSG"], row["structure"])
        for row in defects
    )
    blockers_by_message: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in requirement_blockers:
        blockers_by_message[(row["OP"], row["MSG"])].append(row)
    unresolved_by_message = Counter((row["OP"], row["MSG"]) for row in unresolved_unique)

    message_groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for branch in branches.values():
        message_groups[(branch["OP"], branch["MSG"], branch["structure"])].append(branch)

    message_reviews: list[dict[str, Any]] = []
    for (op, msg, structure), message_branches in sorted(message_groups.items()):
        message_blockers = blockers_by_message.get((op, msg), [])
        source_blockers = sum(
            1 for blocker in message_blockers if is_source_blocking_status(blocker["status"])
        )
        other_blockers = sum(
            1 for blocker in message_blockers if not is_source_blocking_status(blocker["status"])
        )
        inherited_op32_source_block = False
        if op == "OP32" and source_blockers == 0:
            # OP32 has 170 requirement rows but 24 runtime MSG. Messages without a dedicated
            # requirement table are still preflight-blocked by unresolved imported XSD/model versions.
            source_blockers = 1
            inherited_op32_source_block = True
        unique_field_defects = defects_by_message_structure[(op, msg, structure)]
        if unique_field_defects or other_blockers:
            review_status = "EXPLICIT_DEFECT"
        elif source_blockers:
            review_status = "SOURCE_BLOCKED"
        else:
            review_status = "PASS"
        notes: list[str] = []
        if inherited_op32_source_block:
            notes.append("Inherited OP32 UNRESOLVED_STRUCTURE_VERSION/XSD-model source block; no dedicated requirement row for this MSG.")
        if source_blockers and review_status == "EXPLICIT_DEFECT":
            notes.append("Message also has explicit source-blocked requirements; runtime defects remain separately actionable where source is sufficient.")
        if unresolved_by_message[(op, msg)]:
            notes.append("Complex structured-rule targets are retained explicitly and are not reduced to guessed static field policy.")
        matrix_rows = sum(
            matrix_rows_by_branch[(branch["OP"], branch["PRC"], branch["TRN"], branch["MSG"], branch["structure"])]
            for branch in message_branches
        )
        message_reviews.append({
            "OP": op,
            "PRC": join_unique(branch["PRC"] for branch in message_branches),
            "TRN": join_unique(branch["TRN"] for branch in message_branches),
            "MSG": msg,
            "structure": structure,
            "review_status": review_status,
            "matrix_rows": matrix_rows,
            "unique_field_defects": unique_field_defects,
            "source_blockers": source_blockers,
            "other_blockers": other_blockers,
            "unresolved_structured_rules": unresolved_by_message[(op, msg)],
            "notes": " ".join(notes),
        })

    process_to_op = {process_code: op_number(root) for process_code, root in package_roots.items()}
    expected_messages = {(process_to_op[process_code], msg) for process_code, msg in message_seen}
    expected_transactions = {(process_to_op[process_code], trn) for process_code, trn in transaction_seen}
    reviewed_messages = {(row["OP"], row["MSG"]) for row in message_reviews}
    reviewed_transactions = {(branch["OP"], branch["TRN"]) for branch in branches.values()}
    unreviewed_messages = sorted(expected_messages - reviewed_messages)
    unreviewed_transactions = sorted(expected_transactions - reviewed_transactions)
    unknown_policy_rows = [row for row in message_reviews if row["review_status"] not in {"PASS", "EXPLICIT_DEFECT", "SOURCE_BLOCKED"}]
    if unreviewed_messages or unreviewed_transactions or unknown_policy_rows:
        raise RuntimeError(
            "Audit coverage incomplete: "
            f"unreviewed_messages={len(unreviewed_messages)}, "
            f"unreviewed_transactions={len(unreviewed_transactions)}, "
            f"unknown_policy_rows={len(unknown_policy_rows)}"
        )

    def write_csv(name: str, rows: list[dict[str, Any]], columns: list[str]) -> None:
        with (REPORT_DIR / name).open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    write_csv("CROSS_OP_TRN_MSG_MATRIX.csv", matrix, MATRIX_COLUMNS)
    write_csv("CROSS_OP_POLICY_DEFECTS.csv", defects, MATRIX_COLUMNS)
    write_csv("CROSS_OP_CLASSIFIER_RESOLUTION.csv", classifier_unique, CLASSIFIER_COLUMNS)
    write_csv("CROSS_OP_GUI_VALIDATOR_DIVERGENCE.csv", divergences, MATRIX_COLUMNS)
    write_csv("CROSS_OP_SOURCE_BLOCKERS.csv", requirement_blockers, SOURCE_BLOCKER_COLUMNS)
    write_csv("CROSS_OP_MESSAGE_REVIEW.csv", message_reviews, MESSAGE_REVIEW_COLUMNS)
    write_csv(
        "UNRESOLVED_STRUCTURED_RULE_TARGETS.csv",
        unresolved_unique,
        ["OP", "TRN", "MSG", "rule"],
    )

    source_manifest = source_corpus_manifest()
    (REPORT_DIR / "SOURCE_CORPUS_MANIFEST.json").write_text(
        json.dumps(source_manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    status_counts = Counter(row["status"] for row in semantic_matrix)
    branch_status_counts = Counter(row["status"] for row in matrix)
    priority_counts = Counter(row["priority"] for row in defects)
    classifier_counts = Counter(row["STATUS"] for row in classifier_unique)
    blocker_status_counts = Counter(row["status"] for row in requirement_blockers)
    runtime_source_blockers = [
        row for row in requirement_blockers
        if row["OP"] != "OP35.1" and is_source_blocking_status(row["status"])
    ]
    source_report_only_blockers = [
        row for row in requirement_blockers if row["status"] == "SOURCE_REPORT_ONLY_BLOCKED"
    ]
    decision92_resolved = [
        row for row in requirement_blockers
        if row["OP"] == "OP23" and row["status"] == "SOURCE_RESOLVED_RUNTIME_UNIMPLEMENTED"
    ]
    message_review_counts = Counter(row["review_status"] for row in message_reviews)
    blocker_counts_by_op: dict[str, Counter] = defaultdict(Counter)
    for row in requirement_blockers:
        blocker_counts_by_op[row["OP"]][row["status"]] += 1
    op_lines = []
    op_status: dict[str, str] = {}
    for op in sorted({row["OP"] for row in message_reviews}):
        reviews = Counter(row["review_status"] for row in message_reviews if row["OP"] == op)
        if reviews["EXPLICIT_DEFECT"]:
            current_status = "AUDITED_WITH_EXPLICIT_DEFECTS"
        elif reviews["SOURCE_BLOCKED"]:
            current_status = "AUDITED_SOURCE_BLOCKED"
        else:
            current_status = "AUDITED_PASS"
        op_status[op] = current_status
        unique_rows = [row for row in semantic_matrix if row["OP"] == op]
        unique_defects = [row for row in defects if row["OP"] == op]
        op_lines.append(
            f"- {op}: status={current_status}, unique_field_policies={len(unique_rows)}, "
            f"unique_runtime_defects={len(unique_defects)}, source_blocked_requirements={blocker_counts_by_op[op]['SOURCE_BLOCKED'] + blocker_counts_by_op[op]['SOURCE_AND_ENGINE_BLOCKED']}."
        )

    markdown = f"""# CROSS-OP Transaction / Message / GUI Policy Audit

Generated from the current worktree. Production code was not modified by this audit builder.

## Scope

- Runtime OP packages: {len(package_roots)} ({', '.join(sorted(package_roots))}).
- Runtime transactions: {len(transaction_seen)}.
- Runtime messages: {len(message_seen)}.
- Unique MSG/structure field paths reviewed: {len(unique_field_seen)}.
- TRN/MSG/field matrix rows: {len(matrix)}.
- Unique effective field-policy rows after TRN reuse deduplication: {len(semantic_matrix)}.
- Source directory files inventoried by path/content-candidate scope: {len(source_manifest)}.
- OP35.1 / P.TS.01 is not a runtime package in the discovered process set; it remains SOURCE/REPORT_ONLY unless a package is added.
- UNREVIEWED_TRN: {len(unreviewed_transactions)}.
- UNREVIEWED_MSG: {len(unreviewed_messages)}.
- UNKNOWN_POLICY: {len(unknown_policy_rows)}.

## Result counts

- PASS (unique effective field-policy rows): {status_counts['PASS']}.
- GUI_DEFECT: {status_counts['GUI_DEFECT']}.
- POLICY_DEFECT: {status_counts['POLICY_DEFECT']}.
- DEFAULT_VALUE_DEFECT: {status_counts['DEFAULT_VALUE_DEFECT']}.
- VALIDATOR_DEFECT: {status_counts['VALIDATOR_DEFECT']}.
- GUI_VALIDATOR_DIVERGENCE: {status_counts['GUI_VALIDATOR_DIVERGENCE']}.
- SOURCE_BLOCKED runtime requirements: {len(runtime_source_blockers)}.
- SOURCE/REPORT_ONLY blocked OP35.1 messages: {len(source_report_only_blockers)}.
- AMBIGUOUS: {status_counts['AMBIGUOUS']}.
- P0 unique defects: {priority_counts['P0']}.
- P1 unique defects: {priority_counts['P1']}.
- P2 unique defects: {priority_counts['P2']}.

Raw branch-level matrix counts are retained only in `CROSS_OP_TRN_MSG_MATRIX.csv`; the headline defect counts above are deduplicated by effective MSG/structure/field policy semantics.

## Message review coverage

- PASS branches: {message_review_counts['PASS']}.
- EXPLICIT_DEFECT branches: {message_review_counts['EXPLICIT_DEFECT']}.
- SOURCE_BLOCKED branches: {message_review_counts['SOURCE_BLOCKED']}.
- Coverage gate: UNREVIEWED_TRN=0, UNREVIEWED_MSG=0, UNKNOWN_POLICY=0.

## Requirement/source blocker accounting

- SOURCE_BLOCKED: {blocker_status_counts['SOURCE_BLOCKED']}.
- SOURCE_AND_ENGINE_BLOCKED: {blocker_status_counts['SOURCE_AND_ENGINE_BLOCKED']}.
- ENGINE_BLOCKED: {blocker_status_counts['ENGINE_BLOCKED']}.
- PARTIAL_PROOF: {blocker_status_counts['PARTIAL_PROOF']}.
- REVIEWED_BLOCKER: {blocker_status_counts['REVIEWED_BLOCKER']}.
- SOURCE_RESOLVED_RUNTIME_UNIMPLEMENTED: {blocker_status_counts['SOURCE_RESOLVED_RUNTIME_UNIMPLEMENTED']}.
- SOURCE_REPORT_ONLY_BLOCKED: {blocker_status_counts['SOURCE_REPORT_ONLY_BLOCKED']}.
- OP23 Decision №92 historical classifier source blockers resolved by current exact-name evidence: {len(decision92_resolved)}.

## Classifier resolution rows

- RESOLVED_FIXED_CODE: {classifier_counts['RESOLVED_FIXED_CODE']}.
- RESOLVED_CODE_OR_NAME: {classifier_counts['RESOLVED_CODE_OR_NAME']}.
- STILL_EXTERNAL: {classifier_counts['STILL_EXTERNAL']}.
- AMBIGUOUS: {classifier_counts['AMBIGUOUS']}.
- SOURCE_CONFLICT: {classifier_counts['SOURCE_CONFLICT']}.

## Per-OP matrix summary

{chr(10).join(op_lines)}

## Method and limits

The matrix starts from structure cardinality and overlays current source-referenced message rules in increasing authority: `field_usage`, `fixed_values`, reducible `structured_rules`, then explicit `MessageFieldPolicy`. GUI state is taken from the actual `EaeuXmlApplication.get_form()` result for every real TRN/MSG branch. Validator state records enforcement through `field_usage`, `fixed_values`, structured rules, explicit `MessageFieldPolicy` sanitization/required checks, or structure semantics.

Conditional FIXED/FORBIDDEN structured rules are treated as context-dependent policies and do not create unconditional `DEFAULT_VALUE_DEFECT` rows. Complex structured rules that cannot be safely reduced to one static field policy are retained in `UNRESOLVED_STRUCTURED_RULE_TARGETS.csv`; they are explicitly reviewed rather than guessed.

Source state is kept separate from runtime policy state in `CROSS_OP_SOURCE_BLOCKERS.csv`. OP32 remains source-blocked because exact imported model/XSD versions and Clark QNames are unresolved. OP49 source conflicts remain source conflicts. OP26 input/UI policies are treated as current project behavior and are not promoted to normative fixed values without source proof. OP35.1 remains source/report-only.

Classifier resolution is exact-name only. For local P.CLS.027 data, only one exact name-to-code match yields `RESOLVED_FIXED_CODE`; ambiguous or absent exact names are not force-resolved. Current Decision №92 evidence in `/Users/tema/Documents/Work/Документы_xml/92 решение.pdf` supersedes the stale OP23 historical “classifier unavailable” premise for the exact document-kind names found on pp.13-14 and 17, while runtime enforcement/proof remains a separate question.
"""
    (REPORT_DIR / "CROSS_OP_TRANSACTION_POLICY_AUDIT.md").write_text(markdown, encoding="utf-8")

    summary = {
        "ops_found": sorted(process_to_op.values()),
        "runtime_processes": {process_to_op[code]: code for code in sorted(process_to_op)},
        "trn_total": len(transaction_seen),
        "msg_total": len(message_seen),
        "fields_reviewed": len(unique_field_seen),
        "matrix_rows": len(matrix),
        "unique_effective_policy_rows": len(semantic_matrix),
        "status_counts": dict(status_counts),
        "branch_status_counts": dict(branch_status_counts),
        "priority_counts": dict(priority_counts),
        "classifier_counts": dict(classifier_counts),
        "requirement_blocker_status_counts": dict(blocker_status_counts),
        "runtime_source_blocked_requirements": len(runtime_source_blockers),
        "source_report_only_blocked_messages": len(source_report_only_blockers),
        "op23_decision92_source_resolved_runtime_unimplemented": len(decision92_resolved),
        "message_review_counts": dict(message_review_counts),
        "op_status": op_status,
        "op35_1_status": "SOURCE_REPORT_ONLY/BLOCKED_BY_SOURCE",
        "unreviewed_trn": len(unreviewed_transactions),
        "unreviewed_msg": len(unreviewed_messages),
        "unknown_policy": len(unknown_policy_rows),
        "unresolved_structured_rule_targets": len(unresolved_unique),
        "source_files_inventoried": len(source_manifest),
    }
    (REPORT_DIR / "AUDIT_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    build()
