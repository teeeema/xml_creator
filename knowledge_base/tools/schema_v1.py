#!/usr/bin/env python3
"""Build and validate the deterministic machine-readable KB schema v1.0.

The canonical ``*.yaml`` files intentionally use JSON syntax. JSON is a valid
YAML 1.2 subset, which keeps serialization deterministic and avoids adding a
new YAML dependency solely for the migration layer.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import build_kb as legacy


ROOT = Path(__file__).resolve().parents[2]
KB = ROOT / "knowledge_base"
REPORT_DIR = ROOT / "codex_reports" / "KNOWLEDGE_BASE"
DATA_DIR = KB / "data"
SCHEMA_DIR = KB / "schemas"
INDEX_DIR = KB / "indexes"
SCHEMA_VERSION = "1.0"
GENERATOR = "knowledge_base/tools/schema_v1.py"

ENTITY_DIRS = {
    "requirements": DATA_DIR / "requirements",
    "messages": DATA_DIR / "messages",
    "transactions": DATA_DIR / "transactions",
    "processes": DATA_DIR / "processes",
    "structures": DATA_DIR / "structures",
    "fields": DATA_DIR / "fields",
    "classifiers": DATA_DIR / "classifiers",
    "decisions": DATA_DIR / "decisions",
    "project_state": DATA_DIR / "project_state",
}

INDEX_FILES = {
    "requirements": INDEX_DIR / "requirements.json",
    "messages": INDEX_DIR / "messages.json",
    "transactions": INDEX_DIR / "transactions.json",
    "processes": INDEX_DIR / "processes.json",
    "structures": INDEX_DIR / "structures.json",
    "fields": INDEX_DIR / "fields.json",
    "classifiers": INDEX_DIR / "classifiers.json",
    "dependencies": INDEX_DIR / "dependencies.json",
    "gaps": INDEX_DIR / "gaps.json",
}

EXPECTED_SCOPE = {"OP22": 1609, "OP23": 710, "OP26": 239, "OP32": 170, "OP49": 166}
EXPECTED_CANONICAL_CURRENT = dict(EXPECTED_SCOPE)

WRITTEN_FILES: set[Path] = set()
CHANGED_FILES: set[Path] = set()


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def ensure_allowed(path: Path) -> None:
    resolved = path.resolve()
    if not (resolved.is_relative_to(KB.resolve()) or resolved.is_relative_to(REPORT_DIR.resolve())):
        raise RuntimeError(f"Refusing to write outside KB/report scope: {path}")


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_text(path: Path, text: str) -> None:
    ensure_allowed(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    WRITTEN_FILES.add(path.resolve())
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        return
    path.write_text(text, encoding="utf-8")
    CHANGED_FILES.add(path.resolve())


def write_machine(path: Path, data: Any) -> None:
    write_text(path, stable_json(data))


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def clean(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


def absent_text(value: Any) -> bool:
    text = str(value or "").strip()
    if not text:
        return True
    upper = text.upper()
    return upper.startswith(("NONE", "MISSING", "NOT_WIRED", "UNVERIFIED"))


def one_or_none(values: Iterable[Any]) -> list[str]:
    out: list[str] = []
    for value in values:
        text = clean(value)
        if text and text not in out:
            out.append(text)
    return out


def split_ids(value: Any) -> list[str]:
    return [x.strip() for x in str(value or "").split(";") if x.strip()]


def safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._:-]+", "_", value).strip("_") or "UNRESOLVED"


def git_state() -> dict[str, Any]:
    def run(*args: str) -> str:
        return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False).stdout.strip()

    status = run("git", "status", "--porcelain=v1").splitlines()
    return {
        "head": run("git", "rev-parse", "--verify", "HEAD") or None,
        "branch": run("git", "branch", "--show-current") or None,
        "dirty_entries": len(status),
        "status": status,
    }


def source_state() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[tuple[str, int], int]]:
    rows = load_json(INDEX_DIR / "source_index.json", []) or []
    by_id = {row.get("source_id"): row for row in rows if row.get("source_id")}
    page_rows = load_json(INDEX_DIR / "page_mapping.json", []) or []
    printed = {
        (row.get("source_id"), int(row.get("pdf_page"))): int(row.get("printed_page"))
        for row in page_rows
        if row.get("source_id") and row.get("pdf_page") and row.get("printed_page")
    }
    return rows, by_id, printed


def schema_documents() -> dict[str, dict[str, Any]]:
    common = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {"schema_version": {"const": SCHEMA_VERSION}},
        "required": ["schema_version"],
    }
    requirement = {
        **common,
        "$id": "requirement.schema.json",
        "properties": {
            **common["properties"],
            "identity": {
                "type": "object",
                "properties": {
                    "canonical_id": {"type": "string"},
                    "op": {"type": ["string", "null"]},
                    "process": {"type": ["string", "null"]},
                    "procedure": {"type": ["string", "null"]},
                    "transaction": {"type": ["string", "null"]},
                    "message": {"type": ["string", "null"]},
                    "requirement": {"type": ["string", "null"]},
                    "source_requirement_number": {"type": ["string", "null"]},
                    "source_occurrence": {"type": ["integer", "null"], "minimum": 1},
                    "canonical_disambiguator": {"type": ["string", "null"]},
                },
                "required": ["canonical_id", "op", "process", "procedure", "transaction", "message", "requirement"],
            },
            "normative": {"type": "object", "required": ["source_text", "plain_language"]},
            "source": {"type": "object", "required": ["document", "source_path", "pdf_page", "printed_page", "section", "table", "item", "evidence"]},
            "structure": {"type": "object", "required": ["id", "version", "root_qname", "atomic_qname", "xml_path"]},
            "fields": {"type": "array"},
            "dependencies": {"type": "object"},
            "relationships": {"type": "object"},
            "implementation": {"type": "object"},
            "verification": {"type": "object"},
            "gap": {"type": "object"},
            "provenance": {"type": "object"},
            "project_state": {"type": "object"},
        },
        "required": [
            "schema_version", "identity", "normative", "source", "structure", "fields", "dependencies",
            "relationships", "implementation", "verification", "gap", "provenance", "project_state",
        ],
    }
    simple_required = {
        "message": ["identity", "purpose", "flow", "structure", "requirements", "sources", "dependencies", "runtime", "project_state"],
        "transaction": ["identity", "plain_language", "participants", "type", "messages", "protocol", "decision5", "sources", "runtime", "project_state"],
        "process": ["identity", "purpose", "participants", "operations", "procedures", "transactions", "messages", "structures", "requirements", "dependencies", "known_blockers", "runtime", "sources", "project_state"],
        "structure": ["identity", "root", "xsd", "source", "usage", "field_index", "dependencies", "evidence", "known_gaps"],
        "fields": ["structure", "fields"],
        "classifier": ["identity", "official_name", "required_version", "machine_readable_payload", "sources", "used_by", "evidence"],
        "decision": ["identity", "fields", "action", "addressing", "sources", "evidence"],
        "dependency_graph": ["nodes", "edges"],
        "project_state": ["captured_at", "git_head", "branch", "dirty_entries", "git_status", "inputs"],
    }
    out = {"requirement": requirement}
    for name, required in simple_required.items():
        out[name] = {
            **common,
            "$id": f"{name}.schema.json",
            "properties": {**common["properties"], **{key: {} for key in required}},
            "required": ["schema_version", *required],
        }
    return out


def write_schemas() -> None:
    for name, schema in schema_documents().items():
        write_machine(SCHEMA_DIR / f"{name}.schema.json", schema)


def validate_schema_documents() -> list[str]:
    errors: list[str] = []
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"malformed schema {path.name}: {type(exc).__name__}: {exc}")
            continue
        if data.get("type") != "object" or data.get("properties", {}).get("schema_version", {}).get("const") != SCHEMA_VERSION:
            errors.append(f"invalid schema_version contract in {path.name}")
    return errors


def validate_op49_import() -> dict[str, Any]:
    path = ROOT / "codex_reports" / "OP49_P_DS_01" / "OP49_REAUDIT_REQUIREMENTS.csv"
    if not path.exists():
        return {"status": "MISSING", "reason": "OP49_REAUDIT_REQUIREMENTS.csv not present"}
    rows = read_csv(path)
    ids = [row.get("canonical_id", "").strip() for row in rows]
    counts = Counter(row.get("message", "").strip() for row in rows)
    expected = legacy.OP49_CONFIRMED_SCOPE
    missing_source_text = sum(not clean(row.get("source_text")) for row in rows)
    missing_source_trace = sum(
        not legacy.normalize_page(row.get("pdf_page", ""))
        or not clean(row.get("table"))
        or not clean(row.get("table_item"))
        for row in rows
    )
    missing_closure = sum(not clean(row.get("closure_criterion")) for row in rows)
    valid = (
        len(rows) == 166
        and len(set(ids)) == 166
        and all(ids)
        and all(row.get("op") == "OP49" and row.get("process") == "P.DS.01" for row in rows)
        and missing_source_text == 0
        and missing_source_trace == 0
        and missing_closure == 0
        and all(counts.get(msg, 0) == count for msg, count in expected.items())
    )
    result = {
        "status": "PASS" if valid else "FAILED_VALIDATION_GATE",
        "rows": len(rows),
        "unique_ids": len(set(ids)),
        "message_counts": dict(sorted(counts.items())),
        "missing_source_text": missing_source_text,
        "missing_source_trace": missing_source_trace,
        "missing_closure_criteria": missing_closure,
        "strict_implemented_confirmed": 0,
        "strict_open": len(rows),
    }
    if not valid:
        return result
    return result


def validate_op26_reconciliation(records: list[dict[str, str]]) -> dict[str, Any]:
    op26 = [row for row in records if row.get("op") == "OP26"]
    ids = [row.get("canonical_requirement_id", "") for row in op26]
    counts = Counter(row.get("message", "") for row in op26)
    duplicate_source_fives = [
        row for row in op26
        if row.get("message") == "P.MM.01.MSG.028" and clean(row.get("current_source_item")) == "5"
    ]
    source_occurrences = sorted(int(row.get("source_occurrence") or 1) for row in duplicate_source_fives)
    traceable = sum(
        bool(clean(row.get("source_text")))
        and bool(legacy.normalize_page(row.get("source_page", "")))
        and bool(clean(row.get("source_table_or_item")))
        for row in op26
    )
    valid = (
        len(op26) == 239
        and len(set(ids)) == 239
        and counts.get("P.MM.01.MSG.002") == 87
        and counts.get("P.MM.01.MSG.028") == 8
        and len(duplicate_source_fives) == 2
        and source_occurrences == [1, 2]
        and traceable == 239
    )
    return {
        "status": "PASS" if valid else "FAILED_VALIDATION_GATE",
        "rows": len(op26),
        "unique_ids": len(set(ids)),
        "message_002": counts.get("P.MM.01.MSG.002", 0),
        "message_028": counts.get("P.MM.01.MSG.028", 0),
        "duplicate_source_item_5_rows": len(duplicate_source_fives),
        "duplicate_source_item_5_occurrences": source_occurrences,
        "source_trace_complete": traceable,
    }


def current_records() -> tuple[list[dict[str, str]], dict[str, Any], dict[str, Any]]:
    records = legacy.canonical_records()
    op49_gate = validate_op49_import()
    op26_gate = validate_op26_reconciliation(records)
    if op49_gate.get("status") != "PASS":
        raise RuntimeError(f"OP49 import gate failed: {op49_gate}")
    if op26_gate.get("status") != "PASS":
        raise RuntimeError(f"OP26 reconciliation gate failed: {op26_gate}")
    ids = [row.get("canonical_requirement_id", "") for row in records]
    if len(ids) != len(set(ids)):
        duplicates = [item for item, count in Counter(ids).items() if count > 1]
        raise RuntimeError(f"Duplicate canonical IDs before migration: {duplicates[:20]}")
    return records, op26_gate, op49_gate


def load_dependency_sources() -> tuple[dict[str, list[dict[str, str]]], dict[str, list[dict[str, str]]], dict[str, list[dict[str, str]]]]:
    classifier_by_req: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(ROOT / "codex_reports" / "OP32_P_MM_06" / "OP32_CLASSIFIER_SOURCE_INVENTORY.csv"):
        if row.get("canonical_requirement_id"):
            classifier_by_req[row["canonical_requirement_id"]].append(row)
    external_by_req: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(ROOT / "codex_reports" / "OP32_P_MM_06" / "OP32_EXTERNAL_REGISTRY_RECOVERY.csv"):
        if row.get("canonical_requirement_id"):
            external_by_req[row["canonical_requirement_id"]].append(row)
    closure_by_req: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(REPORT_DIR / "KB_ENRICHMENT_GAPS.csv"):
        if row.get("knowledge_item"):
            closure_by_req[row["knowledge_item"]].append(row)
    return classifier_by_req, external_by_req, closure_by_req


def qname_payload(raw: Any, status: str) -> dict[str, Any]:
    text = clean(raw)
    namespace = None
    local_name = None
    clark = None
    if text:
        match = re.fullmatch(r"\{([^}]+)\}([A-Za-z_][\w.-]*)", text)
        if match and status == "RESOLVED_CLARK":
            namespace, local_name = match.groups()
            clark = text
        elif re.fullmatch(r"[A-Za-z_][\w.-]*:[A-Za-z_][\w.-]*", text):
            local_name = text.split(":", 1)[1]
    return {
        "raw": text,
        "namespace": namespace,
        "local_name": local_name,
        "clark_name": clark,
        "status": status,
    }


def root_qname_payload(structure: dict[str, Any] | None) -> dict[str, Any]:
    if not structure:
        return {"namespace": None, "local_name": None, "clark_name": None, "status": "MISSING"}
    raw = clean(structure.get("root_qname"))
    evidence = clean(structure.get("root_qname_evidence")) or "MISSING"
    if raw and raw.startswith("CONFLICT:"):
        return {"namespace": None, "local_name": None, "clark_name": None, "status": "CONFLICT"}
    match = re.fullmatch(r"\{([^}]+)\}([A-Za-z_][\w.-]*)", raw or "")
    if match:
        return {"namespace": match.group(1), "local_name": match.group(2), "clark_name": raw, "status": "CONFIRMED" if evidence.startswith("CONFIRMED") else evidence}
    return {"namespace": None, "local_name": None, "clark_name": None, "status": "UNRESOLVED"}


def gap_category(status: str) -> str | None:
    mapping = {
        "OPEN_PRODUCTION_MAPPING": "PRODUCTION_MAPPING",
        "OPEN_ENGINE": "ENGINE",
        "OPEN_CLASSIFIER": "CLASSIFIER",
        "OPEN_EXTERNAL_REGISTRY": "EXTERNAL_REGISTRY",
        "OPEN_SOURCE_CONFLICT": "SOURCE_CONFLICT",
        "OPEN_NORMATIVE_AMBIGUITY": "NORMATIVE_AMBIGUITY",
        "OPEN_MISSING_STRUCTURE": "MISSING_STRUCTURE",
        "OPEN_MISSING_NORMATIVE_DATA": "MISSING_NORMATIVE_DATA",
        "OTHER": "OTHER",
    }
    return mapping.get(status)


def proof(value: Any) -> dict[str, Any]:
    text = clean(value)
    if not text:
        return {"status": "MISSING", "test": None}
    upper = text.upper()
    if upper.startswith("NOT_WIRED"):
        return {"status": "NOT_WIRED", "test": None, "note": text}
    if upper.startswith(("NONE", "MISSING")):
        return {"status": "MISSING", "test": None, "note": text}
    return {"status": "PRESENT", "test": text}


def inherited_relation(record: dict[str, str]) -> list[dict[str, Any]]:
    if record.get("message") != "P.SP.03.MSG.014":
        return []
    text = " ".join([record.get("source_table_or_item", ""), record.get("source_text", ""), record.get("trace_source_refs", "")])
    match = re.search(r"inherited from[^\n]*?MSG\.013(?:[^\n]*?item|[^\n]*?requirement)?\s*(\d+)", text, flags=re.I)
    if not match:
        match = re.search(r"Inherited semantic requirement\s+(\d+)\s+from\s+P\.SP\.03\.MSG\.013", text, flags=re.I)
    if not match:
        return []
    req_no = int(match.group(1))
    item = "3-34" if "3-34" in text else None
    return [
        {
            "requirement": f"P.SP.03.MSG.013.REQ.{req_no:03d}",
            "relation": "NORMATIVE_REFERENCE",
            "source": {
                "document": clean(record.get("source")),
                "table": "23" if "Таблица 23" in text or "Table 23" in text else None,
                "item": item,
                "pdf_page": legacy.normalize_page(record.get("source_page", "")),
                "evidence": "CONFIRMED_PDF" if legacy.normalize_page(record.get("source_page", "")) else "AUDIT_DERIVED",
            },
        }
    ]


def requirement_object(
    record: dict[str, str],
    source_by_id: dict[str, dict[str, Any]],
    printed: dict[tuple[str, int], int],
    structures: dict[str, dict[str, Any]],
    fields_by_structure_path: dict[tuple[str, str], list[dict[str, Any]]],
    classifier_by_req: dict[str, list[dict[str, str]]],
    external_by_req: dict[str, list[dict[str, str]]],
    closure_by_req: dict[str, list[dict[str, str]]],
    classifier_ids: set[str],
    git_head: str | None,
) -> dict[str, Any]:
    cid = record["canonical_requirement_id"]
    op = clean(record.get("op"))
    process = clean(record.get("process"))
    message = clean(record.get("message")) or clean(legacy.requirement_id_parts(cid)[0])
    requirement_no = clean(legacy.requirement_id_parts(cid)[1])
    status = clean(record.get("status_normalized")) or "OTHER"
    document = clean(record.get("source"))
    source_id = legacy.source_id_for(document or "", process or "")
    source_entry = source_by_id.get(source_id, {})
    pdf_page = legacy.normalize_page(record.get("source_page", ""))
    structure_id = clean(record.get("structure"))
    structure = structures.get(structure_id or "")
    versions = structure.get("versions", []) if structure else []
    structure_version = clean(record.get("structure_version")) or (versions[0] if len(versions) == 1 else None)
    qstatus = legacy.qname_status(record)
    xml_path = clean(record.get("xml_path"))
    source_requirement_number = clean(record.get("current_source_item"))
    if not source_requirement_number:
        item_match = re.search(r"(?:пункт|item)\s*(\d+)", str(record.get("source_table_or_item", "")), flags=re.I)
        source_requirement_number = item_match.group(1) if item_match else None
    source_occurrence = int(record.get("source_occurrence") or 1) if source_requirement_number else None
    source_table = clean(record.get("current_source_table"))
    if not source_table:
        table_match = re.search(r"(?:Таблица|Table)\s*(\d+)", str(record.get("source_table_or_item", "")), flags=re.I)
        source_table = table_match.group(1) if table_match else clean(record.get("source_table_or_item"))
    source_section = clean(record.get("source_section"))
    exact_fields: list[dict[str, Any]] = []
    if structure_id and xml_path:
        for field in fields_by_structure_path.get((structure_id, xml_path), []):
            exact_fields.append({"field_id": clean(field.get("field_id")), "path": xml_path, "evidence": clean(field.get("evidence_level"))})

    classifier_deps: list[dict[str, Any]] = []
    for row in classifier_by_req.get(cid, []):
        ids = split_ids(row.get("classifier_id"))
        names = split_ids(row.get("classifier_name"))
        versions_dep = split_ids(row.get("required_version"))
        for index, classifier_id in enumerate(ids):
            if classifier_id not in classifier_ids:
                continue
            classifier_deps.append(
                {
                    "classifier": classifier_id,
                    "name": names[index] if len(names) == len(ids) else clean(row.get("classifier_name")),
                    "version": versions_dep[index] if len(versions_dep) == len(ids) else clean(row.get("required_version")),
                    "evidence": {
                        "level": "AUDIT_DERIVED",
                        "source": clean(row.get("normative_source")),
                        "pdf_page": legacy.normalize_page(row.get("page", "")),
                        "table": clean(row.get("table")),
                    },
                }
            )

    external_deps = [
        {
            "resource": clean(row.get("external_system_or_resource")),
            "lookup_required": clean(row.get("lookup_required")),
            "expected_key": clean(row.get("expected_key")),
            "expected_result": clean(row.get("expected_result")),
            "evidence": {"level": "AUDIT_DERIVED", "source": clean(row.get("source"))},
        }
        for row in external_by_req.get(cid, [])
        if clean(row.get("external_system_or_resource"))
    ]
    recorded_dependencies: list[dict[str, Any]] = []
    dependency_type = clean(record.get("dependency_type"))
    dependency_id = clean(record.get("dependency_id"))
    if dependency_type or dependency_id:
        recorded_dependencies.append(
            {
                "type": dependency_type,
                "id": dependency_id,
                "secondary": clean(record.get("secondary_dependencies")),
                "evidence": "AUDIT_DERIVED",
            }
        )

    relation = inherited_relation(record)
    missing_text = clean(record.get("new_missing_information")) or clean(record.get("missing_information"))
    action_text = clean(record.get("recommended_action"))
    closure = clean(record.get("closure_criterion"))
    if not closure:
        closure = next((clean(row.get("closure_criterion")) for row in closure_by_req.get(cid, []) if clean(row.get("closure_criterion"))), None)
    if not closure and status != "IMPLEMENTED_CONFIRMED":
        closure = legacy.closure_criterion_for(status)

    production_rule = clean(record.get("production_rule"))
    production_rules = [] if absent_text(production_rule) else [production_rule]
    production_files: list[str] = []
    cfg = next((cfg for cfg in legacy.PROCESS_CONFIG.values() if cfg["process"] == process), None)
    if cfg and message:
        candidate = ROOT / cfg["package"] / "message_rules" / f"{message}.yaml"
        if candidate.exists():
            production_files.append(str(candidate.relative_to(ROOT)))
    engine_capability = clean(record.get("required_engine_capability"))
    engine_capabilities = [] if absent_text(engine_capability) else [engine_capability]

    positive = proof(record.get("positive_xml_case"))
    negative = proof(record.get("negative_xml_case"))
    runtime = proof(record.get("regression_test"))
    real_xml_status = "PRESENT" if positive["status"] == "PRESENT" and negative["status"] == "PRESENT" else "INCOMPLETE"

    source_evidence = clean(record.get("evidence_level")) or "AUDIT_DERIVED"
    source_page_ref = f"sources/{source_id}/pages/page_{pdf_page:03d}.md" if source_id and pdf_page else None
    gap_open = status != "IMPLEMENTED_CONFIRMED"
    result = {
        "schema_version": SCHEMA_VERSION,
        "identity": {
            "canonical_id": cid,
            "op": op,
            "process": process,
            "procedure": clean(record.get("procedure")),
            "transaction": clean(record.get("transaction")),
            "message": message,
            "requirement": requirement_no,
            "source_requirement_number": source_requirement_number,
            "source_occurrence": source_occurrence,
            "canonical_disambiguator": clean(record.get("canonical_disambiguator")),
        },
        "normative": {
            "source_text": clean(record.get("source_text")),
            "plain_language": {"meaning": clean(record.get("plain_language_meaning")), "purpose": None},
        },
        "source": {
            "document": document,
            "source_path": clean(source_entry.get("absolute_path")),
            "pdf_page": pdf_page,
            "printed_page": printed.get((source_id, pdf_page)) if source_id and pdf_page else None,
            "section": source_section,
            "table": source_table,
            "item": source_requirement_number,
            "occurrence": source_occurrence,
            "evidence": {"level": source_evidence, "source_page_ref": source_page_ref},
        },
        "structure": {
            "id": structure_id,
            "version": structure_version,
            "root_qname": root_qname_payload(structure),
            "atomic_qname": qname_payload(record.get("xml_qname"), qstatus),
            "xml_path": xml_path,
        },
        "fields": exact_fields,
        "dependencies": {
            "classifiers": classifier_deps,
            "external_registries": external_deps,
            "recorded": recorded_dependencies,
            "structures": [structure_id] if structure_id else [],
            "requirements": [item["requirement"] for item in relation],
        },
        "relationships": {"inherits_from": relation, "referenced_by": [], "related_to": []},
        "implementation": {
            "status": status,
            "production_rules": production_rules,
            "production_files": production_files,
            "engine_capabilities": engine_capabilities,
        },
        "verification": {
            "positive_test": positive,
            "negative_test": negative,
            "real_xml": {"status": real_xml_status},
            "runtime": runtime,
        },
        "gap": {
            "status": "OPEN" if gap_open else "CLOSED",
            "category": gap_category(status) if gap_open else None,
            "reason": clean(record.get("current_state")) or clean(record.get("new_status")) or status,
            "missing": [missing_text] if gap_open and missing_text else [],
            "do_not_do": [],
            "required_action": [action_text] if gap_open and action_text else [],
            "closure_criteria": [closure] if gap_open and closure else [],
            "evidence_status": "INCOMPLETE_EVIDENCE" if gap_open and not closure else "RECORDED",
        },
        "provenance": {
            "normative": [{
                "level": source_evidence,
                "source": document,
                "pdf_page": pdf_page,
                "section": source_section,
                "table": source_table,
                "item": source_requirement_number,
                "occurrence": source_occurrence,
            }],
            "implementation": ([{"level": "CONFIRMED_PRODUCTION", "rules": production_rules, "files": production_files}] if status == "IMPLEMENTED_CONFIRMED" and production_rules else []),
            "runtime": ([{"level": "AUDIT_DERIVED", "test": runtime.get("test")}] if runtime.get("status") == "PRESENT" else []),
        },
        "project_state": {
            "snapshot": "data/project_state/current.json",
            "git_head": git_head,
            "verified_at": None,
            "plain_explanation": clean(record.get("plain_explanation")),
            "plain_explanation_evidence": "AUDIT_DERIVED" if clean(record.get("plain_explanation")) else None,
            "audit_notes": clean(record.get("audit_notes")),
        },
    }
    return result


def build_requirements(
    records: list[dict[str, str]],
    source_by_id: dict[str, dict[str, Any]],
    printed: dict[tuple[str, int], int],
    structure_index: list[dict[str, Any]],
    field_index: list[dict[str, Any]],
    classifier_index: list[dict[str, Any]],
    git_head: str | None,
) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, str]]], dict[str, list[dict[str, str]]]]:
    structures = {row["id"]: row for row in structure_index}
    fields_by_structure_path: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in field_index:
        if row.get("structure") and row.get("path"):
            fields_by_structure_path[(row["structure"], row["path"])].append(row)
    classifier_by_req, external_by_req, closure_by_req = load_dependency_sources()
    classifier_ids = {row["classifier_id"] for row in classifier_index}
    out: dict[str, dict[str, Any]] = {}
    for record in records:
        obj = requirement_object(
            record, source_by_id, printed, structures, fields_by_structure_path,
            classifier_by_req, external_by_req, closure_by_req, classifier_ids, git_head,
        )
        out[obj["identity"]["canonical_id"]] = obj
    for cid, req in out.items():
        for relation in req["relationships"]["inherits_from"]:
            target = out.get(relation["requirement"])
            if target:
                target["relationships"]["referenced_by"].append(
                    {"requirement": cid, "relation": relation["relation"], "source": relation["source"]}
                )
    for req in out.values():
        req["relationships"]["referenced_by"] = sorted(req["relationships"]["referenced_by"], key=lambda x: x["requirement"])
    return out, classifier_by_req, external_by_req


def pilot_validation(requirements: dict[str, dict[str, Any]]) -> dict[str, Any]:
    def first(predicate: Any) -> str | None:
        return next((cid for cid, obj in sorted(requirements.items()) if predicate(obj)), None)

    pilot_ids = {
        "op22_implemented": first(lambda x: x["identity"]["op"] == "OP22" and x["implementation"]["status"] == "IMPLEMENTED_CONFIRMED"),
        "op22_open": first(lambda x: x["identity"]["op"] == "OP22" and x["implementation"]["status"] != "IMPLEMENTED_CONFIRMED"),
        "op23_inherited": "P.SP.03.MSG.014.REQ.023" if "P.SP.03.MSG.014.REQ.023" in requirements else None,
        "op23_classifier_blocked": first(lambda x: x["identity"]["op"] == "OP23" and x["implementation"]["status"] == "OPEN_CLASSIFIER"),
        "op26": first(lambda x: x["identity"]["op"] == "OP26"),
        "op32_unresolved_qname": first(lambda x: x["identity"]["op"] == "OP32" and x["structure"]["atomic_qname"]["status"] == "UNRESOLVED"),
    }
    errors: list[str] = []
    required_top = set(schema_documents()["requirement"]["required"])
    for label, cid in pilot_ids.items():
        if not cid:
            errors.append(f"pilot missing: {label}")
            continue
        obj = requirements[cid]
        missing = sorted(required_top - set(obj))
        if missing:
            errors.append(f"pilot {label} missing keys: {missing}")
        round_trip = json.loads(stable_json(obj))
        if round_trip != obj:
            errors.append(f"pilot {label} round-trip mismatch")
    inherited = requirements.get("P.SP.03.MSG.014.REQ.023")
    if inherited and not inherited["relationships"]["inherits_from"]:
        errors.append("OP23 MSG.014 inherited pilot lost normative inheritance relation")
    return {"status": "PASS" if not errors else "FAIL", "pilot_ids": pilot_ids, "errors": errors}


def source_refs(value: Any) -> list[dict[str, Any]]:
    refs = value if isinstance(value, list) else []
    return [dict(ref) for ref in refs if isinstance(ref, dict)]


def entity_catalog() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    messages: dict[str, dict[str, Any]] = {}
    transactions: dict[str, dict[str, Any]] = {}
    processes: dict[str, dict[str, Any]] = {}
    raw_by_process: dict[str, dict[str, Any]] = {}
    for op, cfg in legacy.PROCESS_CONFIG.items():
        ent = legacy.package_entities(cfg)
        raw_by_process[cfg["process"]] = ent
        for row in ent["messages"]:
            code = clean(row.get("message_code"))
            if code:
                messages[code] = {"op": op, "process": cfg["process"], "raw": row}
        for row in ent["transactions"]:
            code = clean(row.get("transaction_code"))
            if code:
                transactions[code] = {"op": op, "process": cfg["process"], "raw": row}
        processes[cfg["process"]] = {"op": op, "cfg": cfg, "raw": ent["process"], "entities": ent}
    return messages, transactions, processes, raw_by_process


def process_version(process_meta: dict[str, Any]) -> str | None:
    for ref in source_refs(process_meta.get("source_refs")):
        candidate = clean(ref.get("version_context")) or clean(ref.get("item"))
        if candidate:
            match = re.search(r"\b\d+\.\d+\.\d+\b", candidate)
            if match:
                return match.group(0)
    return None


def build_messages(requirements: dict[str, dict[str, Any]], catalog: dict[str, dict[str, Any]], git_head: str | None) -> dict[str, dict[str, Any]]:
    req_by_message: dict[str, list[str]] = defaultdict(list)
    for cid, req in requirements.items():
        if req["identity"]["message"]:
            req_by_message[req["identity"]["message"]].append(cid)
    out: dict[str, dict[str, Any]] = {}
    for code, item in catalog.items():
        raw = item["raw"]
        req_ids = sorted(req_by_message.get(code, []))
        classifier_ids = sorted({dep["classifier"] for cid in req_ids for dep in requirements[cid]["dependencies"]["classifiers"]})
        external = sorted({dep["resource"] for cid in req_ids for dep in requirements[cid]["dependencies"]["external_registries"] if dep.get("resource")})
        sender = clean(raw.get("sender_participant")) or clean(raw.get("sender"))
        receiver = clean(raw.get("receiver_participant")) or clean(raw.get("receiver"))
        out[code] = {
            "schema_version": SCHEMA_VERSION,
            "identity": {"message": code, "op": item["op"], "process": item["process"]},
            "purpose": {"name": clean(raw.get("name")), "description": clean(raw.get("description"))},
            "flow": {"direction": clean(raw.get("direction")), "sender": sender, "receiver": receiver},
            "structure": {"id": clean(raw.get("structure_id")), "version": clean(raw.get("structure_version"))},
            "requirements": req_ids,
            "sources": source_refs(raw.get("source_refs")),
            "dependencies": {"classifiers": classifier_ids, "external_registries": external},
            "runtime": {"status": clean(raw.get("status"))},
            "project_state": {"snapshot": "data/project_state/current.json", "git_head": git_head, "verified_at": None},
        }
    return out


def build_transactions(catalog: dict[str, dict[str, Any]], git_head: str | None) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for code, item in catalog.items():
        raw = item["raw"]
        responses = raw.get("response_messages") or []
        if isinstance(responses, str):
            responses = [responses]
        participants = {
            key: raw.get(key)
            for key in ["initiator", "responder", "sender", "receiver", "initiator_participant", "responder_participant"]
            if raw.get(key) not in (None, "", [])
        }
        protocol = {
            "timeout": raw.get("timeout") if "timeout" in raw else None,
            "retry": raw.get("retry") if "retry" in raw else raw.get("retries") if "retries" in raw else None,
            "signature": raw.get("signature") if "signature" in raw else None,
        }
        out[code] = {
            "schema_version": SCHEMA_VERSION,
            "identity": {"transaction": code, "op": item["op"], "process": item["process"], "procedure": clean(raw.get("procedure_code"))},
            "plain_language": {"name": clean(raw.get("name")), "description": clean(raw.get("description"))},
            "participants": participants,
            "type": clean(raw.get("type")) or clean(raw.get("transaction_type")),
            "messages": {"initiating": clean(raw.get("initiating_message")), "responses": sorted(clean(x) for x in responses if clean(x))},
            "protocol": protocol,
            "decision5": {"reference": "data/decisions/Decision_5.yaml"},
            "sources": source_refs(raw.get("source_refs")),
            "runtime": {"status": clean(raw.get("status"))},
            "project_state": {"snapshot": "data/project_state/current.json", "git_head": git_head, "verified_at": None},
        }
    return out


def build_processes(
    requirements: dict[str, dict[str, Any]],
    messages: dict[str, dict[str, Any]],
    transactions: dict[str, dict[str, Any]],
    catalog: dict[str, dict[str, Any]],
    git_head: str | None,
) -> dict[str, dict[str, Any]]:
    req_by_process: dict[str, list[str]] = defaultdict(list)
    for cid, req in requirements.items():
        if req["identity"]["process"]:
            req_by_process[req["identity"]["process"]].append(cid)
    out: dict[str, dict[str, Any]] = {}
    for process, item in catalog.items():
        ent = item["entities"]
        raw = item["raw"]
        msg_ids = sorted(code for code, obj in messages.items() if obj["identity"]["process"] == process)
        trn_ids = sorted(code for code, obj in transactions.items() if obj["identity"]["process"] == process)
        req_ids = sorted(req_by_process.get(process, []))
        structure_ids = sorted({messages[mid]["structure"]["id"] for mid in msg_ids if messages[mid]["structure"]["id"]})
        blocker_counts = Counter(requirements[cid]["implementation"]["status"] for cid in req_ids if requirements[cid]["gap"]["status"] == "OPEN")
        out[process] = {
            "schema_version": SCHEMA_VERSION,
            "identity": {"op": item["op"], "process": process, "version": process_version(raw)},
            "purpose": {"name": clean(raw.get("name")), "description": clean(raw.get("description"))},
            "participants": sorted(clean(x.get("participant_code")) for x in ent["participants"] if clean(x.get("participant_code"))),
            "operations": sorted(clean(x.get("operation_code")) for x in ent["operations"] if clean(x.get("operation_code"))),
            "procedures": sorted(clean(x.get("procedure_code")) for x in ent["procedures"] if clean(x.get("procedure_code"))),
            "transactions": trn_ids,
            "messages": msg_ids,
            "structures": structure_ids,
            "requirements": req_ids,
            "dependencies": {
                "classifiers": sorted({dep["classifier"] for cid in req_ids for dep in requirements[cid]["dependencies"]["classifiers"]}),
                "external_registries": sorted({dep["resource"] for cid in req_ids for dep in requirements[cid]["dependencies"]["external_registries"] if dep.get("resource")}),
            },
            "known_blockers": dict(sorted(blocker_counts.items())),
            "runtime": {"requirement_inventory_status": item["cfg"]["requirement_status"]},
            "sources": source_refs(raw.get("source_refs")),
            "project_state": {"snapshot": "data/project_state/current.json", "git_head": git_head, "verified_at": None},
        }
    return out


def build_structures_and_fields(
    records: list[dict[str, str]],
    structure_index: list[dict[str, Any]],
    field_index: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    inventory = legacy.structure_inventory(records)
    fields_by_structure: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in field_index:
        fields_by_structure[row.get("structure", "")].append(row)
    structures: dict[str, dict[str, Any]] = {}
    fields_docs: dict[str, dict[str, Any]] = {}
    for row in structure_index:
        sid = row["id"]
        inv = inventory.get(sid, {})
        refs = inv.get("source_refs", []) if isinstance(inv, dict) else []
        first_ref = refs[0] if refs else {}
        xsd_names = list(row.get("xsd_filename") or [])
        root = root_qname_payload(row)
        structures[sid] = {
            "schema_version": SCHEMA_VERSION,
            "identity": {"structure": sid, "versions": list(row.get("versions") or [])},
            "root": root,
            "xsd": {"declared_filename": xsd_names[0] if len(xsd_names) == 1 else None, "declared_filenames": xsd_names, "local_payload": row.get("xsd_status") == "AVAILABLE_LOCAL"},
            "source": {"source_refs": refs, "primary": first_ref or None},
            "usage": {"messages": list(row.get("used_by_messages") or []), "requirements": list(row.get("used_by_requirements") or [])},
            "field_index": {"path": f"data/fields/{safe_filename(sid)}.json", "count": int(row.get("field_count") or 0)},
            "dependencies": {"imports": list(inv.get("imports") or []) if isinstance(inv, dict) else []},
            "evidence": {"root_qname": clean(row.get("root_qname_evidence")), "xsd_status": clean(row.get("xsd_status"))},
            "known_gaps": [gap for gap in ["MISSING_ROOT_QNAME" if root["status"] in {"MISSING", "UNRESOLVED"} else None, "MISSING_XSD_PAYLOAD" if row.get("xsd_status") != "AVAILABLE_LOCAL" else None] if gap],
        }
        field_rows: list[dict[str, Any]] = []
        for field in sorted(fields_by_structure.get(sid, []), key=lambda x: (str(x.get("version", "")), str(x.get("field_id", "")), str(x.get("path", "")))):
            qname = None
            if re.fullmatch(r"\{[^}]+\}[A-Za-z_][\w.-]*", str(field.get("local_name", ""))):
                qname = field.get("local_name")
            min_occurs = field.get("min_occurs")
            required = None
            try:
                required = int(min_occurs) > 0
            except (TypeError, ValueError):
                pass
            field_rows.append(
                {
                    "field_id": clean(field.get("field_id")),
                    "path": clean(field.get("path")),
                    "qname": qname,
                    "datatype": clean(field.get("datatype")),
                    "min_occurs": field.get("min_occurs") if field.get("min_occurs") != "" else None,
                    "max_occurs": field.get("max_occurs") if field.get("max_occurs") != "" else None,
                    "required": required,
                    "source": {
                        "document": clean(field.get("source_document")),
                        "pdf_page": field.get("source_page"),
                        "table": clean(field.get("source_table")),
                        "item": clean(field.get("source_item")),
                    },
                    "evidence": clean(field.get("evidence_level")),
                }
            )
        fields_docs[sid] = {"schema_version": SCHEMA_VERSION, "structure": sid, "fields": field_rows}
    return structures, fields_docs


def build_classifiers(classifier_index: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    inventory = read_csv(ROOT / "codex_reports" / "OP32_P_MM_06" / "OP32_CLASSIFIER_SOURCE_INVENTORY.csv")
    rows_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in inventory:
        for cid in split_ids(row.get("classifier_id")):
            rows_by_id[cid].append(row)
    out: dict[str, dict[str, Any]] = {}
    for row in classifier_index:
        cid = row["classifier_id"]
        evidence_rows = rows_by_id.get(cid, [])
        sources = [
            {
                "document": clean(item.get("normative_source")),
                "pdf_page": legacy.normalize_page(item.get("page", "")),
                "table": clean(item.get("table")),
                "evidence": "AUDIT_DERIVED",
            }
            for item in evidence_rows
        ]
        if not sources and cid in legacy.OP32_CLASSIFIER_CATALOG_ONLY:
            cat = legacy.OP32_CLASSIFIER_CATALOG_ONLY[cid]
            sources.append({"document": cat["normative_source"], "pdf_page": legacy.normalize_page(cat["page"]), "table": "Table 9", "evidence": "CONFIRMED_PDF"})
        out[cid] = {
            "schema_version": SCHEMA_VERSION,
            "identity": {"classifier": cid},
            "official_name": clean(row.get("official_name")),
            "required_version": clean(row.get("version")),
            "machine_readable_payload": bool(row.get("machine_readable")),
            "sources": sources,
            "used_by": sorted(row.get("used_by") or []),
            "evidence": {"entity": "CONFIRMED_PDF", "payload": "MISSING" if not row.get("machine_readable") else "CONFIRMED_PRODUCTION"},
        }
    return out


def build_decision() -> dict[str, Any]:
    note_path = KB / "decisions" / "Decision_5.md"
    text = note_path.read_text(encoding="utf-8", errors="replace") if note_path.exists() else ""
    terms = ["To", "ReplyTo", "From", "FaultTo", "Action", "MessageID", "RelatesTo", "RelatesAction", "ProcedureID", "ConversationID", "Integration", "TrackID", "AcceptTime"]
    fields: dict[str, Any] = {}
    for term in terms:
        section_match = re.search(rf"## {re.escape(term)}\n\n(.*?)(?=\n## |\Z)", text, flags=re.S)
        section = section_match.group(1) if section_match else ""
        pages = sorted({int(x) for x in re.findall(r"page_(\d{3})", section)})
        fields[term] = {"status": "CONFIRMED_PDF" if "CONFIRMED_PDF" in section else "MISSING", "source_pages": pages}
    action_confirmed = "int://CP/PROCESS/VERSION/PRC/TRN/MSG" in text and "CONFIRMED_PDF" in text
    address_confirmed = "EAEU://" in text and "CONFIRMED_PDF" in text
    return {
        "schema_version": SCHEMA_VERSION,
        "identity": {"decision": "Decision No. 5"},
        "fields": fields,
        "action": {"format": "int://CP/PROCESS/VERSION/PRC/TRN/MSG" if action_confirmed else None, "status": "CONFIRMED_PDF" if action_confirmed else "MISSING"},
        "addressing": {"prefix": "EAEU://" if address_confirmed else None, "status": "CONFIRMED_PDF" if address_confirmed else "MISSING"},
        "sources": [{"source_id": "DECISION_5", "path": "sources/DECISION_5/FULL.md"}],
        "evidence": "CONFIRMED_PDF_TERM_INDEX",
    }


def field_node_id(structure: str, field: dict[str, Any]) -> str:
    material = f"{structure}\0{field.get('field_id')}\0{field.get('path')}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]
    return f"FIELD:{structure}:{digest}"


def resource_node_id(resource: str) -> str:
    return "EXTERNAL_REGISTRY:" + hashlib.sha256(resource.encode("utf-8")).hexdigest()[:16]


def recorded_dependency_node_id(dep_type: str | None, dep_id: str | None) -> str:
    material = f"{dep_type or ''}\0{dep_id or ''}"
    return "RECORDED_DEPENDENCY:" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def build_dependency_graph(
    requirements: dict[str, dict[str, Any]],
    messages: dict[str, dict[str, Any]],
    transactions: dict[str, dict[str, Any]],
    processes: dict[str, dict[str, Any]],
    structures: dict[str, dict[str, Any]],
    fields_docs: dict[str, dict[str, Any]],
    classifiers: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: dict[tuple[str, str, str], dict[str, Any]] = {}

    def add_node(node_id: str, kind: str, data: dict[str, Any] | None = None) -> None:
        nodes.setdefault(node_id, {"id": node_id, "kind": kind, "data": data or {}})

    def add_edge(kind: str, source: str, target: str, evidence: dict[str, Any]) -> None:
        key = (kind, source, target)
        edges.setdefault(key, {"type": kind, "from": source, "to": target, "evidence": evidence})

    for cid, req in requirements.items():
        add_node(cid, "REQUIREMENT", {"op": req["identity"]["op"], "message": req["identity"]["message"]})
        sid = req["structure"]["id"]
        if sid:
            add_edge("REQUIREMENT_USES_STRUCTURE", cid, sid, {"level": req["source"]["evidence"]["level"], "source": req["source"]["document"]})
        for field_ref in req["fields"]:
            for field in fields_docs.get(sid or "", {}).get("fields", []):
                if field.get("field_id") == field_ref.get("field_id") and field.get("path") == field_ref.get("path"):
                    fid = field_node_id(sid, field)
                    add_edge("REQUIREMENT_USES_FIELD", cid, fid, {"level": field_ref.get("evidence"), "source": field.get("source")})
        for dep in req["dependencies"]["classifiers"]:
            add_edge("REQUIREMENT_DEPENDS_ON_CLASSIFIER", cid, dep["classifier"], dep["evidence"])
        for dep in req["dependencies"]["external_registries"]:
            resource = dep.get("resource")
            if resource:
                rid = resource_node_id(resource)
                add_node(rid, "EXTERNAL_REGISTRY", {"name": resource})
                add_edge("REQUIREMENT_DEPENDS_ON_EXTERNAL_REGISTRY", cid, rid, dep["evidence"])
        for dep in req["dependencies"].get("recorded", []):
            if not dep.get("type") and not dep.get("id"):
                continue
            did = recorded_dependency_node_id(dep.get("type"), dep.get("id"))
            add_node(did, "RECORDED_DEPENDENCY", {"type": dep.get("type"), "id": dep.get("id"), "secondary": dep.get("secondary")})
            add_edge("REQUIREMENT_HAS_RECORDED_DEPENDENCY", cid, did, {"level": dep.get("evidence"), "source": req["project_state"]["snapshot"]})
        for rel in req["relationships"]["inherits_from"]:
            add_edge("REQUIREMENT_INHERITS_REQUIREMENT", cid, rel["requirement"], {"level": rel["source"]["evidence"], "source": rel["source"]})
        for rule in req["implementation"]["production_rules"]:
            rid = "RULE:" + hashlib.sha256(rule.encode("utf-8")).hexdigest()[:16]
            add_node(rid, "PRODUCTION_RULE", {"rule": rule})
            add_edge("REQUIREMENT_IMPLEMENTED_BY_RULE", cid, rid, {"level": "CONFIRMED_PRODUCTION", "source": req["implementation"]["production_files"]})
        test = req["verification"]["runtime"].get("test")
        if req["verification"]["runtime"]["status"] == "PRESENT" and test:
            tid = "TEST:" + hashlib.sha256(test.encode("utf-8")).hexdigest()[:16]
            add_node(tid, "TEST", {"test": test})
            add_edge("REQUIREMENT_VERIFIED_BY_TEST", cid, tid, {"level": "AUDIT_DERIVED", "source": test})

    for sid, structure in structures.items():
        add_node(sid, "STRUCTURE", {"root": structure["root"]})
    for sid, doc in fields_docs.items():
        for field in doc["fields"]:
            add_node(field_node_id(sid, field), "FIELD", {"structure": sid, "field_id": field.get("field_id"), "path": field.get("path")})
    for cid, classifier in classifiers.items():
        add_node(cid, "CLASSIFIER", {"name": classifier.get("official_name")})
    for mid, message in messages.items():
        add_node(mid, "MESSAGE", {"process": message["identity"]["process"]})
        sid = message["structure"]["id"]
        if sid:
            add_edge("MESSAGE_USES_STRUCTURE", mid, sid, {"level": "AUDIT_DERIVED", "source": message["sources"]})
    for tid, transaction in transactions.items():
        add_node(tid, "TRANSACTION", {"process": transaction["identity"]["process"]})
        mids = [transaction["messages"]["initiating"], *transaction["messages"]["responses"]]
        for mid in mids:
            if mid:
                add_edge("TRANSACTION_CONTAINS_MESSAGE", tid, mid, {"level": "AUDIT_DERIVED", "source": transaction["sources"]})
    for pid, process in processes.items():
        add_node(pid, "PROCESS", {"op": process["identity"]["op"]})
        for tid in process["transactions"]:
            add_edge("PROCESS_CONTAINS_TRANSACTION", pid, tid, {"level": "AUDIT_DERIVED", "source": process["sources"]})
    return {
        "schema_version": SCHEMA_VERSION,
        "nodes": sorted(nodes.values(), key=lambda x: (x["kind"], x["id"])),
        "edges": sorted(edges.values(), key=lambda x: (x["type"], x["from"], x["to"])),
    }


def write_entities(entities: dict[str, dict[str, dict[str, Any]]], fields_docs: dict[str, dict[str, Any]], decision: dict[str, Any]) -> None:
    for cid, obj in sorted(entities["requirements"].items()):
        write_machine(ENTITY_DIRS["requirements"] / f"{cid}.yaml", obj)
    for key in ["messages", "transactions", "processes", "structures", "classifiers"]:
        for entity_id, obj in sorted(entities[key].items()):
            write_machine(ENTITY_DIRS[key] / f"{safe_filename(entity_id)}.yaml", obj)
    for sid, obj in sorted(fields_docs.items()):
        write_machine(ENTITY_DIRS["fields"] / f"{safe_filename(sid)}.json", obj)
    write_machine(ENTITY_DIRS["decisions"] / "Decision_5.yaml", decision)


def write_project_snapshot(state: dict[str, Any], op26_gate: dict[str, Any], op49_gate: dict[str, Any]) -> None:
    input_paths = [
        ROOT / "codex_reports" / "OP23_P_SP_03" / "OP23_FINAL_REQUIREMENTS.csv",
        ROOT / "codex_reports" / "OP26_P_MM_01" / "OP26_REAUDIT_REQUIREMENTS.csv",
        ROOT / "codex_reports" / "OP26_P_MM_01" / "OP26_WHAT_IS_MISSING_FOR_FULL_IMPLEMENTATION.md",
        ROOT / "codex_reports" / "OP26_P_MM_01" / "OP26_FULL_IMPLEMENTATION_READINESS.md",
        ROOT / "codex_reports" / "OP32_P_MM_06" / "OP32_SOURCE_RECOVERY_REQUIREMENTS.csv",
        ROOT / "codex_reports" / "OP49_P_DS_01" / "OP49_REAUDIT_REQUIREMENTS.csv",
        ROOT / "codex_reports" / "OP49_P_DS_01" / "OP49_REAUDIT_AUDIT.md",
        REPORT_DIR / "KB_ENRICHMENT_GAPS.csv",
    ]
    inputs = []
    for path in input_paths:
        if path.exists():
            inputs.append({"path": str(path.relative_to(ROOT)), "sha256": legacy.sha256(path)})
    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "captured_at": now_iso(),
        "git_head": state["head"],
        "branch": state["branch"],
        "dirty_entries": state["dirty_entries"],
        "git_status": state["status"],
        "inputs": inputs,
        "op26_gate": op26_gate,
        "op49_gate": op49_gate,
        "note": "Timestamped PROJECT_STATE only; canonical entity files reference this snapshot and do not embed a build timestamp.",
    }
    write_machine(ENTITY_DIRS["project_state"] / "current.json", snapshot)


def indexes_from_entities(
    entities: dict[str, dict[str, dict[str, Any]]],
    fields_docs: dict[str, dict[str, Any]],
    graph: dict[str, Any],
) -> dict[str, Any]:
    req_idx = [
        {
            "canonical_id": cid,
            "op": obj["identity"]["op"],
            "process": obj["identity"]["process"],
            "message": obj["identity"]["message"],
            "implementation_status": obj["implementation"]["status"],
            "gap_status": obj["gap"]["status"],
            "gap_category": obj["gap"]["category"],
            "structure": obj["structure"]["id"],
            "atomic_qname_status": obj["structure"]["atomic_qname"]["status"],
            "path": f"data/requirements/{cid}.yaml",
        }
        for cid, obj in sorted(entities["requirements"].items())
    ]
    msg_idx = [{"message": mid, "process": obj["identity"]["process"], "structure": obj["structure"]["id"], "requirements": len(obj["requirements"]), "path": f"data/messages/{safe_filename(mid)}.yaml"} for mid, obj in sorted(entities["messages"].items())]
    trn_idx = [{"transaction": tid, "process": obj["identity"]["process"], "initiating_message": obj["messages"]["initiating"], "responses": obj["messages"]["responses"], "path": f"data/transactions/{safe_filename(tid)}.yaml"} for tid, obj in sorted(entities["transactions"].items())]
    proc_idx = [{"process": pid, "op": obj["identity"]["op"], "requirements": len(obj["requirements"]), "messages": len(obj["messages"]), "transactions": len(obj["transactions"]), "path": f"data/processes/{safe_filename(pid)}.yaml"} for pid, obj in sorted(entities["processes"].items())]
    struct_idx = [{"structure": sid, "root_qname": obj["root"]["clark_name"], "root_qname_status": obj["root"]["status"], "fields": obj["field_index"]["count"], "path": f"data/structures/{safe_filename(sid)}.yaml"} for sid, obj in sorted(entities["structures"].items())]
    fields_idx = [{"structure": sid, "fields": len(doc["fields"]), "path": f"data/fields/{safe_filename(sid)}.json"} for sid, doc in sorted(fields_docs.items())]
    classifier_idx = [{"classifier": cid, "machine_readable_payload": obj["machine_readable_payload"], "used_by": len(obj["used_by"]), "path": f"data/classifiers/{safe_filename(cid)}.yaml"} for cid, obj in sorted(entities["classifiers"].items())]
    gap_idx = [
        {
            "canonical_id": cid,
            "op": obj["identity"]["op"],
            "message": obj["identity"]["message"],
            "category": obj["gap"]["category"],
            "reason": obj["gap"]["reason"],
            "missing": obj["gap"]["missing"],
            "required_action": obj["gap"]["required_action"],
            "closure_criteria": obj["gap"]["closure_criteria"],
            "path": f"data/requirements/{cid}.yaml",
        }
        for cid, obj in sorted(entities["requirements"].items())
        if obj["gap"]["status"] == "OPEN"
    ]
    return {
        "requirements": req_idx,
        "messages": msg_idx,
        "transactions": trn_idx,
        "processes": proc_idx,
        "structures": struct_idx,
        "fields": fields_idx,
        "classifiers": classifier_idx,
        "dependencies": graph,
        "gaps": gap_idx,
    }


def write_indexes_v1(indexes: dict[str, Any]) -> None:
    for name, path in INDEX_FILES.items():
        payload = indexes[name]
        if name != "dependencies":
            payload = {"schema_version": SCHEMA_VERSION, "items": payload}
        write_machine(path, payload)
    counts = {name: len(indexes[name]) if isinstance(indexes[name], list) else len(indexes[name].get("items", [])) for name in ["requirements", "messages", "transactions", "processes", "structures", "fields", "classifiers", "gaps"]}
    graph = indexes["dependencies"]
    md = [
        "---",
        f'generated_by: "{GENERATOR}"',
        f'schema_version: "{SCHEMA_VERSION}"',
        "---",
        "",
        "# Machine-readable KB schema v1.0",
        "",
        "Canonical data lives under `knowledge_base/data/`. These JSON-syntax `.yaml` files are valid YAML 1.2 and are the source for the v1 generated indexes.",
        "",
    ]
    for name in ["requirements", "messages", "transactions", "processes", "structures", "fields", "classifiers", "gaps"]:
        md.append(f"- {name}: **{counts[name]}** — `indexes/{name}.json`")
    md.extend([f"- dependency nodes: **{len(graph['nodes'])}**", f"- dependency edges: **{len(graph['edges'])}**", ""])
    write_text(INDEX_DIR / "SCHEMA_V1.md", "\n".join(md))


def write_agent_start() -> None:
    text = """# Agent Start Here\n\n1. Start with the Knowledge Base; open the original PDF/XSD only when KB evidence is insufficient, conflicting, stale, or ambiguous.\n2. Keep `SOURCE`, `KNOWLEDGE`, and `PROJECT_STATE` separate.\n3. `AUDIT_DERIVED` and `HISTORICAL` are not normative proof.\n4. Never invent QName, namespace, version, classifier code, page, table, field path, or other missing normative data.\n5. Before any production edit, inspect the current Git state because OP23/OP26 and shared code may be changing in parallel.\n6. A production YAML rule by itself does not close a normative requirement.\n7. Closure requires normative evidence + production mapping + positive test + negative test + runtime proof.\n8. Canonical schema v1.0 data is under `data/`; generated machine indexes are under `indexes/`.\n"""
    write_text(KB / "AGENT_START_HERE.md", text)


