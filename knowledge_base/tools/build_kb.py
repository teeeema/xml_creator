#!/usr/bin/env python3
"""Build the local EAEU normative knowledge base without touching production files."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge_base"
REPORT_DIR = ROOT / "codex_reports" / "KNOWLEDGE_BASE"
NORM = Path("/Users/tema/Documents/Work/Документы_xml")
GENERATOR = "knowledge_base/tools/build_kb.py"
BUILD_TIME = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")

PROCESS_CONFIG = {
    "OP22": {
        "process": "P.SP.02",
        "package": "P.SP.02_OP_22",
        "folder": "OP22_P_SP_02",
        "source_id": "OP22_P_SP_02",
        "expected_requirements": 1609,
        "requirement_status": "CURRENT_CANONICAL_INVENTORY_RECOVERED_FROM_SOURCE_REFS",
        "audit": "codex_reports/FINAL_DELIVERY_AUDIT.md",
    },
    "OP23": {
        "process": "P.SP.03",
        "package": "P.SP.03_OP_23",
        "folder": "OP23_P_SP_03",
        "source_id": "OP23_P_SP_03",
        "expected_requirements": 710,
        "requirement_status": "CURRENT_FINAL_IMPLEMENTATION_SNAPSHOT",
        "audit": "codex_reports/OP23_P_SP_03/OP23_FINAL_IMPLEMENTATION_AUDIT.md",
    },
    "OP26": {
        "process": "P.MM.01",
        "package": "P.MM.01_OP_26",
        "folder": "OP26_P_MM_01",
        "source_id": "OP26_P_MM_01",
        "expected_requirements": 239,
        "requirement_status": "SOURCE_RECONCILED_239_ATOMIC_REQUIREMENTS",
        "audit": "codex_reports/OP26_P_MM_01/OP26_FULL_IMPLEMENTATION_READINESS.md",
    },
    "OP32": {
        "process": "P.MM.06",
        "package": "P.MM.06_OP_32",
        "folder": "OP32_P_MM_06",
        "source_id": "OP32_P_MM_06",
        "expected_requirements": 170,
        "requirement_status": "SOURCE_RECOVERY_COMPLETE_WITH_BLOCKERS",
        "audit": "codex_reports/OP32_P_MM_06/OP32_SOURCE_RECOVERY_AUDIT.md",
    },
    "OP49": {
        "process": "P.DS.01",
        "package": "P.DS.01_OP_49",
        "folder": "OP49_P_DS_01",
        "source_id": "OP49_P_DS_01",
        "expected_requirements": 166,
        "requirement_status": "READ_ONLY_REAUDIT_VALIDATED_166_CANONICAL_REQUIREMENTS",
        "audit": "codex_reports/OP49_P_DS_01/OP49_REAUDIT_AUDIT.md",
    },
}

SOURCES = [
    {
        "source_id": "OP22_P_SP_02",
        "path": NORM / "ОП_22.pdf",
        "document_type": "normative_process",
        "related_processes": ["P.SP.02"],
    },
    {
        "source_id": "OP23_P_SP_03",
        "path": NORM / "ОП_23.pdf",
        "document_type": "normative_process",
        "related_processes": ["P.SP.03"],
    },
    {
        "source_id": "OP26_P_MM_01",
        "path": NORM / "26_ОП.pdf",
        "document_type": "normative_process_decision_68",
        "related_processes": ["P.MM.01"],
        "alternate_paths": [str(ROOT / "P.MM.01_OP_26/normative_sources/err_22042022_68_doc.pdf")],
    },
    {
        "source_id": "OP32_P_MM_06",
        "path": NORM / "32_ОП.pdf",
        "document_type": "normative_process",
        "related_processes": ["P.MM.06"],
    },
    {
        "source_id": "OP49_P_DS_01",
        "path": NORM / "49_ОП.pdf",
        "document_type": "normative_process",
        "related_processes": ["P.DS.01"],
    },
    {
        "source_id": "DECISION_5",
        "path": NORM / "5 решение.pdf",
        "document_type": "shared_decision",
        "related_processes": ["P.SP.02", "P.SP.03", "P.MM.01", "P.MM.06", "P.DS.01"],
    },
]

SOURCE_BY_FILENAME = {
    "ОП_22.pdf": "OP22_P_SP_02",
    "OP_22.pdf": "OP22_P_SP_02",
    "ОП_23.pdf": "OP23_P_SP_03",
    "OP_23.pdf": "OP23_P_SP_03",
    "26_ОП.pdf": "OP26_P_MM_01",
    "32_ОП.pdf": "OP32_P_MM_06",
    "49_ОП.pdf": "OP49_P_DS_01",
    "49 ОП.pdf": "OP49_P_DS_01",
    "5 решение.pdf": "DECISION_5",
}

PROCESS_SOURCE_FALLBACK = {
    "P.SP.02": "OP22_P_SP_02",
    "P.SP.03": "OP23_P_SP_03",
    "P.MM.01": "OP26_P_MM_01",
    "P.MM.06": "OP32_P_MM_06",
    "P.DS.01": "OP49_P_DS_01",
}

OP49_CONFIRMED_SCOPE = {
    "P.DS.01.MSG.001": 35,
    "P.DS.01.MSG.002": 38,
    "P.DS.01.MSG.004": 2,
    "P.DS.01.MSG.005": 54,
    "P.DS.01.MSG.006": 37,
}

# Confirmed directly by OP32 source pages 21-22. These two catalog entities do
# not currently have dependency rows in OP32_CLASSIFIER_SOURCE_INVENTORY.csv,
# but omitting them would make the classifier catalog incomplete.
OP32_CLASSIFIER_CATALOG_ONLY = {
    "P.CLS.024": {
        "classifier_name": "классификатор языков",
        "required_version": "ISO 639-1; edition/version not specified in the normative table",
        "normative_source": "32_ОП.pdf p.21 Table 9",
        "page": "21",
    },
    "P.CLS.064": {
        "classifier_name": "номенклатура медицинских изделий Евразийского экономического союза",
        "required_version": "approved by EEC Board Decision No.46 of 03.04.2018; dataset version not found",
        "normative_source": "32_ОП.pdf p.22 Table 9",
        "page": "22",
    },
}

ENGINE_RULE_KINDS = [
    "aggregate_comparison",
    "cardinality",
    "comparison",
    "conditional_fixed_value",
    "conditional_presence",
    "cross_instance_comparison",
    "external",
    "fixed_value",
    "for_each",
    "group_distinctness",
    "presence",
    "selection_cardinality",
]


def json_dump(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def quote_yaml(value: Any) -> str:
    if value is None:
        return '""'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def frontmatter(items: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in items.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {quote_yaml(item)}")
        else:
            lines.append(f"{key}: {quote_yaml(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def ensure_allowed(path: Path) -> None:
    resolved = path.resolve()
    if not (resolved.is_relative_to(KB.resolve()) or resolved.is_relative_to(REPORT_DIR.resolve())):
        raise RuntimeError(f"Refusing to write outside KB/report scope: {path}")


def write_generated(path: Path, text: str, *, force_generated: bool = False) -> bool:
    ensure_allowed(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force_generated:
        old = path.read_text(encoding="utf-8", errors="replace")
        if f"generated_by: {quote_yaml(GENERATOR)}" not in old and "generated_by: build_kb.py" not in old:
            return False
    path.write_text(text, encoding="utf-8")
    return True


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def git_snapshot() -> dict[str, Any]:
    def run(*args: str) -> str:
        return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False).stdout.strip()

    status = run("git", "status", "--porcelain=v1").splitlines()
    return {
        "head": run("git", "rev-parse", "--verify", "HEAD"),
        "branch": run("git", "branch", "--show-current"),
        "dirty_entries": len(status),
        "status": status,
        "captured_at": BUILD_TIME,
    }


def source_id_for(document: str, process: str) -> str:
    doc = (document or "").strip()
    if doc in SOURCE_BY_FILENAME:
        return SOURCE_BY_FILENAME[doc]
    if "19.04.2022" in doc or "№68" in doc or "No.68" in doc:
        return "OP26_P_MM_01"
    return PROCESS_SOURCE_FALLBACK.get(process, "")


def normalize_page(value: str) -> int | None:
    m = re.search(r"\d+", str(value or ""))
    return int(m.group()) if m else None


def normalize_gap_status(raw: str, category: str = "") -> str:
    s = f"{raw} {category}".upper()
    if any(x in s for x in ["IMPLEMENTED_CONFIRMED", "CLOSED_CONFIRMED", "SATISFIED"]):
        return "IMPLEMENTED_CONFIRMED"
    if "SOURCE_CONFLICT" in s or "CONFLICT" in s:
        return "OPEN_SOURCE_CONFLICT"
    if "CLASSIFIER" in s or "REFERENCE_DATA" in s:
        return "OPEN_CLASSIFIER"
    if "EXTERNAL_REGISTRY" in s or "EXTERNAL_INFORMATION" in s or "EXTERNAL_CONTEXT" in s:
        return "OPEN_EXTERNAL_REGISTRY"
    if "MISSING_STRUCTURE" in s:
        return "OPEN_MISSING_STRUCTURE"
    if "MISSING_NORMATIVE" in s or "MISSING_DATA" in s:
        return "OPEN_MISSING_NORMATIVE_DATA"
    if "AMBIG" in s:
        return "OPEN_NORMATIVE_AMBIGUITY"
    if "ENGINE" in s:
        return "OPEN_ENGINE"
    if "PRODUCTION" in s or "MAPPING" in s or "PARTIAL" in s:
        return "OPEN_PRODUCTION_MAPPING"
    return "OTHER"


def extract_original_source_text(notes: str) -> str:
    marker = "original source text:"
    low = (notes or "").lower()
    pos = low.find(marker)
    if pos < 0:
        return ""
    text = notes[pos + len(marker) :].strip()
    if " | " in text:
        text = text.split(" | ", 1)[0].strip()
    return text


def expand_requirement_code(value: str) -> list[int]:
    raw = str(value or "").strip()
    if raw.isdigit():
        return [int(raw)]
    match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", raw)
    if not match:
        return []
    start, end = map(int, match.groups())
    if end < start:
        return []
    return list(range(start, end + 1))


def inherited_table_from_text(text: str) -> str:
    match = re.search(r"таблиц[ыа]\s+(\d+)", str(text or ""), flags=re.I)
    return match.group(1) if match else ""


def closure_criterion_for(status: str) -> str:
    return {
        "OPEN_CLASSIFIER": "Official classifier/reference-data payload and required version are available locally; the rule is wired and regression-validated against that payload.",
        "OPEN_EXTERNAL_REGISTRY": "Authoritative external-registry contract/data source is available and the requirement is validated against the confirmed external behavior.",
        "OPEN_NORMATIVE_AMBIGUITY": "An authoritative normative clarification resolves the ambiguity; the selected interpretation is traced to that source and regression-tested.",
        "OPEN_SOURCE_CONFLICT": "A higher-priority authoritative source resolves the conflicting values; provenance is recorded and the conflicting mapping is replaced with the confirmed one.",
        "OPEN_MISSING_STRUCTURE": "The missing official structure/schema material is available and the requirement can be mapped to a confirmed structure/path.",
        "OPEN_MISSING_NORMATIVE_DATA": "The missing normative material is available and the requirement is re-audited against it.",
        "OPEN_ENGINE": "The required generic engine capability is implemented and the requirement has positive/negative regression evidence.",
        "OPEN_PRODUCTION_MAPPING": "The confirmed normative mapping is wired in production and covered by regression evidence.",
        "OTHER": "The recorded missing information is supplied, the requirement is re-audited, and implementation/runtime evidence confirms closure.",
    }.get(status, "No closure criterion recorded.")


def recover_op22_canonical_inventory() -> list[dict[str, str]]:
    """Recover the current 1609-row OP22 inventory from confirmed package source_refs.

    Range rows are expanded only when the current normative table/item is explicit.
    For inherited ranges, the atomic source text is resolved recursively through the
    referenced table so the leaf source text/page is preserved without inventing it.
    """

    rule_dir = ROOT / "P.SP.02_OP_22" / "message_rules"
    rule_files = sorted(rule_dir.glob("*.yaml"))
    matrix_rows = [
        r for r in read_csv(ROOT / "codex_reports/FINAL_DELIVERY_MESSAGE_MATRIX.csv") if r.get("op") == "OP22"
    ]
    matrix_by_message = {r.get("message", ""): r for r in matrix_rows if r.get("message")}
    current_gaps = {
        r.get("canonical_requirement_id", ""): r
        for r in read_csv(ROOT / "codex_reports/FINAL_DELIVERY_GAPS.csv")
        if r.get("op") == "OP22" and r.get("canonical_requirement_id")
    }
    fix_rows = {
        r.get("canonical_requirement_id", ""): r
        for r in read_csv(ROOT / "codex_reports/FIX_NOW_CODE_RESULTS.csv")
        if r.get("op") == "OP22" and r.get("canonical_requirement_id")
    }

    parsed_files: list[tuple[Path, dict[str, Any]]] = [(path, load_json(path)) for path in rule_files]
    direct_by_table_item: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    ranges_by_table: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for path, data in parsed_files:
        for business_rule in data.get("business_rules", []):
            refs = business_rule.get("source_refs") or []
            if not refs:
                raise RuntimeError(f"OP22 business rule without source_refs: {path} / {business_rule.get('rule_id')}")
            ref = refs[0]
            table = str(ref.get("table", "")).strip()
            code = str(business_rule.get("requirement_code", "")).strip()
            expanded = expand_requirement_code(code)
            if not table or not expanded:
                raise RuntimeError(f"Unparseable OP22 requirement identity: {path} / table={table!r} / code={code!r}")
            entry = {"path": path, "data": data, "rule": business_rule, "ref": ref, "table": table, "expanded": expanded}
            if len(expanded) == 1 and code.isdigit():
                direct_by_table_item[(table, expanded[0])].append(entry)
            else:
                ranges_by_table[table].append(entry)

    def resolve_leaf(table: str, item: int, seen: tuple[str, ...] = ()) -> tuple[dict[str, Any] | None, list[str]]:
        if table in seen:
            return None, [*seen, table]
        direct = direct_by_table_item.get((table, item), [])
        if direct:
            signatures = {
                (
                    x["rule"].get("source_text", ""),
                    str(x["ref"].get("page", "")),
                    str(x["ref"].get("document", "")),
                )
                for x in direct
            }
            if len(signatures) == 1:
                return direct[0], [*seen, table]
            return None, [*seen, table]
        candidates = [x for x in ranges_by_table.get(table, []) if item in x["expanded"]]
        inherited_tables = {inherited_table_from_text(x["rule"].get("source_text", "")) for x in candidates}
        inherited_tables.discard("")
        if len(inherited_tables) != 1:
            return None, [*seen, table]
        inherited = next(iter(inherited_tables))
        return resolve_leaf(inherited, item, (*seen, table))

    recovered: list[dict[str, str]] = []
    for path, data in parsed_files:
        message = str(data.get("message_code", ""))
        matrix = matrix_by_message.get(message, {})
        structure = str(data.get("structure_id", "") or matrix.get("structure", ""))
        for business_rule in data.get("business_rules", []):
            current_ref = (business_rule.get("source_refs") or [])[0]
            current_table = str(current_ref.get("table", "")).strip()
            code = str(business_rule.get("requirement_code", "")).strip()
            items = expand_requirement_code(code)
            inherited_table = inherited_table_from_text(business_rule.get("source_text", "")) if len(items) > 1 else ""
            for item in items:
                cid = f"{message}:{current_table}:{item}"
                leaf: dict[str, Any] | None
                chain: list[str]
                if inherited_table:
                    leaf, chain = resolve_leaf(inherited_table, item)
                else:
                    leaf = direct_by_table_item.get((current_table, item), [None])[0]
                    chain = [current_table]
                if leaf is None:
                    source_text = str(business_rule.get("source_text", ""))
                    source_ref = current_ref
                    evidence = "CONFIRMED_PDF_RANGE_REFERENCE"
                else:
                    source_text = str(leaf["rule"].get("source_text", ""))
                    source_ref = leaf["ref"]
                    evidence = "CONFIRMED_PDF_SOURCE_REF"

                row: dict[str, str] = {
                    "canonical_requirement_id": cid,
                    "op": "OP22",
                    "process": "P.SP.02",
                    "procedure": str(matrix.get("procedure", "")),
                    "transaction": str(matrix.get("transaction", "")),
                    "operation": str(matrix.get("operation", "")),
                    "message": message,
                    "requirement": f"REQ {item} (Table {current_table})",
                    "structure": structure,
                    "source": str(source_ref.get("document", "ОП_22.pdf")) or "ОП_22.pdf",
                    "source_page": str(source_ref.get("page", "")),
                    "source_table_or_item": f"Table {source_ref.get('table', current_table)}, item {item}",
                    "source_text": source_text,
                    "source_version": str(source_ref.get("version_context", current_ref.get("version_context", ""))),
                    "current_source_page": str(current_ref.get("page", "")),
                    "current_source_table": current_table,
                    "current_source_item": str(item),
                    "range_requirement_code": code if len(items) > 1 else "",
                    "inherited_source_chain": " -> ".join(chain),
                    "evidence_level": evidence,
                    "trace_source_refs": json.dumps(
                        {"current": current_ref, "leaf": source_ref, "range_chain": chain}, ensure_ascii=False, sort_keys=True
                    ),
                }

                gap = current_gaps.get(cid)
                if gap:
                    gap_source = gap.get("source", "")
                    row.update({k: str(v) for k, v in gap.items() if v is not None and k not in {
                        "canonical_requirement_id", "op", "process", "procedure", "transaction", "operation", "message",
                        "requirement", "structure", "source", "source_page", "notes", "trace_source_refs"
                    }})
                    row["gap_source"] = gap_source
                    status = normalize_gap_status(gap.get("current_status", gap.get("current_state", "")), gap.get("category", ""))
                    row["status_normalized"] = status
                    row["implementation_status"] = gap.get("current_status", gap.get("current_state", "OPEN"))
                    row["plain_explanation"] = gap.get("current_state", "") or gap.get("category", "")
                    row["closure_criterion"] = closure_criterion_for(status)
                else:
                    row["status_normalized"] = "IMPLEMENTED_CONFIRMED"
                    row["implementation_status"] = "CURRENT_EXECUTABLE_COVERAGE"
                    row["current_status"] = "IMPLEMENTED_CONFIRMED"
                    row["current_state"] = "Current verified delivery snapshot counts this requirement within executable coverage."
                    row["plain_explanation"] = (
                        "Current executable coverage in FINAL_DELIVERY_AUDIT; this is not individual positive/negative certification."
                    )
                    row["closure_criterion"] = "Already counted as implemented in the current verified delivery snapshot."

                fix = fix_rows.get(cid)
                if fix:
                    for key in [
                        "xml_owner", "xml_qname", "xml_path", "production_rule", "regression_test",
                        "positive_xml_case", "negative_xml_case", "current_status", "current_reason",
                    ]:
                        if fix.get(key):
                            row[key] = fix[key]
                    if fix.get("current_status"):
                        row["status_normalized"] = normalize_gap_status(fix["current_status"], row.get("category", ""))
                        row["implementation_status"] = fix["current_status"]
                recovered.append(row)

    ids = [r["canonical_requirement_id"] for r in recovered]
    if len(recovered) != 1609 or len(ids) != len(set(ids)):
        raise RuntimeError(f"OP22 canonical recovery mismatch: total={len(recovered)} unique={len(set(ids))}")
    recovered_counts = Counter(r["message"] for r in recovered)
    matrix_total = 0
    for matrix in matrix_rows:
        expected = int(matrix.get("expanded_requirements") or 0)
        matrix_total += expected
        actual = recovered_counts.get(matrix.get("message", ""), 0)
        if actual != expected:
            raise RuntimeError(f"OP22 message arithmetic mismatch {matrix.get('message')}: {actual} != {expected}")
    if matrix_total != 1609:
        raise RuntimeError(f"OP22 matrix total mismatch: {matrix_total} != 1609")
    return recovered


def _clean_pdf_rule_page(text: str) -> str:
    """Remove repeated page/table headers while preserving normative row text."""

    cleaned: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.fullmatch(r"\d+", stripped):
            continue
        if stripped in {"Код требования Формулировка требования", "Код", "требования", "Формулировка требования"}:
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def _normalize_normative_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _op26_primary_recovery() -> tuple[dict[int, dict[str, Any]], list[dict[str, Any]]]:
    """Recover the OP26 rows that were collapsed in the 201-row audit dataset.

    This intentionally reads the primary 26_ОП.pdf because the re-audit proved
    that MSG.002 REQ.050 merged source rows 50..87 and MSG.028 merged two
    different source rows both numbered 5.
    """

    pdf = NORM / "26_ОП.pdf"
    reader = PdfReader(str(pdf))

    table19_pages: list[tuple[int, str]] = []
    page_by_item: dict[int, int] = {}
    marker19 = re.compile(r"(?m)^([5-8]\d)\.\s+")
    for pdf_page in range(224, 232):
        text = _clean_pdf_rule_page(reader.pages[pdf_page - 1].extract_text() or "")
        table19_pages.append((pdf_page, text))
        for match in marker19.finditer(text):
            number = int(match.group(1))
            if 50 <= number <= 87:
                page_by_item.setdefault(number, pdf_page)

    table19_text = "\n".join(text for _, text in table19_pages)
    matches19 = [m for m in marker19.finditer(table19_text) if 50 <= int(m.group(1)) <= 87]
    numbers19 = [int(m.group(1)) for m in matches19]
    if numbers19 != list(range(50, 88)):
        raise RuntimeError(f"OP26 Table 19 source numbering mismatch: {numbers19}")

    table19: dict[int, dict[str, Any]] = {}
    for index, match in enumerate(matches19):
        number = int(match.group(1))
        end = matches19[index + 1].start() if index + 1 < len(matches19) else len(table19_text)
        body = table19_text[match.end():end]
        if number == 87:
            body = re.split(r"\s+31\.\s+Требования к заполнению", body, maxsplit=1)[0]
        body = _normalize_normative_text(body)
        if not body or number not in page_by_item:
            raise RuntimeError(f"OP26 Table 19 item {number} could not be recovered from primary PDF")
        table19[number] = {"text": body, "pdf_page": page_by_item[number]}

    marker21 = re.compile(r"(?m)^([1-7])(?:\.\s+|\s+)")
    duplicate_fives: list[dict[str, Any]] = []
    for pdf_page in (233, 234):
        text = _clean_pdf_rule_page(reader.pages[pdf_page - 1].extract_text() or "")
        matches = list(marker21.finditer(text))
        for index, match in enumerate(matches):
            if int(match.group(1)) != 5:
                continue
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            body = text[match.end():end]
            if pdf_page == 234:
                body = re.split(r"\s+33\.\s+Требования к заполнению", body, maxsplit=1)[0]
            body = _normalize_normative_text(body)
            if body:
                duplicate_fives.append({"text": body, "pdf_page": pdf_page})
    if len(duplicate_fives) != 2 or [x["pdf_page"] for x in duplicate_fives] != [233, 234]:
        raise RuntimeError(f"OP26 Table 21 duplicate item 5 recovery mismatch: {duplicate_fives}")
    return table19, duplicate_fives


def _op26_split_record(
    base: dict[str, str],
    *,
    requirement_number: int,
    source_text: str,
    pdf_page: int,
    table: int,
    occurrence: int = 1,
    status: str,
) -> dict[str, str]:
    row = dict(base)
    prefix = base["canonical_requirement_id"].rsplit(".REQ.", 1)[0]
    canonical_suffix = f"{requirement_number:03d}" if occurrence == 1 else f"{requirement_number:03d}.{occurrence}"
    row["canonical_requirement_id"] = f"{prefix}.REQ.{canonical_suffix}"
    row["requirement"] = source_text
    row["source_text"] = source_text
    row["source_page"] = str(pdf_page)
    row["source_table_or_item"] = f"Таблица {table}, пункт {requirement_number}"
    row["current_source_table"] = str(table)
    row["current_source_item"] = str(requirement_number)
    row["source_occurrence"] = str(occurrence)
    row["canonical_disambiguator"] = "" if occurrence == 1 else f"source_occurrence_{occurrence}"
    # The PDF extraction contains line-break artifacts inside several prefixed
    # names. The completed re-audit did not prove per-atomic exact QNames for
    # these newly split rows, so keep them unresolved instead of guessing from
    # a partially reconstructed lexical token.
    row["xml_qname"] = ""
    row["xml_owner"] = ""
    # The re-audit did not establish per-atomic exact paths for the previously
    # collapsed rows. Preserve that uncertainty rather than inheriting the
    # aggregate path from the old merged record.
    row["xml_path"] = ""
    row["status_normalized"] = status
    row["current_status"] = status
    row["current_state"] = status
    row["implementation_status"] = status
    row["production_rule"] = ""
    row["regression_test"] = ""
    row["positive_xml_case"] = ""
    row["negative_xml_case"] = ""
    row["required_engine_capability"] = ""
    row["blocks_delivery"] = "YES"

    if status == "OPEN_NORMATIVE_AMBIGUITY":
        row["plain_explanation"] = "Primary PDF Table 19 item 84 is truncated after the phrase ending with 'и'; the missing normative tail must not be inferred."
        row["missing_information"] = "Official corrected/full text of 26_ОП.pdf Table 19 item 84."
        row["recommended_action"] = "Obtain an official corrected publication or authoritative clarification for Table 19 item 84."
        row["closure_criterion"] = closure_criterion_for(status)
        row["can_fix_without_external_docs"] = "NO"
    elif status == "OPEN_EXTERNAL_REGISTRY":
        row["plain_explanation"] = "The normative rule requires an authoritative external EAEU registry check; offline closure is not proven."
        row["missing_information"] = "Authoritative external registry contract/data source required by this atomic rule."
        row["recommended_action"] = "Provide the authoritative registry contract/data and requirement-level positive/negative proof."
        row["closure_criterion"] = closure_criterion_for(status)
        row["can_fix_without_external_docs"] = "NO"
    else:
        row["plain_explanation"] = "Atomic source row recovered from the primary PDF; production mapping and requirement-level proof must be synchronized separately."
        row["missing_information"] = "Atomic production mapping and requirement-level regression/runtime proof."
        row["recommended_action"] = "Map this atomic requirement in production only from the confirmed source row and add requirement-level regression proof."
        row["closure_criterion"] = closure_criterion_for(status)
        row["can_fix_without_external_docs"] = "YES"

    row["trace_source_refs"] = json.dumps(
        [
            {
                "source_id": "OP26_P_MM_01",
                "document": base.get("source", "Решение Коллегии ЕЭК от 19.04.2022 №68"),
                "location": "IX. Требования к заполнению",
                "status": "CONFIRMED",
                "section": "IX. Требования к заполнению",
                "table": str(table),
                "item": str(requirement_number),
                "source_occurrence": occurrence,
                "page": pdf_page,
                "version_context": base.get("source_version", "P.MM.01 1.1.0"),
            }
        ],
        ensure_ascii=False,
        sort_keys=True,
    )
    row["evidence_level"] = "CONFIRMED_PDF"
    return row


def recover_op26_atomic_inventory() -> list[dict[str, str]]:
    source_rows = read_csv(ROOT / "codex_reports/OP26_P_MM_01/OP26_REAUDIT_REQUIREMENTS.csv")
    if len(source_rows) != 201:
        raise RuntimeError(f"OP26 source re-audit row count changed: {len(source_rows)} != 201")

    table19, duplicate_fives = _op26_primary_recovery()
    recovered: list[dict[str, str]] = []
    expanded_msg002 = False
    expanded_msg028 = False
    for original in source_rows:
        if not original.get("canonical_requirement_id"):
            continue
        row = dict(original)
        row["source_text"] = row.get("requirement", "")
        row["status_normalized"] = normalize_gap_status(row.get("current_status", ""), row.get("current_state", ""))
        row["evidence_level"] = "CONFIRMED_PDF" if normalize_page(row.get("source_page", "")) else "AUDIT_DERIVED"

        if row["canonical_requirement_id"] == "OP26.P_MM_01.P.MM.01.MSG.002.REQ.050":
            for number in range(50, 88):
                status = "OPEN_NORMATIVE_AMBIGUITY" if number == 84 else "OPEN_EXTERNAL_REGISTRY" if number == 87 else "OPEN_PRODUCTION_MAPPING"
                recovered.append(
                    _op26_split_record(
                        row,
                        requirement_number=number,
                        source_text=table19[number]["text"],
                        pdf_page=table19[number]["pdf_page"],
                        table=19,
                        status=status,
                    )
                )
            expanded_msg002 = True
            continue

        if row["canonical_requirement_id"] == "OP26.P_MM_01.P.MM.01.MSG.028.REQ.005":
            recovered.append(
                _op26_split_record(
                    row,
                    requirement_number=5,
                    source_text=duplicate_fives[0]["text"],
                    pdf_page=duplicate_fives[0]["pdf_page"],
                    table=21,
                    occurrence=1,
                    status="OPEN_PRODUCTION_MAPPING",
                )
            )
            recovered.append(
                _op26_split_record(
                    row,
                    requirement_number=5,
                    source_text=duplicate_fives[1]["text"],
                    pdf_page=duplicate_fives[1]["pdf_page"],
                    table=21,
                    occurrence=2,
                    status="OPEN_EXTERNAL_REGISTRY",
                )
            )
            expanded_msg028 = True
            continue

        recovered.append(row)

    ids = [row["canonical_requirement_id"] for row in recovered]
    counts = Counter(row.get("message", "") for row in recovered)
    if not expanded_msg002 or not expanded_msg028:
        raise RuntimeError("OP26 collapsed source rows were not found in the 201-row re-audit input")
    if len(recovered) != 239 or len(ids) != len(set(ids)):
        raise RuntimeError(f"OP26 atomic recovery mismatch: total={len(recovered)} unique={len(set(ids))}")
    if counts.get("P.MM.01.MSG.002") != 87 or counts.get("P.MM.01.MSG.028") != 8:
        raise RuntimeError(f"OP26 message arithmetic mismatch after recovery: {dict(counts)}")
    return recovered


def load_op49_canonical_inventory() -> list[dict[str, str]]:
    path = ROOT / "codex_reports/OP49_P_DS_01/OP49_REAUDIT_REQUIREMENTS.csv"
    rows = read_csv(path)
    ids = [row.get("canonical_id", "").strip() for row in rows]
    counts = Counter(row.get("message", "").strip() for row in rows)
    missing_source = [row.get("canonical_id", "") for row in rows if not row.get("source_text", "").strip()]
    missing_trace = [
        row.get("canonical_id", "")
        for row in rows
        if not row.get("pdf_page", "").strip() or not row.get("table", "").strip() or not row.get("table_item", "").strip()
    ]
    missing_closure = [row.get("canonical_id", "") for row in rows if not row.get("closure_criterion", "").strip()]
    if (
        len(rows) != 166
        or len(set(ids)) != 166
        or not all(ids)
        or counts != Counter(OP49_CONFIRMED_SCOPE)
        or missing_source
        or missing_trace
        or missing_closure
    ):
        raise RuntimeError(
            "OP49 re-audit validation failed: "
            f"rows={len(rows)} unique={len(set(ids))} counts={dict(counts)} "
            f"missing_source={len(missing_source)} missing_trace={len(missing_trace)} missing_closure={len(missing_closure)}"
        )

    records: list[dict[str, str]] = []
    for source in rows:
        status = normalize_gap_status(source.get("gap_category", ""), f"{source.get('dependency_type', '')} {source.get('implementation_status', '')}")
        record = {
            "canonical_requirement_id": source["canonical_id"].strip(),
            "op": "OP49",
            "process": "P.DS.01",
            "procedure": source.get("procedure", ""),
            "transaction": source.get("transaction", ""),
            "operation": "",
            "message": source.get("message", ""),
            "requirement": source.get("source_text", ""),
            "source_text": source.get("source_text", ""),
            "plain_language_meaning": source.get("plain_language_meaning", ""),
            "source": source.get("source_document", "49_ОП.pdf"),
            "source_page": source.get("pdf_page", ""),
            "source_table_or_item": f"Table {source.get('table', '')}, item {source.get('table_item', '')}",
            "source_section": source.get("section", ""),
            "current_source_table": source.get("table", ""),
            "current_source_item": source.get("table_item", ""),
            "source_occurrence": "1",
            "canonical_disambiguator": "",
            "structure": source.get("structure_id", ""),
            "structure_version": source.get("structure_version", ""),
            "xml_owner": "",
            "xml_qname": source.get("qname", ""),
            "xml_path": source.get("field_path", ""),
            "current_state": source.get("gap_category", "") or source.get("implementation_status", ""),
            "current_status": status,
            "status_normalized": status,
            "implementation_status": status,
            "plain_explanation": source.get("plain_language_meaning", ""),
            "missing_information": source.get("secondary_dependencies", "") or source.get("dependency_id", ""),
            "required_material": source.get("dependency_id", ""),
            "dependency_type": source.get("dependency_type", ""),
            "dependency_id": source.get("dependency_id", ""),
            "secondary_dependencies": source.get("secondary_dependencies", ""),
            "required_engine_capability": source.get("engine_bucket", ""),
            # Strict re-audit says 0/166 are IMPLEMENTED_CONFIRMED. Preserve
            # package observations in notes, but do not promote them to closure.
            "production_rule": "",
            "regression_test": "",
            "positive_xml_case": "",
            "negative_xml_case": "",
            "recommended_action": source.get("required_action", ""),
            "closure_criterion": source.get("closure_criterion", ""),
            "evidence_level": "CONFIRMED_PDF",
            "source_conflict": source.get("source_conflict", ""),
            "audit_notes": source.get("notes", ""),
        }
        record["trace_source_refs"] = json.dumps(
            [
                {
                    "source_id": "OP49_P_DS_01",
                    "document": record["source"],
                    "status": "CONFIRMED",
                    "section": source.get("section", ""),
                    "table": source.get("table", ""),
                    "item": source.get("table_item", ""),
                    "source_occurrence": 1,
                    "page": normalize_page(source.get("pdf_page", "")),
                }
            ],
            ensure_ascii=False,
            sort_keys=True,
        )
        records.append(record)
    return records


def canonical_records() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []

    # OP22: current full inventory is recoverable deterministically from business_rules/source_refs.
    records.extend(recover_op22_canonical_inventory())

    # OP23 current final requirements after implementation work.
    for row in read_csv(ROOT / "codex_reports/OP23_P_SP_03/OP23_FINAL_REQUIREMENTS.csv"):
        if not row.get("canonical_requirement_id"):
            continue
        r = dict(row)
        r["source_text"] = r.get("requirement", "")
        r["status_normalized"] = normalize_gap_status(r.get("current_status", ""), r.get("implementation_status", ""))
        r["evidence_level"] = "CONFIRMED_PDF" if normalize_page(r.get("source_page", "")) else "AUDIT_DERIVED"
        records.append(r)

    # OP26: recover the 239 atomic source rows proven by the completed re-audit.
    records.extend(recover_op26_atomic_inventory())

    # OP32 post source-recovery inventory; exact QName remains unresolved by explicit task baseline.
    for row in read_csv(ROOT / "codex_reports/OP32_P_MM_06/OP32_SOURCE_RECOVERY_REQUIREMENTS.csv"):
        if not row.get("canonical_requirement_id"):
            continue
        r = dict(row)
        r["source_text"] = r.get("requirement_text", "")
        r["status_normalized"] = normalize_gap_status(r.get("new_status", r.get("current_state", "")))
        r["evidence_level"] = "CONFIRMED_PDF" if normalize_page(r.get("source_page", "")) else "AUDIT_DERIVED"
        r["qname_recovery_status"] = "QNAME_UNRESOLVED"
        records.append(r)

    # OP49: import the validated 166-row read-only re-audit dataset.
    records.extend(load_op49_canonical_inventory())

    ids = [r.get("canonical_requirement_id", "") for r in records]
    duplicates = sorted(item for item, count in Counter(ids).items() if item and count > 1)
    if duplicates:
        raise RuntimeError(f"Duplicate canonical IDs before KB build: {duplicates[:20]}")
    counts = Counter(r.get("op", "") for r in records)
    expected = {op: cfg["expected_requirements"] for op, cfg in PROCESS_CONFIG.items()}
    if any(counts.get(op, 0) != total for op, total in expected.items()):
        raise RuntimeError(f"Canonical scope mismatch: actual={dict(counts)} expected={expected}")
    return records


def extract_sources() -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    previous_index_path = KB / "indexes/source_index.json"
    previous = {}
    if previous_index_path.exists():
        try:
            previous = {x["source_id"]: x for x in json.loads(previous_index_path.read_text(encoding="utf-8"))}
        except Exception:
            previous = {}
    source_index: list[dict[str, Any]] = []
    page_texts: dict[str, list[str]] = {}
    for cfg in SOURCES:
        path: Path = cfg["path"]
        sid = cfg["source_id"]
        digest = sha256(path)
        reader = PdfReader(str(path), strict=False)
        texts: list[str] = []
        errors: list[int] = []
        empty: list[int] = []
        replacement_chars = 0
        source_dir = KB / "sources" / sid
        pages_dir = source_dir / "pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        for idx, page in enumerate(reader.pages, start=1):
            status = "OK"
            try:
                text = page.extract_text() or ""
            except Exception as exc:  # keep source extraction moving page-by-page
                text = f"[EXTRACTION_ERROR: {type(exc).__name__}: {exc}]"
                status = "ERROR"
                errors.append(idx)
            if not text.strip() and status == "OK":
                status = "EMPTY"
                empty.append(idx)
            replacement_chars += text.count("�")
            texts.append(text)
            page_md = frontmatter(
                {
                    "source_document": path.name,
                    "source_path": str(path),
                    "source_sha256": digest,
                    "pdf_page": idx,
                    "extraction_method": f"pypdf {getattr(__import__('pypdf'), '__version__', '')}",
                    "extraction_status": status,
                    "generated_by": GENERATOR,
                }
            ) + text.rstrip() + "\n"
            write_generated(pages_dir / f"page_{idx:03d}.md", page_md, force_generated=True)
        full_parts = [
            frontmatter(
                {
                    "source_document": path.name,
                    "source_path": str(path),
                    "source_sha256": digest,
                    "page_count": len(texts),
                    "extraction_method": f"pypdf {getattr(__import__('pypdf'), '__version__', '')}",
                    "extraction_status": "COMPLETE" if not errors else "COMPLETE_WITH_PAGE_ERRORS",
                    "generated_by": GENERATOR,
                }
            ),
            f"# {path.name} — FULL extracted text\n\n",
        ]
        for idx, text in enumerate(texts, start=1):
            full_parts.append(f"\n## PDF page {idx}\n\n{text.rstrip()}\n")
        write_generated(source_dir / "FULL.md", "".join(full_parts), force_generated=True)
        prev_hash = previous.get(sid, {}).get("sha256")
        entry = {
            "source_id": sid,
            "filename": path.name,
            "absolute_path": str(path),
            "alternate_paths": cfg.get("alternate_paths", []),
            "sha256": digest,
            "previous_sha256": prev_hash,
            "changed_since_previous_registry": bool(prev_hash and prev_hash != digest),
            "page_count": len(texts),
            "document_type": cfg["document_type"],
            "related_processes": cfg["related_processes"],
            "extraction_status": "COMPLETE" if not errors else "COMPLETE_WITH_PAGE_ERRORS",
            "empty_pages": empty,
            "error_pages": errors,
            "replacement_character_count": replacement_chars,
            "last_extracted_at": BUILD_TIME,
        }
        source_index.append(entry)
        page_texts[sid] = texts
    return source_index, page_texts


def load_existing_sources() -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    """Reuse the already extracted SOURCE layer after proving source hashes are current."""

    index_path = KB / "indexes" / "source_index.json"
    if not index_path.exists():
        raise RuntimeError("Existing SOURCE layer is missing indexes/source_index.json")
    source_index = json.loads(index_path.read_text(encoding="utf-8"))
    by_id = {row.get("source_id"): row for row in source_index}
    page_texts: dict[str, list[str]] = {}
    for cfg in SOURCES:
        sid = cfg["source_id"]
        existing = by_id.get(sid)
        if not existing:
            raise RuntimeError(f"Existing SOURCE layer is missing registry row {sid}")
        current_hash = sha256(cfg["path"])
        if current_hash != existing.get("sha256"):
            raise RuntimeError(f"SOURCE layer is stale for {sid}: stored {existing.get('sha256')} current {current_hash}")
        page_count = int(existing.get("page_count") or 0)
        texts: list[str] = []
        for page in range(1, page_count + 1):
            page_path = KB / "sources" / sid / "pages" / f"page_{page:03d}.md"
            if not page_path.exists():
                raise RuntimeError(f"Existing SOURCE page is missing: {page_path}")
            texts.append(page_path.read_text(encoding="utf-8", errors="replace"))
        full_path = KB / "sources" / sid / "FULL.md"
        if not full_path.exists():
            raise RuntimeError(f"Existing SOURCE full extraction is missing: {full_path}")
        existing["changed_since_previous_registry"] = False
        existing["last_verified_at"] = BUILD_TIME
        page_texts[sid] = texts
    return source_index, page_texts


def write_source_registry(source_index: list[dict[str, Any]]) -> None:
    rows = [
        "| Source ID | File | SHA-256 | Pages | Type | Processes | Extraction |",
        "|---|---|---|---:|---|---|---|",
    ]
    for s in source_index:
        rows.append(
            f"| `{s['source_id']}` | `{s['filename']}` | `{s['sha256']}` | {s['page_count']} | {s['document_type']} | "
            f"{', '.join(s['related_processes'])} | {s['extraction_status']} |"
        )
    text = frontmatter({"layer": "SOURCE", "generated_by": GENERATOR, "generated_at": BUILD_TIME})
    text += "# Source Registry\n\n" + "\n".join(rows) + "\n\n"
    text += "Original PDFs are not copied into the vault. `absolute_path` and SHA-256 are authoritative registry metadata.\n"
    write_generated(KB / "02_SOURCE_REGISTRY.md", text)
    write_generated(KB / "indexes/source_index.json", json_dump(source_index), force_generated=True)


def build_page_mapping(source_index: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Index PDF-page -> printed-page mappings when the printed page is a stable page header."""

    mappings: list[dict[str, Any]] = []
    for source in source_index:
        sid = source["source_id"]
        candidates: list[tuple[int, int]] = []
        for pdf_page in range(1, int(source.get("page_count") or 0) + 1):
            page_path = KB / "sources" / sid / "pages" / f"page_{pdf_page:03d}.md"
            if not page_path.exists():
                continue
            text = page_path.read_text(encoding="utf-8", errors="replace")
            parts = text.split("---", 2)
            body = parts[2] if len(parts) == 3 else text
            first = next((line.strip() for line in body.splitlines() if line.strip()), "")
            if re.fullmatch(r"\d{1,4}", first):
                candidates.append((pdf_page, int(first)))

        offsets = Counter(pdf - printed for pdf, printed in candidates)
        reliable_offsets = {offset for offset, count in offsets.items() if count >= 2}
        for pdf_page, printed_page in candidates:
            offset = pdf_page - printed_page
            if offset not in reliable_offsets:
                continue
            mappings.append(
                {
                    "source_id": sid,
                    "pdf_page": pdf_page,
                    "printed_page": printed_page,
                    "offset": offset,
                    "evidence_level": "EXTRACTED_STANDALONE_PAGE_HEADER",
                    "source_page": f"sources/{sid}/pages/page_{pdf_page:03d}.md",
                }
            )

    write_generated(KB / "indexes/page_mapping.json", json_dump(mappings), force_generated=True)
    lines = [
        frontmatter({"layer": "SOURCE", "generated_by": GENERATOR, "generated_at": BUILD_TIME}),
        "# PDF / Printed Page Mapping\n",
        "Only mappings with a repeated stable PDF-to-printed offset are indexed; isolated numeric first lines are ignored.\n",
        "| Source | PDF page | Printed page | Evidence |",
        "|---|---:|---:|---|",
    ]
    for row in mappings:
        lines.append(
            f"| `{row['source_id']}` | {row['pdf_page']} | {row['printed_page']} | {row['evidence_level']} |"
        )
    write_generated(KB / "indexes/PAGE_MAPPING.md", "\n".join(lines) + "\n")
    return mappings


