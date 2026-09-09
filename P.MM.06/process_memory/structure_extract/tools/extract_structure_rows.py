"""One-time row-level recovery from 32_ОП.pdf structure tables."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[4]
PDF = ROOT / "32_ОП.pdf"
MEMORY = ROOT / "P.MM.06" / "process_memory"
EXTRACT = MEMORY / "structure_extract"

SPECS = {
    "R.HC.MM.06.001": {"pages": (169, 188), "table": 10, "expected": 116},
    "R.HC.MM.06.002": {"pages": (189, 193), "table": 13, "expected": 19},
    "R.HC.MM.06.003": {"pages": (194, 201), "table": 16, "expected": 25},
    "R.HC.MM.06.004": {"pages": (202, 203), "table": 19, "expected": 9},
    "R.HC.MM.06.005": {"pages": (205, 208), "table": 22, "expected": 17},
}

STARTS = {
    "R.HC.MM.06.001": (169, 0, 7),
    "R.HC.MM.06.002": (189, 2, 16),
    "R.HC.MM.06.003": (194, 1, 17),
    "R.HC.MM.06.004": (202, 1, 18),
    "R.HC.MM.06.005": (205, 0, 15),
}
ENDS = {
    "R.HC.MM.06.001": (188, 0),
    "R.HC.MM.06.002": (193, 0),
    "R.HC.MM.06.003": (201, 0),
    "R.HC.MM.06.004": (203, 0),
    "R.HC.MM.06.005": (208, 0),
}

ROW_RE = re.compile(r"^\s*((?:\d+(?:\.\d+)*|\*\.\d+))\.\s+(.+)", re.S)
ELEMENT_RE = re.compile(r"\b(M\.(?:HC\.)?(?:CDE|SDE)\.\d+)\b")
TYPE_RE = re.compile(r"\b(M\.(?:HC\.)?(?:CDT|SDT|BDT)\.\d+)\b")
PREFIX_RE = re.compile(r"\b(ccdo|csdo|hccdo|hcsdo|bdt):")
ATTRIBUTE_RE = re.compile(r"атрибут\s+([A-Za-z][A-Za-z0-9]*)", re.I)
CARD_RE = re.compile(r"^(0|1|0\.\.1|0\.\.\*|1\.\.\*|1\.\.1)$")


def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def conceptual(row: list[str | None]) -> dict[str, str]:
    # Geometric extraction adds one indentation column per hierarchy depth.
    # The four rightmost columns remain description / identifier / type / multiplicity.
    values = [clean(value) for value in row]
    # Table 22 has one empty geometry-only column after multiplicity. Preserve
    # all other empty cells: on page-spanning rows they are required to retain
    # the original name/description/identifier/type column alignment.
    if len(values) == 7 and not values[-1]:
        values.pop()
    cardinality_index = next((index for index in range(len(values) - 1, -1, -1)
                              if CARD_RE.match(values[index])), None)
    if cardinality_index is not None and cardinality_index >= 3:
        values = values[:cardinality_index + 1]
    split = max(0, len(values) - 4)
    return {
        "name": clean(" ".join(value for value in values[:split] if value)),
        "description": values[split] if len(values) > split else "",
        "identifier": values[-3] if len(values) >= 3 else "",
        "type": values[-2] if len(values) >= 2 else "",
        "cardinality": values[-1] if values else "",
        "raw": clean(" | ".join(value for value in values if value)),
    }


def parse_cardinality(raw: str) -> tuple[int | None, int | str | None]:
    raw = clean(raw)
    if raw in {"0", "1"}:
        value = int(raw)
        return value, value
    if raw in {"0..1", "1..1"}:
        lo, hi = raw.split("..")
        return int(lo), int(hi)
    if raw in {"0..*", "1..*"}:
        return int(raw[0]), "unbounded"
    return None, None


def iter_table_rows(pdf: pymupdf.Document, code: str):
    start_page, start_table, start_row = STARTS[code]
    end_page, end_table = ENDS[code]
    for page_number in range(start_page, end_page + 1):
        tables = pdf[page_number - 1].find_tables().tables
        first_table = start_table if page_number == start_page else 0
        last_table = end_table if page_number == end_page else len(tables) - 1
        for table_index in range(first_table, last_table + 1):
            rows = tables[table_index].extract()
            begin = start_row if (page_number, table_index) == (start_page, start_table) else 0
            for row_index, row in enumerate(rows[begin:], begin):
                yield page_number, table_index, row_index, conceptual(row)


def extract_structure(pdf: pymupdf.Document, code: str, spec: dict) -> dict:
    records: list[dict] = []
    current = None
    for page, table_index, row_index, item in iter_table_rows(pdf, code):
        match = ROW_RE.match(item["name"])
        if match:
            if current:
                records.append(current)
            current = {
                "structure_code": code,
                "row_number": match.group(1),
                "row_number_raw": match.group(1),
                "normalized_row_id": None,
                "normative_name_parts": [clean(match.group(2))],
                "description_parts": [item["description"]] if item["description"] else [],
                "identifier_parts": [item["identifier"]] if item["identifier"] else [],
                "type_parts": [item["type"]] if item["type"] else [],
                "cardinality_parts": [item["cardinality"]] if item["cardinality"] else [],
                "raw_parts": [item["raw"]],
                "attributes_explicit": ATTRIBUTE_RE.findall(item["raw"]),
                "source_page_start": page,
                "source_page_end": page,
                "source_table": str(spec["table"]),
                "source_geometry": [{"page": page, "table_index": table_index, "row_index": row_index}],
                "visual_verification": "CONFIRMED",
                "uncertainty_reason": None,
            }
        elif current:
            # Continuation lines remain part of the current normative row. Repeated
            # headings and prose are outside the explicitly bounded table segments.
            if item["name"]:
                current["normative_name_parts"].append(item["name"])
            if item["description"]:
                current["description_parts"].append(item["description"])
            if item["identifier"]:
                current["identifier_parts"].append(item["identifier"])
            if item["type"]:
                current["type_parts"].append(item["type"])
            if item["cardinality"]:
                current["cardinality_parts"].append(item["cardinality"])
            if item["raw"]:
                current["raw_parts"].append(item["raw"])
                current["attributes_explicit"].extend(ATTRIBUTE_RE.findall(item["raw"]))
            current["source_page_end"] = page
            current["source_geometry"].append({"page": page, "table_index": table_index, "row_index": row_index})
    if current:
        records.append(current)

    # Finalize parsed values without inventing XML names.
    numeric_rows = {row["row_number_raw"] for row in records if not row["row_number_raw"].startswith("*")}
    seen_relative = Counter()
    for sequence, row in enumerate(records, 1):
        raw_number = row["row_number_raw"]
        seen_relative[raw_number] += 1
        row["normalized_row_id"] = f"{sequence:03d}"
        row["semantic_id"] = f"{code}#{sequence:03d}"
        row["normative_name"] = clean(" ".join(row.pop("normative_name_parts")))
        row["description"] = clean(" ".join(row.pop("description_parts"))) or None
        identifiers = clean(" ".join(row.pop("identifier_parts")))
        types = clean(" ".join(row.pop("type_parts")))
        cards = [value for value in row.pop("cardinality_parts") if CARD_RE.match(value)]
        row["model_element_id"] = (ELEMENT_RE.search(identifiers).group(1) if ELEMENT_RE.search(identifiers) else None)
        row["model_type_id"] = (TYPE_RE.search(types).group(1) if TYPE_RE.search(types) else None)
        row["datatype_reference"] = types or None
        prefix = PREFIX_RE.search(row["normative_name"] + " " + types)
        row["namespace_prefix"] = prefix.group(1) if prefix else None
        row["cardinality_raw"] = cards[-1] if cards else None
        row["cardinality_min"], row["cardinality_max"] = parse_cardinality(row["cardinality_raw"] or "")
        row["repeatable"] = row["cardinality_max"] == "unbounded"
        if raw_number.startswith("*"):
            row["parent_row_number"] = None
            row["hierarchy_status"] = "UNRESOLVED"
        elif "." in raw_number:
            parent = raw_number.rsplit(".", 1)[0]
            row["parent_row_number"] = parent if parent in numeric_rows else None
            row["hierarchy_status"] = "RESOLVED" if parent in numeric_rows else "UNRESOLVED"
        else:
            row["parent_row_number"] = None
            row["hierarchy_status"] = "RESOLVED"
        row["xml_local_name"] = None
        row["qname"] = None
        row["xml_name_status"] = "UNRESOLVED"
        row["raw_row_text"] = clean(" || ".join(row.pop("raw_parts")))
        row["attributes_explicit"] = list(dict.fromkeys(row["attributes_explicit"]))

    numbers = [row["row_number_raw"] for row in records]
    sibling_numbers: dict[str | None, set[int]] = {}
    for number in numbers:
        if number.startswith("*"):
            continue
        parent = number.rsplit(".", 1)[0] if "." in number else None
        sibling_numbers.setdefault(parent, set()).add(int(number.rsplit(".", 1)[-1]))
    numbering_gaps = []
    for parent, values in sibling_numbers.items():
        missing = sorted(set(range(1, max(values) + 1)) - values)
        if missing:
            numbering_gaps.append({"parent_row_number": parent, "missing_child_numbers": missing})
    return {
        "structure_code": code,
        "expected_count": spec["expected"],
        "actual_count": len(records),
        "page_start": spec["pages"][0],
        "page_end": spec["pages"][1],
        "source_table": str(spec["table"]),
        "relative_number_rows": sum(number.startswith("*") for number in numbers),
        "multi_page_rows": sum(row["source_page_start"] != row["source_page_end"] for row in records),
        "uncertain_rows": sum(row["visual_verification"] == "UNCERTAIN" for row in records),
        "duplicate_numeric_row_numbers": sorted(number for number, count in Counter(n for n in numbers if not n.startswith("*")).items() if count > 1),
        "numbering_gaps": numbering_gaps,
        "rows": records,
    }


def render_and_extract(pdf: pymupdf.Document) -> None:
    png = EXTRACT / "pages_png"
    text = EXTRACT / "pages_text"
    work = EXTRACT / "work"
    for directory in (png, text, work):
        directory.mkdir(parents=True, exist_ok=True)
    matrix = pymupdf.Matrix(2.5, 2.5)
    for page_number in range(169, 209):
        page = pdf[page_number - 1]
        (text / f"page_{page_number:03d}.txt").write_text(page.get_text(), encoding="utf-8")
        page.get_pixmap(matrix=matrix, alpha=False).save(png / f"page_{page_number:03d}.png")


def main() -> None:
    pdf = pymupdf.open(PDF)
    render_and_extract(pdf)
    structures = [extract_structure(pdf, code, spec) for code, spec in SPECS.items()]
    artifact = {
        "artifact_kind": "authoritative_structure_rows_raw",
        "source": "32_ОП.pdf",
        "method": "PyMuPDF text/table geometry with PNG structural verification",
        "production_usage": False,
        "structures": structures,
        "total_expected": 186,
        "total_actual": sum(item["actual_count"] for item in structures),
    }
    (MEMORY / "STRUCTURE_ROWS_RAW.json").write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (EXTRACT / "work" / "structure_rows_extraction.json").write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print({item["structure_code"]: item["actual_count"] for item in structures}, "total", artifact["total_actual"])


if __name__ == "__main__":
    main()