def entity_required_keys(kind: str) -> list[str]:
    schema = schema_documents()[kind]
    return list(schema["required"])


def validate_machine_files(paths: Iterable[Path]) -> list[str]:
    errors: list[str] = []
    for path in sorted(set(paths)):
        if not path.exists():
            errors.append(f"missing machine-readable file: {path.relative_to(ROOT)}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"malformed machine-readable file {path.relative_to(ROOT)}: {type(exc).__name__}: {exc}")
            continue
        if data.get("schema_version") != SCHEMA_VERSION:
            errors.append(f"invalid schema_version in {path.relative_to(ROOT)}")
    return errors


def current_stale_sources(source_rows: list[dict[str, Any]]) -> list[str]:
    by_id = {row.get("source_id"): row for row in source_rows}
    stale: list[str] = []
    for cfg in legacy.SOURCES:
        sid = cfg["source_id"]
        path = cfg["path"]
        stored = by_id.get(sid, {}).get("sha256")
        current = legacy.sha256(path) if path.exists() else None
        if not stored or not current or stored != current:
            stale.append(sid)
    return stale


def deterministic_paths() -> list[Path]:
    paths: list[Path] = []
    for key, directory in ENTITY_DIRS.items():
        if key == "project_state":
            continue
        paths.extend(path for path in directory.rglob("*") if path.is_file())
    paths.extend(path for path in SCHEMA_DIR.rglob("*.json") if path.is_file())
    paths.extend(path for path in INDEX_FILES.values() if path.exists())
    paths.append(INDEX_DIR / "SCHEMA_V1.md")
    paths.append(KB / "AGENT_START_HERE.md")
    return sorted(set(paths))


def deterministic_fingerprint() -> str:
    digest = hashlib.sha256()
    for path in deterministic_paths():
        digest.update(str(path.relative_to(ROOT)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def validate_all(
    entities: dict[str, dict[str, dict[str, Any]]],
    fields_docs: dict[str, dict[str, Any]],
    indexes: dict[str, Any],
    source_rows: list[dict[str, Any]],
    pilot: dict[str, Any],
    reproducibility: dict[str, Any],
    op26_gate: dict[str, Any],
    op49_gate: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    errors: list[str] = []
    warnings: list[dict[str, str]] = []
    requirements = entities["requirements"]
    messages = entities["messages"]
    transactions = entities["transactions"]
    structures = entities["structures"]
    classifiers = entities["classifiers"]

    errors.extend(pilot.get("errors", []))
    ids = list(requirements)
    duplicates = [item for item, count in Counter(ids).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate canonical IDs: {duplicates[:20]}")
    for cid, req in requirements.items():
        if req.get("schema_version") != SCHEMA_VERSION:
            errors.append(f"invalid schema_version: {cid}")
        if req.get("identity", {}).get("canonical_id") != cid:
            errors.append(f"missing/mismatched canonical_id: {cid}")
        missing_keys = [key for key in entity_required_keys("requirement") if key not in req]
        if missing_keys:
            errors.append(f"requirement {cid} missing keys: {missing_keys}")
        message = req["identity"]["message"]
        if message not in messages:
            errors.append(f"requirement {cid} references nonexistent message {message}")
        sid = req["structure"]["id"]
        if sid and sid not in structures:
            errors.append(f"requirement {cid} references nonexistent confirmed structure {sid}")
        for relation in req["relationships"]["inherits_from"]:
            if relation["requirement"] not in requirements:
                errors.append(f"broken canonical relation {cid} -> {relation['requirement']}")
        for dep in req["dependencies"]["classifiers"]:
            if dep["classifier"] not in classifiers:
                errors.append(f"requirement {cid} references nonexistent classifier {dep['classifier']}")
        if req["gap"]["status"] == "OPEN" and not req["gap"]["closure_criteria"]:
            errors.append(f"OPEN GAP without closure criterion: {cid}")

        if not any(req["normative"]["plain_language"].values()):
            warnings.append({"severity": "WARNING", "code": "MISSING_PLAIN_LANGUAGE", "entity": cid, "detail": "No confirmed plain-language meaning/purpose was migrated."})
        aq = req["structure"]["atomic_qname"]
        if aq["status"] != "RESOLVED_CLARK":
            warnings.append({"severity": "INCOMPLETE_EVIDENCE", "code": "MISSING_QNAME", "entity": cid, "detail": f"Atomic QName status: {aq['status']}"})
        if aq.get("namespace") is None:
            warnings.append({"severity": "INCOMPLETE_EVIDENCE", "code": "MISSING_NAMESPACE", "entity": cid, "detail": "Atomic namespace is not confirmed."})
        if req["verification"]["positive_test"]["status"] != "PRESENT":
            warnings.append({"severity": "WARNING", "code": "MISSING_POSITIVE_TEST", "entity": cid, "detail": req["verification"]["positive_test"]["status"]})
        if req["verification"]["negative_test"]["status"] != "PRESENT":
            warnings.append({"severity": "WARNING", "code": "MISSING_NEGATIVE_TEST", "entity": cid, "detail": req["verification"]["negative_test"]["status"]})
        if req["verification"]["runtime"]["status"] != "PRESENT":
            warnings.append({"severity": "WARNING", "code": "MISSING_RUNTIME_PROOF", "entity": cid, "detail": req["verification"]["runtime"]["status"]})

    for cid, classifier in classifiers.items():
        if not classifier["machine_readable_payload"]:
            warnings.append({"severity": "INCOMPLETE_EVIDENCE", "code": "MISSING_CLASSIFIER_PAYLOAD", "entity": cid, "detail": "Confirmed classifier entity has no registered machine-readable payload."})
    for sid, structure in structures.items():
        if structure["root"]["clark_name"] is None:
            warnings.append({"severity": "INCOMPLETE_EVIDENCE", "code": "MISSING_STRUCTURE_QNAME", "entity": sid, "detail": structure["root"]["status"]})
        if structure["root"]["namespace"] is None:
            warnings.append({"severity": "INCOMPLETE_EVIDENCE", "code": "MISSING_STRUCTURE_NAMESPACE", "entity": sid, "detail": structure["root"]["status"]})

    for tid, transaction in transactions.items():
        mids = [transaction["messages"]["initiating"], *transaction["messages"]["responses"]]
        for mid in mids:
            if mid and mid not in messages:
                errors.append(f"transaction {tid} references nonexistent message {mid}")
    graph = indexes["dependencies"]
    node_ids = {node["id"] for node in graph["nodes"]}
    broken_graph = [edge for edge in graph["edges"] if edge["from"] not in node_ids or edge["to"] not in node_ids]
    if broken_graph:
        errors.append(f"dependency graph has {len(broken_graph)} broken endpoints")

    counts_by_op = Counter(req["identity"]["op"] for req in requirements.values())
    for op, expected in EXPECTED_CANONICAL_CURRENT.items():
        if counts_by_op.get(op, 0) != expected:
            errors.append(f"{op} canonical count {counts_by_op.get(op, 0)} != {expected}")
    if op26_gate.get("status") != "PASS":
        errors.append(f"OP26 reconciliation gate failed: {op26_gate}")
    if op49_gate.get("status") != "PASS":
        errors.append(f"OP49 import gate failed: {op49_gate}")
    if counts_by_op.get("OP22") == 1609:
        op22_status = Counter(req["implementation"]["status"] for req in requirements.values() if req["identity"]["op"] == "OP22")
        if op22_status.get("IMPLEMENTED_CONFIRMED", 0) != 1263:
            errors.append(f"OP22 IMPLEMENTED_CONFIRMED {op22_status.get('IMPLEMENTED_CONFIRMED', 0)} != 1263")
        if 1609 - op22_status.get("IMPLEMENTED_CONFIRMED", 0) != 346:
            errors.append("OP22 OPEN count != 346")

    op32 = [req for req in requirements.values() if req["identity"]["op"] == "OP32"]
    op32_resolved = sum(req["structure"]["atomic_qname"]["status"] == "RESOLVED_CLARK" for req in op32)
    op32_unresolved = len(op32) - op32_resolved
    if op32_resolved != 0 or op32_unresolved != 170:
        errors.append(f"OP32 atomic QName invariant violated: resolved={op32_resolved} unresolved={op32_unresolved}")

    op26 = [req for req in requirements.values() if req["identity"]["op"] == "OP26"]
    op49 = [req for req in requirements.values() if req["identity"]["op"] == "OP49"]
    op26_source_trace = sum(
        bool(req["normative"]["source_text"])
        and bool(req["source"]["pdf_page"])
        and bool(req["source"]["table"])
        and bool(req["source"]["item"])
        for req in op26
    )
    op49_source_trace = sum(
        bool(req["normative"]["source_text"])
        and bool(req["source"]["pdf_page"])
        and bool(req["source"]["table"])
        and bool(req["source"]["item"])
        for req in op49
    )
    if op26_source_trace != 239:
        errors.append(f"OP26 source trace complete {op26_source_trace} != 239")
    if op49_source_trace != 166:
        errors.append(f"OP49 source trace complete {op49_source_trace} != 166")

    op49_status = Counter(req["implementation"]["status"] for req in op49)
    op49_implemented = op49_status.get("IMPLEMENTED_CONFIRMED", 0)
    op49_open = sum(req["gap"]["status"] == "OPEN" for req in op49)
    if op49_implemented != 0 or op49_open != 166:
        errors.append(f"OP49 strict closure invariant violated: implemented={op49_implemented} open={op49_open}")

    duplicate_source_item_5 = sorted(
        (
            req["identity"]["canonical_id"],
            req["identity"].get("source_occurrence"),
            req["source"].get("item"),
        )
        for req in op26
        if req["identity"]["message"] == "P.MM.01.MSG.028" and req["source"].get("item") == "5"
    )
    expected_duplicate_source_item_5 = [
        ("OP26.P_MM_01.P.MM.01.MSG.028.REQ.005", 1, "5"),
        ("OP26.P_MM_01.P.MM.01.MSG.028.REQ.005.2", 2, "5"),
    ]
    if duplicate_source_item_5 != expected_duplicate_source_item_5:
        errors.append(f"OP26 duplicate source item 5 representation mismatch: {duplicate_source_item_5}")

    machine_paths = [
        *(ENTITY_DIRS["requirements"] / f"{cid}.yaml" for cid in requirements),
        *(ENTITY_DIRS["messages"] / f"{safe_filename(cid)}.yaml" for cid in messages),
        *(ENTITY_DIRS["transactions"] / f"{safe_filename(cid)}.yaml" for cid in transactions),
        *(ENTITY_DIRS["processes"] / f"{safe_filename(cid)}.yaml" for cid in entities["processes"]),
        *(ENTITY_DIRS["structures"] / f"{safe_filename(cid)}.yaml" for cid in structures),
        *(ENTITY_DIRS["classifiers"] / f"{safe_filename(cid)}.yaml" for cid in classifiers),
        *(ENTITY_DIRS["fields"] / f"{safe_filename(cid)}.json" for cid in fields_docs),
        ENTITY_DIRS["decisions"] / "Decision_5.yaml",
        ENTITY_DIRS["project_state"] / "current.json",
        *INDEX_FILES.values(),
    ]
    errors.extend(validate_machine_files(machine_paths))

    requirement_files = list(ENTITY_DIRS["requirements"].glob("*.yaml"))
    expected_req_files = {f"{cid}.yaml" for cid in requirements}
    actual_req_files = {path.name for path in requirement_files}
    missing_req_files = sorted(expected_req_files - actual_req_files)
    extra_req_files = sorted(actual_req_files - expected_req_files)
    if missing_req_files:
        errors.append(f"missing requirement files: {missing_req_files[:20]}")
    if extra_req_files:
        errors.append(f"unexpected/stale requirement files: {extra_req_files[:20]}")

    stale = current_stale_sources(source_rows)
    if stale:
        errors.append(f"stale sources: {stale}")
    broken_md = legacy.validate_links()
    if broken_md:
        errors.append(f"broken internal Markdown links: {len(broken_md)}")
    if reproducibility.get("status") != "PASS":
        errors.append(f"reproducibility failed: {reproducibility}")

    legacy_qnames = load_json(INDEX_DIR / "qname_index.json", {}) or {}
    legacy_stats = load_json(REPORT_DIR / "KB_BUILD_STATS.json", {}) or {}
    gaps = indexes["gaps"]
    gaps_with_closure = sum(bool(item.get("closure_criteria")) for item in gaps)
    validation = {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if not errors else "FAIL",
        "generated_at": now_iso(),
        "requirements_scope": sum(EXPECTED_SCOPE.values()),
        "requirements_canonical": len(requirements),
        "canonical_requirement_files": len(requirement_files),
        "by_op": {op: {"canonical": counts_by_op.get(op, 0), "scope": EXPECTED_SCOPE[op]} for op in EXPECTED_SCOPE},
        "messages_migrated": len(messages),
        "transactions_migrated": len(transactions),
        "processes_migrated": len(entities["processes"]),
        "structures_migrated": len(structures),
        "fields_migrated": sum(len(doc["fields"]) for doc in fields_docs.values()),
        "classifiers_migrated": len(classifiers),
        "dependency_nodes": len(graph["nodes"]),
        "dependency_edges": len(graph["edges"]),
        "open_gaps": len(gaps),
        "gaps_with_closure_criteria": gaps_with_closure,
        "qnames_resolved": len(legacy_qnames.get("resolved", [])),
        "qnames_unresolved": len(legacy_qnames.get("unresolved", [])),
        "qname_conflicts": int(legacy_stats.get("qname_conflicts", 0)),
        "op32_atomic_qname_resolved": op32_resolved,
        "op32_atomic_qname_unresolved": op32_unresolved,
        "op26_source_trace_complete": op26_source_trace,
        "op49_source_trace_complete": op49_source_trace,
        "op49_implemented_confirmed": op49_implemented,
        "op49_open": op49_open,
        "duplicate_source_item_handling": {
            "source_item": "5",
            "canonical_entities": [row[0] for row in duplicate_source_item_5],
            "source_occurrences": [row[1] for row in duplicate_source_item_5],
            "status": "PASS" if duplicate_source_item_5 == expected_duplicate_source_item_5 else "FAIL",
        },
        "duplicate_canonical_ids": len(duplicates),
        "missing_requirement_files": len(missing_req_files),
        "unexpected_requirement_files": len(extra_req_files),
        "broken_canonical_relations": sum("broken canonical relation" in error for error in errors),
        "broken_dependency_graph_endpoints": len(broken_graph),
        "broken_internal_links": len(broken_md),
        "stale_sources": len(stale),
        "warnings": len(warnings),
        "warning_counts": dict(sorted(Counter(row["code"] for row in warnings).items())),
        "errors": errors,
        "pilot": pilot,
        "op26_gate": op26_gate,
        "op49_gate": op49_gate,
        "reproducibility": reproducibility,
        "production_files_changed": 0,
        "shared_engine_changed": 0,
        "gui_changed": 0,
    }
    return validation, warnings


def write_warning_csv(warnings: list[dict[str, str]]) -> None:
    from io import StringIO
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=["severity", "code", "entity", "detail"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(warnings)
    payload = buf.getvalue()
    write_text(REPORT_DIR / "KB_SCHEMA_V1_GAPS.csv", payload)


def write_scope_gap_csv(gaps: list[dict[str, Any]]) -> None:
    from io import StringIO

    fieldnames = [
        "canonical_id", "op", "message", "category", "reason", "missing",
        "required_action", "closure_criteria", "path",
    ]
    rows: list[dict[str, str]] = []
    for gap in gaps:
        row: dict[str, str] = {}
        for key in fieldnames:
            value = gap.get(key)
            row[key] = stable_json(value).strip() if isinstance(value, (list, dict)) else str(value or "")
        rows.append(row)
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    write_text(REPORT_DIR / "KB_CANONICAL_SCOPE_2894_GAPS.csv", buf.getvalue())


def write_reports(
    validation: dict[str, Any],
    pilot: dict[str, Any],
    initial_existing: set[Path],
    current_state: dict[str, Any],
) -> None:
    write_machine(REPORT_DIR / "KB_SCHEMA_V1_VALIDATION.json", validation)
    write_machine(REPORT_DIR / "KB_CANONICAL_SCOPE_2894_VALIDATION.json", validation)
    design = f"""# KB Schema v1.0 Design\n\n## Canonical model\n\n`SOURCE → KNOWLEDGE → PROJECT_STATE` remains the architectural boundary. Canonical entity files live under `knowledge_base/data/`; generated indexes live under `knowledge_base/indexes/`. Existing Markdown/source notes are retained.\n\nAll canonical `*.yaml` files use JSON syntax, which is a valid YAML 1.2 subset. This gives deterministic stdlib serialization without adding PyYAML. Unknown scalar values are `null`; known-empty collections are `[]`.\n\n## Timestamp policy\n\nCanonical entities do not embed build timestamps. They reference `data/project_state/current.json`, the only timestamped canonical project-state output, so repeated builds do not rewrite thousands of entity files.\n\n## Evidence policy\n\nNormative and project-state evidence remain distinct. `CONFIRMED_PRODUCTION` and `CONFIRMED_RUNTIME` are never promoted to normative proof. OP32 atomic QName remains independent from structure-root QName.\n\n## Schemas\n\nJSON Schema documents are in `knowledge_base/schemas/` with `schema_version = \"1.0\"`. Custom deterministic validation enforces cross-entity invariants that JSON Schema alone cannot prove.\n"""
    write_text(REPORT_DIR / "KB_SCHEMA_V1_DESIGN.md", design)
    migration = "# KB Schema v1.0 Migration\n\n"
    migration += "The migration reused the existing SOURCE extraction and current canonical KB inputs; no mass PDF extraction was performed.\n\n"
    migration += "## Pilot\n\n"
    migration += f"- Status: **{pilot['status']}**\n"
    for name, cid in pilot["pilot_ids"].items():
        migration += f"- {name}: `{cid}`\n"
    migration += "\n## Full migration\n\n"
    migration += f"- Requirements: {validation['requirements_canonical']}\n- Messages: {validation['messages_migrated']}\n- Transactions: {validation['transactions_migrated']}\n- Processes: {validation['processes_migrated']}\n- Structures: {validation['structures_migrated']}\n- Fields: {validation['fields_migrated']}\n- Classifiers: {validation['classifiers_migrated']}\n"
    migration += f"- OP49 gate: `{validation['op49_gate']['status']}`; canonical OP49 rows: {validation['by_op']['OP49']['canonical']}\n"
    write_text(REPORT_DIR / "KB_SCHEMA_V1_MIGRATION.md", migration)

    scope_migration = f"""# Canonical KB Scope 2894 Migration

## Baseline

- Schema version: `{SCHEMA_VERSION}`
- Superseded known scope: **2849**.
- Previous Schema v1 canonical entities: **2690** (OP49 was not materialized).
- New canonical scope: **2894** atomic requirements.
- Canonical entity delta: **+204** = OP26 **+38** + OP49 **+166**.

## New scope

| OP | Canonical requirements |
|---|---:|
| OP22 | {validation['by_op']['OP22']['canonical']} |
| OP23 | {validation['by_op']['OP23']['canonical']} |
| OP26 | {validation['by_op']['OP26']['canonical']} |
| OP32 | {validation['by_op']['OP32']['canonical']} |
| OP49 | {validation['by_op']['OP49']['canonical']} |
| **TOTAL** | **{validation['requirements_canonical']}** |

## Identity rule for duplicate source numbering

Normative source numbering remains source metadata. For OP26 MSG.028 the two distinct Table 21 rows both remain source item `5`; canonical identity uses `source_occurrence` and a deterministic canonical disambiguator. No synthetic normative item number is introduced.

## Validation

- Status: **{validation['status']}**
- Duplicate canonical IDs: **{validation['duplicate_canonical_ids']}**
- Missing requirement files: **{validation['missing_requirement_files']}**
- Broken canonical relations: **{validation['broken_canonical_relations']}**
- Broken internal links: **{validation['broken_internal_links']}**
- Stale sources: **{validation['stale_sources']}**
- Reproducibility: **{validation['reproducibility']['status']}**
"""
    write_text(REPORT_DIR / "KB_CANONICAL_SCOPE_2894_MIGRATION.md", scope_migration)

    op26_report = f"""# OP26 Canonical Reconciliation: 201 → 239

The original `26_ОП.pdf` is authoritative for this reconciliation.

- Before: **201** canonical records.
- After: **239** atomic canonical requirements.
- New atomic requirements: **38**.
- MSG.002: **50 → 87** canonical atomic rows. Old REQ.050 had collapsed source items 50–87; the primary PDF shows 38 separately numbered rows across PDF pages 224–231.
- MSG.028: **7 → 8** canonical atomic rows. Table 21 contains two different source rows numbered `5` on PDF pages 233 and 234.
- Table 19 item 84 remains `OPEN_NORMATIVE_AMBIGUITY` because the primary publication is truncated at PDF page 230. No missing tail was inferred.
- Source trace complete: **{validation['op26_source_trace_complete']} / 239**.

## Duplicate source item 5

- First canonical entity: `OP26.P_MM_01.P.MM.01.MSG.028.REQ.005`, source item `5`, occurrence `1`.
- Second canonical entity: `OP26.P_MM_01.P.MM.01.MSG.028.REQ.005.2`, source item `5`, occurrence `2`.
- The `.2` suffix is a canonical disambiguator only. It is not a normative requirement number.

Project-state implementation evidence was not copied from the old merged rows into newly split atomic rows. Their status remains open until requirement-level implementation/runtime proof is synchronized.

## Project-state snapshot from the completed re-audit

These are audit/project-state counts, not additional normative requirements:

- Atomic source requirements: **239**.
- Current production structured rules observed by the re-audit: **159**.
- Atomic production mappings missing at that checkpoint: **80**.
- Classified as safe to implement from already-confirmed local normative text: **52**.
- Classified as blocked by missing/conflicting external information: **28**.
- `MISSING_XSD`: **8** structure payloads.
- Version placeholders: **4**.
- `UNRESOLVED_QNAME`: **198** audit items.
- Classifier dependencies: **22** atomic checks (11 `codeListId` + 11 membership).
- External-registry dependencies: **11**.
- Source conflicts: **5**.
- Normative ambiguity: **1** (Table 19 item 84).

These counts remain PROJECT_STATE/AUDIT_DERIVED and are not promoted to normative proof.
"""
    write_text(REPORT_DIR / "KB_OP26_239_RECONCILIATION.md", op26_report)

    op49_counts = validation["op49_gate"].get("message_counts", {})
    op49_report = f"""# OP49 Canonical Import: 166

Validated input: `codex_reports/OP49_P_DS_01/OP49_REAUDIT_REQUIREMENTS.csv`.

Primary-source boundary checks were repeated against `/Users/tema/Documents/Work/Документы_xml/49_ОП.pdf`: PDF page 79 starts Table 10 / MSG.001, page 85 contains Table 10 requirement 35, page 103 starts Table 14 / MSG.006, and page 108 contains Table 14 requirements 32–37. These directly confirm the two ranges missed by the superseded 159-row checkpoint.

- Imported: **166** canonical requirements / **166** unique IDs.
- MSG.001: **{op49_counts.get('P.DS.01.MSG.001', 0)}**
- MSG.002: **{op49_counts.get('P.DS.01.MSG.002', 0)}**
- MSG.003: **0**
- MSG.004: **{op49_counts.get('P.DS.01.MSG.004', 0)}**
- MSG.005: **{op49_counts.get('P.DS.01.MSG.005', 0)}**
- MSG.006: **{op49_counts.get('P.DS.01.MSG.006', 0)}**
- Missing source text: **{validation['op49_gate'].get('missing_source_text', 0)}**
- Missing source trace: **{validation['op49_gate'].get('missing_source_trace', 0)}**
- Missing closure criteria: **{validation['op49_gate'].get('missing_closure_criteria', 0)}**
- Strict `IMPLEMENTED_CONFIRMED`: **{validation['op49_implemented_confirmed']}**
- Strict OPEN: **{validation['op49_open']}**
- Canonical source trace complete: **{validation['op49_source_trace_complete']} / 166**

The re-audit records three source-conflict patterns affecting 35 requirement rows. The migration preserves those conflicts as unresolved evidence and does not select either side by inference.

OP49 audit dependency identifiers are preserved as `AUDIT_DERIVED` recorded-dependency nodes in the dependency graph. The country→currency dependency remains the descriptive `OFFICIAL_MEMBER_STATE_CURRENCY_CODE_MAPPING`; no classifier number or payload is invented.
"""
    write_text(REPORT_DIR / "KB_OP49_166_IMPORT.md", op49_report)

    created = sorted(path for path in CHANGED_FILES if path not in initial_existing)
    modified = sorted(path for path in CHANGED_FILES if path in initial_existing)
    audit = "# KB Schema v1.0 Audit\n\n"
    audit += f"- Status: **{validation['status']}**\n- Schema version: **{SCHEMA_VERSION}**\n- Reproducibility: **{validation['reproducibility']['status']}**\n"
    audit += f"- Requirements: **{validation['requirements_canonical']} / {validation['requirements_scope']}**\n"
    for op in ["OP22", "OP23", "OP26", "OP32", "OP49"]:
        row = validation["by_op"][op]
        audit += f"- {op}: **{row['canonical']} / {row['scope']}**\n"
    audit += f"- Dependency graph: {validation['dependency_nodes']} nodes / {validation['dependency_edges']} edges\n"
    audit += f"- Open gaps: {validation['open_gaps']}; with closure criteria: {validation['gaps_with_closure_criteria']}\n"
    audit += f"- OP32 atomic QName: {validation['op32_atomic_qname_resolved']} resolved / {validation['op32_atomic_qname_unresolved']} unresolved\n"
    audit += f"- Broken canonical relations: {validation['broken_canonical_relations']}\n- Broken internal links: {validation['broken_internal_links']}\n- Stale sources: {validation['stale_sources']}\n"
    audit += "\n## Git safety\n\n"
    audit += "- Production files changed by this builder: 0\n- Shared engine changed by this builder: 0\n- GUI changed by this builder: 0\n"
    audit += f"- Git HEAD: `{current_state['head']}`\n"
    audit += "\n## CURRENT_BUILDER_INVOCATION_CREATED_FILES\n\n" + ("\n".join(f"- `{path.relative_to(ROOT)}`" for path in created) or "- None") + "\n"
    audit += "\n## CURRENT_BUILDER_INVOCATION_MODIFIED_FILES\n\n" + ("\n".join(f"- `{path.relative_to(ROOT)}`" for path in modified) or "- None") + "\n"
    audit += "\n## EXACT_SESSION_MANIFEST\n\nSee `KB_CANONICAL_SCOPE_2894_SESSION_FILES.md` for the comparison against the SHA-256 snapshot captured before this migration session modified the allowed directories. See `KB_SCHEMA_V1_INITIAL_GIT_STATUS.txt` for the initial repository status snapshot.\n"
    if validation["errors"]:
        audit += "\n## Errors\n\n" + "\n".join(f"- {error}" for error in validation["errors"]) + "\n"
    write_text(REPORT_DIR / "KB_SCHEMA_V1_AUDIT.md", audit)


def build_once(initial_existing: set[Path]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    write_schemas()
    schema_errors = validate_schema_documents()
    if schema_errors:
        raise RuntimeError("; ".join(schema_errors))
    records, op26_gate, op49_gate = current_records()
    source_rows, source_by_id, printed = source_state()
    structure_index = load_json(INDEX_DIR / "structure_index.json", []) or []
    field_index = load_json(INDEX_DIR / "field_index.json", []) or []
    classifier_index = load_json(INDEX_DIR / "classifier_index.json", []) or []
    state = git_state()
    requirements, _, _ = build_requirements(records, source_by_id, printed, structure_index, field_index, classifier_index, state["head"])
    pilot = pilot_validation(requirements)
    if pilot["status"] != "PASS":
        raise RuntimeError("Pilot migration failed: " + "; ".join(pilot["errors"]))
    message_catalog, transaction_catalog, process_catalog, _ = entity_catalog()
    messages = build_messages(requirements, message_catalog, state["head"])
    transactions = build_transactions(transaction_catalog, state["head"])
    processes = build_processes(requirements, messages, transactions, process_catalog, state["head"])
    structures, fields_docs = build_structures_and_fields(records, structure_index, field_index)
    classifiers = build_classifiers(classifier_index)
    decision = build_decision()
    entities = {
        "requirements": requirements,
        "messages": messages,
        "transactions": transactions,
        "processes": processes,
        "structures": structures,
        "classifiers": classifiers,
    }
    graph = build_dependency_graph(requirements, messages, transactions, processes, structures, fields_docs, classifiers)
    indexes = indexes_from_entities(entities, fields_docs, graph)
    write_entities(entities, fields_docs, decision)
    write_project_snapshot(state, op26_gate, op49_gate)
    write_indexes_v1(indexes)
    write_agent_start()
    return {"entities": entities, "fields_docs": fields_docs, "indexes": indexes, "source_rows": source_rows}, pilot, {"op26": op26_gate, "op49": op49_gate}, state, {"decision": decision}


def main() -> int:
    initial_existing = {path.resolve() for base in [KB, REPORT_DIR] if base.exists() for path in base.rglob("*") if path.is_file()}
    first, first_pilot, first_gates, _, _ = build_once(initial_existing)
    fingerprint_1 = deterministic_fingerprint()
    second, second_pilot, second_gates, final_state, _ = build_once(initial_existing)
    fingerprint_2 = deterministic_fingerprint()
    reproducibility = {
        "status": "PASS" if fingerprint_1 == fingerprint_2 else "FAIL",
        "first_fingerprint": fingerprint_1,
        "second_fingerprint": fingerprint_2,
        "excluded_timestamped_output": "data/project_state/current.json",
    }
    if first_pilot != second_pilot or first_gates != second_gates:
        reproducibility["status"] = "FAIL"
        reproducibility["input_consistency"] = "pilot_or_import_gate_changed_between_passes"

    validation, warnings = validate_all(
        second["entities"], second["fields_docs"], second["indexes"], second["source_rows"], second_pilot, reproducibility,
        second_gates["op26"], second_gates["op49"]
    )
    write_warning_csv(warnings)
    write_scope_gap_csv(second["indexes"]["gaps"])
    write_reports(validation, second_pilot, initial_existing, final_state)
    print(stable_json(validation), end="")
    return 0 if validation["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