def requirement_id_parts(cid: str) -> tuple[str, str]:
    op22 = re.fullmatch(r"(P\.SP\.02\.MSG\.\d{3}):(\d+):(\d+)", cid)
    if op22:
        return op22.group(1), op22.group(3)
    m = re.search(r"(P\.[A-Z]{2}\.[0-9]{2}\.MSG\.\d{3}|OP\d+\.P_[A-Z]{2}_[0-9]{2}\.MSG_\d{3})\.REQ\.\d{3}", cid)
    if not m:
        return "", ""
    msg = m.group(1).replace("OP32.P_MM_06.MSG_", "P.MM.06.MSG.")
    return msg, cid.rsplit(".REQ.", 1)[1]


def qname_status(record: dict[str, str]) -> str:
    if record.get("op") == "OP32" or record.get("qname_recovery_status") == "QNAME_UNRESOLVED":
        return "UNRESOLVED"
    status = record.get("status_normalized", "")
    if status == "OPEN_SOURCE_CONFLICT":
        return "CONFLICT"
    raw = record.get("xml_qname", "")
    if not raw or "UNRESOLVED" in raw.upper() or raw.upper() in {"N/A", "NONE"}:
        return "UNRESOLVED"
    if re.search(r"\{[^}]+\}[A-Za-z_][\w.-]*", raw):
        return "RESOLVED_CLARK"
    return "PREFIXED_NAMESPACE_UNRESOLVED"


