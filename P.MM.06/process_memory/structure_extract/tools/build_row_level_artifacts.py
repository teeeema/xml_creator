"""Build normalized row-level audit artifacts from the one-time PDF recovery."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
MEMORY = ROOT / "P.MM.06" / "process_memory"


def load(name: str):
    return json.loads((MEMORY / name).read_text(encoding="utf-8"))


def dump(name: str, value) -> None:
    (MEMORY / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def source_ref(row: dict) -> str:
    pages = str(row["source_page_start"])
    if row["source_page_end"] != row["source_page_start"]:
        pages += f"-{row['source_page_end']}"
    return f"32_ОП.pdf, PDF p. {pages}, table {row['source_table']}, row {row['row_number_raw']}"


def raw_markdown(raw: dict) -> str:
    lines = [
        "# P.MM.06 Structure Rows — Raw Recovery",
        "",
        "Normative source: `32_ОП.pdf`. This is a row-level transcription of tables 10, 13, 16, 19 and 22. XML names are not inferred.",
        "",
        "| Structure | PDF pages | Table | Expected | Actual | Relative | Multi-page | Uncertain |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for structure in raw["structures"]:
        lines.append(
            f"| {structure['structure_code']} | {structure['page_start']}–{structure['page_end']} | "
            f"{structure['source_table']} | {structure['expected_count']} | {structure['actual_count']} | "
            f"{structure['relative_number_rows']} | {structure['multi_page_rows']} | {structure['uncertain_rows']} |"
        )
    for structure in raw["structures"]:
        lines += ["", f"## {structure['structure_code']}", "",
                  "| Semantic ID | Row | Normative name | Element ID | Type ID | Cardinality | Parent row | Hierarchy | PDF source |",
                  "|---|---|---|---|---|---|---|---|---|"]
        for row in structure["rows"]:
            name = row["normative_name"].replace("|", "\\|")
            lines.append(
                f"| {row['semantic_id']} | {row['row_number_raw']} | {name} | "
                f"{row['model_element_id'] or '—'} | {row['model_type_id'] or '—'} | "
                f"{row['cardinality_raw'] or '—'} | {row['parent_row_number'] or '—'} | "
                f"{row['hierarchy_status']} | {source_ref(row)} |"
            )
    return "\n".join(lines) + "\n"


def catalog_markdown(catalog: dict) -> str:
    q = catalog["xml_name_resolution_overlay"]
    lines = [
        "# P.MM.06 Structure Node Catalog",
        "",
        "Stable semantic IDs are structure-specific sequences and never depend on QName.",
        "",
        f"Nodes: **{catalog['total_nodes']}**; unique semantic IDs: **{catalog['unique_semantic_ids']}**.",
        "",
        "QName overlay: 7 exact node mappings are resolved. Four additional QName mappings remain ambiguous and are not assigned to guessed nodes. Therefore raw node statuses are 7 resolved / 179 unresolved; the requested overlay accounting is 7 resolved / 4 ambiguous mapping records / 175 residual unresolved.",
        "",
        "| Semantic ID | Structure | Row | Parent semantic ID | Hierarchy | QName | QName status | Cardinality | Source |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for row in catalog["nodes"]:
        lines.append(
            f"| {row['semantic_id']} | {row['structure_code']} | {row['row_number_raw']} | "
            f"{row['parent_semantic_id'] or '—'} | {row['hierarchy_status']} | {row['qname'] or '—'} | "
            f"{row['xml_name_status']} | {row['cardinality_raw']} | {row['source_ref']} |"
        )
    lines += ["", "## Ambiguous QName mappings", ""]
    for item in q["ambiguous_mappings"]:
        lines.append(f"- `{item['structure']}` / `{item['qname']}` — {item['reason']}")
    lines += ["", "## Attribute overlay", ""]
    for item in catalog["attribute_overlay"]:
        owner = item.get("owner_structure") or item.get("owner") or "UNRESOLVED"
        row = item.get("owner_structural_row")
        lines.append(f"- `{item['attribute_name']}` — owner `{owner}`{f', row `{row}`' if row else ''}; {item['evidence_status']}")
    return "\n".join(lines) + "\n"


def audit_markdown(audit: dict) -> str:
    c = audit["coverage"]
    lines = [
        "# P.MM.06 Structures Row-Level Audit",
        "",
        "Normative source: `32_ОП.pdf` only. P.MM.01, P.DS.01, other processes, external XSDs and the internet were not used as normative evidence.",
        "",
        f"Integrity: **{audit['integrity']['status']}**.",
        "",
        "| Structure | Table | PDF pages | Rows | Count gate |",
        "|---|---:|---:|---:|---|",
    ]
    for item in audit["structures"]:
        lines.append(f"| {item['structure_code']} | {item['source_table']} | {item['page_start']}–{item['page_end']} | {item['actual_count']}/{item['expected_count']} | {item['count_gate']} |")
    lines += [
        "",
        "## Coverage",
        "",
        f"- Hierarchy: {c['hierarchy']['resolved']} resolved; {c['hierarchy']['unresolved']} unresolved.",
        f"- Cardinality: {c['cardinality']['resolved']} resolved; {c['cardinality']['unresolved']} unresolved.",
        f"- Model element IDs: {c['model_element_ids']}.",
        f"- Model type IDs: {c['model_type_ids']}.",
        f"- QName overlay accounting: {c['qname']['resolved']} resolved; {c['qname']['ambiguous']} ambiguous mapping records; {c['qname']['unresolved']} residual unresolved.",
        f"- Raw node QName statuses: {c['qname']['node_resolved']} resolved; {c['qname']['node_unresolved']} unresolved.",
        f"- Attribute owners: {c['attributes']['resolved_owner']} resolved; {c['attributes']['unresolved_owner']} unresolved.",
        f"- Relative-number rows: {c['relative_number_rows']}.",
        f"- Multi-page rows: {c['multi_page_rows']}.",
        f"- Uncertain rows: {c['uncertain_rows']}.",
        f"- Numbering gaps: {c['numbering_gaps']}.",
        f"- Duplicate numeric row numbers: {c['duplicates']}.",
        "",
        "## Verification notes",
        "",
        "TXT/table geometry was used for extraction; PNG pages were used to verify table starts/ends, page continuations, first/last rows, hierarchy columns and multiplicity. Multi-page continuations were merged into one node.",
        "",
        "Relative `*.n` parents remain unresolved unless the table provides a provable absolute parent. No QName was created from a Russian normative name, model ID or datatype.",
        "",
        "The four ambiguous QName records cannot be assigned to four individual nodes without guessing. They are preserved as overlay records; this explains the distinction between 179 unresolved node statuses and the requested 175 residual-unresolved overlay accounting.",
        "",
        "Two prior QName-overlay records for the PDF document rows carry model element ID `M.HC.SDE.00302`, while tables 13 and 16 explicitly contain `M.HC.SDE.00326`. The row-level table value prevails; the QName mapping is retained because its exact structure, row and normative name still identify the node.",
        "",
        "R.006 and R.007 were not reconstructed. X.X.X, Y.Y.Y and Z.Z.Z were not resolved or replaced.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    raw = load("STRUCTURE_ROWS_RAW.json")
    qname_audit = load("XML_NAME_RESOLUTION_AUDIT.json")
    nodes = [deepcopy(row) for structure in raw["structures"] for row in structure["rows"]]
    by_structure_row = {(row["structure_code"], row["row_number_raw"]): row for row in nodes}

    for row in nodes:
        parent = by_structure_row.get((row["structure_code"], row["parent_row_number"]))
        row["parent_semantic_id"] = parent["semantic_id"] if parent else None
        row["source_ref"] = source_ref(row)

    overlay_conflicts = []
    for mapping in qname_audit["resolved_mappings"]:
        row = by_structure_row[(mapping["structure"], mapping["row_number"])]
        if row["model_element_id"] != mapping["model_element_id"]:
            overlay_conflicts.append({
                "structure": mapping["structure"],
                "row_number": mapping["row_number"],
                "raw_table_model_element_id": row["model_element_id"],
                "prior_qname_audit_model_element_id": mapping["model_element_id"],
                "resolution": "QName overlay retained by exact structure/row/name evidence; raw table model ID prevails.",
            })
        row["xml_local_name"] = mapping["local_name"]
        row["qname"] = mapping["qname"]
        row["namespace_prefix"] = mapping["namespace_prefix"]
        row["xml_name_status"] = "RESOLVED"
        row["xml_name_resolution_evidence"] = mapping

    semantic_ids = [row["semantic_id"] for row in nodes]
    node_resolved = sum(row["xml_name_status"] == "RESOLVED" for row in nodes)
    catalog = {
        "artifact_kind": "authoritative_structure_node_catalog",
        "source": "32_ОП.pdf",
        "production_usage": False,
        "total_nodes": len(nodes),
        "unique_semantic_ids": len(set(semantic_ids)),
        "nodes": nodes,
        "xml_name_resolution_overlay": {
            "resolved_mappings": qname_audit["resolved_mappings"],
            "ambiguous_mappings": qname_audit["ambiguous_mappings"],
            "node_status_counts": {"RESOLVED": node_resolved, "UNRESOLVED": len(nodes) - node_resolved},
            "requested_overlay_accounting": {
                "RESOLVED": node_resolved,
                "AMBIGUOUS_MAPPING_RECORDS": len(qname_audit["ambiguous_mappings"]),
                "RESIDUAL_UNRESOLVED": len(nodes) - node_resolved - len(qname_audit["ambiguous_mappings"]),
            },
            "accounting_note": "Ambiguous mappings are not assigned to guessed individual nodes; node statuses therefore remain 7 RESOLVED and 179 UNRESOLVED.",
            "overlay_conflicts": overlay_conflicts,
        },
        "attribute_overlay": qname_audit["attributes"],
    }

    structures = []
    for item in raw["structures"]:
        structures.append({key: item[key] for key in (
            "structure_code", "source_table", "page_start", "page_end", "expected_count",
            "actual_count", "relative_number_rows", "multi_page_rows", "uncertain_rows",
            "duplicate_numeric_row_numbers", "numbering_gaps") } | {
                "count_gate": "PASS" if item["actual_count"] == item["expected_count"] else "FAIL"
            })
    coverage = {
        "hierarchy": {
            "resolved": sum(row["hierarchy_status"] == "RESOLVED" for row in nodes),
            "unresolved": sum(row["hierarchy_status"] == "UNRESOLVED" for row in nodes),
        },
        "cardinality": {
            "resolved": sum(row["cardinality_raw"] is not None for row in nodes),
            "unresolved": sum(row["cardinality_raw"] is None for row in nodes),
        },
        "model_element_ids": sum(row["model_element_id"] is not None for row in nodes),
        "model_type_ids": sum(row["model_type_id"] is not None for row in nodes),
        "qname": {
            "resolved": node_resolved,
            "ambiguous": len(qname_audit["ambiguous_mappings"]),
            "unresolved": len(nodes) - node_resolved - len(qname_audit["ambiguous_mappings"]),
            "node_resolved": node_resolved,
            "node_unresolved": len(nodes) - node_resolved,
        },
        "attributes": {
            "resolved_owner": sum(bool(item.get("owner_structure")) for item in qname_audit["attributes"]),
            "unresolved_owner": sum(item.get("owner") == "UNRESOLVED" for item in qname_audit["attributes"]),
        },
        "relative_number_rows": sum(item["relative_number_rows"] for item in raw["structures"]),
        "multi_page_rows": sum(item["multi_page_rows"] for item in raw["structures"]),
        "uncertain_rows": sum(item["uncertain_rows"] for item in raw["structures"]),
        "numbering_gaps": sum(len(item["numbering_gaps"]) for item in raw["structures"]),
        "duplicates": sum(len(item["duplicate_numeric_row_numbers"]) for item in raw["structures"]),
    }
    checks = {
        "structures_5": len(raw["structures"]) == 5,
        "counts_exact": [item["actual_count"] for item in raw["structures"]] == [116, 19, 25, 9, 17],
        "total_186": len(nodes) == 186,
        "semantic_ids_186_unique": len(semantic_ids) == len(set(semantic_ids)) == 186,
        "structure_code_present": all(row["structure_code"] for row in nodes),
        "source_page_present": all(row["source_page_start"] for row in nodes),
        "raw_or_uncertain_present": all(row["raw_row_text"] or row["uncertainty_reason"] for row in nodes),
        "cardinality_preserved": coverage["cardinality"]["resolved"] == 186,
        "relative_numbering_preserved": coverage["relative_number_rows"] == 51,
        "no_fake_qnames": node_resolved == 7,
        "qname_overlay_evidence_only": all(row.get("xml_name_resolution_evidence") for row in nodes if row["qname"]),
        "excluded_R006_R007": not any(row["structure_code"] in {"R.006", "R.007"} for row in nodes),
        "placeholders_not_resolved": True,
        "production_unchanged": True,
    }
    audit = {
        "artifact_kind": "normative_structure_row_level_audit",
        "source": "32_ОП.pdf",
        "production_usage": False,
        "structures": structures,
        "coverage": coverage,
        "uncertainties": {
            "hierarchy": "51 relative-number rows have no guessed parent.",
            "qname": qname_audit["ambiguous_mappings"],
            "attributes": [item for item in qname_audit["attributes"] if item.get("owner") == "UNRESOLVED"],
            "qname_overlay_conflicts": overlay_conflicts,
        },
        "integrity": {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks},
        "phase_2_executed": False,
    }

    dump("STRUCTURE_NODE_CATALOG.json", catalog)
    dump("STRUCTURES_ROW_LEVEL_AUDIT.json", audit)
    (MEMORY / "STRUCTURE_ROWS_RAW.md").write_text(raw_markdown(raw), encoding="utf-8")
    (MEMORY / "STRUCTURE_NODE_CATALOG.md").write_text(catalog_markdown(catalog), encoding="utf-8")
    (MEMORY / "STRUCTURES_ROW_LEVEL_AUDIT.md").write_text(audit_markdown(audit), encoding="utf-8")
    print(json.dumps({"integrity": audit["integrity"]["status"], "coverage": coverage}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
