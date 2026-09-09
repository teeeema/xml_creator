"""Build non-normative requirement candidates from PDF table cells."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[4]
PDF_PATH = ROOT / "32_ОП.pdf"
WORK_ROOT = ROOT / "P.MM.06" / "process_memory" / "source_extract" / "work"

# (physical PDF page, zero-based PyMuPDF table index)
TABLE_SEGMENTS: dict[str, list[tuple[int, int]]] = {
    "P.MM.06.MSG.001": [(108, 0), (109, 0), (110, 0)],
    "P.MM.06.MSG.002": [(110, 1), (111, 0), (112, 0), (113, 0), (114, 0), (115, 0), (116, 0)],
    "P.MM.06.MSG.003": [(116, 1), (117, 0)],
    "P.MM.06.MSG.012": [(117, 1)],
    "P.MM.06.MSG.014": [(145, 1), (146, 0)],
    "P.MM.06.MSG.015": [(146, 1), (147, 0)],
    "P.MM.06.MSG.016": [(147, 1), (148, 0)],
    "P.MM.06.MSG.018": [(148, 1), (149, 0), (150, 0)],
    "P.MM.06.MSG.019": [(150, 1), (151, 0)],
    "P.MM.06.MSG.020": [(151, 1), (152, 0), (153, 0)],
    "P.MM.06.MSG.021": [(153, 1), (154, 0)],
    "P.MM.06.MSG.022": [(155, 0), (156, 0)],
    "P.MM.06.MSG.023": [(156, 1), (157, 0)],
    "P.MM.06.MSG.024": [(157, 1)],
}

TABLE_NUMBERS = {
    "P.MM.06.MSG.001": "13", "P.MM.06.MSG.002": "14",
    "P.MM.06.MSG.003": "15", "P.MM.06.MSG.012": "16",
    "P.MM.06.MSG.014": "16", "P.MM.06.MSG.015": "17",
    "P.MM.06.MSG.016": "18", "P.MM.06.MSG.018": "19",
    "P.MM.06.MSG.019": "20", "P.MM.06.MSG.020": "21",
    "P.MM.06.MSG.021": "22", "P.MM.06.MSG.022": "23",
    "P.MM.06.MSG.023": "24", "P.MM.06.MSG.024": "25",
}


def clean_cell(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def extract_message(doc: pymupdf.Document, msg_code: str) -> dict:
    requirements: list[dict] = []
    for page_number, table_index in TABLE_SEGMENTS[msg_code]:
        tables = doc[page_number - 1].find_tables().tables
        if table_index >= len(tables):
            raise RuntimeError(
                f"{msg_code}: page {page_number} has no table index {table_index}"
            )
        for row in tables[table_index].extract():
            number = clean_cell(row[0] if row else None)
            text = clean_cell(row[1] if len(row) > 1 else None)
            if number.isdigit() and text:
                requirements.append({
                    "number": number,
                    "raw_text": text,
                    "page_start": page_number,
                    "page_end": page_number,
                    "continues_across_pages": False,
                    "candidate_status": "PENDING_VISUAL_VERIFICATION",
                })
            elif not number and text and requirements:
                previous = requirements[-1]
                previous["raw_text"] = f'{previous["raw_text"]} {text}'.strip()
                if page_number != previous["page_start"]:
                    previous["page_end"] = page_number
                    previous["continues_across_pages"] = True

    numbers = [int(item["number"]) for item in requirements]
    counts = Counter(numbers)
    pages = [page for page, _ in TABLE_SEGMENTS[msg_code]]
    return {
        "msg_code": msg_code,
        "table": TABLE_NUMBERS[msg_code],
        "page_start": min(pages),
        "page_end": max(pages),
        "first_requirement": str(min(numbers)) if numbers else None,
        "last_requirement": str(max(numbers)) if numbers else None,
        "total_requirements": len(requirements),
        "numbering_gaps": [
            str(number) for number in range(min(numbers), max(numbers) + 1)
            if number not in counts
        ] if numbers else [],
        "duplicate_numbers": [str(n) for n, count in sorted(counts.items()) if count > 1],
        "requirements": requirements,
    }


def main() -> None:
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(PDF_PATH)
    messages = [extract_message(doc, code) for code in TABLE_SEGMENTS]
    payload = {
        "artifact_kind": "requirement_candidates",
        "source": "32_ОП.pdf",
        "status": "CANDIDATE_ONLY",
        "method": "PyMuPDF table-cell extraction; PNG verification required",
        "messages": messages,
    }
    (WORK_ROOT / "requirement_candidates.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# Requirement candidates", "",
        "Candidate-only table-cell extraction. PNG verification remains authoritative.", "",
        "| MSG | Table | Pages | First | Last | Count | Gaps | Duplicates |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for message in messages:
        lines.append(
            f'| {message["msg_code"]} | {message["table"]} | '
            f'{message["page_start"]}-{message["page_end"]} | '
            f'{message["first_requirement"]} | {message["last_requirement"]} | '
            f'{message["total_requirements"]} | '
            f'{", ".join(message["numbering_gaps"]) or "-"} | '
            f'{", ".join(message["duplicate_numbers"]) or "-"} |'
        )
    (WORK_ROOT / "requirement_candidates.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