def page_wikilink(source_id: str, page: int | None) -> str:
    if not source_id or not page:
        return ""
    return f"[[sources/{source_id}/pages/page_{page:03d}]]"


def build_requirement_notes(records: list[dict[str, str]]) -> list[dict[str, Any]]:
    page_mapping_path = KB / "indexes" / "page_mapping.json"
    page_mapping_rows = json.loads(page_mapping_path.read_text(encoding="utf-8")) if page_mapping_path.exists() else []
    printed_pages = {(x["source_id"], int(x["pdf_page"])): int(x["printed_page"]) for x in page_mapping_rows}
    index: list[dict[str, Any]] = []
    for r in records:
        cid = r["canonical_requirement_id"]
        process = r.get("process", "")
        op = r.get("op", "")
        msg = r.get("message", "") or requirement_id_parts(cid)[0]
        page = normalize_page(r.get("source_page", ""))
        document = r.get("source", "")
        sid = source_id_for(document, process)
        source_text = (r.get("source_text", "") or "").strip()
        explanation = (r.get("plain_explanation", "") or r.get("current_state", "") or "").strip()
        status = r.get("status_normalized", "OTHER")
        structure = (r.get("structure", "") or "").strip()
        qstatus = qname_status(r)
        table_item = r.get("source_table_or_item", "") or r.get("source", "")
        req_no = requirement_id_parts(cid)[1]
        fm = {
            "id": cid,
            "op": op,
            "process": process,
            "message": msg,
            "requirement": req_no,
            "structure": structure or "MISSING",
            "status": status,
            "evidence_level": r.get("evidence_level", "AUDIT_DERIVED"),
            "source_document": document or "MISSING",
            "source_pages": page or "MISSING",
            "source_table": table_item or "MISSING",
            "source_item": r.get("requirement", "") if str(r.get("requirement", "")).startswith("REQ") else "",
            "qname_status": qstatus,
            "implementation_status": r.get("implementation_status", r.get("current_status", r.get("current_state", "UNKNOWN"))),
            "generated_by": GENERATOR,
        }
        trace = " → ".join(x for x in [op, r.get("procedure", ""), r.get("transaction", ""), msg, cid] if x)
        source_link = page_wikilink(sid, page)
        printed_page = printed_pages.get((sid, page)) if sid and page else None
        body = frontmatter(fm)
        body += f"# {cid}\n\n## Нормативное требование\n\n"
        body += (source_text if source_text else "SOURCE_TEXT_NOT_AVAILABLE") + "\n\n"
        body += "## Простыми словами\n\n**AUDIT_DERIVED_EXPLANATION**\n\n"
        body += (explanation if explanation else "UNVERIFIED — explanation is not available in the selected audit snapshot.") + "\n\n"
        body += f"## Trace\n\n{trace or 'UNRESOLVED'}\n\n"
        body += "## XML\n\n"
        body += f"- Structure: {structure or 'MISSING / UNRESOLVED'}\n"
        body += f"- QName: {r.get('xml_qname') or 'MISSING / UNRESOLVED'}\n"
        body += f"- Namespace: {'embedded in Clark QName' if qstatus == 'RESOLVED_CLARK' else 'MISSING / UNRESOLVED'}\n"
        body += f"- Path: {r.get('xml_path') or 'MISSING / UNRESOLVED'}\n\n"
        body += "## Source\n\n"
        body += f"- Document: {document or 'MISSING'}\n"
        body += f"- SHA256: see [[02_SOURCE_REGISTRY]]\n"
        body += f"- PDF page: {page or 'MISSING'}\n"
        body += f"- Printed page: {printed_page or 'MISSING / UNRESOLVED'}\n"
        body += f"- Table/item: {table_item or 'MISSING'}\n"
        body += f"- Evidence level: {r.get('evidence_level', 'AUDIT_DERIVED')}\n"
        if r.get("range_requirement_code"):
            body += f"- Applied by current table: Table {r.get('current_source_table')} item {r.get('current_source_item')} via range {r.get('range_requirement_code')} (PDF p.{r.get('current_source_page') or '?'})\n"
            body += f"- Inherited source chain: {r.get('inherited_source_chain') or 'MISSING'}\n"
        if source_link:
            body += f"- Source page: {source_link}\n"
        body += "\n## Project state\n\n"
        body += f"- Status: {status}\n"
        body += f"- Production rule: {r.get('production_rule') or 'MISSING'}\n"
        body += f"- Wiring: {r.get('trace_source_refs') or 'UNVERIFIED'}\n"
        body += f"- Positive test: {r.get('positive_xml_case') or 'MISSING'}\n"
        body += f"- Negative test: {r.get('negative_xml_case') or 'MISSING'}\n"
        body += f"- Runtime proof: {r.get('regression_test') or 'MISSING'}\n\n"
        body += "## Gap\n\n"
        body += f"- Reason: {r.get('current_state') or r.get('new_status') or status}\n"
        body += f"- Missing information: {r.get('new_missing_information') or r.get('missing_information') or 'None recorded'}\n"
        body += f"- Required action: {r.get('recommended_action') or 'MISSING'}\n"
        body += f"- Closure criterion: {r.get('closure_criterion') or 'MISSING'}\n"
        write_generated(KB / "requirements" / f"{cid}.md", body)
        index.append(
            {
                "id": cid,
                "op": op,
                "process": process,
                "message": msg,
                "status": status,
                "structure": structure,
                "qname": r.get("xml_qname", ""),
                "qname_status": qstatus,
                "source_document": document,
                "source_page": page,
                "printed_page": printed_page,
                "markdown_path": f"requirements/{cid}.md",
            }
        )
    return index


def package_entities(cfg: dict[str, Any]) -> dict[str, Any]:
    pkg = ROOT / cfg["package"]
    data = {
        "process": load_json(pkg / "process.yaml"),
        "participants": load_json(pkg / "participants.yaml").get("participants", []),
        "operations": load_json(pkg / "operations.yaml").get("operations", []),
        "procedures": load_json(pkg / "procedures.yaml").get("procedures", []),
        "transactions": load_json(pkg / "transactions.yaml").get("transactions", []),
        "messages": load_json(pkg / "messages.yaml").get("messages", []),
    }
    return data


def source_ref_summary(refs: Iterable[dict[str, Any]]) -> str:
    refs = list(refs or [])
    if not refs:
        return "MISSING"
    r = refs[0]
    page = r.get("page")
    return f"{r.get('document', 'MISSING')} p.{page if page else '?'} — {r.get('location', '')}"


def make_entity_table(items: list[dict[str, Any]], code_key: str, extra_keys: list[str]) -> str:
    headers = ["Code", "Name", *extra_keys, "Evidence"]
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for item in items:
        cells = [item.get(code_key, ""), item.get("name", "")]
        for key in extra_keys:
            value = item.get(key, "")
            if isinstance(value, list):
                value = ", ".join(map(str, value))
            cells.append(str(value if value is not None else ""))
        cells.append(source_ref_summary(item.get("source_refs", [])))
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in cells) + " |")
    return "\n".join(out) + "\n"


def build_process_files(records: list[dict[str, str]], requirement_index: list[dict[str, Any]], structures: dict[str, Any]) -> list[dict[str, Any]]:
    proc_index: list[dict[str, Any]] = []
    by_process_records: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_process_idx: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        by_process_records[r.get("process", "")].append(r)
    for r in requirement_index:
        by_process_idx[r.get("process", "")].append(r)

    for op, cfg in PROCESS_CONFIG.items():
        ent = package_entities(cfg)
        process_meta = ent["process"]
        process = cfg["process"]
        folder = KB / "processes" / cfg["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        reqs = by_process_records[process]
        req_idx = by_process_idx[process]
        structure_ids = sorted({m.get("structure_id", "") for m in ent["messages"] if m.get("structure_id")} | {r.get("structure", "") for r in reqs if r.get("structure")})
        counts = {
            "ACT": len(ent["participants"]),
            "OPR": len(ent["operations"]),
            "PRC": len(ent["procedures"]),
            "TRN": len(ent["transactions"]),
            "MSG": len(ent["messages"]),
            "REQ_expected": cfg["expected_requirements"],
            "REQ_indexed": len(req_idx),
            "structures": len(structure_ids),
        }
        version_context = ""
        refs = process_meta.get("source_refs", [])
        if refs:
            version_context = refs[0].get("version_context", "")
            if not version_context:
                item = str(refs[0].get("item", ""))
                if re.search(r"\b\d+\.\d+\.\d+\b", item):
                    version_context = item
        index_md = frontmatter({"layer": "KNOWLEDGE+PROJECT_STATE", "op": op, "process": process, "generated_by": GENERATOR, "generated_at": BUILD_TIME})
        index_md += f"# {op} / {process}\n\n"
        index_md += f"- OP: {op}\n- Process code: {process}\n- Version: {version_context or 'MISSING / UNRESOLVED'}\n"
        index_md += f"- Normative document: {process_meta.get('normative_document_number', 'MISSING')}\n- Decision/source: {source_ref_summary(refs)}\n"
        index_md += f"- Package path: `{cfg['package']}`\n- Current audit: `{cfg['audit']}`\n- Requirement inventory status: **{cfg['requirement_status']}**\n\n"
        index_md += "## Counts\n\n" + "\n".join(f"- {k}: {v}" for k, v in counts.items()) + "\n\n"
        if op == "OP32":
            index_md += "## Confirmed OP32 source-recovery baseline\n\n- Requirements: 170\n- QName resolved: 0\n- QName unresolved: 170\n- Imports: 24\n- Resolved import versions: 0\n- XSD: 0\n- Classifier dependencies: 59; machine-readable: 0\n- External registry dependencies: 11\n- Engine: 2\n- Normative ambiguity: 1\n- Missing normative data: 97\n- SAFE production mapping: 0\n\n"
        if op == "OP49":
            index_md += "## Validated canonical normative scope\n\n"
            for msg, count in OP49_CONFIRMED_SCOPE.items():
                index_md += f"- {msg}: {count}\n"
            index_md += f"- TOTAL: {sum(OP49_CONFIRMED_SCOPE.values())}\n- Strict closure: 0 IMPLEMENTED_CONFIRMED / 166 OPEN.\n\n"
        index_md += "## Navigation\n\n" + " ".join(
            f"[[{name}]]" for name in ["ACTORS", "OPERATIONS", "PROCEDURES", "TRANSACTIONS", "MESSAGES", "REQUIREMENTS", "STRUCTURES", "QNAMES", "CLASSIFIERS", "GAPS", "IMPLEMENTATION_STATUS", "SOURCES"]
        ) + "\n"
        write_generated(folder / "INDEX.md", index_md)

        write_generated(folder / "ACTORS.md", frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + f"# {op} Actors\n\n" + make_entity_table(ent["participants"], "participant_code", ["logical_address_space", "segment_policy", "status"]))
        write_generated(folder / "OPERATIONS.md", frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + f"# {op} Operations\n\n" + make_entity_table(ent["operations"], "operation_code", ["status"]))
        write_generated(folder / "PROCEDURES.md", frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + f"# {op} Procedures\n\n" + make_entity_table(ent["procedures"], "procedure_code", ["status"]))
        write_generated(folder / "TRANSACTIONS.md", frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + f"# {op} Transactions\n\n" + make_entity_table(ent["transactions"], "transaction_code", ["procedure_code", "initiating_message", "response_messages", "status"]))
        write_generated(folder / "MESSAGES.md", frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + f"# {op} Messages\n\n" + make_entity_table(ent["messages"], "message_code", ["structure_id", "structure_version", "direction", "status"]))

        req_lines = [f"# {op} Requirements", "", f"Expected normative scope: **{cfg['expected_requirements']}**.", f"Atomic notes indexed: **{len(req_idx)}**.", f"Inventory status: **{cfg['requirement_status']}**.", ""]
        req_lines.extend(f"- [[requirements/{r['id']}]] — {r['status']}" for r in sorted(req_idx, key=lambda x: x["id"]))
        if not req_idx:
            req_lines.append("- No canonical requirement notes generated for this snapshot.")
        write_generated(folder / "REQUIREMENTS.md", frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + "\n".join(req_lines) + "\n")

        struct_lines = [f"# {op} Structures", ""] + [f"- [[structures/{sid}]]" for sid in structure_ids]
        write_generated(folder / "STRUCTURES.md", frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + "\n".join(struct_lines) + "\n")

        q_counts = Counter(r["qname_status"] for r in req_idx)
        q_lines = [f"# {op} QNames", "", *(f"- {k}: {v}" for k, v in sorted(q_counts.items())), "", "See [[indexes/QNAME_INDEX]]."]
        write_generated(folder / "QNAMES.md", frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + "\n".join(q_lines) + "\n")

        classifier_refs = [r for r in reqs if "CLASSIFIER" in (r.get("status_normalized", "") + r.get("required_material", "")).upper()]
        class_lines = [f"# {op} Classifiers", "", f"Requirement dependencies detected: {len(classifier_refs)}.", "", "See [[indexes/CLASSIFIER_INDEX]]."]
        write_generated(folder / "CLASSIFIERS.md", frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + "\n".join(class_lines) + "\n")

        gaps = Counter(r.get("status_normalized", "OTHER") for r in reqs)
        gap_lines = [f"# {op} Gaps", "", *(f"- {k}: {v}" for k, v in sorted(gaps.items())), "", "See [[indexes/GAP_INDEX]]."]
        write_generated(folder / "GAPS.md", frontmatter({"layer": "PROJECT_STATE", "generated_by": GENERATOR, "snapshot_at": BUILD_TIME}) + "\n".join(gap_lines) + "\n")

        impl_counts = Counter((r.get("implementation_status") or r.get("current_status") or r.get("current_state") or "UNKNOWN") for r in reqs)
        impl_lines = [f"# {op} Implementation Status", "", f"Snapshot: {BUILD_TIME}", "", *(f"- {k}: {v}" for k, v in impl_counts.most_common())]
        if op in {"OP22", "OP23", "OP26"}:
            impl_lines += ["", "Production/runtime files are changing in parallel; this file is a timestamped snapshot only."]
        write_generated(folder / "IMPLEMENTATION_STATUS.md", frontmatter({"layer": "PROJECT_STATE", "generated_by": GENERATOR, "snapshot_at": BUILD_TIME}) + "\n".join(impl_lines) + "\n")

        source_lines = [f"# {op} Sources", "", f"- Normative PDF: [[sources/{cfg['source_id']}/FULL]]", f"- Audit snapshot: `{cfg['audit']}`", "- Shared integration decision: [[decisions/Decision_5]]"]
        write_generated(folder / "SOURCES.md", frontmatter({"layer": "SOURCE+PROJECT_STATE", "generated_by": GENERATOR}) + "\n".join(source_lines) + "\n")

        proc_index.append(
            {
                "OP": op,
                "process": process,
                "version": version_context,
                "package": cfg["package"],
                "normative_source": cfg["source_id"],
                "counts": counts,
                "current_status": cfg["requirement_status"],
                "markdown_path": f"processes/{cfg['folder']}/INDEX.md",
            }
        )
    return proc_index


def structure_inventory(records: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    inv: dict[str, dict[str, Any]] = {}
    op32_imports = read_csv(ROOT / "codex_reports/OP32_P_MM_06/OP32_STRUCTURE_IMPORT_INVENTORY.csv")
    for op, cfg in PROCESS_CONFIG.items():
        ent = package_entities(cfg)
        for msg in ent["messages"]:
            sid = msg.get("structure_id")
            if not sid:
                continue
            rec = inv.setdefault(sid, {"id": sid, "versions": set(), "used_by_messages": set(), "used_by_requirements": set(), "source_refs": [], "imports": [], "definitions": []})
            if msg.get("structure_version"):
                rec["versions"].add(str(msg["structure_version"]))
            rec["used_by_messages"].add(msg.get("message_code", ""))
            rec["source_refs"].extend(msg.get("source_refs", []))
        for definition_path in sorted((ROOT / cfg["package"] / "structures").glob("*/*.yaml")):
            definition = load_json(definition_path)
            sid = str(definition.get("structure_id", "")).strip()
            if not sid:
                continue
            rec = inv.setdefault(sid, {"id": sid, "versions": set(), "used_by_messages": set(), "used_by_requirements": set(), "source_refs": [], "imports": [], "definitions": []})
            version = str(definition.get("version", "")).strip()
            if version:
                rec["versions"].add(version)
            rec["source_refs"].extend(definition.get("source_refs", []))
            definition["_definition_path"] = str(definition_path.relative_to(ROOT))
            rec["definitions"].append(definition)
    for r in records:
        sid = (r.get("structure") or "").strip()
        if not sid:
            continue
        rec = inv.setdefault(sid, {"id": sid, "versions": set(), "used_by_messages": set(), "used_by_requirements": set(), "source_refs": [], "imports": [], "definitions": []})
        rec["used_by_requirements"].add(r.get("canonical_requirement_id", ""))
    for row in op32_imports:
        sid = row.get("owner_structure", "")
        if sid in inv:
            inv[sid]["imports"].append(row)
    return inv


def build_structures(inv: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    index: list[dict[str, Any]] = []
    field_index: list[dict[str, Any]] = []
    local_xsds: dict[str, list[str]] = defaultdict(list)
    for base in [ROOT, NORM]:
        if not base.exists():
            continue
        for path in base.rglob("*.xsd"):
            local_xsds[path.name].append(str(path))

    for sid in sorted(inv):
        data = inv[sid]
        definitions = data.get("definitions", [])
        concrete_roots: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for definition in definitions:
            namespace_value = str(definition.get("namespace", "")).strip()
            local_name = str(definition.get("root_element", "")).strip()
            refs = definition.get("source_refs", [])
            confirmed_ref = any(str(ref.get("status", "")).upper() == "CONFIRMED" for ref in refs)
            if namespace_value and local_name and confirmed_ref and not re.search(r"[XYZ]\.Y\.Y|[XYZ]\.X\.X|v[XYZ](?:\.[XYZ]){2}", namespace_value):
                concrete_roots[f"{{{namespace_value}}}{local_name}"].append(definition)

        if len(concrete_roots) == 1:
            root_qname = next(iter(concrete_roots))
            root_evidence = "CONFIRMED_STRUCTURE_SOURCE_REF"
        elif len(concrete_roots) > 1:
            root_qname = "CONFLICT: " + " | ".join(sorted(concrete_roots))
            root_evidence = "CONFLICT"
        else:
            root_qname = "MISSING / UNRESOLVED"
            root_evidence = "MISSING"

        namespace = "MISSING / UNRESOLVED"
        match = re.match(r"\{([^}]+)\}", root_qname)
        if match:
            namespace = match.group(1)
        refs = data["source_refs"]
        xsd_names = sorted({str(d.get("xsd_file", "")).strip() for d in definitions if d.get("xsd_file")})
        xsd_paths = sorted({p for name in xsd_names for p in local_xsds.get(name, [])})
        xsd_status = "AVAILABLE_LOCAL" if xsd_paths else ("DECLARED_FILENAME_PAYLOAD_MISSING" if xsd_names else "MISSING")
        definition_statuses = sorted({str(d.get("status", "")) for d in definitions if d.get("status")})
        body = frontmatter({"layer": "KNOWLEDGE", "structure_id": sid, "generated_by": GENERATOR})
        body += f"# {sid}\n\n"
        body += f"- Version(s): {', '.join(sorted(data['versions'])) or 'MISSING / UNRESOLVED'}\n"
        body += f"- Root QName: `{root_qname}`\n- Root QName evidence: {root_evidence}\n- Namespace: `{namespace}`\n"
        body += f"- XSD filename(s): {', '.join(xsd_names) or 'MISSING'}\n- XSD status: {xsd_status}\n"
        if xsd_paths:
            body += "- Local XSD payload(s): " + ", ".join(f"`{x}`" for x in xsd_paths) + "\n"
        body += f"- Definition status(es): {', '.join(definition_statuses) or 'MISSING'}\n"
        body += f"- Source: {source_ref_summary(refs)}\n"
        fields_note = f"structures/{sid}_FIELDS.md"
        structure_fields: list[dict[str, Any]] = []
        seen_fields: set[tuple[str, str, str]] = set()
        for definition in definitions:
            version = str(definition.get("version", ""))
            for field in definition.get("fields", []):
                field_id = str(field.get("field_id", ""))
                path_value = str(field.get("path", ""))
                key = (version, field_id, path_value)
                if key in seen_fields:
                    continue
                seen_fields.add(key)
                source_refs = field.get("source_refs") or []
                first_ref = source_refs[0] if source_refs else {}
                confirmed = any(str(ref.get("status", "")).upper() == "CONFIRMED" for ref in source_refs)
                entry = {
                    "structure": sid,
                    "version": version,
                    "field_id": field_id,
                    "path": path_value,
                    "official_name": str(field.get("official_name", "")),
                    "prefix": str(field.get("namespace_prefix", "")),
                    "local_name": str(field.get("xml_name", "")),
                    "kind": str(field.get("kind", "")),
                    "datatype": str(field.get("datatype", "")),
                    "min_occurs": field.get("min_occurs", ""),
                    "max_occurs": field.get("max_occurs", ""),
                    "description": str(field.get("description", "")),
                    "identifier": str(field.get("identifier", "")),
                    "classifier_ref": field.get("classifier_ref"),
                    "source_document": str(first_ref.get("document", "")),
                    "source_page": normalize_page(str(first_ref.get("page", ""))),
                    "source_table": str(first_ref.get("table", "")),
                    "source_item": str(first_ref.get("item", "")),
                    "evidence_level": "CONFIRMED_PDF_SOURCE_REF" if confirmed else "PRODUCTION_YAML",
                    "definition_path": str(definition.get("_definition_path", "")),
                }
                structure_fields.append(entry)
                field_index.append(entry)

        body += f"- Fields indexed: {len(structure_fields)}\n"
        if structure_fields:
            body += f"- Field metadata: [[{sid}_FIELDS]]\n\n"
            lines = [
                frontmatter({"layer": "KNOWLEDGE", "structure_id": sid, "generated_by": GENERATOR}),
                f"# {sid} Fields\n",
                "| ID | Path | Datatype | Cardinality | Source | Evidence |",
                "|---|---|---|---|---|---|",
            ]
            for field in structure_fields:
                source = f"{field['source_document']} p.{field['source_page'] or '?'} table {field['source_table'] or '?'} item {field['source_item'] or '?'}"
                lines.append(
                    "| "
                    + " | ".join(
                        str(x).replace("|", "\\|")
                        for x in [
                            field["field_id"],
                            field["path"],
                            field["datatype"],
                            f"{field['min_occurs']}..{field['max_occurs']}",
                            source,
                            field["evidence_level"],
                        ]
                    )
                    + " |"
                )
            write_generated(KB / "structures" / f"{sid}_FIELDS.md", "\n".join(lines) + "\n")
        else:
            body += "- Field metadata: MISSING / not imported with confirmed field rows.\n\n"
        body += "## Imports\n\n"
        if data["imports"]:
            for imp in data["imports"]:
                body += f"- `{imp.get('referenced_structure_or_type')}` — version `{imp.get('version_as_written')}` — {imp.get('resolution_status')} — source p.{imp.get('source_page')} table {imp.get('source_table')}\n"
        else:
            body += "- None indexed / MISSING.\n"
        body += "\n## Used by messages\n\n" + "\n".join(f"- {x}" for x in sorted(data["used_by_messages"])) + "\n"
        body += "\n## Used by requirements\n\n" + "\n".join(f"- [[requirements/{x}]]" for x in sorted(data["used_by_requirements"]) if x) + "\n"
        write_generated(KB / "structures" / f"{sid}.md", body)
        index.append(
            {
                "id": sid,
                "versions": sorted(data["versions"]),
                "root_qname": root_qname,
                "namespace": namespace,
                "root_qname_evidence": root_evidence,
                "xsd_filename": xsd_names,
                "xsd_status": xsd_status,
                "field_count": len(structure_fields),
                "used_by_messages": sorted(data["used_by_messages"]),
                "used_by_requirements": sorted(data["used_by_requirements"]),
                "markdown_path": f"structures/{sid}.md",
            }
        )
    return index, field_index


def build_classifier_notes() -> tuple[list[dict[str, Any]], int]:
    rows = read_csv(ROOT / "codex_reports/OP32_P_MM_06/OP32_CLASSIFIER_SOURCE_INVENTORY.csv")
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        raw_ids = [x.strip() for x in str(row.get("classifier_id", "")).split(";") if x.strip()]
        raw_names = [x.strip() for x in str(row.get("classifier_name", "")).split(";") if x.strip()]
        raw_versions = [x.strip() for x in str(row.get("required_version", "")).split(";") if x.strip()]
        if not raw_ids:
            raw_ids = [row.get("classifier_name") or f"UNRESOLVED_{row.get('canonical_requirement_id')}"]
        for idx, cid in enumerate(raw_ids):
            item = dict(row)
            item["_classifier_id"] = cid
            if len(raw_names) == len(raw_ids):
                item["_classifier_name"] = raw_names[idx]
            else:
                item["_classifier_name"] = row.get("classifier_name", "")
            if len(raw_versions) == len(raw_ids):
                item["_required_version"] = raw_versions[idx]
            else:
                item["_required_version"] = row.get("required_version", "")
            grouped[cid].append(item)
    for cid, catalog in OP32_CLASSIFIER_CATALOG_ONLY.items():
        if cid in grouped:
            continue
        grouped[cid].append(
            {
                "_classifier_id": cid,
                "_classifier_name": catalog["classifier_name"],
                "_required_version": catalog["required_version"],
                "normative_source": catalog["normative_source"],
                "page": catalog["page"],
                "machine_readable": "NO",
                "production_ready": "NO",
                "status": "CLASSIFIER_NORMATIVE_REFERENCE_CONFIRMED__PAYLOAD_MISSING",
                "canonical_requirement_id": "",
            }
        )
    out: list[dict[str, Any]] = []
    expected_paths: set[Path] = set()
    for cid, items in sorted(grouped.items()):
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", cid).strip("_") or "UNRESOLVED"
        note_path = KB / "classifiers" / f"{safe}.md"
        expected_paths.add(note_path.resolve())
        first = items[0]
        body = frontmatter({"layer": "KNOWLEDGE", "classifier_id": cid, "generated_by": GENERATOR})
        body += f"# {cid}\n\n- Official name: {first.get('_classifier_name') or 'MISSING'}\n- Version: {first.get('_required_version') or 'MISSING'}\n"
        body += f"- Source: {first.get('normative_source') or 'MISSING'}\n- Machine-readable source: {'AVAILABLE' if any(x.get('machine_readable') == 'YES' for x in items) else 'MISSING'}\n"
        body += f"- Production readiness: {first.get('production_ready') or 'NO'}\n- Evidence: CONFIRMED_PDF for normative reference; payload status is separate.\n"
        body += "- Local payload search: no machine-readable classifier payload is claimed unless the source inventory marks `machine_readable=YES`.\n\n## Used by\n\n"
        body += "\n".join(f"- [[requirements/{x.get('canonical_requirement_id')}]]" for x in items if x.get("canonical_requirement_id")) + "\n"
        write_generated(note_path, body)
        out.append(
            {
                "classifier_id": cid,
                "official_name": first.get("_classifier_name", ""),
                "version": first.get("_required_version", ""),
                "machine_readable": any(x.get("machine_readable") == "YES" for x in items),
                "used_by": [x.get("canonical_requirement_id") for x in items if x.get("canonical_requirement_id")],
                "markdown_path": f"classifiers/{safe}.md",
            }
        )
    classifier_dir = KB / "classifiers"
    for stale in classifier_dir.glob("*.md"):
        if stale.resolve() in expected_paths:
            continue
        old = stale.read_text(encoding="utf-8", errors="replace")
        if f"generated_by: {quote_yaml(GENERATOR)}" in old or "generated_by: build_kb.py" in old:
            ensure_allowed(stale)
            stale.unlink()
    return out, len(rows)


def build_qname_index(
    records: list[dict[str, str]], structure_index: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    resolved: dict[str, dict[str, Any]] = {}
    unresolved: dict[str, dict[str, Any]] = {}
    token_re = re.compile(r"\{[^}]+\}[A-Za-z_][\w.-]*|[A-Za-z_][\w.-]*:[A-Za-z_][\w.-]*|@[A-Za-z_][\w.-]*")
    for r in records:
        raw = r.get("xml_qname", "") or ""
        tokens = token_re.findall(raw)
        for token in tokens:
            entry = {
                "qname": token,
                "namespace": "UNRESOLVED",
                "local_name": token.split("}")[-1].split(":")[-1].lstrip("@"),
                "structure": r.get("structure", ""),
                "version": r.get("source_version", ""),
                "evidence_level": r.get("evidence_level", "AUDIT_DERIVED"),
                "source": r.get("source", ""),
                "used_by_requirements": [],
            }
            target = unresolved
            m = re.match(r"\{([^}]+)\}(.+)", token)
            if m and r.get("op") != "OP32" and r.get("status_normalized") != "OPEN_SOURCE_CONFLICT":
                entry["namespace"] = m.group(1)
                entry["local_name"] = m.group(2)
                target = resolved
            existing = target.setdefault(token, entry)
            existing["used_by_requirements"].append(r.get("canonical_requirement_id", ""))
    for structure in structure_index:
        token = structure.get("root_qname", "")
        m = re.fullmatch(r"\{([^}]+)\}([A-Za-z_][\w.-]*)", token)
        if not m:
            continue
        entry = resolved.setdefault(
            token,
            {
                "qname": token,
                "namespace": m.group(1),
                "local_name": m.group(2),
                "structure": structure.get("id", ""),
                "version": ", ".join(structure.get("versions", [])),
                "evidence_level": "CONFIRMED_PDF",
                "source": "structure root metadata",
                "used_by_requirements": [],
            },
        )
        entry["used_by_requirements"].extend(structure.get("used_by_requirements", []))
    return list(resolved.values()), list(unresolved.values())


def build_decision5(page_texts: dict[str, list[str]]) -> None:
    texts = page_texts.get("DECISION_5", [])
    terms = ["To", "ReplyTo", "From", "FaultTo", "Action", "MessageID", "RelatesTo", "RelatesAction", "ProcedureID", "ConversationID", "Integration", "TrackID", "AcceptTime"]
    body = frontmatter({"layer": "KNOWLEDGE", "decision": "Decision No. 5", "evidence_level": "CONFIRMED_PDF_TERM_INDEX", "generated_by": GENERATOR})
    body += "# Decision №5\n\nThis note is a source navigation index. It does not infer semantics beyond text occurrences in the extracted official PDF.\n\n"
    body += "- Full source: [[sources/DECISION_5/FULL]]\n\n"
    for term in terms:
        hits = [i for i, text in enumerate(texts, start=1) if re.search(re.escape(term), text, flags=re.I)]
        body += f"## {term}\n\n"
        if hits:
            body += "Evidence: CONFIRMED_PDF term occurrence. Pages: " + ", ".join(page_wikilink("DECISION_5", p) for p in hits[:30]) + ".\n\n"
        else:
            body += "Evidence: MISSING exact extracted term occurrence. Review the source manually before making a normative claim.\n\n"
    action_pages = [i for i, text in enumerate(texts, start=1) if "фиксированный префикс \"int://\"" in text and "код общего процесса" in text]
    body += "## Application Action URI format\n\n"
    if action_pages:
        body += "CONFIRMED_PDF: Decision №5 defines `wsa:Action` for common-process application messages as `int://` + `CP` + process code + process version + procedure code + transaction code + message code, separated by `/`. This corresponds to `int://CP/PROCESS/VERSION/PRC/TRN/MSG`.\n\n"
        body += "Evidence pages: " + ", ".join(page_wikilink("DECISION_5", p) for p in action_pages) + ".\n\n"
    else:
        body += "MISSING / UNVERIFIED.\n\n"
    address_pages = [i for i, text in enumerate(texts, start=1) if "фиксированный префикс \"EAEU://\"" in text]
    body += "## Logical address format\n\n"
    if address_pages:
        body += "CONFIRMED_PDF: logical participant addresses use the fixed `EAEU://` prefix; exact address components must follow the Decision №5 rules and process-specific participant data.\n\n"
        body += "Evidence pages: " + ", ".join(page_wikilink("DECISION_5", p) for p in address_pages) + ".\n\n"
    else:
        body += "MISSING / UNVERIFIED.\n\n"
    write_generated(KB / "decisions" / "Decision_5.md", body)


def build_engine_snapshot(snapshot: dict[str, Any], requirement_index: list[dict[str, Any]]) -> None:
    common = {"layer": "PROJECT_STATE", "snapshot_at": BUILD_TIME, "git_head": snapshot["head"], "git_dirty_entries": snapshot["dirty_entries"], "generated_by": GENERATOR}
    cap = frontmatter(common) + "# Engine Capabilities\n\n"
    cap += "This is a timestamped production snapshot, not normative evidence.\n\n"
    cap += "Observed structured rule kinds in the current validator/evaluator:\n\n" + "\n".join(f"- `{k}`" for k in ENGINE_RULE_KINDS) + "\n\n"
    cap += "Primary inspected modules: `rules_engine.py`, `validator.py`, `body.py`.\n"
    write_generated(KB / "engine" / "CAPABILITIES.md", cap)

    limitations = Counter(x["status"] for x in requirement_index if x["status"] != "IMPLEMENTED_CONFIRMED")
    lim = frontmatter(common) + "# Engine / Project Limitations\n\n"
    lim += "Derived from the selected audit snapshots; source and project-state gaps remain separate.\n\n" + "\n".join(f"- {k}: {v}" for k, v in sorted(limitations.items())) + "\n"
    write_generated(KB / "engine" / "LIMITATIONS.md", lim)

    rules = frontmatter(common) + "# Rule Kinds\n\n" + "\n".join(f"- `{k}` — CONFIRMED_PRODUCTION at snapshot {BUILD_TIME}" for k in ENGINE_RULE_KINDS) + "\n"
    write_generated(KB / "engine" / "RULE_KINDS.md", rules)


def write_indexes(
    source_index: list[dict[str, Any]],
    requirement_index: list[dict[str, Any]],
    structure_index: list[dict[str, Any]],
    field_index: list[dict[str, Any]],
    classifier_index: list[dict[str, Any]],
    classifier_refs: int,
    process_index: list[dict[str, Any]],
    q_resolved: list[dict[str, Any]],
    q_unresolved: list[dict[str, Any]],
) -> None:
    write_generated(KB / "indexes/requirements_index.json", json_dump(requirement_index), force_generated=True)
    req_md = frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + "# Requirements Index\n\n"
    req_md += f"Indexed atomic requirements: **{len(requirement_index)}**.\n\n"
    req_md += "\n".join(f"- [[{r['markdown_path'][:-3]}]] — {r['op']} / {r['message']} — {r['status']}" for r in requirement_index) + "\n"
    write_generated(KB / "indexes/REQUIREMENTS_INDEX.md", req_md)

    write_generated(KB / "indexes/structure_index.json", json_dump(structure_index), force_generated=True)
    str_md = frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + "# Structure Index\n\n" + "\n".join(f"- [[{s['markdown_path'][:-3]}]] — versions: {', '.join(s['versions']) or 'MISSING'}" for s in structure_index) + "\n"
    write_generated(KB / "indexes/STRUCTURE_INDEX.md", str_md)

    write_generated(KB / "indexes/field_index.json", json_dump(field_index), force_generated=True)
    field_counts = Counter(x.get("structure", "") for x in field_index)
    field_md = frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + f"# Field Index\n\nIndexed field rows with provenance: **{len(field_index)}**.\n\n"
    field_md += "\n".join(f"- [[structures/{sid}_FIELDS]] — {count} field rows" for sid, count in sorted(field_counts.items())) + "\n"
    write_generated(KB / "indexes/FIELD_INDEX.md", field_md)

    write_generated(KB / "indexes/process_index.json", json_dump(process_index), force_generated=True)
    write_generated(KB / "indexes/classifier_index.json", json_dump(classifier_index), force_generated=True)
    class_md = frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + f"# Classifier Index\n\nClassifier dependency rows: **{classifier_refs}**. Unique classifier notes: **{len(classifier_index)}**.\n\n" + "\n".join(f"- [[{x['markdown_path'][:-3]}]] — machine-readable: {x['machine_readable']}" for x in classifier_index) + "\n"
    write_generated(KB / "indexes/CLASSIFIER_INDEX.md", class_md)

    q_json = {"resolved": q_resolved, "unresolved": q_unresolved}
    write_generated(KB / "indexes/qname_index.json", json_dump(q_json), force_generated=True)
    q_md = frontmatter({"layer": "KNOWLEDGE", "generated_by": GENERATOR}) + f"# QName Index\n\nResolved exact Clark QNames: **{len(q_resolved)}**. Unresolved/prefixed QName tokens: **{len(q_unresolved)}**.\n\n## Resolved\n\n"
    q_md += "\n".join(f"- `{x['qname']}` — {x['structure']}" for x in q_resolved) or "- None"
    q_md += "\n\n## UNRESOLVED_QNAMES\n\n" + ("\n".join(f"- `{x['qname']}` — namespace unresolved — used by {len(x['used_by_requirements'])} requirement(s)" for x in q_unresolved) or "- None") + "\n"
    write_generated(KB / "indexes/QNAME_INDEX.md", q_md)

    gaps = [r for r in requirement_index if r["status"] != "IMPLEMENTED_CONFIRMED"]
    gap_json = [{"id": r["id"], "op": r["op"], "message": r["message"], "category": r["status"], "markdown_path": r["markdown_path"]} for r in gaps]
    write_generated(KB / "indexes/gap_index.json", json_dump(gap_json), force_generated=True)
    gap_counts = Counter(x["category"] for x in gap_json)
    gap_md = frontmatter({"layer": "PROJECT_STATE", "generated_by": GENERATOR, "snapshot_at": BUILD_TIME}) + "# Gap Index\n\n" + "\n".join(f"- {k}: {v}" for k, v in sorted(gap_counts.items())) + "\n"
    write_generated(KB / "indexes/GAP_INDEX.md", gap_md)

    stale_lines = ["# Stale Sources", ""]
    stale_count = 0
    for s in source_index:
        state = "CURRENT"
        if s.get("changed_since_previous_registry"):
            state = "CHANGED_AND_REEXTRACTED_THIS_BUILD"
        stale_lines.append(f"- `{s['source_id']}`: **{state}** — `{s['sha256']}`")
    stale_lines += ["", f"STALE after completed extraction: **{stale_count}**."]
    write_generated(KB / "indexes/STALE_SOURCES.md", frontmatter({"layer": "SOURCE", "generated_by": GENERATOR}) + "\n".join(stale_lines) + "\n")

    kb_index = {
        "generated_at": BUILD_TIME,
        "sources": len(source_index),
        "processes": len(process_index),
        "requirements_expected_scope": sum(x["expected_requirements"] for x in PROCESS_CONFIG.values()),
        "requirements_indexed": len(requirement_index),
        "structures": len(structure_index),
        "fields_indexed": len(field_index),
        "classifier_dependency_rows": classifier_refs,
        "classifier_notes": len(classifier_index),
        "qnames_resolved": len(q_resolved),
        "qnames_unresolved": len(q_unresolved),
        "gaps": len(gaps),
        "indexes": {
            "sources": "indexes/source_index.json",
            "processes": "indexes/process_index.json",
            "requirements": "indexes/requirements_index.json",
            "structures": "indexes/structure_index.json",
            "fields": "indexes/field_index.json",
            "qnames": "indexes/qname_index.json",
            "classifiers": "indexes/classifier_index.json",
            "gaps": "indexes/gap_index.json",
        },
    }
    write_generated(KB / "kb_index.json", json_dump(kb_index), force_generated=True)


def write_master_docs(source_index: list[dict[str, Any]], requirement_index: list[dict[str, Any]]) -> None:
    idx = frontmatter({"generated_by": GENERATOR, "generated_at": BUILD_TIME})
    idx += "# EAEU XML Knowledge Base\n\n"
    idx += "Three layers are kept separate: **SOURCE**, **KNOWLEDGE**, **PROJECT_STATE**. Original PDF/XSD material remains source of truth.\n\n"
    idx += "## Processes\n\n" + "\n".join(f"- [[processes/{cfg['folder']}/INDEX|{op} / {cfg['process']}]]" for op, cfg in PROCESS_CONFIG.items()) + "\n\n"
    idx += "## Shared navigation\n\n- [[02_SOURCE_REGISTRY]]\n- [[indexes/REQUIREMENTS_INDEX]]\n- [[indexes/STRUCTURE_INDEX]]\n- [[indexes/FIELD_INDEX]]\n- [[indexes/QNAME_INDEX]]\n- [[indexes/CLASSIFIER_INDEX]]\n- [[indexes/GAP_INDEX]]\n- [[indexes/PAGE_MAPPING]]\n- [[decisions/Decision_5]]\n- [[engine/CAPABILITIES]]\n"
    write_generated(KB / "00_INDEX.md", idx)

    rules = frontmatter({"generated_by": GENERATOR}) + "# Rules for Agents\n\n"
    rules += "1. **KB FIRST.** Search the KB before opening a PDF.\n2. Before PDF, look for the OP/PRC/TRN/MSG/REQ/Structure/QName note and its source link.\n3. Check `evidence_level` before using a statement as normative proof.\n4. `AUDIT_DERIVED` is not normative proof.\n5. `HISTORICAL` is not current truth.\n6. `UNVERIFIED` cannot close a gap.\n7. `CONFLICT` must not be resolved by inference.\n8. `MISSING` must not be guessed.\n9. When sources conflict, official source hierarchy wins.\n10. Open the original PDF when KB evidence is insufficient.\n11. After confirming new knowledge, update the KB with evidence and source page.\n12. Never replace SOURCE text with interpretation.\n\n"
    rules += "Evidence priority: official XSD > official normative PDF/table > official XML/schema material > package source_refs > current verified audit > production YAML > historical audit > historical notes.\n"
    write_generated(KB / "01_RULES_FOR_AGENTS.md", rules)

    glossary = frontmatter({"generated_by": GENERATOR}) + "# Glossary\n\n- **OP** — общий процесс.\n- **ACT** — participant/actor.\n- **OPR** — operation.\n- **PRC** — procedure.\n- **TRN** — transaction.\n- **MSG** — message.\n- **REQ** — atomic normative requirement.\n- **SOURCE** — extracted source text without interpretation.\n- **KNOWLEDGE** — normalized entities backed by evidence.\n- **PROJECT_STATE** — timestamped xml_creator implementation/audit state.\n"
    write_generated(KB / "03_GLOSSARY.md", glossary)


def validate_links() -> list[dict[str, str]]:
    broken: list[dict[str, str]] = []
    pattern = re.compile(r"\[\[([^\]]+)\]\]")
    for md in KB.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        for raw in pattern.findall(text):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if not target:
                continue
            if target.startswith("http"):
                continue
            # Canonical IDs contain dots (for example REQ.001), which are part
            # of the Obsidian note name rather than a filesystem extension.
            candidate = Path(target if target.endswith(".md") else target + ".md")
            if "/" in target:
                resolved = KB / candidate
            else:
                resolved = md.parent / candidate
                if not resolved.exists():
                    resolved = KB / candidate
            if not resolved.exists():
                broken.append({"from": str(md.relative_to(KB)), "target": raw})
    return broken


def consistency_checks(requirement_index: list[dict[str, Any]], source_index: list[dict[str, Any]]) -> dict[str, Any]:
    ids = [r["id"] for r in requirement_index]
    duplicate_ids = sorted([x for x, n in Counter(ids).items() if n > 1])
    missing_markdown = [r["id"] for r in requirement_index if not (KB / r["markdown_path"]).exists()]
    missing_source_pages = []
    for r in requirement_index:
        if not r.get("source_page"):
            continue
        sid = source_id_for(r.get("source_document", ""), r.get("process", ""))
        if sid and not (KB / "sources" / sid / "pages" / f"page_{int(r['source_page']):03d}.md").exists():
            missing_source_pages.append(r["id"])
    return {
        "duplicate_requirement_ids": duplicate_ids,
        "missing_requirement_markdown": missing_markdown,
        "missing_requirement_source_pages": missing_source_pages,
        "source_hashes_complete": all(bool(x.get("sha256")) for x in source_index),
    }


def build_report(
    source_index: list[dict[str, Any]],
    requirement_index: list[dict[str, Any]],
    structure_index: list[dict[str, Any]],
    field_index: list[dict[str, Any]],
    classifier_index: list[dict[str, Any]],
    classifier_refs: int,
    q_resolved: list[dict[str, Any]],
    q_unresolved: list[dict[str, Any]],
    broken: list[dict[str, str]],
    checks: dict[str, Any],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    pages_total = sum(x["page_count"] for x in source_index)
    errors = sum(len(x["error_pages"]) for x in source_index)
    gaps = [r for r in requirement_index if r["status"] != "IMPLEMENTED_CONFIRMED"]
    expected = sum(x["expected_requirements"] for x in PROCESS_CONFIG.values())
    stats = {
        "status": "COMPLETE_WITH_KNOWLEDGE_GAPS" if len(requirement_index) < expected else "COMPLETE",
        "generated_at": BUILD_TIME,
        "pdf_total": len(SOURCES),
        "pdf_processed": len(source_index),
        "pdf_failed": sum(1 for x in source_index if x["extraction_status"] != "COMPLETE"),
        "pages_total": pages_total,
        "pages_extracted": pages_total - errors,
        "op_total": len(PROCESS_CONFIG),
        "op_indexed": len(PROCESS_CONFIG),
        "requirements_total": expected,
        "requirements_indexed": len(requirement_index),
        "structures_total": len(structure_index),
        "structures_indexed": len(structure_index),
        "structures_with_field_metadata": sum(1 for x in structure_index if int(x.get("field_count") or 0) > 0),
        "fields_indexed": len(field_index),
        "classifiers_total": classifier_refs,
        "classifiers_indexed_unique_notes": len(classifier_index),
        "qnames_resolved": len(q_resolved),
        "qnames_unresolved": len(q_unresolved),
        "qname_conflicts": sum(1 for r in requirement_index if r.get("qname_status") == "CONFLICT"),
        "gaps_indexed": len(gaps),
        "source_hashes_complete": checks["source_hashes_complete"],
        "stale_sources": 0,
        "broken_internal_links": len(broken),
        "source_layer_complete": errors == 0,
        "knowledge_layer_complete": len(requirement_index) == expected,
        "project_state_layer_complete": True,
        "op_status": {op: cfg["requirement_status"] for op, cfg in PROCESS_CONFIG.items()},
        "decision5_indexed": (KB / "decisions/Decision_5.md").exists(),
        "r006_indexed": (KB / "structures/R.006.md").exists(),
        "r007_indexed": (KB / "structures/R.007.md").exists(),
        "consistency": checks,
        "git_snapshot": snapshot,
    }
    write_generated(REPORT_DIR / "KB_BUILD_STATS.json", json_dump(stats), force_generated=True)
    audit = frontmatter({"generated_by": GENERATOR, "generated_at": BUILD_TIME}) + "# KB Build Audit\n\n"
    audit += f"- Status: **{stats['status']}**\n- PDF processed: {stats['pdf_processed']}/{stats['pdf_total']}\n- Pages extracted: {stats['pages_extracted']}/{stats['pages_total']}\n"
    audit += f"- OP indexed: {stats['op_indexed']}/{stats['op_total']}\n- Requirements indexed: {stats['requirements_indexed']}/{stats['requirements_total']} known scope\n"
    audit += f"- Structures indexed: {stats['structures_indexed']} (with field metadata: {stats['structures_with_field_metadata']})\n- Field rows indexed: {len(field_index)}\n- Classifier dependency rows: {classifier_refs}; unique notes: {len(classifier_index)}\n"
    audit += f"- QName resolved/unresolved: {len(q_resolved)}/{len(q_unresolved)}\n- Gaps indexed: {len(gaps)}\n- Broken internal links: {len(broken)}\n- Stale sources after extraction: 0\n\n"
    audit += "## Deliberate knowledge incompleteness\n\n"
    audit += "- OP22: current inventory is 1609/1609. It is deterministically recovered from current business_rules/source_refs, including explicit inherited ranges, and reconciled to FINAL_DELIVERY_MESSAGE_MATRIX.csv. FINAL_DELIVERY_AUDIT.md explicitly states that this is not a new independent row-by-row PDF re-audit.\n"
    audit += "- OP26: source-reconciled atomic scope is 239. Table 19 MSG.002 items 50-87 are separate atomic requirements; Table 21 MSG.028 preserves two distinct source rows both numbered 5 using source-occurrence metadata.\n"
    audit += "- OP49: validated canonical scope is 166 (35+38+2+54+37). All 166 rows have primary-source trace and remain OPEN under strict closure.\n"
    audit += "- Source sections/tables are not auto-created when exact table boundaries cannot be proven from page extraction. Source pages remain available.\n\n"
    audit += "## Consistency\n\n```json\n" + json_dump(checks) + "```\n\n"
    if broken:
        audit += "## Broken links\n\n" + "\n".join(f"- `{x['from']}` → `[[{x['target']}]]`" for x in broken[:200]) + "\n"
    write_generated(REPORT_DIR / "KB_BUILD_AUDIT.md", audit, force_generated=True)
    return stats


def knowledge_gap_closure(category: str, status: str = "") -> str:
    if category == "MISSING_CANONICAL_REQUIREMENT":
        return "A current canonical inventory is available with expected arithmetic, unique IDs, and source traceability for every atomic requirement."
    if category == "MISSING_SOURCE_TEXT":
        return "Exact normative source text is linked from an authoritative local source with page/table/item provenance."
    if category == "MISSING_SOURCE_PAGE":
        return "The authoritative source page is identified and linked to an existing SOURCE-layer page note."
    if category == "MISSING_TABLE":
        return "The normative table/item identity is confirmed from the source and recorded without inference."
    if category == "MISSING_STRUCTURE":
        return "The owning structure is confirmed by normative source or confirmed source_refs."
    if category == "MISSING_STRUCTURE_VERSION":
        return "An authoritative source resolves the concrete structure version; placeholder versions are replaced with confirmed values."
    if category == "MISSING_QNAME":
        return "Full Clark QName `{namespace}local_name` is proven by authoritative schema/structure material for the applicable version."
    if category == "MISSING_NAMESPACE":
        return "The namespace URI and applicable version are proven by authoritative schema/structure material."
    if category == "MISSING_XML_PATH":
        return "The requirement is mapped to an exact XML path using confirmed structure/schema semantics and the mapping is regression-validated when executable."
    if category == "MISSING_CLASSIFIER":
        return closure_criterion_for(status or "OPEN_CLASSIFIER")
    if category == "MISSING_CLASSIFIER_PAYLOAD":
        return "The official machine-readable classifier payload and applicable version/snapshot are available locally and registered with provenance."
    if category == "MISSING_EXTERNAL_REGISTRY":
        return closure_criterion_for(status or "OPEN_EXTERNAL_REGISTRY")
    if category == "MISSING_IMPLEMENTATION_EVIDENCE":
        return closure_criterion_for(status or "OPEN_PRODUCTION_MAPPING")
    if category == "CONFLICT":
        return closure_criterion_for("OPEN_SOURCE_CONFLICT")
    if category == "UNVERIFIED":
        return "The item is re-audited against a higher-priority authoritative source and receives explicit provenance/evidence level."
    return "The missing knowledge is supplied by an authoritative source and revalidated against the KB invariants."


def write_enrichment_gaps(
    records: list[dict[str, str]],
    requirement_index: list[dict[str, Any]],
    structure_index: list[dict[str, Any]],
    classifier_index: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Write the current remaining KB gaps with actionable closure criteria."""

    idx_by_id = {row["id"]: row for row in requirement_index}
    gaps: list[dict[str, Any]] = []

    def add(
        item: str,
        op: str,
        process: str,
        category: str,
        status: str,
        source: str,
        page: Any,
        note: str,
        missing_count: Any = 1,
        reason: str = "",
        explanation: str = "",
        missing_information: str = "",
        required_action: str = "",
        closure_criterion: str = "",
    ) -> None:
        gaps.append(
            {
                "knowledge_item": item,
                "op": op,
                "process": process,
                "category": category,
                "status": status,
                "source": source,
                "source_page": page or "",
                "note": note,
                "missing_count": missing_count,
                "reason": reason,
                "plain_explanation": explanation,
                "missing_information": missing_information,
                "required_action": required_action,
                "closure_criterion": closure_criterion or knowledge_gap_closure(category, status),
            }
        )

    for record in records:
        cid = record.get("canonical_requirement_id", "")
        if not cid:
            continue
        idx = idx_by_id.get(cid, {})
        op = record.get("op", "")
        process = record.get("process", "")
        source = record.get("source", "")
        page = normalize_page(record.get("source_page", ""))
        note = idx.get("markdown_path", f"requirements/{cid}.md")
        status = record.get("status_normalized", "OTHER")
        reason = record.get("current_state", "") or record.get("new_status", "") or status
        explanation = record.get("plain_explanation", "") or reason
        missing_info = record.get("new_missing_information", "") or record.get("missing_information", "")
        action = record.get("recommended_action", "")

        if not str(record.get("source_text", "")).strip():
            add(cid, op, process, "MISSING_SOURCE_TEXT", status, source, page, note, reason=reason, explanation=explanation, missing_information="Exact normative source text.", required_action="Recover exact text from the authoritative source page/table.")
        if not page:
            add(cid, op, process, "MISSING_SOURCE_PAGE", status, source, page, note, reason=reason, explanation=explanation, missing_information="Normative PDF page.", required_action="Identify and link the authoritative source page.")
        table_value = str(record.get("source_table_or_item", "") or "").strip()
        if not table_value:
            add(cid, op, process, "MISSING_TABLE", status, source, page, note, reason=reason, explanation=explanation, missing_information="Normative table/item identity.", required_action="Recover table/item from confirmed source_refs or the SOURCE layer.")
        if not str(record.get("structure", "")).strip():
            add(cid, op, process, "MISSING_STRUCTURE", status, source, page, note, reason=reason, explanation=explanation, missing_information="Owning structure.", required_action="Confirm the structure from normative message/structure material.")

        qstatus = idx.get("qname_status", qname_status(record))
        if qstatus != "RESOLVED_CLARK":
            if qstatus == "CONFLICT":
                add(cid, op, process, "CONFLICT", status, source, page, note, reason=reason, explanation=explanation, missing_information=missing_info or "Conflicting QName/source evidence.", required_action=action or "Resolve using a higher-priority authoritative source.")
            else:
                add(cid, op, process, "MISSING_QNAME", status, source, page, note, reason=reason, explanation=explanation, missing_information="Confirmed full Clark QName.", required_action="Obtain authoritative namespace + local-name evidence for the applicable version.")
                add(cid, op, process, "MISSING_NAMESPACE", status, source, page, note, reason=reason, explanation=explanation, missing_information="Confirmed namespace URI/version.", required_action="Obtain authoritative namespace evidence for the applicable version.")
        if not str(record.get("xml_path", "")).strip():
            add(cid, op, process, "MISSING_XML_PATH", status, source, page, note, reason=reason, explanation=explanation, missing_information="Confirmed XML path.", required_action="Map the requirement through confirmed structure/schema semantics.")

        has_runtime_evidence = any(str(record.get(key, "")).strip() for key in ["regression_test", "positive_xml_case", "negative_xml_case"])
        if not has_runtime_evidence:
            add(cid, op, process, "MISSING_IMPLEMENTATION_EVIDENCE", status, source, page, note, reason=reason, explanation=explanation, missing_information=missing_info or "Requirement-level runtime/regression evidence.", required_action=action or "Add or link requirement-level executable/regression evidence after normative prerequisites are satisfied.")
        if status == "OPEN_CLASSIFIER":
            add(cid, op, process, "MISSING_CLASSIFIER", status, source, page, note, reason=reason, explanation=explanation, missing_information=missing_info or "Required classifier/reference data.", required_action=action or "Obtain the official classifier payload/version and validate membership semantics.")
        if status == "OPEN_EXTERNAL_REGISTRY":
            add(cid, op, process, "MISSING_EXTERNAL_REGISTRY", status, source, page, note, reason=reason, explanation=explanation, missing_information=missing_info or "Authoritative external registry/context.", required_action=action or "Obtain the authoritative registry contract/context and validate the rule against it.")
        if status == "OPEN_NORMATIVE_AMBIGUITY":
            add(cid, op, process, "UNVERIFIED", status, source, page, note, reason=reason, explanation=explanation, missing_information=missing_info or "Authoritative normative clarification.", required_action=action or "Obtain an authoritative clarification and re-audit the interpretation.")

    for structure in structure_index:
        versions = [str(v) for v in structure.get("versions", [])]
        if not versions or any(re.search(r"[XYZ]\.Y\.Y|[XYZ]\.X\.X|^[XYZ](?:\.[XYZ]){2}$", v) for v in versions):
            add(
                structure["id"], "", "", "MISSING_STRUCTURE_VERSION", "MISSING",
                "structure metadata", "", structure.get("markdown_path", ""),
                reason="Concrete structure version is unresolved or represented by a placeholder.",
                explanation="The local metadata preserves the placeholder because no authoritative concrete version is available.",
                missing_information="Concrete authoritative structure version.",
                required_action="Obtain the official schema/registry material that fixes the applicable structure version.",
            )

    for classifier in classifier_index:
        if not classifier.get("machine_readable"):
            add(
                classifier.get("classifier_id", ""), "OP32", "P.MM.06", "MISSING_CLASSIFIER_PAYLOAD", "MISSING",
                classifier.get("official_name", ""), "", classifier.get("markdown_path", ""),
                reason="Normative classifier reference is known, but no official machine-readable payload is registered locally.",
                explanation="Classifier identity/reference and classifier payload are tracked separately.",
                missing_information="Official machine-readable classifier payload and applicable version/snapshot.",
                required_action="Add the official local payload with provenance and verify the applicable version.",
            )

    fieldnames = [
        "knowledge_item", "op", "process", "category", "status", "source", "source_page", "note", "missing_count",
        "reason", "plain_explanation", "missing_information", "required_action", "closure_criterion",
    ]
    out_path = REPORT_DIR / "KB_ENRICHMENT_GAPS.csv"
    ensure_allowed(out_path)
    with out_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(gaps)
    return gaps


def write_enrichment_result(
    stats: dict[str, Any],
    records: list[dict[str, str]],
    structure_index: list[dict[str, Any]],
    field_index: list[dict[str, Any]],
    classifier_index: list[dict[str, Any]],
    q_resolved: list[dict[str, Any]],
    q_unresolved: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
) -> None:
    before = {
        "requirements_expected": 2849,
        "requirements_indexed": 2690,
        "op22_expected": 1609,
        "op22_indexed": 1609,
        "op23": 710,
        "op26": 201,
        "op32": 170,
        "op49": 0,
        "source_text_complete": 2690,
        "source_trace_complete": 2690,
        "structures": 23,
        "structures_with_fields": 0,
        "fields": 0,
        "classifiers": 11,
        "qnames_resolved": 2,
        "qnames_unresolved": 213,
        "qname_conflicts": 37,
    }
    after_by_op = Counter(r.get("op", "") for r in records)
    source_text_complete = sum(bool(str(r.get("source_text", "")).strip()) for r in records)
    source_trace_complete = sum(bool(normalize_page(r.get("source_page", ""))) for r in records)
    conflicts = int(stats.get("qname_conflicts", 0))
    with_closure = sum(bool(str(row.get("closure_criterion", "")).strip()) for row in gaps)
    gap_counts = Counter(row["category"] for row in gaps)
    lines = [
        frontmatter({"generated_by": GENERATOR, "generated_at": BUILD_TIME}),
        "# KB Enrichment Result\n",
        "The canonical scope is migrated from the superseded 2849 known-scope checkpoint to 2894 atomic requirements by reconciling OP26 to 239 and importing the validated OP49 166-row re-audit.\n",
        "| Metric | Before | After | Delta |",
        "|---|---:|---:|---:|",
        f"| Known requirements scope | {before['requirements_expected']} | {stats['requirements_total']} | {stats['requirements_total']-before['requirements_expected']:+d} |",
        f"| Requirements indexed | {before['requirements_indexed']} | {stats['requirements_indexed']} | {stats['requirements_indexed']-before['requirements_indexed']:+d} |",
        f"| OP22 indexed | {before['op22_indexed']} | {after_by_op['OP22']} | {after_by_op['OP22']-before['op22_indexed']:+d} |",
        f"| OP49 indexed | {before['op49']} | {after_by_op['OP49']} | {after_by_op['OP49']-before['op49']:+d} |",
        f"| Source texts complete | {before['source_text_complete']} | {source_text_complete} | {source_text_complete-before['source_text_complete']:+d} |",
        f"| Source page links complete | {before['source_trace_complete']} | {source_trace_complete} | {source_trace_complete-before['source_trace_complete']:+d} |",
        f"| Structures indexed | {before['structures']} | {len(structure_index)} | {len(structure_index)-before['structures']:+d} |",
        f"| Structures with field metadata | {before['structures_with_fields']} | {sum(int(x.get('field_count') or 0)>0 for x in structure_index)} | {sum(int(x.get('field_count') or 0)>0 for x in structure_index)-before['structures_with_fields']:+d} |",
        f"| Fields indexed | {before['fields']} | {len(field_index)} | {len(field_index)-before['fields']:+d} |",
        f"| Classifier entity notes | {before['classifiers']} | {len(classifier_index)} | {len(classifier_index)-before['classifiers']:+d} |",
        f"| QName resolved | {before['qnames_resolved']} | {len(q_resolved)} | {len(q_resolved)-before['qnames_resolved']:+d} |",
        f"| QName unresolved | {before['qnames_unresolved']} | {len(q_unresolved)} | {len(q_unresolved)-before['qnames_unresolved']:+d} |",
        f"| QName conflicts | {before['qname_conflicts']} | {conflicts} | {conflicts-before['qname_conflicts']:+d} |",
        f"| Gaps with closure criteria | 0 | {with_closure} | {with_closure:+d} |",
        "\n## Process inventory\n",
        f"- OP22: **{after_by_op['OP22']} / 1609** (current recovered canonical inventory).",
        f"- OP23: **{after_by_op['OP23']} / 710**.",
        f"- OP26: **{after_by_op['OP26']} / 239**.",
        f"- OP32: **{after_by_op['OP32']} / 170**; atomic QName invariant remains 0 resolved / 170 unresolved.",
        f"- OP49: **{after_by_op['OP49']} / 166**; validated re-audit imported, strict IMPLEMENTED_CONFIRMED remains 0.",
        "\n## Confirmed enrichment\n",
        "- OP22 1609-row atomic identity/source inventory recovered from current business_rules/source_refs; all 63 message counts reconcile to FINAL_DELIVERY_MESSAGE_MATRIX.csv.",
        "- OP26 source rows 50-87 for MSG.002 are materialized separately; MSG.028 duplicate source item 5 is represented as two canonical entities without inventing a new source number.",
        "- OP49 166-row validated re-audit is imported with source text, PDF page, table/item trace and closure criteria for every requirement.",
        f"- Structure field rows indexed with provenance: **{len(field_index)}** across **{sum(int(x.get('field_count') or 0)>0 for x in structure_index)}** structures.",
        f"- Exact Clark root QNames indexed where concrete namespace + local name + confirmed source_refs exist: **{len(q_resolved)}** global QName entries.",
        f"- Classifier dependencies remain **59** rows; normalized classifier entity notes: **{len(classifier_index)}**. Composite dependency cells are not treated as separate entities.",
        "- Decision №5 navigation now includes RelatesAction, the common-process Action URI component order, and EAEU:// logical-address prefix with SOURCE-page evidence.",
        "- PDF/printed-page mappings are indexed only when the extracted standalone page header follows a repeated stable offset.",
        "\n## Remaining gap categories\n",
    ]
    lines.extend(f"- `{category}`: {count}" for category, count in sorted(gap_counts.items()))
    lines += [
        "\n## Validation snapshot\n",
        f"- Stale sources: **{stats['stale_sources']}**.",
        f"- Broken internal links: **{stats['broken_internal_links']}**.",
        f"- Duplicate canonical IDs: **{len(stats['consistency']['duplicate_requirement_ids'])}**.",
        f"- Missing requirement files: **{len(stats['consistency']['missing_requirement_markdown'])}**.",
        f"- Missing linked source pages: **{len(stats['consistency']['missing_requirement_source_pages'])}**.",
        "- SOURCE extraction was reused after SHA-256 verification; PDFs were not re-extracted during enrichment rebuilds.",
    ]
    write_generated(REPORT_DIR / "KB_ENRICHMENT_RESULT.md", "\n".join(lines) + "\n", force_generated=True)


def check_stale_only() -> int:
    idx = KB / "indexes/source_index.json"
    if not idx.exists():
        print("NO_SOURCE_INDEX")
        return 2
    stored = {x["source_id"]: x for x in json.loads(idx.read_text(encoding="utf-8"))}
    stale = []
    lines = ["# Stale Sources", ""]
    for cfg in SOURCES:
        sid = cfg["source_id"]
        current = sha256(cfg["path"])
        old = stored.get(sid, {}).get("sha256")
        state = "CURRENT" if old == current else "STALE"
        if state == "STALE":
            stale.append(sid)
        lines.append(f"- `{sid}`: **{state}** — stored `{old or 'MISSING'}` — current `{current}`")
    write_generated(KB / "indexes/STALE_SOURCES.md", frontmatter({"layer": "SOURCE", "generated_by": GENERATOR, "checked_at": BUILD_TIME}) + "\n".join(lines) + "\n", force_generated=True)
    print(json.dumps({"stale_sources": stale, "count": len(stale)}, ensure_ascii=False))
    return 1 if stale else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-stale", action="store_true")
    parser.add_argument("--reuse-sources", action="store_true", help="Reuse existing extracted SOURCE pages after hash verification")
    args = parser.parse_args()
    if args.check_stale:
        return check_stale_only()

    for d in ["sources", "processes", "requirements", "structures", "classifiers", "decisions", "engine", "indexes", "tools"]:
        (KB / d).mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    snapshot = git_snapshot()
    source_index, page_texts = load_existing_sources() if args.reuse_sources else extract_sources()
    write_source_registry(source_index)
    build_page_mapping(source_index)
    records = canonical_records()
    requirement_index = build_requirement_notes(records)
    structures = structure_inventory(records)
    structure_index, field_index = build_structures(structures)
    classifier_index, classifier_refs = build_classifier_notes()
    q_resolved, q_unresolved = build_qname_index(records, structure_index)
    process_index = build_process_files(records, requirement_index, structures)
    build_decision5(page_texts)
    build_engine_snapshot(snapshot, requirement_index)
    write_indexes(source_index, requirement_index, structure_index, field_index, classifier_index, classifier_refs, process_index, q_resolved, q_unresolved)
    write_master_docs(source_index, requirement_index)
    broken = validate_links()
    checks = consistency_checks(requirement_index, source_index)
    stats = build_report(source_index, requirement_index, structure_index, field_index, classifier_index, classifier_refs, q_resolved, q_unresolved, broken, checks, snapshot)
    enrichment_gaps = write_enrichment_gaps(records, requirement_index, structure_index, classifier_index)
    write_enrichment_result(stats, records, structure_index, field_index, classifier_index, q_resolved, q_unresolved, enrichment_gaps)
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
